"""Generate print-ready photo books from a folder of photos."""

import argparse
from pathlib import Path

import yaml


def main() -> None:
    parser = argparse.ArgumentParser(prog="photoalbums", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("plan", help="scan a photo folder and write an editable book plan")
    p.add_argument("photos", type=Path, help="folder with photos (e.g. a Google Photos download)")
    p.add_argument("-o", "--out", type=Path, default=Path("book.yaml"))
    p.add_argument("--format", default="25x20")
    p.add_argument("--title", help="optional title page at the start of the book")
    p.add_argument("--pages", type=int, help="aim for roughly this many pages")
    p.add_argument("--burst-seconds", type=float, default=2.0, help="drop shots taken closer together")

    r = sub.add_parser("render", help="render a book plan to PDF")
    r.add_argument("plan", type=Path)
    r.add_argument("-o", "--out", type=Path, help="print PDF (default: <plan>.pdf)")
    r.add_argument("--spreads", action="store_true", help="also write a facing-pages preview PDF")
    r.add_argument("--dpi", type=int, default=300)

    sub.add_parser("formats", help="list book formats")

    args = parser.parse_args()
    if args.command == "plan":
        from .formats import FORMATS
        from .plan import build_plan, write_plan
        from .scan import scan

        photos = scan(args.photos)
        plan = build_plan(photos, args.photos, FORMATS[args.format], args.title, args.pages, args.burst_seconds)
        write_plan(plan, args.out)
        n_pages = sum(len(s["pages"]) + 1 for s in plan["sections"]) + bool(args.title)
        kept = sum(len(pg["photos"]) for s in plan["sections"] for pg in s["pages"])
        print(f"{kept} of {len(photos)} photos (bursts dropped) -> {len(plan['sections'])} sections, ~{n_pages} pages -> {args.out}")

    elif args.command == "render":
        from .render import render_print, render_spreads

        plan = yaml.safe_load(args.plan.read_text())
        out = args.out or args.plan.with_suffix(".pdf")
        r = render_print(plan, out, args.dpi)
        print(f"print PDF -> {out}")
        if args.spreads:
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
