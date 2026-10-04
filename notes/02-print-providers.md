# Exploration 02: Photo book print providers (alternatives to Blurb)

Date: 2026-10-04

What we need: a high-quality hardcover photo book, landscape, about 25x20 cm (10x8"). Shipped to Belgium, so EU production is a plus (no customs or import VAT). We generate the interior and cover as **print-ready PDFs from a script**, so the provider must accept a PDF upload or have an API.

Legend: ✅ confirmed by an official or current source · ⚠️ partial or unverified · ❌ not offered, as far as I could find.
Prices are starting prices or examples. Most labs run near-permanent discounts of 20-50%, so always check the live configurator.

## 1. Blurb baseline: exact PDF specs for Standard Landscape "10x8"

Queried live from Blurb's PDF to Book calculator (blurb.com/make/pdf_to_book/booksize_calculator) on 2026-10-04. Settings: `standard_landscape`, 50 pages, Premium Matte, Hardcover Dust Jacket.

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

## 2. Comparison table

| Provider | Accepts PDF? / how | Size near 25x20 cm landscape | Layflat | Paper / print | Price hint (~40-60 pp hardcover) | Production / EU shipping | API | Quality reputation |
|---|---|---|---|---|---|---|---|---|
| **Blurb** (baseline) | ✅ PDF to Book: interior PDF of single pages + cover PDF; online preflight | "10x8" = 24.1x20.3 cm trim; Large Landscape 13x11 | ✅ (photo or ProLine uncoated) | HP Indigo press; Premium Matte/Lustre, ProLine papers; layflat on photo paper | ~€35-60 before discounts (estimate) | NL plant for EU, ships to BE in ~1-2 days | ✅ Print API (business or partner oriented) | Solid, consistent; known baseline |
| **Saal Digital** (DE) | ✅ "PDF Upload" design mode in the online shop: separate **cover PDF + inner-pages PDF** at Saal's template dimensions; Photoshop/InDesign templates in the "Professional Zone" | **28x19** (27.5x19.3 cm closed); also 21x28, 30x30, etc. No exact 25x20 | ✅ **standard on all books, free** | **Real photo paper**: Fujifilm Crystal Archive HD Album (gloss, matte, silk, 368 g/m²) **or** "HighEnd print matte" inkjet on uncoated paper | 28x19 from ~€25 (26 pp, on sale; list €34); 50 pp roughly €45-70 (estimate, check configurator) | Germany; often ships in 1-2 days; EU shipping | ❌ no public API | **Excellent**: DigitalCameraWorld 2026 "best professional photo book"; strong colour, fast |
| **CEWE** (DE; sold via cewe.be, Kruidvat, HEMA, AH fotoservice) | ✅ "PDF to Book": InDesign Template Generator gives exact cover and content templates; upload cover PDF + content PDF; instant preflight (dimensions, PDF version). 3 mm bleed on pages, 10 mm on cover, sRGB, min. 26 pp in steps of 4. ⚠️ Confirmed on cewe.co.uk and fotoservice.ah.nl (NL). **Not found on cewe.be**, so check whether Belgian orders can use it | Large Liggend **28x21 cm** (most popular format) | ✅ only with photographic paper | Digital print (Classic, High Gloss, True Matte) up to 178 pp, or **photographic silver-halide paper** with layflat up to 114 pp | 28x21 from ~€35; Test-Aankoop June 2025: 24 pp matte hardcover €44.95 + €5.75 shipping | Germany (Oldenburg etc.); excellent BE/NL retail presence | ❌ | Very good, mainstream market leader; often wins consumer tests |
| **Viaprinto** (CEWE's B2B/PDF print shop, DE) | ✅ PDF-native book printing | A4 landscape (29.7x21) | ❌ (⚠️ unverified) | Digital press, 170 g/m² | ⚠️ not checked | Germany | ❌ | Good print, more "document" than "photo book" |
| **Albelli / Bonusprint** (Storio Group, NL) | ❌ none found: only their own editor/app | Landscape L ~28x21 | ✅ (premium layflat option) | Digital press; photo paper on premium lines | ~€30-50 | NL/EU | ❌ | Good mid-range |
| **Photobox** (Storio Group) | ❌ none found: own editor only | A4 landscape | ✅ "A4 Pro Lay Flat" (Fujifilm Crystal Archive Lustre) | Digital press 170-230 gsm; Pro layflat on silver-halide | A4 Pro Layflat ~£45 for 26 pp + £1.49 per extra page (older review) | EU | ❌ | Good |
| **WhiteWall** (DE) | ✅ **PDF upload with auto-generated InDesign/Affinity IDML templates** after you pick format, paper, cover and page count. Inside pages as **single pages**, bleed on 3 sides; cover as one spread; sRGB; pages in steps of 4; up to 1 GB | **"Exhibition A4 Landscape" 27x20.5 cm**: the closest to 25x20 of all providers | ✅ with photographic paper | **Fuji Crystal Archive** photo paper (gloss, silk-matt, deep matt) or inkjet (gloss, silk-matt, high gloss) | from ~£33 / €35 (28 pp); premium, so 50 pp layflat photo paper likely €80-150 (estimate) | Germany (Frechen); ~12 working days | ❌ | **Gallery/pro grade**, highly rated by photo press |
| **Peecho** (NL) | ✅ upload a PDF in the dashboard ("no print marks needed"); file-setup guide per product | ⚠️ fixed sizes, not listed publicly (A4, square, etc.) | ✅ 190 gsm E-Photo Lustre, 18-122 pp | Hardcover on Mohawk Superfine (gloss/uncoated) or layflat on lustre; HP Indigo | Hardcover "from €5.20" base (B2B), layflat price on request | NL HQ; global hubs (partner Prodigi); W-Europe 2-7 days + 4-6 days production | ✅ Print API | Good; B2B/print-on-demand focus |
| **Prodigi** (UK) | ✅ via API / dashboard with your files | ⚠️ sizes not verified | ✅ (Mohawk Superfine 160 gsm / Mohawk ProPhoto 190 gsm, 18-80 pp) | HP Indigo press | ⚠️ not found | UK + global labs; ⚠️ UK to BE means post-Brexit customs unless an EU lab is routed | ✅ well-documented REST API | Good; business-focused |
| **Lulu** (US) | ✅ upload interior PDF + cover PDF (templates and cover calculator); ✅ **Lulu Print API** (REST, per-order PDFs) | **US Letter Landscape 11x8.5 in (27.9x21.6 cm)** hardcover casewrap | ❌ | 80# Premium Color coated (inkjet/press, not photo paper) | 11x8.5 hardcover premium colour from $14.76 (base pages) + per page; 50 pp ~$30-40 (estimate) | Global network incl. **France** and UK printers | ✅ Print API, easy and self-serve | OK for books; **not photo-book grade** |
| **Gelato** (NO) | ✅ upload print-ready file via dashboard / API (multi-page PDF) | Landscape 8x11 in (~28x21 cm) hardcover | ❌ | 170 gsm silk-coated, glued binding, matte-laminated cover | ⚠️ not found (low-mid) | 140+ partner printers in 32 countries incl. EU; 2-5 days | ✅ Order API | Mixed or variable (depends on local partner); merchandise oriented |
| **Pixartprinting** (IT, Cimpress) | ⚠️ PDF is its normal workflow for print products; photo book PDF upload not confirmed | ⚠️ | ⚠️ | Digital press | ⚠️ | Italy, EU | ❌ | Good commercial printer |
| **Mixam** (UK) | ✅ PDF upload (art books, layflat) | Custom sizes | ✅ | Digital press | quote-based | UK (also US, others); ⚠️ EU customs | ❌ | Good; print-shop style |
| **Printique** (Adorama, US) | ❌ no PDF; own editor (you can place full-page images) | 11x8.5 landscape | ✅ layflat at no upcharge | **Lustre photo paper** (silver halide), excellent | ~$60-90 | US only; international shipping limited/expensive | ❌ | **DigitalCameraWorld 2026 "best overall"** |
| **Mixbook** (US) | ❌ own editor only | 11x8.5 landscape | ✅ (option) | Press, matte/semi-gloss; layflat photo paper option | budget, heavy discounts | US; ⚠️ international shipping limited | ❌ | Best budget pick (DCW 2026) |
| **Shutterfly** (US) | ❌ own editor only | 11x8 landscape | ✅ | Press | budget | **US only** | ❌ | Mass-market |
| **Artifact Uprising** (US) | ❌ own editor only | 11x8.25 layflat; 10x8 hardcover | ✅ (Superfine matte or photo lustre, ~300 gsm "layflat insert") | Premium | layflat ~$4.60-5.75 per page, so 50 pp roughly $250+ | US; international "special conditions" | ❌ | Premium design and materials; some print-quality complaints |
| **MILK Books** (NZ) | ❌ none found: own editor only | Medium Landscape 23.5x18.8 cm; others up to ~32x24 cm | ✅ (some lines) | Premium, linen and leather covers | Premium (€100+) | NZ/AU-based; ⚠️ production location unclear | ❌ | Luxury, gift-grade |

### Google Photos integration
Since the March 2025 Library API change, most "import from Google Photos" buttons broke or moved to the Picker API.
- **Shutterfly** still documents connecting a Google Photos account.
- **Google Photos itself** sells (square) photo books.
- I found no current confirmation for Saal, CEWE, WhiteWall or Blurb.

None of this matters for our PDF pipeline: we build the PDFs locally anyway (see note 01).

## 3. Recommendation (easy + high quality + PDF upload + EU)

1. **Saal Digital: best all-rounder.**
   - True PDF upload in the normal online shop (cover PDF + pages PDF).
   - Real Fujifilm photo paper, with layflat free on every book.
   - German production, very fast, top-rated quality in 2026 reviews, competitive prices.
   - Catch: the closest landscape size is **28x19 (27.5x19.3 cm)**, not 25x20. Get exact pixel/mm dimensions from the Professional Zone templates; the page loads them with JavaScript, so I couldn't read them here.
2. **WhiteWall: highest quality, closest size.**
   - **27x20.5 cm "Exhibition A4 Landscape"** on Fuji Crystal Archive with layflat.
   - Clean PDF workflow: single pages with 3-side bleed, plus a generated IDML template giving exact dimensions per config.
   - Pricier and slower (~12 working days). Choose it for "the good album".
3. **CEWE: cheapest good option.**
   - **28x21 cm**, with photographic-paper layflat or digital print.
   - Mature PDF to Book flow with instant preflight, sold everywhere in BE/NL.
   - Check first that PDF to Book can be ordered for Belgian delivery (confirmed for UK and AH-NL, not seen on cewe.be).

Keep **Blurb** as the fallback: known, NL-printed, 24.1x20.3 cm trim. If we ever want full automation (order by API), **Peecho** (NL, layflat lustre) or the **Lulu Print API** are the realistic options. Lulu's paper is a step below photo paper.

**Design implication for the generator:** make the trim size, bleed (3-side for interiors, 4-side for covers), safe margins and spine width per-provider config. Blurb (24.13x20.32), Saal (27.5x19.3), WhiteWall (27x20.5) and CEWE (28x21) all differ, and the aspect ratio ranges from 1.19 to 1.42.

## Sources

- Blurb PDF to Book calculator (queried live): https://www.blurb.com/make/pdf_to_book/booksize_calculator
- Blurb pricing: https://www.blurb.co.uk/pricing ; Choice listing of Blurb 10x8 hardcover: https://www.choice.com.au/products/electronics-and-technology/internet/using-online-services/blurb-standard-landscape-10x8in-25x20-cm-hardcover-imagewrap
- Blurb EU production (NL): https://id.nl/zekerheid-en-gemak/veilig-online/beveiligingssoftware/online-boekuitgeverij-blurb-start-vanuit-nederland ; https://www.blurb.co.uk/shipping.html
- Saal Digital 28x19: https://www.saal-digital.eu/photo-book/28-x-19-photo-book
- Saal Digital design modes (PDF Upload): https://www.saal-digital.eu/help-center/online-designer/design-modes-for-photo-books/
- Saal Digital Upload your PDF: https://www.saal-digital.eu/service/professional-zone/upload-your-pdf-in-the-online-shop/
- Saal Digital Optimise your PDF: https://www.saal-digital.eu/service/professional-zone/optimise-your-pdf/
- Saal Digital Professional Zone (templates and dimensions): https://www.saal-digital.eu/photo-book/professional-zone/
- Saal Digital layflat standard: https://www.saal-digital.eu/photo-book/layflat-binding
- CEWE PDF to Book user guide: https://www.cewe.co.uk/pdf-to-book-user-guide.html ; PDF: https://cdn.cewe.co.uk/downloads/user-guide.pdf ; https://www.cewe.co.uk/pdf2book.html
- CEWE InDesign/PDF at AH fotoservice (NL): https://fotoservice.ah.nl/cewe-fotoboeken/indesign.html
- CEWE Large Liggend 28x21: https://fotoservice.ah.nl/cewe-fotoboeken/large-liggend-10759-gs.html ; Test-Aankoop: https://www.test-aankoop.be/hightech/fotodiensten/vergelijker/cewe-fotoboek-large-liggend/489/120041
- Test-Aankoop best photo services: https://www.test-aankoop.be/hightech/fotodiensten/nieuws/beste-fotodiensten
- WhiteWall coffee table book: https://whitewall.com/uk/coffee-table-book
- WhiteWall PDF upload: https://www.whitewall.com/eu/coffee-table-book/pdf-upload
- WhiteWall dimensions guide: https://service.whitewall.com/hc/en-us/articles/4411250911377-03-Setting-the-correct-dimensions-for-cover-and-content-pages
- Peecho layflat: https://peecho.com/products/books/layflat ; photo books: https://peecho.com/blog/print-on-demand-photo-books ; PDF to book: https://webflow.peecho.com/blog/pdf-to-book-printing
- Lulu photo books: https://www.lulu.com/create/photo-books ; products: https://www.lulu.com/products ; Print API products: https://www.lulu.com/print-api/products ; API help: https://help.api.lulu.com/ ; shipping: https://blog.lulu.com/international-book-shipping/
- Gelato photo books: https://www.gelato.com/products/photo-books ; sizes: https://gelato.com/blog/photo-book-sizes ; design help: https://support.gelato.com/en/articles/8996282-how-do-i-design-a-photo-book
- Photobox A4 Pro Lay Flat review: https://amateurphotographer.com/field-tests/accessory_reviews/a4-pro-lay-flat-photo-book-review/ ; https://www.digitalcameraworld.com/reviews/photobox-photo-book-review
- Artifact Uprising layflat: https://www.artifactuprising.com/photo-books/layflat-photo-album
- MILK Books (sizes, via reviews): https://www.5minutesformom.com/milk-medium-landscape-milk-books-photobook-giveaway/ ; https://www.productreview.com.au/listings/milk-books
- Mixam layflat: https://www.mixam.co.uk/layflat
- Viaprinto/Albelli comparison (Macwelt): https://www.macwelt.de/article/928725/urlaubsfotos-fotobuchanbieter-im-vergleich.html
- DigitalCameraWorld best photo books 2026: https://www.digitalcameraworld.com/buying-guides/the-best-photo-books-in-2020-create-a-personalized-picture-album-online
- PetaPixel best photo book services 2026: https://petapixel.com/best-photo-book-services/
- Tom's Guide best photo books 2025: https://tomsguide.com/best-picks/best-photo-books
- Shutterfly + Google Photos: https://www.shutterfly.com/ideas/how-to-upload-google-photos-to-shutterfly/
