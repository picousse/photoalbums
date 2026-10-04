# Exploration 04: Belgian, Ghent and Benelux options

Date: 2026-10-04. Follows up on `02-print-providers.md` (mostly German, UK and US services).

Requirement for our flow: the service must accept **our own finished layout** (a PDF, or full-page or spread images). Services that only offer their own online editor can't take what our generator makes.

## Summary

| Service | Where | Accepts our layout? | Quality | Fit |
|---|---|---|---|---|
| **smartphoto** | **Wetteren, next to Ghent**. Belgian company that prints books in its own lab | ❌ No PDF upload found. Own editor/app only | Mainstream consumer | Local, but **doesn't fit the PDF flow**. Workaround below |
| **CEWE** via Kruidvat / HEMA / cewe.be | Germany, sold in Belgian shops | ✅ "PDF to Book" confirmed on cewe.co.uk and fotoservice.ah.nl (NL); ⚠️ not found on cewe.be | Photo paper + layflat option | Order through the **Dutch AH site** if cewe.be lacks it (check delivery to BE) |
| **Fotofabriek** | Netherlands | ✅ "PDF Uploader" for own designs; InDesign templates | Wins Dutch/Belgian consumer tests; Test-Aankoop lists its A4 Liggend hardcover | **Strong Benelux candidate**. Check exact landscape size and photo-paper options |
| **Profotonet** | Netherlands, professional lab | ⚠️ Not PDF: you import **full JPG/TIFF spreads** into their Album Designer (templates as InDesign/PSD) | Highest: Fujifilm HD Album photo paper, layflat as standard, no logo | **Strong candidate for a premium book**. The renderer would need a "JPG spreads" output (easy to add) |
| **Bookmundo, De Boekdrukker** | Netherlands, print-on-demand book printers | ✅ PDF | Press printing of books, not photo-book grade | Fallback only |
| **Graphius** (Ghent), **Die Keure** (Bruges) | Belgium, offset art-book printers | ✅ (professional prepress) | Excellent, used for museum and art books | **Only for runs of ~300+ copies**. Overkill for a family album |
| Ghent print shops + bookbinders | Ghent | ✅ (bring a PDF) | Depends on the shop; digital press + handbinding | Possible one-off "craft" option; quote needed. Not researched in depth |

## Conclusions

1. **No Ghent or Belgian consumer service accepts a PDF.** smartphoto is local (Wetteren) but only works through its own editor. As a workaround, you could export each page as one full-page image and place it in a single-photo, full-bleed smartphoto template. That's fiddly and their bleed and crop handling is unknown, so it's not recommended.
2. **Best Benelux candidates for our flow:** **Fotofabriek** (PDF upload, good consumer-test results) and **Profotonet** (pro lab, photo paper, layflat, but takes JPG spreads).
3. **Overall shortlist** (with `02-print-providers.md`): Saal Digital (DE), Fotofabriek (NL), Profotonet (NL), WhiteWall (DE), CEWE (DE, via the NL site).
4. Belgian offset printers (Graphius, Die Keure) only make sense if we ever print many copies of one book.

## Next steps

- Get exact landscape sizes, page and cover templates and prices for **Fotofabriek** and **Profotonet**, then add presets in `src/photoalbums/formats.py`.
- Add a `render --jpg-spreads` output for labs that take spread images (Profotonet).
- Check Test-Aankoop's latest photo book comparison (Belgian consumer test) for quality ratings.

## Sources

- smartphoto location and own lab: https://www.element61.be/en/company/smartphoto-0
- smartphoto profits/background: https://thedeadpixelssociety.com/shift-to-gifts-drives-smartphoto-profits-via-tijd/
- Test-Aankoop, best photo book services: https://www.test-aankoop.be/hightech/fotodiensten/nieuws/beste-fotodiensten
- Test-Achats, Fotofabriek Hardcover A4 Liggend: https://www.test-achats.be/hightech/services-photos/comparateur/fotofabriek-hardcover-a4-liggend/489/120040
- Fotofabriek InDesign template guide: https://www.fotofabriek.nl/content/pdf/fotofabriek-templates-handleiding-indesign.pdf
- Fotofabriek PDF uploader (review): https://id.nl/huis-en-entertainment/computer-en-gaming/software/de-leukste-manieren-om-je-vakantiefoto-s-te-delen-66727
- Profotonet, submitting your own design: https://profotonet.com/en/blog/tips-and-advice/submit-your-photo-book-in-a-different-way/
- Profotonet photo books: https://www.profotonet.com/en/blog/products-materials/make-a-photo-book
- CEWE PDF to Book (NL, Albert Heijn): https://fotoservice.ah.nl/cewe-fotoboeken/indesign.html
- CEWE PDF to Book (UK): https://www.cewe.co.uk/pdf2book.html
- Die Keure / Belgian art-book printers: https://printers.oogaboogastore.com/post/119670489
- Graphius / Snoeck / Imschoot overview (search results): https://snoeckpublisher.be/?p=19
- De Boekdrukker reviews: https://au.trustpilot.com/review/deboekdrukker.nl
- Ghent bookbinding listings: https://www.bsearch.be/binden-van-boeken-en-brochures/
