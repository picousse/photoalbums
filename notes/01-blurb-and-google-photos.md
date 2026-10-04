# Exploration 01: Blurb printing + Google Photos source

Date: 2026-10-04

Context: we used to design photo albums ourselves and print them as hardcover books with Blurb. The photos live in Google Photos.

## Blurb: ways to get a book printed

| Route | What it is | Fit for automation |
|---|---|---|
| BookWright | Free desktop layout app from Blurb, still maintained (updated March 2026) | Manual only |
| Adobe InDesign plug-in | Blurb templates and upload from inside InDesign | Manual |
| **PDF to Book** | Upload print-ready PDFs (interior + cover) made in any tool | **Good**: we can generate the PDFs ourselves |
| Print API | REST print-on-demand API (orders, PDF upload, tracking), launched 2018 with partners such as StoryWorth | Partner/business-oriented, probably overkill for personal use |

### PDF to Book requirements (from public docs, check against Blurb's calculator before printing)

- PDF/X-3:2002 export.
- Even page count. Photo books run 20 to 440 pages; prices start at 20 pages.
- Images at 150 to 300 DPI. Max upload 2 GB.
- Interior is one PDF with **single pages** (not spreads). Page 1 is a right-hand page, so spreads are pairs (2-3, 4-5, ...).
- Cover is a separate single-page PDF (back + spine + front). Spine width depends on page count and paper, so **make the cover last**.
- Use 100% K for black text; no spot or registration colours.
- Exact trim, bleed and safe-zone sizes per format come from Blurb's book size calculator. Don't hard-code them from memory.
- Cover types: Hardcover ImageWrap, Hardcover Dust Jacket, Softcover.

### Photo book formats

Mini Square 5x5", Small Square 7x7", Standard Portrait 8x10", Standard Landscape 10x8", Large Square 12x12", Large Landscape 13x11".

These names are rounded. Standard Landscape is really 9.5 x 8 in trim; see `02-print-providers.md` for the exact calculator values.

## Google Photos: getting the photos out

API change on **31 March 2025**: the Library API's `photoslibrary.readonly`, `photoslibrary.sharing` and full `photoslibrary` scopes were removed. Calls that used them now return 403. An app can only read media **it uploaded itself**.

What still works:

1. **Picker API**: the user opens a Google picker and selects photos or an album for a session. The app then downloads those items. Works well for "pick the photos for this album" and is the official route.
2. **Google Takeout**: bulk export of the whole library or chosen albums as zip files with JSON metadata sidecars (dates, GPS, descriptions). Good for a one-off or periodic offline copy. Slow and manual.
3. **Manual download** of an album from the web UI (zip).

The Library API can no longer browse the whole library, so any tool should take a **local folder of photos** as input. The Picker API or Takeout can fill that folder.

## Possible pipeline

```
Google Photos --(Picker API / Takeout)--> local folder
   --> select & order (by date / event, drop duplicates & blurry shots)
   --> auto-layout pages (templates: 1-up, 2-up, 4-up, full-bleed spread)
   --> render interior PDF (PDF/X-3, correct trim+bleed) + cover PDF (spine from page count)
   --> upload to Blurb "PDF to Book" --> hardcover
```

## Open questions

- Which book size and paper did we use before? That sets the template dimensions.
- How much should be automatic and how much hand-tuned? Fully automatic layout, or a draft that gets edited?
- Captions or text pages?
- PDF rendering stack: Python (reportlab / weasyprint + Ghostscript for PDF/X), or HTML/CSS paged media?

## Sources

- Blurb PDF to Book: https://www.blurb.com/pdf-to-book
- Blurb photo book sizes: https://www.blurb.co.uk/lp/photo-books
- Blurb-ready PDF criteria: https://openlab.citytech.cuny.edu/csanchez-eportfolio/academics/courses/sample-course/blurbbookspecs/
- Blurb PDF workflow news: https://www.photographyblog.com/news/new_pdf_to_book_workflow_from_blurb
- Blurb Print API launch: https://thedeadpixelssociety.com/blurb-inc-launches-new-print-api-with-two-partners/
- BookWright status: https://www.capterra.com/p/228872/BookWright/
- Google Photos API updates: https://developers.google.com/photos/support/updates
- Google Photos release notes: https://developers.google.com/photos/library/support/release-notes
