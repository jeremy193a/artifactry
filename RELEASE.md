# Artifactry v0.3.0

Artifactry is now ready as a public AI-agent skill pack for turning Markdown into polished artifacts: DOCX, PDF, PPTX, PNG/JPG carousels, and multi-format content bundles.

This release focuses on making Artifactry usable from real agent workflows, especially Claude Chat/Desktop and Claude Code.

## Highlights

- **Claude Chat/Desktop skill path**: package Artifactry as `artifactry.zip`, upload it through Claude Skills, and ask Claude to export Markdown into polished files.
- **Claude Code plugin path**: install with the canonical plugin name `artifactry@artifactry`.
- **Slash command workflow**: use `/artifactry` for new work, with `/md-artifacts` kept as a backwards-compatible legacy alias.
- **15 style guides**: detailed generic style systems inspired by `DESIGN.md` patterns, without exposing copied brand names.
- **DOCX showcase**: five downloadable Word document examples showing distinct document styles.
- **Visual showcase**: signature PNG previews for all 15 style guides.
- **Style-guide enforcement**: named Markdown style guides now require guide-led layouts instead of generic JSON token fallback output.
- **Visual audit gate**: HTML/CSS decks and carousels can be audited for off-canvas elements, clipped text, and text overlap before PNG/PPTX export.
- **Markdown routing**: support for `doctype: document | slides | carousel | docs`.
- **Includes/partials**: compose larger projects with `{{ include: sections/example.md }}`.
- **Export validation**: validate DOCX, PDF, PPTX, PNG, and JPG outputs before delivery.

## Install

### Claude Code

```text
/plugin marketplace add artifactry https://github.com/jeremy193a/artifactry.git
/plugin install artifactry@artifactry
```

Restart Claude Code, then run:

```text
/artifactry README.md as a DOCX using Broadsheet Intelligence
```

### Claude Chat / Desktop

Claude Chat/Desktop uses a Skill ZIP:

```bash
python scripts/package_claude_skill.py
```

Upload:

```text
dist/artifactry.zip
```

Then prompt Claude:

```text
Use the Artifactry skill. I uploaded a Markdown file. Ask me which output format, style, and size I want, then export and validate the files.
```

## What Changed

- Renamed the public plugin identity from `md-export-skills` to `artifactry`.
- Kept `/md-artifacts` as a legacy alias so older workflows still work.
- Added clearer Claude Chat/Desktop installation guidance.
- Added a richer README structure for public users.
- Added 15 style archetypes for more differentiated exports.
- Added DOCX showcase files with direct download links.
- Added generated reference DOCX support for styled document output.
- Added preflight checks for Python packages and system tools.
- Added include expansion that ignores include syntax inside fenced code blocks.
- Added stronger Claude Code command prompts for export brief, style selection, routing, rendering, and validation.
- Added `visual_audit_html.py` to catch rendered layout defects before screenshot export.
- Added guardrails so public, marketing, showcase, premium, portfolio, and social carousel exports use Markdown style guides as creative direction, not just token themes.

## Style Guides

Artifactry ships with these public style archetypes:

- Regulated Ledger
- Human Workshop
- Swiss Protocol
- Terminal Operator
- Aurora Product
- Metrics Command
- Broadsheet Intelligence
- Black Label Cinema
- Playful Systems
- Image Market
- Spatial Canvas
- Blueprint Infra
- Commerce Editorial
- Motion Premiere
- Performance Machine

## Current Routes

- Markdown to DOCX
- Markdown to styled HTML/PDF
- Markdown to HTML/CSS slide canvas
- HTML slide visual audit before screenshot export
- Slide canvas to PNG/JPG
- PNG/JPG slides to PPTX
- Markdown bundles through frontmatter and agent routing

## Known Direction

The current PPTX route prioritizes visual fidelity by assembling slide images into PowerPoint. The next major improvement path is a native editable PPTX route:

```text
Markdown -> deck plan -> design spec -> SVG slides -> DrawingML/native PPTX
```

That would make generated text, shapes, and charts editable directly in PowerPoint while keeping the existing image-based route for social and presentation-ready visual fidelity.

## Credits

Artifactry is inspired by [getdesign.md](https://getdesign.md/) and the public [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) collection.
