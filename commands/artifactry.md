---
description: Use Artifactry to convert Markdown into DOCX, PDF, PPTX, PNG, JPG, or multi-format bundles.
argument-hint: "[markdown file or export request]"
---

# Artifactry

Use the `export-designer` agent if it is available. Use the `artifactry` skill and its scripts for the export workflow.

User request:

```text
$ARGUMENTS
```

Run a quick preflight when tools may be missing:

```bash
python scripts/check_requirements.py
```

If the preflight reports missing packages or system tools, ask for permission before installing them. Then continue:

```text
diagnose -> ask -> route -> style -> render -> validate -> deliver
```

If output type, style, or size is missing, ask:

```text
Before I export, choose the target:
1. Output: DOCX, PDF, PPTX, PNG/JPG carousel, or bundle?
2. Style: one of Artifactry's 15 styles (Regulated Ledger, Human Workshop, Swiss Protocol, Terminal Operator, Aurora Product, Metrics Command, Broadsheet Intelligence, Black Label Cinema, Playful Systems, Image Market, Spatial Canvas, Blueprint Infra, Commerce Editorial, Motion Premiere, Performance Machine), or local DESIGN.md?
3. Size: A4/Letter, 16:9, 4:5, 1:1, 9:16, or custom?
4. Priority: editable file, final polished visual, or both?
```

Use deterministic text rendering and validate outputs before answering.
