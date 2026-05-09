# Agent Instructions

Use `$artifactry` when the user asks to convert Markdown into Word, PDF, PPTX, PNG, JPG, or a bundle of these files.

For Claude Code, prefer the bundled `export-designer` agent for complex export jobs:

```text
.claude/agents/export-designer.md
```

## Operating Rules

- Follow the loop: diagnose -> ask -> search -> route -> refactor -> render -> validate -> deliver.
- Read the Markdown before converting.
- Prefer polished artifact-specific workflows over blind Pandoc conversion.
- Use `DESIGN.md` when present.
- Search local reference patterns before choosing a route:

```bash
python skills/artifactry/scripts/search_references.py "institutional clarity 16:9 presentation"
```

- If the user names a style from getdesign.md, install/read that style when possible.
- Keep generated source artifacts editable.
- Validate final files before responding.

## Fast Decision Tree

- Report, worksheet, SOP, handout, proposal -> DOCX route.
- Presentation deck -> HTML/CSS render to PNG, then PPTX route.
- Social carousel -> HTML/CSS render to PNG/JPG route.
- Final handout PDF -> DOCX/Pandoc/Word-derived PDF route.
- Designed slide PDF -> image/deck-derived PDF route.

## Do Not

- Let image generation render final text-heavy slides.
- Deliver raw default Pandoc output when the user asked for design.
- Ignore Vietnamese diacritics.
- Skip validation.
