"""Page layouts. Each layout places photo frames on a page.

Frames are (x, y, w, h) in mm, measured from the top-left of the trim box.
A frame with `fit=True` takes the photo's own aspect ratio (no cropping),
centred inside the given box.
"""

from dataclasses import dataclass

from .formats import BookFormat


@dataclass(frozen=True)
class Frame:
    x: float
    y: float
    w: float
    h: float
    fit: bool = False  # shrink to the photo's aspect instead of cropping
    bleed: bool = False  # extend to the page edge (past the trim)

    @property
    def aspect(self) -> float:
        return self.w / self.h


def frames(layout: str, fmt: BookFormat) -> list[Frame]:
    m, g = fmt.margin, fmt.gap
    W, H = fmt.trim_w - 2 * m, fmt.trim_h - 2 * m  # live area
    half_w, half_h = (W - g) / 2, (H - g) / 2

    if layout == "full":
        return [Frame(0, 0, fmt.trim_w, fmt.trim_h, bleed=True)]
    if layout == "single":
        return [Frame(m, m, W, H, fit=True)]
    if layout == "duo":
        return [Frame(m, m, half_w, H), Frame(m + half_w + g, m, half_w, H)]
    if layout == "duo-offset":
        h = half_h
        w = h * 1.5
        return [Frame(m, m, w, h), Frame(m + W - w, m + h + g, w, h)]
    if layout == "trio":
        return [
            Frame(m, m, half_w, H),
            Frame(m + half_w + g, m, half_w, half_h),
            Frame(m + half_w + g, m + half_h + g, half_w, half_h),
        ]
    if layout == "trio-portrait":
        w = (W - 2 * g) / 3
        h = min(H, w * 1.5)
        y = m + (H - h) / 2
        return [Frame(m + i * (w + g), y, w, h) for i in range(3)]
    if layout == "quad":
        return [
            Frame(m + c * (half_w + g), m + r * (half_h + g), half_w, half_h)
            for r in range(2)
            for c in range(2)
        ]
    raise ValueError(f"unknown layout {layout!r}; choose from {', '.join(LAYOUTS)}")


LAYOUTS = ["full", "single", "duo", "duo-offset", "trio", "trio-portrait", "quad"]
