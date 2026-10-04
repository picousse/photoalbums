"""Pick the best photos: measure sharpness and exposure, group shots of the
same moment, keep the best of each, and write contact sheets for review."""

import json
import math
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import yaml
from PIL import Image, ImageDraw, ImageFont, ImageOps
from scipy import ndimage

from .scan import Photo, register_heif_opener

register_heif_opener()

FONT = Path(__file__).parent / "fonts" / "NotoSans-Light.ttf"
THUMB = 400  # px, long edge of cached thumbnails
SAME_SHOT = 10  # dhash distance below which two photos are copies of one shot
MAX_KEEP = 3  # photos kept per moment by the automatic pass


def _dhash(gray: Image.Image) -> int:
    small = np.asarray(gray.resize((9, 8), Image.LANCZOS), dtype=np.int16)
    bits = (small[:, 1:] > small[:, :-1]).flatten()
    return int("".join("1" if b else "0" for b in bits), 2)


def _analyse(args: tuple[Path, Path]) -> dict:
    path, thumb_path = args
    with Image.open(path) as img:
        img.draft("RGB", (1600, 1600))  # fast JPEG decode at reduced size
        img = ImageOps.exif_transpose(img).convert("RGB")
    img.thumbnail((1024, 1024))
    thumb = img.copy()
    thumb.thumbnail((THUMB, THUMB))
    thumb_path.parent.mkdir(parents=True, exist_ok=True)
    thumb.save(thumb_path, quality=85)

    gray_img = img.convert("L")
    gray = np.asarray(gray_img, dtype=np.float32)
    # Sharpness of the sharpest regions: a sharp subject against a soft
    # background should still count as sharp.
    lap = np.abs(ndimage.laplace(gray))
    h, w = lap.shape
    tiles = lap[: h // 8 * 8, : w // 8 * 8].reshape(8, h // 8, 8, w // 8).mean(axis=(1, 3))
    sharpness = float(np.sort(tiles.flatten())[-6:].mean())
    return {
        "sharpness": sharpness,
        "dark": float((gray < 8).mean()),
        "bright": float((gray > 247).mean()),
        "brightness": float(gray.mean() / 255),
        "dhash": _dhash(gray_img),
    }


def analyse_all(photos: list[Photo], photos_dir: Path, cache_dir: Path) -> dict[str, dict]:
    """Metrics per photo, cached by file name, size and modification time."""
    cache_file = cache_dir / "metrics.json"
    cache = json.loads(cache_file.read_text()) if cache_file.exists() else {}
    todo = []
    for p in photos:
        st = (photos_dir / p.path).stat()
        key = f"{st.st_size}-{int(st.st_mtime)}"
        if cache.get(str(p.path), {}).get("key") != key:
            todo.append((p, key))
    if todo:
        print(f"analysing {len(todo)} photos...")
        jobs = [(photos_dir / p.path, cache_dir / "thumbs" / p.path.with_suffix(".jpg")) for p, _ in todo]
        with ProcessPoolExecutor() as pool:
            for (p, key), metrics in zip(todo, pool.map(_analyse, jobs, chunksize=8)):
                cache[str(p.path)] = {"key": key, **metrics}
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps(cache))
    return {str(p.path): cache[str(p.path)] for p in photos}


def quality(m: dict, sharp_median: float) -> float:
    """Heuristic score: sharpness relative to the album, minus exposure problems."""
    score = float(np.log(m["sharpness"] / sharp_median))
    score -= 4 * max(0.0, m["dark"] - 0.05) + 4 * max(0.0, m["bright"] - 0.03)
    score -= 2 * max(0.0, abs(m["brightness"] - 0.45) - 0.25)
    return round(score, 3)


def moments(photos: list[Photo], metrics: dict[str, dict], max_gap: float, max_distance: int) -> list[list[Photo]]:
    """Consecutive photos close in time and visually similar form one moment."""
    groups: list[list[Photo]] = []
    for p in photos:
        if groups:
            group = groups[-1]
            gap = (p.taken - group[-1].taken).total_seconds()
            # Compare with every shot of the moment, not just the last one:
            # two phones shooting the same scene interleave.
            distance = min(_distance(metrics, p, q) for q in group)
            if gap <= max_gap and distance <= max_distance:
                group.append(p)
                continue
        groups.append([p])
    return groups


def _distance(metrics: dict[str, dict], a: Photo, b: Photo) -> int:
    return bin(metrics[str(a.path)]["dhash"] ^ metrics[str(b.path)]["dhash"]).count("1")


def is_forwarded(photo: Photo) -> bool:
    return "-WA" in photo.path.name  # WhatsApp copies: recompressed, no EXIF


def build_selection(photos: list[Photo], metrics: dict[str, dict], max_gap: float, max_distance: int) -> dict:
    sharp_median = float(np.median([m["sharpness"] for m in metrics.values()]))
    # Forwarded copies of photos we also have as originals are dropped.
    originals = [p for p in photos if not is_forwarded(p)]
    duplicates = [
        p for p in photos
        if is_forwarded(p) and min((_distance(metrics, p, q) for q in originals), default=64) <= 10
    ]
    photos = [p for p in photos if p not in duplicates]
    result = []
    for group in moments(photos, metrics, max_gap, max_distance):
        ranked = sorted(group, key=lambda p: quality(metrics[str(p.path)], sharp_median), reverse=True)
        # Near-identical copies (same shot from two phones, bursts) are dropped;
        # of the distinct shots left, keep about one in three.
        distinct, copies = [], []
        for p in ranked:
            (copies if any(_distance(metrics, p, q) <= SAME_SHOT for q in distinct) else distinct).append(p)
        n_keep = min(MAX_KEEP, math.ceil(len(distinct) / 3))
        entry = {
            "time": f"{group[0].taken:%Y-%m-%d %H:%M}",
            "city": group[0].city,
            "keep": [str(p.path) for p in distinct[:n_keep]],
        }
        if distinct[n_keep:]:
            entry["alternates"] = [str(p.path) for p in distinct[n_keep:]]
        if copies:
            entry["copies"] = [str(p.path) for p in copies]
        entry["scores"] = {str(p.path): quality(metrics[str(p.path)], sharp_median) for p in ranked}
        result.append(entry)
    selection = {"moments": result}
    if duplicates:
        selection["forwarded_duplicates"] = [str(p.path) for p in duplicates]
    return selection


def write_selection(selection: dict, path: Path) -> None:
    header = (
        "# Photo selection. Only files under `keep` go into the book.\n"
        "# Move file names between `keep` and `alternates` freely; delete a whole\n"
        "# moment to drop it. `copies` are near-identical shots of a kept photo.\n"
        "# `scores` is the automatic sharpness/exposure score.\n"
    )
    path.write_text(header + yaml.safe_dump(selection, sort_keys=False, allow_unicode=True, width=120))


def kept_files(selection_path: Path) -> set[str]:
    selection = yaml.safe_load(selection_path.read_text())
    return {f for m in selection["moments"] for f in m.get("keep", [])}


def contact_sheets(selection: dict, cache_dir: Path, out_dir: Path, per_sheet: int = 20) -> list[Path]:
    """Numbered sheets of the kept photos, one series per day, for review.
    `index.tsv` maps each number to its file."""
    for old in out_dir.glob("*.jpg"):
        old.unlink()
    out_dir.mkdir(parents=True, exist_ok=True)
    font = ImageFont.truetype(str(FONT), 22)
    cols, cell, pad = 5, 300, 36
    by_day: dict[str, list[str]] = {}
    for m in selection["moments"]:
        by_day.setdefault(m["time"][:10], []).extend(m.get("keep", []))

    sheets, index, n = [], [], 0
    for day, files in by_day.items():
        for start in range(0, len(files), per_sheet):
            chunk = files[start : start + per_sheet]
            rows = (len(chunk) + cols - 1) // cols
            sheet = Image.new("RGB", (cols * cell, rows * (cell + pad)), "white")
            draw = ImageDraw.Draw(sheet)
            for i, file in enumerate(chunk):
                n += 1
                index.append(f"{n}\t{file}")
                with Image.open(cache_dir / "thumbs" / Path(file).with_suffix(".jpg")) as t:
                    t = t.copy()
                t.thumbnail((cell - 8, cell - 8))
                x, y = (i % cols) * cell, (i // cols) * (cell + pad)
                sheet.paste(t, (x + (cell - t.width) // 2, y + pad + (cell - t.height) // 2))
                draw.text((x + 6, y + 4), f"#{n}", fill="black", font=font)
            path = out_dir / f"{day}-{start // per_sheet + 1:02d}.jpg"
            sheet.save(path, quality=85)
            sheets.append(path)
    (out_dir / "index.tsv").write_text("\n".join(index) + "\n")
    return sheets


def parse_numbers(spec: list[str]) -> set[int]:
    """'3 7 12-15' or '3,7,12-15' -> {3, 7, 12, 13, 14, 15}"""
    numbers = set()
    for part in ",".join(spec).split(","):
        if not part.strip():
            continue
        lo, _, hi = part.strip().partition("-")
        numbers.update(range(int(lo), int(hi or lo) + 1))
    return numbers


def drop(selection_path: Path, sheets_dir: Path, numbers: set[int]) -> list[str]:
    """Move photos (by contact sheet number) from `keep` to the front of `alternates`."""
    index = dict(line.split("\t") for line in (sheets_dir / "index.tsv").read_text().splitlines())
    files = {index[str(n)] for n in numbers if str(n) in index}
    selection = yaml.safe_load(selection_path.read_text())
    for m in selection["moments"]:
        dropped = [f for f in m.get("keep", []) if f in files]
        if dropped:
            m["keep"] = [f for f in m["keep"] if f not in files]
            m["alternates"] = dropped + m.get("alternates", [])
    selection["moments"] = [
        {k: v for k, v in m.items() if v or k == "keep"} for m in selection["moments"]
    ]
    write_selection(selection, selection_path)
    return sorted(files)
