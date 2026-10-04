"""Render a book plan to PDF: a print file (single pages with bleed) or a
spreads preview (facing pages side by side, trimmed)."""

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageOps
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

from .formats import FORMATS, MM, BookFormat
from .layouts import frames
from .scan import register_heif_opener

register_heif_opener()

FONTS = Path(__file__).parent / "fonts"
pdfmetrics.registerFont(TTFont("Title", FONTS / "NotoSerif-Light.ttf"))
pdfmetrics.registerFont(TTFont("Subtitle", FONTS / "NotoSans-Light.ttf"))
TEXT_GREY = (0.2, 0.2, 0.2)
MIN_PRINT_DPI = 200


@dataclass
class Page:
    kind: str  # "photos", "title" or "blank"
    layout: str | None = None
    photos: tuple = ()
    title: str = ""
    subtitle: str = ""


def flatten(plan: dict, fmt: BookFormat) -> list[Page]:
    pages = []
    if plan.get("title"):
        pages.append(Page("title", title=plan["title"], subtitle=plan.get("subtitle", "")))
    for section in plan["sections"]:
        if section.get("title"):
            pages.append(Page("title", title=section["title"], subtitle=section.get("subtitle", "")))
        for p in section["pages"]:
            pages.append(Page("photos", layout=p["layout"], photos=tuple(p["photos"])))
    while len(pages) < fmt.min_pages or len(pages) % 2:
        pages.append(Page("blank"))
    return pages


class Renderer:
    def __init__(self, plan: dict, dpi: int):
        self.fmt = FORMATS[plan["format"]]
        self.photos_dir = Path(plan["photos_dir"])
        self.dpi = dpi
        self.warnings: list[str] = []

    def _image(self, entry, w_mm: float, h_mm: float) -> ImageReader:
        file, focus = (entry, (0.5, 0.5)) if isinstance(entry, str) else (
            entry["file"], tuple(entry.get("focus", (0.5, 0.5)))
        )
        with Image.open(self.photos_dir / file) as raw:
            img = ImageOps.exif_transpose(raw).convert("RGB")
        target = w_mm / h_mm
        iw, ih = img.size
        if iw / ih > target:  # too wide: crop the sides
            cw, ch = round(ih * target), ih
        else:
            cw, ch = iw, round(iw / target)
        left = round((iw - cw) * focus[0])
        top = round((ih - ch) * focus[1])
        img = img.crop((left, top, left + cw, top + ch))

        effective_dpi = cw / (w_mm / 25.4)
        if effective_dpi < MIN_PRINT_DPI:
            self.warnings.append(f"{file}: only {effective_dpi:.0f} dpi at this size")
        px = (round(w_mm / 25.4 * self.dpi), round(h_mm / 25.4 * self.dpi))
        if px[0] < cw:
            img = img.resize(px, Image.LANCZOS)
        return ImageReader(img)

    def draw(self, c: Canvas, page: Page, ox: float, oy: float, bleed: tuple[float, float, float, float]):
        """Draw one page with the trim box's lower-left at (ox, oy) points.
        `bleed` is the extra (left, right, top, bottom) mm available past the trim."""
        fmt = self.fmt
        if page.kind == "title":
            cx, cy = ox + fmt.trim_w * MM / 2, oy + fmt.trim_h * MM / 2
            c.setFillColorRGB(*TEXT_GREY)
            c.setFont("Title", 34)
            c.drawCentredString(cx, cy, page.title)
            if page.subtitle:
                c.setFont("Subtitle", 10)
                c.drawCentredString(cx, cy - 26, page.subtitle.upper(), charSpace=1.5)
            return
        if page.kind != "photos":
            return

        for frame, entry in zip(frames(page.layout, fmt), page.photos):
            x, y, w, h = frame.x, frame.y, frame.w, frame.h
            if frame.bleed:
                l, r, t, b = bleed
                x, y, w, h = x - l, y - t, w + l + r, h + t + b
            if frame.fit:
                x, y, w, h = self._fit(entry, x, y, w, h)
            c.drawImage(
                self._image(entry, w, h),
                ox + x * MM,
                oy + (fmt.trim_h - y - h) * MM,
                w * MM,
                h * MM,
            )

    def _fit(self, entry, x, y, w, h):
        file = entry if isinstance(entry, str) else entry["file"]
        with Image.open(self.photos_dir / file) as raw:
            iw, ih = ImageOps.exif_transpose(raw).size
        scale = min(w / iw, h / ih)
        fw, fh = iw * scale, ih * scale
        return x + (w - fw) / 2, y + (h - fh) / 2, fw, fh


def render_print(plan: dict, out: Path, dpi: int = 300) -> Renderer:
    r = Renderer(plan, dpi)
    fmt = r.fmt
    pw, ph = fmt.page_size()
    c = Canvas(str(out), pagesize=(pw * MM, ph * MM))
    c.setTitle(plan.get("title", "Photo book"))
    for no, page in enumerate(flatten(plan, fmt), start=1):
        tx, ty = fmt.trim_origin(no)
        bleed = (tx, pw - tx - fmt.trim_w, fmt.bleed, fmt.bleed)
        c.setPageSize((pw * MM, ph * MM))
        # Trim box tells the printer (and Acrobat's preview) where the page is cut.
        c.setTrimBox((tx * MM, ty * MM, (tx + fmt.trim_w) * MM, (ty + fmt.trim_h) * MM))
        r.draw(c, page, tx * MM, ty * MM, bleed)
        c.showPage()
    c.save()
    return r


def render_spreads(plan: dict, out: Path, dpi: int = 100) -> Renderer:
    """Preview of facing pages as they appear in the bound book."""
    r = Renderer(plan, dpi)
    fmt = r.fmt
    pad = 10  # mm grey border around each spread
    sw, sh = 2 * fmt.trim_w + 2 * pad, fmt.trim_h + 2 * pad
    c = Canvas(str(out), pagesize=(sw * MM, sh * MM))
    pages = flatten(plan, fmt)
    # Page 1 sits alone on the right; then 2-3, 4-5, ...; the last page alone on the left.
    spreads = [(None, 1)] + [(n, n + 1 if n + 1 <= len(pages) else None) for n in range(2, len(pages) + 1, 2)]
    for left, right in spreads:
        c.setFillColorRGB(0.85, 0.85, 0.85)
        c.rect(0, 0, sw * MM, sh * MM, stroke=0, fill=1)
        for no, x0 in ((left, pad), (right, pad + fmt.trim_w)):
            if no is None:
                continue
            ox, oy = x0 * MM, pad * MM
            c.setFillColorRGB(1, 1, 1)
            c.rect(ox, oy, fmt.trim_w * MM, fmt.trim_h * MM, stroke=0, fill=1)
            c.saveState()
            path = c.beginPath()
            path.rect(ox, oy, fmt.trim_w * MM, fmt.trim_h * MM)
            c.clipPath(path, stroke=0, fill=0)
            r.draw(c, pages[no - 1], ox, oy, (0, 0, 0, 0))
            c.restoreState()
            c.setFillColorRGB(0.45, 0.45, 0.45)
            c.setFont("Subtitle", 7)
            c.drawCentredString(ox + fmt.trim_w * MM / 2, 3 * MM, str(no))
        c.setStrokeColorRGB(0.7, 0.7, 0.7)
        c.line((pad + fmt.trim_w) * MM, pad * MM, (pad + fmt.trim_w) * MM, (pad + fmt.trim_h) * MM)
        c.showPage()
    c.save()
    return r
