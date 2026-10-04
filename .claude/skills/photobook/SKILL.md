---
name: photobook
description: Make a printed photo book from an album in this repo - select the best photos (composition, sharpness, duplicates), plan the layout and render the print PDF. Use when the user wants to create, curate, review or render a photo album / photo book.
---

# Photo book workflow

The CLI is `uv run photoalbums`. Albums live in the gitignored `data/` folder:
`data/pictures/<album>/` (photos) and `data/albums/<album>/` (selection, plan, PDFs).

1. `photoalbums new <album>`: create the folders; the user unzips the Google Photos album download into `data/pictures/<album>/`.
2. `photoalbums select <album>`: automatic pass. It measures sharpness and exposure, groups shots of the same moment, drops near-identical copies, keeps the best ~third per moment, and writes `selection.yaml` plus numbered contact sheets in `data/albums/<album>/sheets/` (`index.tsv` maps numbers to files). Without `--force` it only refreshes the sheets.
3. **Claude review** (below): cut the selection to the target size by composition and story.
4. `photoalbums plan <album> --pages N`: layout into `book.yaml` (refuses to overwrite without `--force`).
5. `photoalbums render <album>`: `book.pdf` (print) and `book-spreads.pdf` (preview). Look at the spreads (render pages to PNG with `gs -sDEVICE=png16m -r20`) and fix `book.yaml` where a layout or crop doesn't work.

## Claude review of the selection

Ask for the target first: number of pages (rule of thumb: ~2.5 photos per page, so 60 pages ≈ 150 photos). Divide the photo budget over the days in proportion to how eventful they are, not evenly.

Go through the sheets in `data/albums/<album>/sheets/` day by day with `Read`, and note the numbers to drop. Then apply them per batch: `photoalbums drop <album> 3 7 12-15`. **Sheet numbers stay valid until the sheets are refreshed**, so finish dropping for a set of sheets before running `select` again (which renumbers).

Drop:
- near-duplicates the automatic pass missed (same scene, slightly different framing): keep the strongest one
- "notes" photos: signs, timetables, phone numbers, receipts, parking spots, menus (unless it's a memorable menu)
- blurred, tilted horizons that can't be fixed by cropping, accidental shots, heavy backlight with dark faces
- photos where people's eyes are closed or faces are turned away when a better version of the moment exists
- screenshots and forwarded images of poor quality

Prefer:
- people (the family) over empty scenery when both cover the same moment; faces visible, eyes open, natural expressions
- strong composition: clear subject, clean background, rule of thirds or confident symmetry, leading lines, good light
- variety: a mix of wide views, people, and details per day; landscape photos for full-bleed pages
- one or two "hero" shots per place (the photo you'd frame), keep those even if the day is over budget

Claude does not see EXIF: the sheet file name gives the day, `selection.yaml` gives time and city per moment. Don't try to identify people; describe them ("the boy in the red shirt") when explaining choices to the user.

After the review, report: photos kept per day, what kinds of photos were dropped, and anything uncertain the user should look at themselves (list sheet numbers). The user can also move files between `keep` and `alternates` in `selection.yaml` by hand.
