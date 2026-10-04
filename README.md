# photoalbums

Turns a folder of photos (e.g. a Google Photos / Takeout download) into a
print-ready hardcover photo book PDF. Default format: 25 x 20 cm landscape.

Local data lives in `data/` (gitignored): put downloaded photos in
`data/pictures/<album>/` and keep plans and PDFs in `data/albums/<album>/`.

```sh
uv run photoalbums plan data/pictures/summer -o data/albums/summer/book.yaml --title "Summer 2025" --pages 40
uv run photoalbums render data/albums/summer/book.yaml --spreads
```

Other examples:

```sh
uv run photoalbums plan ~/Pictures/summer -o book.yaml --title "Summer 2025" --pages 40
# edit book.yaml: reorder photos, change layouts, rename sections, set crop focus
uv run photoalbums render book.yaml --spreads   # book.pdf (print) + book-spreads.pdf (preview)
uv run photoalbums formats
```

What `plan` does:

- reads capture time and GPS from EXIF or Google Takeout JSON sidecars
- drops burst shots (photos taken within 2 s of each other)
- groups photos by day, names each group after its most common city (offline lookup), merges consecutive days in the same city
- adds a title page per group (city + dates) and picks page layouts that avoid heavy cropping, vary from page to page and aim for `--pages`

What `render` does:

- print PDF: single pages with bleed and a TrimBox, page 1 is a right-hand page, padded to an even page count (min. 20)
- spreads preview: facing pages as they appear in the bound book
- warns when a photo would print below 200 dpi

No real photos at hand? `uv run scripts/make_sample_photos.py samples/` makes placeholders.

Not done yet: cover PDF (needs the provider's spine width), PDF/X conversion, photo quality selection. See `notes/`.
