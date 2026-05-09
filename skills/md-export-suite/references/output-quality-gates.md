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

Repair:

- If style is raw Pandoc default, regenerate or pass `--reference-doc`.
- If worksheet lines disappear, normalize with `--worksheet-lines`.
- If tables are too wide, convert long cells into bullets or split table.

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

Repair:

- Render taller and crop exact target size.
- Reduce text, increase row height, or split slide.
- Use PNG for text-heavy output; use JPG only for photo-heavy output.
- If Chrome headless captures a browser background band, use `render_images_chrome.py`, which renders taller and crops to exact canvas size.

## PDF

Check:

- File exists and is non-empty.
- Page count is plausible.
- Text is selectable when expected.

Repair:

- For document PDFs, export from DOCX or Pandoc LaTeX.
- For image/deck PDFs, assemble rendered images to preserve design.

## Final Delivery

Return:

- Main output file links.
- Supporting PNG/JPG folder if generated.
- Editable source path when available.
- Short note about tests run and any limitation.
