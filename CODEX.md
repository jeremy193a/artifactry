# Codex Guide

Install the skill locally:

```bash
mkdir -p ~/.codex/skills
ln -s /path/to/md-export-skills/skills/md-export-suite ~/.codex/skills/md-export-suite
```

Use prompt:

```text
Use $md-export-suite to convert this Markdown into the requested export files. Read DESIGN.md if present, generate editable source artifacts, render final files, and validate before answering.
```

Good requests:

```text
Use $md-export-suite to turn bootcamp.md into a 16:9 PPTX and PNG slides using Institutional Clarity style.
```

```text
Use $md-export-suite to turn worksheet.md into a polished DOCX and PDF.
```
