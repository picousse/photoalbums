# LLM skills, MCP servers and AI curation for the photo book pipeline

Research date: 2026-10-04. Repo existence was checked against GitHub (HTTP 200 / API); feature claims come
from READMEs, directory listings and official docs. Points marked **(unverified)** were not tested by us.

Our pipeline today: `photoalbums plan <folder>` (scan EXIF/Takeout sidecars -> drop bursts -> group by
city/day -> paginate -> `book.yaml`) and `photoalbums render book.yaml [--spreads]` (ReportLab PDF with
bleed). The YAML already supports `{file: x.jpg, focus: [x, y]}` for steering crops, which is an obvious place
for AI suggestions to land.

---

## 1. Agent Skills (SKILL.md) relevant to us

### Anthropic official: github.com/anthropics/skills

Current `skills/` folder: academy-guide, algorithmic-art, brand-guidelines, canvas-design, claude-api,
discernment-nudge, doc-coauthoring, docx, frontend-design, internal-comms, mcp-builder, **pdf**, pptx,
**skill-creator**, slack-gif-creator, **theme-factory**, web-artifacts-builder, webapp-testing, xlsx.

| Skill | What it does | Useful here? |
|---|---|---|
| `pdf` | General PDF guide: pypdf (merge/split/rotate), pdfplumber (extract), reportlab (create), qpdf, forms, OCR. Source-available, not open source. | **Somewhat.** It teaches the tools we already use (ReportLab, pypdf), and helps for checking output (page count, page box sizes, extracting images to check DPI). It knows nothing about print-specific needs (bleed, trim box, CMYK/ICC, preflight). Already installed in this environment as `anthropic-skills:pdf`. |
| `canvas-design` | Writes a "design philosophy" .md and then draws a single poster/artwork as PNG/PDF. | **Low.** It is about one-off art, not multi-page photo layout. Could be borrowed for a cover or title page. |
| `theme-factory` | Applies preset color/font themes to artifacts. | **Low.** It might help pick a cover/typography palette. |
| `skill-creator` | Interactive helper for writing, testing and evaluating new skills. | **Yes, as a tool** for writing our own `photobook` skill (section 4). |
| `algorithmic-art`, `frontend-design` | p5.js generative art / web UI. | No. |

### Community skills (registries)

There are big registries (claudskills.com says it indexes 183k+ SKILL.md files; claudemarketplaces.com;
awesome lists such as `travisvn/awesome-claude-skills` and `ComposioHQ/awesome-claude-skills`). Quality varies
a lot and many entries are auto-scraped. Relevant hits:

- **photo-content-recognition-curation-expert** (repo `erichowens/some_claude_skills`, which now redirects to
  `curiositech/some_claude_skills`): describes a CV pipeline for face clustering, near-duplicate detection
  with pHash/DINOHash, burst selection that scores sharpness and face quality, and screenshot filtering.
  **Useful as a reference** for which techniques to use. It is a prompt/knowledge skill, not a tested tool
  **(unverified)**, so read it and borrow ideas rather than install it blindly.
- "Photos" (organize/index a local library with AI metadata) and "PhotoPrism automation" on claudskills.com
  are about library management, not books. **Low relevance.**
- We found **no published skill for photo books, photo-book layout, or print-ready (bleed/ICC) PDF
  generation.** That gap is the main reason to write our own.

---

## 2. MCP servers

### Google Photos (after the 31 March 2025 Library API change)

Background (Google developer blog + docs): on 2025-03-31 Google removed the `photoslibrary.readonly`,
`photoslibrary.sharing` and `photoslibrary` scopes. The Library API now only sees **media the app itself
uploaded**. The only way to read a user's existing photos is the **Picker API**: create a session, the user
opens a Google-hosted picker URL and selects items, the app polls the session and then downloads via
`baseUrl` (valid for 60 minutes). This means any MCP server that claims "search my whole library" through the
Library API no longer works for existing photos.

| Server | Picker? | Notes |
|---|---|---|
| **savethepolarbears/google-photos-mcp** (TypeScript, about 44 stars, last push 2026-08) | Yes: `create_picker_session` / `poll_picker_session` | The most established option. It has 19 tools; its search/album tools use the Library API, so they only cover app-created content. Supports Streamable HTTP transport. |
| **thenavidm/google-photos-mcp-cli** (TypeScript, MCP + CLI, very new, about 1 star) | Yes. It is built around the picker and has `download_picked` (uses `=d` for originals) | It has 26 tools, including album creation and captions/enrichments on app-created albums. Promising but immature **(unverified)**. |
| Composio / Rube "googlephotos" toolkit | Hosted integration | Third-party hosted OAuth. Same API limits apply. Not attractive for a personal tool. |

**Important caveat for us:** Google's docs say that downloading with `baseUrl=d` keeps EXIF **except
location metadata**. Photos fetched through the Picker API (so through any of these MCP servers) **arrive
without GPS**, which breaks our city grouping. **Google Takeout** keeps location in the JSON sidecars (our
`scan._takeout_sidecar` already reads them), and so does a manual download from the Google Photos web UI
**(we believe this keeps the original file, unverified)**. Recommendation: keep Takeout/manual download as
the main input. Use a Picker MCP only for convenient "pick these 200 photos" sessions, and accept that those
photos will be grouped by date only (or by sidecar data if we add it later).

### Image / EXIF MCP servers

- **stass/exif-mcp** (TypeScript, exifr, offline, BSD-2, last push 2025-11): reads EXIF/GPS/XMP/ICC/IPTC,
  orientation and embedded thumbnails from JPEG/PNG/TIFF/HEIC. Handy for ad-hoc questions in a Claude
  session, but **redundant** for us because our Python scanner already does this, and Claude Code can just run
  `exiftool` or our CLI.
- Generic image-processing MCPs (resize, convert) exist in registries such as Glama and LobeHub, but are not
  needed. Pillow in our own CLI is simpler and testable.

Bottom line: **MCP is not where the value is for this project.** A CLI + skill is enough. Claude Code's
`Read` tool can already view image files directly.

---

## 3. Curation: LLM vision and non-LLM helpers

### Recommended layered approach (cheap first, LLM last)

1. **Deterministic filters (free, local):**
   - Blur: variance of the Laplacian (`cv2.Laplacian(gray, cv2.CV_64F).var()` on a downscaled grayscale).
     Thresholds depend on the scene, so compare against the median of the section, not a fixed cutoff.
   - Exposure: histogram clipping (share of pixels at 0/255).
   - Screenshots and receipts: missing camera EXIF, or a screen aspect ratio plus no GPS.
   - Near-duplicates: **imagededup** (`idealo/imagededup`: PHash/DHash/WHash plus a CNN mode) or plain
     `imagehash`. Run this per section, on top of our existing time-based `drop_bursts`.
2. **Embeddings (local, GPU optional):**
   - **OpenCLIP** (`mlfoundations/open_clip`) embeddings for semantic near-duplicate clusters (the same scene
     from slightly different angles) and for diversity-aware selection (greedy max-marginal-relevance:
     quality score minus similarity to photos already chosen).
   - Aesthetic score: **LAION aesthetic predictor** (`LAION-AI/aesthetic-predictor`, linear head on CLIP),
     the **improved-aesthetic-predictor** (`christophschuhmann/improved-aesthetic-predictor`, MLP on CLIP
     ViT-L/14), or **aesthetic-predictor-v2-5** (`discus0434/aesthetic-predictor-v2-5`, SigLIP-based, better
     on real photos according to its README). Be careful: these were trained to rank web images and AI art.
     Treat them as weak tie-breakers inside a cluster, not as absolute truth.
   - **pyiqa / IQA-PyTorch** (`chaofengc/IQA-PyTorch`) bundles NIMA, MUSIQ, CLIP-IQA, BRISQUE, LAION-aes and
     more behind one API. It is the easiest way to try several quality metrics.
   - Cost: CPU is fine for a few thousand photos (minutes). These add torch as a dependency, so put them
     behind an optional extra (`photoalbums[curate]`).
3. **Claude vision (judgement calls only):** run it on the survivors to choose the hero photo per
   section, pick the best of each cluster, write section titles, and suggest `focus` points for crops.

### Using Claude vision cheaply

- Claude does **not** read EXIF (official docs), so pass date/city/filename as text next to each image.
- Token cost is `ceil(w/28) * ceil(h/28)` visual tokens. Claude 4.7+ models allow up to 2576 px / 4784
  tokens; older models allow 1568 px / 1568 tokens. Original photos get downscaled anyway, so **always send
  thumbnails**:
  - A 400x300 thumbnail costs about 15x11 = 165 tokens.
  - **Contact sheets** work well: a 2000x1500 grid of 4x4 numbered thumbnails costs about 3.9k tokens for 16
    photos (about 240 per photo). Claude can compare them side by side ("pick the best 3 of #1-#16").
  - Example: 1,000 candidate photos as 400 px thumbs is about 170k input tokens. At Opus 5 pricing
    ($5/MTok) that is roughly $1, and it is cheaper with Haiku/Sonnet. (Pricing from the vision doc; check
    current prices.)
- Limits: up to 100 to 600 images per API request depending on model. Above 20 images per request, every
  image must be at most 2000 px. The request size limit is 32 MB.
- Inside Claude Code no API code is needed: the CLI writes thumbnails/contact sheets to a cache folder, and
  Claude looks at them with `Read` (a subscription session, so no per-token billing). For unattended or bulk
  runs, use the Messages API (optionally the Batches API for a 50% discount, plus the Files API so images are
  not re-sent on each turn).
- Ask for **structured output** (JSON: `{section, keep:[ids], hero:id, title, focus:{id:[x,y]}}`) and have
  the CLI merge it into `book.yaml`, so the human can still edit the result.
- Claude cannot identify people (policy). "Prefer photos where faces are visible and eyes open" is fine.

---

## 4. Recommendation: write a project skill, yes

**Yes, write `.claude/skills/photobook/SKILL.md`, and keep the intelligence in the CLI.** No existing skill
covers photo books or print PDFs. A short skill makes Claude use our tool consistently instead of
improvising Pillow/ReportLab scripts, and it is cheap to maintain. Do not build an MCP server. Do not depend
on the Google Photos MCPs for primary input (they strip GPS).

Supporting CLI work this implies (small):
- `photoalbums thumbs book.yaml` writes 400 px thumbnails plus per-section numbered contact sheets to
  `.cache/thumbs/`.
- Optionally, `photoalbums score` adds blur/dup/aesthetic scores as comments or fields in the YAML.
- The YAML keeps being the single place where AI and human edits meet.

Sketch:

```markdown
---
name: photobook
description: Build or revise a printed photo book from a photo folder with the photoalbums CLI
  (scan, plan YAML, curate, render PDF). Use when the user mentions the photo book, book.yaml,
  album pages, choosing photos, or rendering the print PDF.
allowed-tools: Bash(uv run photoalbums *) Read Edit
---

## Workflow
1. `uv run photoalbums plan <folder> -o book.yaml [--pages N] [--title ...]`
2. `uv run photoalbums thumbs book.yaml` -> read `.cache/thumbs/<section>-sheet-*.jpg`
   (never open full-size originals; they waste context).
3. Curate per section by editing book.yaml (never other files):
   - remove blurry/duplicate/near-identical shots (keep the best of each cluster)
   - put the hero photo first in a `full`/single layout on the section's first page
   - set `focus: [x, y]` when the subject is off-centre and the frame will crop
   - short section titles (1-4 words, place-based, no clichés); keep the date subtitle
4. `uv run photoalbums render book.yaml --spreads`, read the spreads preview at low DPI,
   fix warnings (low resolution, heavy crop), repeat.
5. Report: pages, photos used/dropped, warnings. Do not upload or order anything.

## Rules
- Format 25x20 landscape; layouts: <list from `photoalbums formats` / YAML header>.
- Ask before dropping more than ~30% of a section.
- Claude cannot see EXIF: rely on the YAML/CLI output for dates and places.
```

Optional later additions: a `reference.md` with layout names and YAML schema, and `disable-model-invocation:
true` if we only want it on `/photobook`. Use `skill-creator` to test the description so the skill triggers
reliably.

---

## Sources

- Anthropic skills repo: https://github.com/anthropics/skills
- pdf skill: https://github.com/anthropics/skills/tree/main/skills/pdf
- canvas-design skill: https://github.com/anthropics/skills/tree/main/skills/canvas-design
- Claude Code skills docs (frontmatter, project skills): https://code.claude.com/docs/en/skills
- Claude vision docs (token formula, limits, no EXIF): https://platform.claude.com/docs/en/build-with-claude/vision
- claudskills.com registry: https://claudskills.com/
- Photo curation skill listing: https://claudemarketplaces.com/skills/erichowens/some_claude_skills/photo-content-recognition-curation-expert
- Its repo: https://github.com/curiositech/some_claude_skills
- Awesome lists: https://github.com/travisvn/awesome-claude-skills, https://github.com/ComposioHQ/awesome-claude-skills
- Google Photos API changes (Picker launch, Library API restrictions): https://developers.googleblog.com/en/google-photos-picker-api-launch-and-library-api-updates/
- Google Photos API updates page: https://developers.google.com/photos/support/updates
- Picker API media items (`=d` keeps EXIF except location; baseUrl 60 min): https://developers.google.com/photos/picker/guides/media-items
- savethepolarbears/google-photos-mcp: https://github.com/savethepolarbears/google-photos-mcp
- thenavidm/google-photos-mcp-cli: https://github.com/thenavidm/google-photos-mcp-cli
- Composio Google Photos toolkit: https://rube.composio.dev/marketplace/googlephotos
- stass/exif-mcp: https://github.com/stass/exif-mcp
- imagededup: https://github.com/idealo/imagededup
- OpenCLIP: https://github.com/mlfoundations/open_clip
- LAION aesthetic predictor: https://github.com/LAION-AI/aesthetic-predictor
- Improved aesthetic predictor: https://github.com/christophschuhmann/improved-aesthetic-predictor
- Aesthetic predictor v2.5: https://github.com/discus0434/aesthetic-predictor-v2-5
- IQA-PyTorch (pyiqa): https://github.com/chaofengc/IQA-PyTorch
