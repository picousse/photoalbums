# photoalbums

Turns a folder of photos (e.g. a Google Photos / Takeout download) into a
print-ready hardcover photo book PDF. Default format: 25 x 20 cm landscape.

Photos and books live in `data/` (gitignored):

```
data/pictures/<album>/   the photos (unzipped Google Photos album download)
data/albums/<album>/     book.yaml (the editable plan), book.pdf, book-spreads.pdf
```

```sh
uv run photoalbums new lisbon-2025      # creates both folders
# unzip the album download into data/pictures/lisbon-2025/
uv run photoalbums select lisbon-2025   # best photo per moment -> selection.yaml + contact sheets
uv run photoalbums drop lisbon-2025 3 7 12-15   # remove photos by contact-sheet number
uv run photoalbums plan lisbon-2025     # options: --pages 40 --title "Lisbon" --format 25x20
# edit data/albums/lisbon-2025/book.yaml: reorder photos, change layouts, rename sections, set crop focus
uv run photoalbums render lisbon-2025   # book.pdf (print) + book-spreads.pdf (preview)
uv run photoalbums list                 # albums and their status
uv run photoalbums formats
```

`plan` refuses to overwrite an existing `book.yaml` (it may hold your edits) unless you pass `--force`.
`plan` and `render` also accept plain paths (a photo folder, a `book.yaml`). Set `PHOTOALBUMS_DATA` to use another data folder.

What `select` does (`data/albums/<album>/selection.yaml`, edit freely):

- measures sharpness (sharpest regions, so a soft background is fine) and exposure per photo; cached
- groups shots of the same moment (within 180 s and visually similar), drops near-identical copies (e.g. the same photo from two phones), keeps the best third per moment
- writes numbered contact sheets per day to `data/albums/<album>/sheets/` for review
- dates WhatsApp images from their file name; photos without GPS take the city of the nearest located photo (within 3 h), useful when only one phone records location

Composition and storytelling are judged by Claude with the project skill `.claude/skills/photobook/SKILL.md` (ask Claude to "review the selection of <album>").

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
