# Exploration 05: Photoshop / graphic design skills and MCP servers

Date: 2026-10-04. Follows `03-llm-skills-and-ai-curation.md` (curation and Google Photos).

Question: what's out there that lets Claude do (or help with) graphic design work, such as Photoshop-style photo editing, page layout and typography, and how could it fit our photo book flow?

**Important constraint: we work on Linux.** Photoshop, Lightroom Classic, InDesign and Affinity don't run natively here. Tools that drive those desktop apps need a Mac or Windows machine. Cloud connectors and Linux-native apps (GIMP, darktable, Scribus) do work.

## 1. Adobe

| Tool | What it is | Runs on | Fit |
|---|---|---|---|
| **Adobe for Creativity** (official, `adobe-creativity.adobe.io/mcp`) | Hosted Adobe MCP connector, GA since April 2026, 50+ tools across Photoshop, Lightroom, Illustrator, InDesign, Firefly, Express, Premiere, Stock. OAuth with an Adobe account | Cloud: available in Claude chat/Desktop/Cowork; any OS | Works at **Express/Firefly level, not full desktop Photoshop**. Could handle quick fixes (auto-tone, background removal, upscaling) on a few hero photos. Needs an Adobe account; check costs |
| Community Photoshop MCPs (e.g. `alisaitteke/photoshop-mcp`, `matrayu/adobe-mcp`) | Drive installed desktop Photoshop/Illustrator/InDesign/Premiere via UXP/ExtendScript | Mac/Windows + Adobe licence | Not usable on this Linux machine |
| InDesign MCPs (`chris-enea/indesign-mcp`, `lucdesign/indesign-mcp-server`, Tlechanteur's, `matthijs1000/indesign-mcp`) | Claude controls InDesign: documents, text, frames, export | Mac/Windows + InDesign | Only useful if we hand the layout to InDesign. Then generating **IDML** from `book.yaml` is the simpler route |

## 2. Open-source, Linux-friendly

| Tool | What it is | Fit |
|---|---|---|
| **dark-table-mcp** | Claude drives a live **darktable** session: plain-language edits ("warmer, lift the shadows"), rating, tagging, styles, batch a look, export | **Most interesting for us.** It works on Linux and gives Lightroom-style editing. Use: give a consistent look to the selected photos before layout, then export to the photo folder |
| **GIMP-MCP** (`libreearth/gimp-mcp`) | Bridges GIMP's Python API to Claude | Pixel-level touch-ups (retouching, removing objects) on single photos. Niche |
| **mcp-imagemagick** | Conversion (e.g. DNG RAW → WebP) via ImageMagick/darktable | Small utility; Pillow already covers what we need |
| **Scribus** (open-source desktop publishing, Python scripting, native PDF/X export) | No MCP server found | **Candidate "finish by hand" editor on Linux.** We could export `book.yaml` to a Scribus document, adjust it by hand, and export PDF/X. Fallback if editing YAML isn't enough |

## 3. Design platforms

| Tool | What it is | Fit |
|---|---|---|
| **Canva** MCP connector (official, 2026) | Create/edit designs, brand kits, templates, export | Canva also prints photo books, but we'd be working inside Canva's sizes and templates. Doesn't fit our generated-PDF flow. Maybe for a cover idea |
| **Figma** MCP (official remote server) | Reads frames/variables for design-to-code | Built for UI work, not print. Not relevant |

## 4. Claude design skills (SKILL.md)

| Skill | What it does | Fit |
|---|---|---|
| `canvas-design` (Anthropic official) | Makes posters/visual pieces as PNG/PDF from a written design philosophy | Could help explore **cover and title page typography** ideas |
| `frontend-design`, `brand-guidelines`, `theme-factory` (Anthropic) | UI design direction / Anthropic branding / colour+font themes | `theme-factory` might help pick font pairings; the others aren't relevant |
| `graphic-design` (community, travisjneuman) | General design principles for print and digital: palettes, typography, layout, feedback | Good to borrow from for a design checklist |
| "Design elevation" skill (Claude resources) | Design critique loop: first principles, element-by-element review, "removal test" | The idea is useful: let Claude **critique our rendered spreads** (rendered as PNG) and suggest layout changes in `book.yaml` |

No published skill targets photo book or print layout specifically. This matches what we found in note 03.

## Conclusions for our flow

1. **Keep layout in our own code.** None of these tools does automatic multi-page photo book layout better than our generator. Most are made for single designs.
2. **Best add-on: darktable + dark-table-mcp** for an optional "develop" step (consistent colour and exposure across the album) before `plan`. It's Linux-native, local and free.
3. **Our own `photobook` skill** (see note 03) should include a short **design rules** section (white space, at most one or two typefaces, title pages minimal, vary density, no tiny photos, a hero photo per section) and a **critique loop**: render spreads to PNG → Claude reviews → edits `book.yaml`.
4. **Hand-editing escape route:** Scribus export (Linux) or IDML export (if anyone ever has InDesign). Only build this if YAML editing turns out to be too clumsy.
5. **The Adobe for Creativity connector** is optional for one-off hero-photo fixes, if an Adobe account is available.

## Sources

- Adobe official connector overview: https://www.usecarly.com/blog/adobe-mcp/
- What the Adobe connector does and doesn't do: https://www.mindstudio.ai/blog/claude-mcp-adobe-vs-photoshop-premiere-what-it-does
- Adobe for Creativity listing: https://mcpservers.org/remote-mcp-servers/adobe-creativity
- Adobe MCP (dev.to): https://dev.to/curatedmcp/adobe-mcp-connect-claude-to-photoshop-acrobat-and-experience-cloud-5h1i
- Mike Chambers on AI + Photoshop/InDesign/Premiere: https://mikechambers.com/blog/post/2025-06-06-exploring-ai-integration-with-adobe-photoshop-indesign-and-premiere-pro
- matrayu/adobe-mcp: https://github.com/matrayu/adobe-mcp
- Photoshop MCP (alisaitteke): https://skillselion.com/mcp/tool/io.github.alisaitteke/photoshop-mcp
- InDesign MCP (chris-enea): https://glama.ai/mcp/servers/chris-enea/indesign-mcp
- InDesign MCP (lucdesign): https://glama.ai/mcp/servers/lucdesign/indesign-mcp-server
- GIMP MCP: https://claudemarketplaces.com/mcp/libreearth/gimp-mcp
- mcp-imagemagick: https://mcpservers.org/en/servers/AeyeOps/mcp-imagemagick
- dark-table-mcp (search result listing): https://glama.ai/mcp/servers/rgdxuhjmlg
- Canva MCP: https://composio.dev/content/canva-mcp-connect-ai-assistants-to-your-canva-designs
- Best design MCP servers 2026: https://mcp.directory/blog/best-mcp-servers-for-design-2026
- Anthropic official skills tour: https://codenote.net/en/posts/anthropic-official-skills-catalog-overview/
- Anthropic: elevate Claude's design using skills: https://claude.com/resources/use-case/elevate-claudes-design-using-skills
- Community graphic-design skill: https://claudeskills.info/skills/travisjneuman/.claude/graphic-design/
