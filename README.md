# Artifactry

![Artifactry hero](assets/md-to-artifacts-hero.jpeg)

Markdown in, polished artifacts out.

Artifactry is an AI-agent skill pack that turns Markdown into designed deliverables: DOCX, PDF, PPTX, PNG/JPG carousels, and multi-format content bundles. It is built for Claude Chat/Desktop, Claude Code, Codex, OpenCode, and other agentic coding environments.

The core idea is simple: Markdown stays the source of truth, while Artifactry gives the agent an export workflow, style system, render scripts, and validation checks so the final files look intentional enough to present, publish, print, or send to a client.

## What It Does

- Converts `.md` files into Word documents, PDFs, decks, social images, and bundles.
- Guides the agent to ask for output type, style, size, and editability before rendering.
- Uses detailed Markdown style guides inspired by `DESIGN.md`, plus script-friendly JSON token fallbacks.
- Supports frontmatter routing with `doctype: document | slides | carousel | docs`.
- Supports includes/partials with `{{ include: sections/module-1.md }}`.
- Renders slide/carousel images through HTML/CSS and Chrome, then assembles PPTX from those images.
- Builds DOCX with generated `reference.docx` files and validates DOCX, PDF, PPTX, PNG, and JPG outputs.

Artifactry includes a Claude Code slash command, a legacy alias, and an agent profile:

```text
/artifactry        canonical command
/md-artifacts     legacy alias for backwards compatibility
export-designer
```

The operating loop is:

```text
diagnose -> ask -> search -> route -> refactor -> render -> validate -> deliver
```

## Install

### Claude Chat / Desktop

Claude Chat/Desktop uses a Skill ZIP, not Claude Code plugins.

1. Tell Claude to install Artifactry

![Artifactry Claude Chat](assets/claude-chat-install.jpeg)

2. Download the artifactry.zip file above
3. Open Claude.ai or Claude Desktop
4. Click + → Manage Skill → Upload a skill
5. Upload the downloaded artifactry.zip file
6. You can use the skill now.

Recommended Claude prompt:

```text
Use the Artifactry skill. I uploaded a Markdown file. Ask me which output format, style, and size I want, then export and validate the files.
```

### Claude Code

Use the HTTPS repo URL exactly:

```text
/plugin marketplace add artifactry https://github.com/jeremy193a/artifactry.git
/plugin install artifactry@artifactry
```

Restart Claude Code, then verify `/artifactry` appears in `/help`.

![Artifactry Claude Code](assets/claude-code-command.png)

Example:

```text
/artifactry examples/showcase/board-brief.md as a 16:9 PPTX and PNG deck using Regulated Ledger
```

Update after a new release:

```text
/plugin marketplace update artifactry
/plugin update artifactry@artifactry
```

Agent install prompt:

```text
Install Artifactry for Claude Code. Use:
claude plugin marketplace add artifactry https://github.com/jeremy193a/artifactry.git
claude plugin install artifactry@artifactry
Then restart Claude Code and confirm /artifactry is available.
```

### Codex / OpenCode

Install the local skill folder in the agent's skill directory:

```bash
mkdir -p ~/.codex/skills
ln -s /path/to/artifactry/skills/artifactry ~/.codex/skills/artifactry
```

See [CODEX.md](CODEX.md) and [OPENCODE.md](OPENCODE.md).

## Agent Preflight

Users should not need to manually reason through system packages. Tell the agent to run the preflight first:

```bash
python scripts/check_requirements.py
```

If anything is missing, the script prints the purpose and install command. The agent should ask for approval before installing system tools.

Recommended setup prompt:

```text
Run python scripts/check_requirements.py. If Python packages are missing, install them with python3 -m pip install -r requirements.txt. If system tools are missing, ask for approval before installing only what this export needs.
```

Artifactry uses:

- Python packages from `requirements.txt`
- Pandoc for conversion routes
- Google Chrome or Chromium for PNG/JPG and styled PDF rendering
- Node/npm for `npx getdesign@latest add <style>`
- LibreOffice for DOCX-to-PDF fidelity
- XeLaTeX only for Pandoc PDF routes that need LaTeX

## Style System

The primary style guides live in:

```text
skills/artifactry/references/style-guides/
```

They are generic archetypes synthesized from a local getdesign.md corpus. Artifactry does not expose copied brand names as public styles.

| Style | Best For |
|---|---|
| Regulated Ledger | Finance, board, compliance, risk, executive artifacts |
| Human Workshop | Training, education, worksheets, enablement |
| Swiss Protocol | Technical memos, specs, founder briefs, strict monochrome docs |
| Terminal Operator | Agent workflows, API guides, automation playbooks |
| Aurora Product | AI/product launches, feature narratives, luminous product decks |
| Metrics Command | KPI reviews, analytics, dashboards, operating reports |
| Broadsheet Intelligence | Research, market analysis, editorial carousels |
| Black Label Cinema | Premium dark decks, portfolios, high-stakes pitches |
| Playful Systems | SaaS onboarding, workflow explainers, internal tools |
| Image Market | Photo-led campaigns, catalogs, product narratives |
| Spatial Canvas | Workshop maps, brainstorms, process diagrams |
| Blueprint Infra | Architecture, infrastructure, API maps, engineering strategy |
| Commerce Editorial | Retail, offers, catalogs, product explainers |
| Motion Premiere | Creative AI, media launches, storyboard narratives |
| Performance Machine | Hardware, automotive, sport, industrial demos |

List available styles:

```bash
python skills/artifactry/scripts/list_styles.py
```

Artifactry can also adapt a local `DESIGN.md` or fetch one with:

```bash
npx getdesign@latest add <style-name>
```

## Showcase

The showcase uses Artifactry's own project story as source material, so the examples are honest: the DOCX files are README/worksheet exports, and the visual gallery is generated from the signature style guides.

### Signature Style Gallery

Built with:

```bash
python scripts/build_signature_showcase.py
```

| Regulated Ledger | Human Workshop | Swiss Protocol |
|---|---|---|
| <img src="assets/showcase/signature/regulated-ledger/slide-01.png" alt="Regulated Ledger showcase" width="260"> | <img src="assets/showcase/signature/human-workshop/slide-01.png" alt="Human Workshop showcase" width="260"> | <img src="assets/showcase/signature/swiss-protocol/slide-01.png" alt="Swiss Protocol showcase" width="260"> |

| Terminal Operator | Aurora Product | Metrics Command |
|---|---|---|
| <img src="assets/showcase/signature/terminal-operator/slide-01.png" alt="Terminal Operator showcase" width="260"> | <img src="assets/showcase/signature/aurora-product/slide-01.png" alt="Aurora Product showcase" width="260"> | <img src="assets/showcase/signature/metrics-command/slide-01.png" alt="Metrics Command showcase" width="260"> |

| Broadsheet Intelligence | Black Label Cinema | Playful Systems |
|---|---|---|
| <img src="assets/showcase/signature/broadsheet-intelligence/slide-01.png" alt="Broadsheet Intelligence showcase" width="260"> | <img src="assets/showcase/signature/black-label-cinema/slide-01.png" alt="Black Label Cinema showcase" width="260"> | <img src="assets/showcase/signature/playful-systems/slide-01.png" alt="Playful Systems showcase" width="260"> |

| Image Market | Spatial Canvas | Blueprint Infra |
|---|---|---|
| <img src="assets/showcase/signature/image-market/slide-01.png" alt="Image Market showcase" width="260"> | <img src="assets/showcase/signature/spatial-canvas/slide-01.png" alt="Spatial Canvas showcase" width="260"> | <img src="assets/showcase/signature/blueprint-infra/slide-01.png" alt="Blueprint Infra showcase" width="260"> |

| Commerce Editorial | Motion Premiere | Performance Machine |
|---|---|---|
| <img src="assets/showcase/signature/commerce-editorial/slide-01.png" alt="Commerce Editorial showcase" width="260"> | <img src="assets/showcase/signature/motion-premiere/slide-01.png" alt="Motion Premiere showcase" width="260"> | <img src="assets/showcase/signature/performance-machine/slide-01.png" alt="Performance Machine showcase" width="260"> |

### DOCX Showcase

Five distinct document styles are checked in for direct download:

| Style | Source | Download |
|---|---|---|
| Regulated Ledger | `README.md` | [Download DOCX](assets/showcase/docx/regulated-ledger-readme.docx?raw=1) |
| Human Workshop | `examples/training-handout/worksheet.md` | [Download DOCX](assets/showcase/docx/human-workshop-worksheet.docx?raw=1) |
| Swiss Protocol | `README.md` | [Download DOCX](assets/showcase/docx/swiss-protocol-readme.docx?raw=1) |
| Terminal Operator | `README.md` | [Download DOCX](assets/showcase/docx/terminal-operator-readme.docx?raw=1) |
| Broadsheet Intelligence | `README.md` | [Download DOCX](assets/showcase/docx/broadsheet-intelligence-readme.docx?raw=1) |

Rebuild a DOCX showcase file:

```bash
python skills/artifactry/scripts/build_document.py README.md --style regulated-ledger --outputs docx --output-dir output/showcase/docx/regulated-ledger
```

## Core Commands

Build the Claude Skill ZIP:

```bash
python scripts/package_claude_skill.py
```

Build a styled document:

```bash
python skills/artifactry/scripts/build_document.py input.md --style human-workshop --outputs docx pdf html --output-dir output/document
```

Build slide images:

```bash
python skills/artifactry/scripts/render_html_deck.py input.md --style terminal-operator --aspect 16:9 --output-dir output/deck
python skills/artifactry/scripts/visual_audit_html.py output/deck/slides-html --aspect 16:9
python skills/artifactry/scripts/render_images_chrome.py output/deck/slides-html --aspect 16:9 --output-dir output/deck/png
```

Validate exports:

```bash
python skills/artifactry/scripts/validate_exports.py output/document/document.docx output/deck
```

## Markdown Conventions

Use frontmatter to route the export:

```yaml
---
title: "AI Training Bootcamp"
doctype: "slides"
outputs: ["pptx", "png"]
style: "terminal-operator"
aspect: "16:9"
---
```

Use includes to split large projects:

```markdown
# AI Training Bootcamp

{{ include: sections/module-1.md }}

{{ include: sections/module-2.md }}
```

Includes are expanded before rendering. Include syntax inside fenced code blocks is left untouched.

## License

MIT

## Credits

Artifactry is inspired by [getdesign.md](https://getdesign.md/) and the public [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) collection. Their detailed `DESIGN.md` examples helped shape the style inheritance model used here.
