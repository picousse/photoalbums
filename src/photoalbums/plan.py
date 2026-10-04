"""Turn a list of photos into an editable book plan (YAML)."""

from collections import Counter
from datetime import date
from itertools import groupby
from pathlib import Path

import yaml

from .formats import BookFormat
from .layouts import LAYOUTS, frames
from .scan import Photo

DEFAULT_DENSITY = 2.2  # photos per page when no page target is given


def drop_bursts(photos: list[Photo], seconds: float) -> list[Photo]:
    """Keep one photo out of shots taken within `seconds` of each other."""
    kept: list[Photo] = []
    for p in photos:
        if kept and (p.taken - kept[-1].taken).total_seconds() < seconds:
            continue
        kept.append(p)
    return kept


def sections(photos: list[Photo]) -> list[tuple[str | None, list[Photo]]]:
    """Group photos by day, give each day its most common city, then merge
    consecutive days that share a city."""
    days = []
    for day, group in groupby(photos, key=lambda p: p.taken.date()):
        group = list(group)
        cities = Counter(p.city for p in group if p.city)
        days.append((cities.most_common(1)[0][0] if cities else None, group))

    merged: list[tuple[str | None, list[Photo]]] = []
    for city, group in days:
        if merged and (city is None or city == merged[-1][0]):
            merged[-1][1].extend(group)
        else:
            merged.append((city, list(group)))
    return merged


def crop_loss(photo_aspect: float, frame_aspect: float) -> float:
    return 1 - min(photo_aspect, frame_aspect) / max(photo_aspect, frame_aspect)


def paginate(photos: list[Photo], fmt: BookFormat, density: float) -> list[dict]:
    """Greedily pick a layout for the next few photos, balancing cropping,
    the target photos-per-page and variety."""
    pages, i = [], 0
    shapes = {name: frames(name, fmt) for name in LAYOUTS}
    while i < len(photos):
        best = None
        for name, frs in shapes.items():
            batch = photos[i : i + len(frs)]
            if len(batch) < len(frs):
                continue
            loss = sum(0 if f.fit else crop_loss(p.aspect, f.aspect) for p, f in zip(batch, frs))
            cost = 2 * loss / len(frs) + 0.6 * abs(len(frs) - density)
            recent = [pg["layout"] for pg in pages[-4:]]
            cost += 0.5 * recent.count(name) + (0.5 if recent[-1:] == [name] else 0)
            if name == "single" and batch[0].aspect > 1:
                cost += 0.6  # a landscape photo looks better full-bleed
            if best is None or cost < best[0]:
                best = (cost, name, batch)
        _, name, batch = best
        pages.append({"layout": name, "photos": [str(p.path) for p in batch]})
        i += len(batch)
    return pages


def date_range(start: date, end: date) -> str:
    if start == end:
        return f"{start.day} {start:%B %Y}"
    if (start.year, start.month) == (end.year, end.month):
        return f"{start.day} – {end.day} {end:%B %Y}"
    if start.year == end.year:
        return f"{start.day} {start:%B} – {end.day} {end:%B %Y}"
    return f"{start.day} {start:%B %Y} – {end.day} {end:%B %Y}"


def build_plan(
    photos: list[Photo],
    photos_dir: Path,
    fmt: BookFormat,
    title: str | None,
    target_pages: int | None,
    burst_seconds: float,
) -> dict:
    photos = drop_bursts(photos, burst_seconds)
    groups = sections(photos)
    if target_pages:
        photo_pages = max(1, target_pages - len(groups) - (1 if title else 0))
        density = max(1.0, len(photos) / photo_pages)
    else:
        density = DEFAULT_DENSITY

    plan: dict = {"format": fmt.name, "photos_dir": str(photos_dir.resolve())}
    if title:
        plan["title"] = title
    plan["sections"] = [
        {
            "title": city or f"{group[0].taken:%B %Y}",
            "subtitle": date_range(group[0].taken.date(), group[-1].taken.date()),
            "pages": paginate(group, fmt, density),
        }
        for city, group in groups
    ]
    return plan


def write_plan(plan: dict, path: Path) -> None:
    header = (
        "# Book plan. Edit freely, then run `photoalbums render` again.\n"
        f"# Layouts: {', '.join(LAYOUTS)}\n"
        "# A photo can also be written as {file: x.jpg, focus: [0.5, 0.3]} to steer\n"
        "# the crop (x, y from 0 to 1; default is the centre).\n"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(header + yaml.safe_dump(plan, sort_keys=False, allow_unicode=True, width=100))
