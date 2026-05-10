# Output Quality Gates

Run these checks before delivering files.

## DOCX

Check:

- File exists and is non-empty.
- ZIP contains `word/document.xml`.
- ZIP contains `word/styles.xml`.
- Title and key Vietnamese text appear in XML.
- Tables exist when expected.
- Headings use heading styles.
- Header/footer, code blocks, lists, block quotes, and table styles are not raw Pandoc defaults.
- Style-guide IDs resolve to a token fallback through `style_resolver.py`.

Repair:

- If style is raw Pandoc default, use `build_document.py` or regenerate with `build_reference_docx.py` and `--reference-doc`.
- If worksheet lines disappear, normalize with `--worksheet-lines`.
- If tables are too wide, convert long cells into bullets or split table.
- If the user asked for a public-facing document, export DOCX and PDF together so visual fidelity can be checked.

## PPTX

Check:

- File exists and is non-empty.
- Slide count is expected.
- Size matches aspect ratio.
- If built from images, one full-slide image exists per slide.

Repair:

- If aspect is wrong, rebuild with correct slide dimensions.
- If slide count is wrong, check sorted image names and missing files.

## PNG/JPG

Check:

- Image count is expected.
- Dimensions match requested aspect.
- Representative images have no gray browser bands.
- Footer and page numbers are visible.
- Text is not clipped or overlapping.
- If the user requested one of the 15 Artifactry style guides, the output reflects that guide's specific visual signature, not just colors.
- Public, marketing, showcase, premium, portfolio, and social carousel outputs use guide-specific composition instead of generic token fallback templates.

Repair:

- Render taller and crop exact target size.
- Reduce text, increase row height, or split slide.
- Use PNG for text-heavy output; use JPG only for photo-heavy output.
- If Chrome headless captures a browser background band, use `render_images_chrome.py`, which renders taller and crops to exact canvas size.
- If the output feels like a generic theme, read the selected Markdown style guide again, create page roles, and rebuild bespoke HTML/CSS/SVG before rendering.

## PDF

Check:

- File exists and is non-empty.
- Page count is plausible.
- Text is selectable when expected.

Repair:

- For styled document PDFs, prefer `build_document.py --pdf-route chrome`; it uses print CSS and does not require LaTeX.
- For PDFs that must match DOCX closely, use `build_document.py --pdf-route soffice`.
- For LaTeX-ready environments, use `build_document.py --pdf-route pandoc`.
- For image/deck PDFs, assemble rendered images to preserve design.

## Final Delivery

Return:

- Main output file links.
- Supporting PNG/JPG folder if generated.
- Editable source path when available.
- Short note about tests run and any limitation.
