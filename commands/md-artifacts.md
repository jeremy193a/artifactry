---
description: Convert Markdown into DOCX, PDF, PPTX, PNG, JPG, or multi-format bundles using Artifactry.
argument-hint: "[markdown file or export request]"
---

# MD Artifacts

Use the `export-designer` agent if it is available. Use the `artifactry` skill and its scripts for the actual export workflow.

User request:

```text
$ARGUMENTS
```

Follow this operating loop:

```text
diagnose -> ask -> route -> style -> render -> validate -> deliver
```

Run preflight when tools may be missing:

```bash
python scripts/check_requirements.py
```

If requirements are missing, ask for permission before installing them.

If output type, style, or size is missing, ask one concise export brief:

```text
Before I export, choose the target:
1. Output: DOCX, PDF, PPTX, PNG/JPG carousel, or bundle?
2. Style: Institutional Clarity, Warm Editorial, Monochrome Precision, Dark Console, Gradient Intelligence, Data Command, Visual Lifestyle, Cinematic Luxury, Playful Productivity, Broadsheet Analysis, or local DESIGN.md?
3. Size: A4/Letter, 16:9, 4:5, 1:1, 9:16, or custom?
4. Priority: editable file, final polished visual, or both?
```

When enough details are present:

1. Read the Markdown file and frontmatter.
2. Expand `{{ include: path.md }}` partials.
3. Apply the chosen style as a full design system, not only color tokens.
4. Use deterministic rendering for text-heavy outputs.
5. Run validation before the final response.
6. Return final file paths, editable source paths, and validation results.

Prefer these scripts from the installed skill when available:

```bash
python skills/artifactry/scripts/normalize_markdown.py
python skills/artifactry/scripts/build_reference_docx.py
python skills/artifactry/scripts/render_html_deck.py
python skills/artifactry/scripts/render_images_chrome.py
python skills/artifactry/scripts/build_pptx_from_images.py
python skills/artifactry/scripts/validate_exports.py
```
