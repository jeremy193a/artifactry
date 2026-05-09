---
name: artifactry
description: Convert Markdown into polished DOCX, PDF, PPTX, PNG/JPG exports with style, aspect ratio, DESIGN.md guidance, and validation.
---

# Artifactry

## Core Rule

Do not do blind format conversion when the user asks for a polished deliverable. First decide the output intent, then shape the Markdown into the right artifact model:

- Documents need hierarchy, readable paragraphs, tables, headers/footers, and reference `.docx` styles.
- Slides need one idea per slide, stable canvas ratios, deterministic text layout, and visual validation.
- Social images need high-resolution fixed canvases, safe margins, and PNG/JPG export.
- PDFs should be produced from the most faithful source for the artifact: DOCX/LaTeX for documents, HTML/images for decks or carousels.

Final text-heavy artifacts must use deterministic text rendering. Do not ask an image model to render final text.

## Workflow

Run preflight when the environment is new or an export route needs external tools:

```bash
python scripts/check_requirements.py
```

If Python packages are missing, install from `requirements.txt`. If system tools are missing, ask the user for approval before installing them. Install only tools required by the requested output route.

0. Start with an export brief gate:
   - If the user already gave output format, style, and aspect/page target, proceed.
   - If any of those are missing, ask one concise question before creating files.
   - Ask for: output type, style/mood, aspect/page size, and whether they want editable source artifacts.
   - Offer practical style choices rather than an open-ended design discussion.

Use this default question:

```text
Before I export, choose the target:
1. Output: DOCX, PDF, PPTX, PNG/JPG carousel, or bundle?
2. Style: choose one Artifactry style guide, a deterministic token fallback, or a local DESIGN.md?
3. Size: A4/Letter, 16:9, 4:5, 1:1, 9:16, or custom?
4. Priority: editable file, final polished visual, or both?
```

List available style guides and token fallbacks with:

```bash
python skills/artifactry/scripts/list_styles.py
```

1. Inspect the Markdown:
   - Read frontmatter if present.
   - Use `doctype` when present: `document`, `slides`, `carousel`, or `docs`.
   - Expand `{{ include: path/to/file.md }}` partials before planning/export.
   - Identify audience, tone, output formats, aspect ratio, brand/style, and deadline.
   - If metadata is missing, infer conservatively from content and user request.
   - Preserve source facts, Vietnamese diacritics, names, dates, numbers, and caveats.

2. Choose an export route:
   - `docx`: business docs, worksheets, reports, SOPs, proposals, handouts.
   - `pptx`: presentations, training decks, executive briefings.
   - `png`/`jpg`: social carousel slides, preview images, fixed-ratio share assets.
   - `pdf`: final reading/printing version.
   - `bundle`: multiple outputs from one source.

3. Apply style:
   - If the repo has a `DESIGN.md`, read it and translate it into export tokens.
   - If the user names a getdesign.md style, run or ask to run `npx getdesign@latest add <style>` when network/tooling is available.
   - Use [design-md-adapter.md](references/design-md-adapter.md) to translate web/UI style rules into document, slide, and image systems.
   - For polished deliverables, prefer the Markdown style guides in [style-guides/INDEX.md](references/style-guides/INDEX.md). Read the chosen guide before planning page roles, slide roles, HTML/CSS, DOCX styling, or PPTX assembly.
   - The JSON styles in `styles/*.json` are deterministic token fallbacks for scripts. They are not the full creative direction.
   - Bundled generic token styles are corpus-derived design systems, not simple themes. Apply `style_dna`, `palette`, `typography.scale`, `shape`, `layout`, `components`, `slides`, `document`, `guardrails`, and `export_translation`.
   - Search local export patterns when route/style is unclear:

```bash
python skills/artifactry/scripts/search_references.py "institutional clarity 16:9 presentation"
```

   - Do not average unrelated brands. Pick one dominant style mode.

4. Normalize source:
   - Use `scripts/normalize_markdown.py` for document-style Markdown, especially worksheets and handouts.
   - For slides/carousels, create a slide plan before rendering. Use [markdown-input-contract.md](references/markdown-input-contract.md).

5. Export:
   - For DOCX, use Pandoc with a reference docx. Generate one with `scripts/build_reference_docx.py` if needed.
   - For PPTX or image decks, prefer HTML/CSS fixed-canvas rendering, then assemble images into PPTX with `scripts/build_pptx_from_images.py`.
   - For quick plain PPTX, Pandoc is acceptable only when the user wants a simple editable outline deck.

6. Validate:
   - Run `scripts/validate_exports.py` on generated files.
   - Inspect representative rendered images for visual artifacts.
   - Fix clipped text, broken Vietnamese marks, wrong dimensions, missing slides/pages, and raw default styling before delivery.

## Frontmatter Contract

Prefer this when creating or repairing Markdown:

```yaml
---
title: "AI Training Bootcamp"
subtitle: "Practical AI workflows for business teams"
author: "Jeremy Nguyen"
date: "2026-05-09"
doctype: "slides"
outputs: ["pptx", "png", "docx"]
style: "institutional-clarity"
tone: "executive training"
audience: "internal team"
aspect: "16:9"
---
```

Supported `aspect` values:

- `16:9`: presentation.
- `4:5`: LinkedIn/Instagram carousel.
- `1:1`: square social post.
- `9:16`: story/reel frame.
- `a4`: document page.
- Custom values such as `1920x1080` or `1638x2048`.

See [aspect-ratios.md](references/aspect-ratios.md) for export dimensions.

Supported `doctype` values:

- `document`: Word/PDF report, proposal, worksheet, SOP, handout.
- `slides`: presentation deck, usually PPTX plus PNG preview.
- `carousel`: fixed-ratio social images, usually PNG/JPG and optional PPTX.
- `docs`: multi-page documentation or knowledge base.

Use includes to compose large projects:

```markdown
# Master Document

{{ include: sections/module-1.md }}

{{ include: sections/module-2.md }}
```

## Output Routes

### Route A: Markdown -> Word/PDF

Use for reports, worksheets, handouts, SOPs, proposals, and internal docs.

```bash
python skills/artifactry/scripts/normalize_markdown.py input.md --output build/input.normalized.md --worksheet-lines
python skills/artifactry/scripts/build_reference_docx.py --output build/reference.docx --style institutional-clarity
pandoc build/input.normalized.md --from=markdown --to=docx --reference-doc=build/reference.docx --output output/document.docx
python skills/artifactry/scripts/validate_exports.py output/document.docx
```

### Route B: Markdown -> Designed Slides/Images/PPTX

Use for premium decks and social carousels.

1. Convert Markdown into a slide plan.
2. Render each slide with HTML/CSS/SVG at fixed dimensions.
3. Screenshot/export to PNG or JPG.
4. Assemble PNGs into PPTX when needed.
5. Validate dimensions and slide count.

```bash
python skills/artifactry/scripts/render_html_deck.py input.md --aspect 16:9 --style institutional-clarity --output-dir build/deck
python skills/artifactry/scripts/render_images_chrome.py build/deck/slides-html --aspect 16:9 --output-dir output/png
python skills/artifactry/scripts/build_pptx_from_images.py output/png --output output/deck.pptx --aspect 16:9
python skills/artifactry/scripts/validate_exports.py output/deck.pptx output/png
```

### Route C: Quick Pandoc Export

Use only when the user asks for fast, simple, editable office files and does not require premium visual design.

```bash
pandoc input.md --from=markdown --to=docx --output output.docx
pandoc input.md --from=markdown --to=pptx --output output.pptx
```

## Quality Gate

Reject and revise before final delivery when:

- Output files are missing, zero-byte, or have the wrong extension.
- PPTX slide count does not match the rendered image count.
- PNG/JPG dimensions do not match the requested aspect ratio.
- DOCX lacks `word/document.xml` or `word/styles.xml`.
- Vietnamese text is missing accents, clipped, or replaced by boxes.
- Tables overflow the page or slide.
- Social/deck images show browser background bands, clipped footer, or overlapping text.
- The final look ignores the selected DESIGN.md style.

## References

- [design-md-adapter.md](references/design-md-adapter.md): translate getdesign.md/DESIGN.md styles into export tokens.
- [style-guides/INDEX.md](references/style-guides/INDEX.md): 15 public Artifactry style guides synthesized from the local DESIGN.md corpus.
- [aspect-ratios.md](references/aspect-ratios.md): supported ratios and pixel/PPTX dimensions.
- [markdown-input-contract.md](references/markdown-input-contract.md): expected Markdown structure for documents, decks, carousels.
- [output-quality-gates.md](references/output-quality-gates.md): validation checklist and repair actions.
