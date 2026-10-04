# Exploration 02: Photo book print providers

Date: 2026-10-04. Covers Blurb, the alternatives in Europe and the US, and Belgian/Ghent/Benelux options.

What we need: a high-quality hardcover photo book, landscape, about 25x20 cm. It ships to Belgium, so EU production is a plus (no customs or import VAT). We generate the interior and cover **ourselves from a script**, so the provider must accept our finished layout: a PDF upload, full-page or spread images, or an API. Services that only offer their own online editor can't take our output.

Legend: ✅ confirmed by an official or current source · ⚠️ partial or unverified · ❌ not offered, as far as I could find.
Prices are starting prices or examples. Most labs run near-permanent discounts of 20-50%, so always check the live configurator.

## 1. Conclusion

**Shortlist:**

| # | Provider | Why | Size closest to 25x20 |
|---|---|---|---|
| 1 | **Saal Digital** (DE) | Best all-rounder: true PDF upload, real Fujifilm photo paper, free layflat, fast, top-rated in 2026 | 27.5x19.3 cm |
| 2 | **Fotofabriek** (NL) | Best Benelux fit for PDF upload; does well in Dutch and Belgian consumer tests | ⚠️ check (A4 landscape listed) |
| 3 | **Profotonet** (NL) | Pro lab: Fujifilm HD Album photo paper, layflat as standard, no logo. Takes **JPG/TIFF spreads**, not PDF | ⚠️ check |
| 4 | **WhiteWall** (DE) | Highest quality and closest size; pricier, ~12 working days | 27x20.5 cm |
| 5 | **CEWE** (DE, via the NL Albert Heijn site) | Cheapest good option; PDF upload not found on cewe.be | 28x21 cm |

- **Blurb** remains the fallback: known, printed in NL, 24.1x20.3 cm trim.
- **Ghent/Belgium:** no consumer service accepts a PDF. smartphoto (Wetteren, next to Ghent) is local but only works through its own editor. Ghent's art-book printers (Graphius) and Bruges' Die Keure only make sense for runs of ~300+ copies. See section 3.
- **Full automation (order by API):** Peecho (NL, layflat lustre) or the Lulu Print API. Lulu's paper is a step below photo paper.
- **None offers exactly 25x20 cm.** The generator keeps trim size, bleed, margins and spine width as per-provider presets (`src/photoalbums/formats.py`). Blurb (24.13x20.32), Saal (27.5x19.3), WhiteWall (27x20.5) and CEWE (28x21) all differ; aspect ratio ranges from 1.19 to 1.42.

## 2. Comparison table

| Provider | Accepts our layout? / how | Size near 25x20 cm landscape | Layflat | Paper / print | Price hint (~40-60 pp hardcover) | Production / EU shipping | API | Quality reputation |
|---|---|---|---|---|---|---|---|---|
| **Recommended, EU** | | | | | | | | |
| **Saal Digital** (DE) | ✅ "PDF Upload" design mode in the online shop: separate **cover PDF + inner-pages PDF** at Saal's template dimensions; Photoshop/InDesign templates in the "Professional Zone" | **28x19** (27.5x19.3 cm closed); also 21x28, 30x30, etc. No exact 25x20 | ✅ **standard on all books, free** | **Real photo paper**: Fujifilm Crystal Archive HD Album (gloss, matte, silk, 368 g/m²) **or** "HighEnd print matte" inkjet on uncoated paper | 28x19 from ~€25 (26 pp, on sale; list €34); 50 pp roughly €45-70 (estimate, check configurator) | Germany; often ships in 1-2 days; EU shipping | ❌ no public API | **Excellent**: DigitalCameraWorld 2026 "best professional photo book"; strong colour, fast |
| **WhiteWall** (DE) | ✅ **PDF upload with auto-generated InDesign/Affinity IDML templates** after you pick format, paper, cover and page count. Inside pages as **single pages**, bleed on 3 sides; cover as one spread; sRGB; pages in steps of 4; up to 1 GB | **"Exhibition A4 Landscape" 27x20.5 cm**: the closest to 25x20 of all providers | ✅ with photographic paper | **Fuji Crystal Archive** photo paper (gloss, silk-matt, deep matt) or inkjet (gloss, silk-matt, high gloss) | from ~£33 / €35 (28 pp); premium, so 50 pp layflat photo paper likely €80-150 (estimate) | Germany (Frechen); ~12 working days | ❌ | **Gallery/pro grade**, highly rated by photo press |
| **CEWE** (DE; sold via cewe.be, Kruidvat, HEMA, AH fotoservice) | ✅ "PDF to Book": InDesign Template Generator gives exact cover and content templates; upload cover PDF + content PDF; instant preflight (dimensions, PDF version). 3 mm bleed on pages, 10 mm on cover, sRGB, min. 26 pp in steps of 4. ⚠️ Confirmed on cewe.co.uk and fotoservice.ah.nl (NL). **Not found on cewe.be**, so check whether Belgian orders can use it | Large Liggend **28x21 cm** (most popular format) | ✅ only with photographic paper | Digital print (Classic, High Gloss, True Matte) up to 178 pp, or **photographic silver-halide paper** with layflat up to 114 pp | 28x21 from ~€35; Test-Aankoop June 2025: 24 pp matte hardcover €44.95 + €5.75 shipping | Germany (Oldenburg etc.); excellent BE/NL retail presence | ❌ | Very good, mainstream market leader; often wins consumer tests |
| **Benelux** | | | | | | | | |
| **Fotofabriek** (NL) | ✅ "PDF Uploader" for own designs; InDesign templates and guide | ⚠️ A4 Liggend hardcover listed by Test-Aankoop; exact landscape sizes to check | ✅ ("vlakliggend", max 140 pp, first page on the left) | ⚠️ photo-paper options to check; 200-300 dpi advised | ⚠️ not checked | Netherlands | ❌ | Wins Dutch/Belgian consumer tests, often cheaper than competitors |
| **Profotonet** (NL) | ⚠️ Not PDF: import **full JPG/TIFF spreads** (sRGB/AdobeRGB) into their Album Designer; InDesign/PSD templates on their sizing page | ⚠️ check sizing page | ✅ **standard** | **Fujifilm HD Album** photo paper (photo-chemical), no barcode or logo | ⚠️ not checked | Netherlands | ❌ | **Pro lab, highest quality** |
| **smartphoto** (BE) | ❌ No PDF upload found; own editor/app only | ⚠️ not checked | ⚠️ | Consumer photo books, printed in their own lab | ⚠️ | **Wetteren, next to Ghent** (BE); serves 14 countries | ❌ | Mainstream consumer |
| **Albelli / Bonusprint** (Storio Group, NL) | ❌ none found: only their own editor/app | Landscape L ~28x21 | ✅ (premium layflat option) | Digital press; photo paper on premium lines | ~€30-50 | NL/EU | ❌ | Good mid-range |
| **Bookmundo**, **De Boekdrukker** (NL) | ✅ PDF (print-on-demand book printers; free shipping to BE for De Boekdrukker) | Various book formats | ⚠️ | Press printing of books, not photo-book grade | ⚠️ | Netherlands | ❌ | Fine for books; fallback only |
| **Peecho** (NL) | ✅ upload a PDF in the dashboard ("no print marks needed"); file-setup guide per product | ⚠️ fixed sizes, not listed publicly (A4, square, etc.) | ✅ 190 gsm E-Photo Lustre, 18-122 pp | Hardcover on Mohawk Superfine (gloss/uncoated) or layflat on lustre; HP Indigo | Hardcover "from €5.20" base (B2B), layflat price on request | NL HQ; global hubs (partner Prodigi); W-Europe 2-7 days + 4-6 days production | ✅ Print API | Good; B2B/print-on-demand focus |
| **Blurb** (US; EU printing in NL) | ✅ PDF to Book: interior PDF of single pages + cover PDF; online preflight | "10x8" = 24.1x20.3 cm trim; Large Landscape 13x11 | ✅ (photo or ProLine uncoated) | HP Indigo press; Premium Matte/Lustre, ProLine papers; layflat on photo paper | ~€35-60 before discounts (estimate) | NL plant for EU, ships to BE in ~1-2 days | ✅ Print API (business or partner oriented) | Solid, consistent; known baseline |
| **Other Europe** | | | | | | | | |
| **Viaprinto** (CEWE's B2B/PDF print shop, DE) | ✅ PDF-native book printing | A4 landscape (29.7x21) | ❌ (⚠️ unverified) | Digital press, 170 g/m² | ⚠️ not checked | Germany | ❌ | Good print, more "document" than "photo book" |
| **Photobox** (Storio Group) | ❌ none found: own editor only | A4 landscape | ✅ "A4 Pro Lay Flat" (Fujifilm Crystal Archive Lustre) | Digital press 170-230 gsm; Pro layflat on silver-halide | A4 Pro Layflat ~£45 for 26 pp + £1.49 per extra page (older review) | EU | ❌ | Good |
| **Pixartprinting** (IT, Cimpress) | ⚠️ PDF is its normal workflow for print products; photo book PDF upload not confirmed | ⚠️ | ⚠️ | Digital press | ⚠️ | Italy, EU | ❌ | Good commercial printer |
| **Gelato** (NO) | ✅ upload print-ready file via dashboard / API (multi-page PDF) | Landscape 8x11 in (~28x21 cm) hardcover | ❌ | 170 gsm silk-coated, glued binding, matte-laminated cover | ⚠️ not found (low-mid) | 140+ partner printers in 32 countries incl. EU; 2-5 days | ✅ Order API | Mixed or variable (depends on local partner); merchandise oriented |
| **Mixam** (UK) | ✅ PDF upload (art books, layflat) | Custom sizes | ✅ | Digital press | quote-based | UK (also US, others); ⚠️ EU customs | ❌ | Good; print-shop style |
| **Prodigi** (UK) | ✅ via API / dashboard with your files | ⚠️ sizes not verified | ✅ (Mohawk Superfine 160 gsm / Mohawk ProPhoto 190 gsm, 18-80 pp) | HP Indigo press | ⚠️ not found | UK + global labs; ⚠️ UK to BE means post-Brexit customs unless an EU lab is routed | ✅ well-documented REST API | Good; business-focused |
| **US / rest of world** | | | | | | | | |
| **Lulu** (US) | ✅ upload interior PDF + cover PDF (templates and cover calculator); ✅ **Lulu Print API** (REST, per-order PDFs) | **US Letter Landscape 11x8.5 in (27.9x21.6 cm)** hardcover casewrap | ❌ | 80# Premium Color coated (inkjet/press, not photo paper) | 11x8.5 hardcover premium colour from $14.76 (base pages) + per page; 50 pp ~$30-40 (estimate) | Global network incl. **France** and UK printers | ✅ Print API, easy and self-serve | OK for books; **not photo-book grade** |
| **Printique** (Adorama, US) | ❌ no PDF; own editor (you can place full-page images) | 11x8.5 landscape | ✅ layflat at no upcharge | **Lustre photo paper** (silver halide), excellent | ~$60-90 | US only; international shipping limited/expensive | ❌ | **DigitalCameraWorld 2026 "best overall"** |
| **Mixbook** (US) | ❌ own editor only | 11x8.5 landscape | ✅ (option) | Press, matte/semi-gloss; layflat photo paper option | budget, heavy discounts | US; ⚠️ international shipping limited | ❌ | Best budget pick (DCW 2026) |
| **Shutterfly** (US) | ❌ own editor only | 11x8 landscape | ✅ | Press | budget | **US only** | ❌ | Mass-market |
| **Artifact Uprising** (US) | ❌ own editor only | 11x8.25 layflat; 10x8 hardcover | ✅ (Superfine matte or photo lustre, ~300 gsm "layflat insert") | Premium | layflat ~$4.60-5.75 per page, so 50 pp roughly $250+ | US; international "special conditions" | ❌ | Premium design and materials; some print-quality complaints |
| **MILK Books** (NZ) | ❌ none found: own editor only | Medium Landscape 23.5x18.8 cm; others up to ~32x24 cm | ✅ (some lines) | Premium, linen and leather covers | Premium (€100+) | NZ/AU-based; ⚠️ production location unclear | ❌ | Luxury, gift-grade |

## 3. Belgium and Ghent

- **smartphoto** (smartphoto group NV) is based in **Wetteren, next to Ghent**, and makes its photo books in its own lab. But I found no PDF upload, only its editor and app.
  - Workaround: export each page as one image and place it in a single-photo, full-bleed smartphoto template. That's fiddly, and their bleed and crop handling is unknown, so it's not recommended.
- **Kruidvat / HEMA / cewe.be** photo books are made by **CEWE** (DE). Use CEWE's PDF to Book, via the NL site if needed.
- **Offset art-book printers:** **Graphius** (Ghent) and **Die Keure** (Bruges, minimum run ~300) do excellent museum and art-book work. Ghent publishers Snoeck and Imschoot work with them. They're only relevant if we ever print many copies of one book.
- **Ghent print shops + bookbinders** (e.g. listed under "binden van boeken"): a possible one-off "craft" option using a digital press and hand binding. Quality depends on the shop, so get a quote. Not researched in depth.

## 4. Blurb: exact PDF specs for Standard Landscape "10x8"

Queried live from Blurb's PDF to Book calculator (blurb.com/make/pdf_to_book/booksize_calculator) on 2026-10-04. Settings: `standard_landscape`, 50 pages, Premium Matte, Hardcover Dust Jacket. The `blurb-standard-landscape` preset in `formats.py` uses these values.

**Important: the "10x8" name is rounded. The real trim is 9.5 x 8.0 in (24.13 x 20.32 cm).**

| Interior page (single pages, not spreads) | inches | points | cm |
|---|---|---|---|
| Final PDF page size (trim + bleed) | **9.625 x 8.25** | **693 x 594** | 24.447 x 20.955 |
| Trim | 9.5 x 8.0 | 684 x 576 | 24.13 x 20.32 |
| Bleed (top, bottom, outside edge only; none at the gutter) | 0.125 | 9 | 0.317 |
| Safe margin (top, bottom, outside) | 0.25 | 18 | 0.635 |
| Safe margin at the binding edge | 0.5 in the table, **0.625 in the page text** (45 pt) | 36 / 45 | 1.27 / 1.587 |

The table and the page text on the same Blurb page disagree about the gutter margin. Use **0.625 in** to be safe.

Because bleed is only on the outside edge, odd (right-hand) pages have the bleed on the right and even pages have it on the left. The 0.125 in of extra width therefore moves from side to side page by page.

**Cover, Hardcover Dust Jacket, 50 pages, Premium Matte:** PDF 28.986 x 8.5 in (2087 x 612 pt). Trim 28.736 x 8.25 in. Bleed 0.125 in all round. Spine 0.458 in (33 pt). Flaps 4.194 in.

- I could not get the **Hardcover ImageWrap** cover numbers or the **layflat** paper options to return from the calculator (layflat came back as all zeros). Read those off the calculator in a browser.
- The cover always depends on page count and paper, so compute it last.

Other Blurb facts (see note 01):
- PDF/X-3, sRGB images, 20-440 pages.
- Papers: Standard, Premium Matte/Lustre, ProLine Uncoated, ProLine Pearl/Medium Gloss, and layflat on photo paper or ProLine uncoated.
- European orders are printed in the Netherlands.
- Price: Standard Landscape ImageWrap starts around £25 for 20 pages, plus about £0.27 per extra page on standard paper (2025 listing, before discounts).

## 5. Google Photos integration

Since the March 2025 Library API change, most "import from Google Photos" buttons broke or moved to the Picker API.
- **Shutterfly** still documents connecting a Google Photos account.
- **Google Photos itself** sells (square) photo books.
- I found no current confirmation for Saal, CEWE, WhiteWall or Blurb.

None of this matters for our pipeline: we build the PDFs locally anyway (see note 01).

## 6. Next steps

- Exact templates and sizes: get page and cover dimensions from Saal's Professional Zone, WhiteWall's generated IDML, and Fotofabriek's and Profotonet's sizing pages. Add presets to `formats.py`.
- Prices: price a ~50-page book at Saal, Fotofabriek, Profotonet and WhiteWall in the live configurators.
- Check whether CEWE PDF to Book can be ordered for Belgian delivery.
- Add a `render --jpg-spreads` output for labs that take spread images (Profotonet).
- Check Test-Aankoop's latest photo book comparison for quality ratings.

## Sources

Blurb
- PDF to Book calculator (queried live): https://www.blurb.com/make/pdf_to_book/booksize_calculator
- Pricing: https://www.blurb.co.uk/pricing ; Choice listing of Blurb 10x8 hardcover: https://www.choice.com.au/products/electronics-and-technology/internet/using-online-services/blurb-standard-landscape-10x8in-25x20-cm-hardcover-imagewrap
- EU production (NL): https://id.nl/zekerheid-en-gemak/veilig-online/beveiligingssoftware/online-boekuitgeverij-blurb-start-vanuit-nederland ; https://www.blurb.co.uk/shipping.html

Saal Digital
- 28x19: https://www.saal-digital.eu/photo-book/28-x-19-photo-book
- Design modes (PDF Upload): https://www.saal-digital.eu/help-center/online-designer/design-modes-for-photo-books/
- Upload your PDF: https://www.saal-digital.eu/service/professional-zone/upload-your-pdf-in-the-online-shop/
- Optimise your PDF: https://www.saal-digital.eu/service/professional-zone/optimise-your-pdf/
- Professional Zone (templates and dimensions): https://www.saal-digital.eu/photo-book/professional-zone/
- Layflat standard: https://www.saal-digital.eu/photo-book/layflat-binding

CEWE
- PDF to Book user guide: https://www.cewe.co.uk/pdf-to-book-user-guide.html ; PDF: https://cdn.cewe.co.uk/downloads/user-guide.pdf ; https://www.cewe.co.uk/pdf2book.html
- InDesign/PDF at AH fotoservice (NL): https://fotoservice.ah.nl/cewe-fotoboeken/indesign.html
- Large Liggend 28x21: https://fotoservice.ah.nl/cewe-fotoboeken/large-liggend-10759-gs.html ; Test-Aankoop: https://www.test-aankoop.be/hightech/fotodiensten/vergelijker/cewe-fotoboek-large-liggend/489/120041

WhiteWall
- Coffee table book: https://whitewall.com/uk/coffee-table-book
- PDF upload: https://www.whitewall.com/eu/coffee-table-book/pdf-upload
- Dimensions guide: https://service.whitewall.com/hc/en-us/articles/4411250911377-03-Setting-the-correct-dimensions-for-cover-and-content-pages

Benelux and Belgium
- Fotofabriek InDesign template guide: https://www.fotofabriek.nl/content/pdf/fotofabriek-templates-handleiding-indesign.pdf
- Fotofabriek PDF uploader (review): https://id.nl/huis-en-entertainment/computer-en-gaming/software/de-leukste-manieren-om-je-vakantiefoto-s-te-delen-66727
- Test-Achats, Fotofabriek Hardcover A4 Liggend: https://www.test-achats.be/hightech/services-photos/comparateur/fotofabriek-hardcover-a4-liggend/489/120040
- Profotonet, submitting your own design: https://profotonet.com/en/blog/tips-and-advice/submit-your-photo-book-in-a-different-way/
- Profotonet photo books: https://www.profotonet.com/en/blog/products-materials/make-a-photo-book
- smartphoto location and own lab: https://www.element61.be/en/company/smartphoto-0 ; https://thedeadpixelssociety.com/shift-to-gifts-drives-smartphoto-profits-via-tijd/
- Test-Aankoop best photo services: https://www.test-aankoop.be/hightech/fotodiensten/nieuws/beste-fotodiensten
- Die Keure / Belgian art-book printers: https://printers.oogaboogastore.com/post/119670489
- Snoeck Publishers: https://snoeckpublisher.be/?p=19
- De Boekdrukker reviews: https://au.trustpilot.com/review/deboekdrukker.nl
- Ghent bookbinding listings: https://www.bsearch.be/binden-van-boeken-en-brochures/
- Peecho layflat: https://peecho.com/products/books/layflat ; photo books: https://peecho.com/blog/print-on-demand-photo-books ; PDF to book: https://webflow.peecho.com/blog/pdf-to-book-printing

Others
- Lulu photo books: https://www.lulu.com/create/photo-books ; products: https://www.lulu.com/products ; Print API products: https://www.lulu.com/print-api/products ; API help: https://help.api.lulu.com/ ; shipping: https://blog.lulu.com/international-book-shipping/
- Gelato photo books: https://www.gelato.com/products/photo-books ; sizes: https://gelato.com/blog/photo-book-sizes ; design help: https://support.gelato.com/en/articles/8996282-how-do-i-design-a-photo-book
- Photobox A4 Pro Lay Flat review: https://amateurphotographer.com/field-tests/accessory_reviews/a4-pro-lay-flat-photo-book-review/ ; https://www.digitalcameraworld.com/reviews/photobox-photo-book-review
- Artifact Uprising layflat: https://www.artifactuprising.com/photo-books/layflat-photo-album
- MILK Books (sizes, via reviews): https://www.5minutesformom.com/milk-medium-landscape-milk-books-photobook-giveaway/ ; https://www.productreview.com.au/listings/milk-books
- Mixam layflat: https://www.mixam.co.uk/layflat
- Viaprinto/Albelli comparison (Macwelt): https://www.macwelt.de/article/928725/urlaubsfotos-fotobuchanbieter-im-vergleich.html
- Shutterfly + Google Photos: https://www.shutterfly.com/ideas/how-to-upload-google-photos-to-shutterfly/

Reviews
- DigitalCameraWorld best photo books 2026: https://www.digitalcameraworld.com/buying-guides/the-best-photo-books-in-2020-create-a-personalized-picture-album-online
- PetaPixel best photo book services 2026: https://petapixel.com/best-photo-book-services/
- Tom's Guide best photo books 2025: https://tomsguide.com/best-picks/best-photo-books
