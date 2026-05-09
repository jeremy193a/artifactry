# Markdown Input Contract

The skill accepts normal Markdown, but quality improves when the source includes frontmatter and clear structure.

## Universal Frontmatter

```yaml
---
title: "Artifact Title"
subtitle: "Optional subtitle"
author: "Owner"
date: "2026-05-09"
doctype: "document"
outputs: ["docx"]
style: "institutional-clarity"
tone: "professional"
audience: "internal team"
aspect: "a4"
---
```

## Doctype

Use `doctype` to remove ambiguity before export:

- `document`: Word/PDF report, proposal, SOP, worksheet, handout.
- `slides`: 16:9 or 9:16 presentation.
- `carousel`: 4:5, 1:1, or 9:16 social image sequence.
- `docs`: documentation site, knowledge base, or multi-page reference.

The agent should choose the route from `doctype` before looking at `outputs`.

## Includes / Partials

Use includes to compose large Markdown projects from smaller files:

```markdown
# AI Training Bootcamp

{{ include: sections/module-1.md }}

{{ include: sections/module-2.md }}

{{ include: sections/workshop.md }}
```

Rules:

- Include paths are relative to the file containing the include.
- Includes may be nested.
- Circular includes must be rejected.
- Expand includes before normalizing headings, splitting slides, or converting.
- Keep partial files free of frontmatter unless they are also standalone documents.

## Document Structure

Use for Word/PDF.

```markdown
# Title

Short summary or purpose.

## 1. Context

## 2. Key Points

## 3. Recommendation

## Appendix
```

Rules:

- One `#` title.
- `##` for main sections.
- `###` for subsections.
- Tables should be narrow and readable.
- Use `**Note:**`, `**Risk:**`, `**Decision:**` for callouts.
- Keep ASCII diagrams in fenced code blocks.

## Worksheet Structure

Use for printable training sheets.

```markdown
# Worksheet Title

**Name:** ____________________

## 1. Section

### Prompt
> Instruction text.

___________________________________________________
___________________________________________________
```

Use the normalizer with `--worksheet-lines` to convert underscore-only lines into stable writing lines.

## Deck Structure

Use for presentations.

```markdown
# Deck Title

## Slide 1: Main message

- Point one
- Point two

---

## Slide 2: Main message
```

Rules:

- One idea per slide.
- Keep bullets short.
- Put speaker notes under `Notes:` if needed.
- If no slide breaks exist, infer slides from `##` sections.

## Carousel Structure

Use for social images.

```markdown
# Carousel Title

## Slide 1 — Hook

One strong claim.

## Slide 2 — Evidence

- Fact
- Number
- Caveat
```

Rules:

- Prefer 6-12 slides.
- Keep each slide self-contained.
- Include sources in a `Sources` section if factual.
