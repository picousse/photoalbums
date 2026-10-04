"""Generate print-ready photo books from a folder of photos."""

import argparse
import os
import sys
from pathlib import Path

import yaml

# data/pictures/<album>/ holds the photos, data/albums/<album>/ the plan and PDFs.
DATA = Path(os.environ.get("PHOTOALBUMS_DATA", Path(__file__).resolve().parents[2] / "data"))
PICTURES, ALBUMS = DATA / "pictures", DATA / "albums"


def album_dirs(name: str) -> tuple[Path, Path]:
    return PICTURES / name, ALBUMS / name


def resolve_photos(album: str) -> tuple[Path, Path]:
    """Accept an album name (data/pictures/<name>) or any photo folder path.
    Returns (photos folder, album output folder)."""
    photos, out_dir = album_dirs(album)
    if not photos.is_dir() and Path(album).is_dir():
        photos = Path(album)
        out_dir = ALBUMS / photos.resolve().name
    return photos, out_dir


def resolve_plan(album: str) -> Path:
    """Accept an album name or a path to a book.yaml."""
    plan = ALBUMS / album / "book.yaml"
    return plan if plan.is_file() else Path(album)


def main() -> None:
    parser = argparse.ArgumentParser(prog="photoalbums", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    n = sub.add_parser("new", help="create the folders for a new album")
    n.add_argument("album", help="album name, e.g. lisbon-2025")

    sub.add_parser("list", help="list albums and their status")

    p = sub.add_parser("plan", help="scan an album's photos and write an editable book plan")
    p.add_argument("album", help="album name (data/pictures/<album>) or a photo folder path")
    p.add_argument("-o", "--out", type=Path, help="default: data/albums/<album>/book.yaml")
    p.add_argument("--force", action="store_true", help="overwrite an existing (possibly edited) plan")
    p.add_argument("--format", default="25x20")
    p.add_argument("--title", help="optional title page at the start of the book")
    p.add_argument("--pages", type=int, help="aim for roughly this many pages")
    p.add_argument("--burst-seconds", type=float, default=2.0, help="drop shots taken closer together")

    r = sub.add_parser("render", help="render a book plan to PDF")
    r.add_argument("album", help="album name or a path to a book.yaml")
    r.add_argument("-o", "--out", type=Path, help="print PDF (default: next to the plan)")
    r.add_argument("--no-spreads", action="store_true", help="skip the facing-pages preview PDF")
    r.add_argument("--dpi", type=int, default=300)

    sub.add_parser("formats", help="list book formats")

    args = parser.parse_args()
    if args.command == "new":
        photos, out_dir = album_dirs(args.album)
        photos.mkdir(parents=True, exist_ok=True)
        out_dir.mkdir(parents=True, exist_ok=True)
        print(f"Put the photos (unzipped album download) in:\n  {photos}")
        print(f"Then run:\n  uv run photoalbums plan {args.album}")

    elif args.command == "list":
        names = sorted({d.name for root in (PICTURES, ALBUMS) if root.is_dir() for d in root.iterdir() if d.is_dir()})
        if not names:
            print(f"No albums yet. Create one with: uv run photoalbums new <name>")
        for name in names:
            photos, out_dir = album_dirs(name)
            n_files = sum(1 for f in photos.rglob("*") if f.is_file() and f.suffix.lower() != ".json") if photos.is_dir() else 0
            status = "rendered" if (out_dir / "book.pdf").exists() else "planned" if (out_dir / "book.yaml").exists() else "no plan"
            print(f"{name:30} {n_files:5} files  {status}")

    elif args.command == "plan":
        from .formats import FORMATS
        from .plan import build_plan, write_plan
        from .scan import scan

        photos_dir, out_dir = resolve_photos(args.album)
        if not photos_dir.is_dir():
            sys.exit(f"No photo folder {photos_dir}. Create it with: uv run photoalbums new {args.album}")
        out = args.out or out_dir / "book.yaml"
        if out.exists() and not args.force:
            sys.exit(f"{out} already exists (and may contain your edits). Use --force to overwrite it.")

        photos = scan(photos_dir)
        if not photos:
            sys.exit(f"No photos found in {photos_dir}.")
        plan = build_plan(photos, photos_dir, FORMATS[args.format], args.title, args.pages, args.burst_seconds)
        write_plan(plan, out)
        n_pages = sum(len(s["pages"]) + 1 for s in plan["sections"]) + bool(args.title)
        kept = sum(len(pg["photos"]) for s in plan["sections"] for pg in s["pages"])
        print(f"{kept} of {len(photos)} photos (bursts dropped) -> {len(plan['sections'])} sections, ~{n_pages} pages -> {out}")
        print(f"Edit it if you like, then run: uv run photoalbums render {args.album}")

    elif args.command == "render":
        from .render import render_print, render_spreads

        plan_path = resolve_plan(args.album)
        if not plan_path.is_file():
            sys.exit(f"No plan found for {args.album}. Run first: uv run photoalbums plan {args.album}")
        plan = yaml.safe_load(plan_path.read_text())
        out = args.out or plan_path.with_suffix(".pdf")
        r = render_print(plan, out, args.dpi)
        print(f"print PDF -> {out}")
        if not args.no_spreads:
            preview = out.with_name(out.stem + "-spreads.pdf")
            render_spreads(plan, preview)
            print(f"spreads preview -> {preview}")
        for w in dict.fromkeys(r.warnings):
            print(f"warning: {w}")

    elif args.command == "formats":
        from .formats import FORMATS

        for f in FORMATS.values():
            pw, ph = f.page_size()
            print(f"{f.name:28} trim {f.trim_w}x{f.trim_h} mm, page {pw:.1f}x{ph:.1f} mm  {f.description}")
