# Claude / Claude Code Guide

For browser-based Claude Chat, use [CLAUDE_CHAT.md](CLAUDE_CHAT.md). This file focuses on Claude Code.

## Agent

This repo includes a Claude Code agent:

```text
.claude/agents/export-designer.md
```

Use it when the task is more than a simple conversion:

```text
Use the export-designer agent to turn this Markdown into a 16:9 presentation and 4:5 carousel using Institutional Clarity style.
```

The agent follows:

```text
diagnose -> ask -> search -> route -> refactor -> render -> validate -> deliver
```

When using this project with Claude or Claude Code, ask explicitly:

```text
Use the local skill at skills/md-export-suite to convert this Markdown into a polished export.
```

Recommended prompt:

```text
Use $md-export-suite. Ask me which output, style, and size I want first if I have not specified them. Then read my Markdown, apply local DESIGN.md if present, generate the files, and validate before answering.
```

Claude Code plugin install:

```text
/plugin marketplace add https://github.com/jeremy193a/md-to-artifacts.git
/plugin install md-export-skills@md-export-skills
```

Restart Claude Code after installing.

Use the bundled slash command:

```text
/md-artifacts examples/showcase/board-brief.md as a 16:9 PPTX and PNG deck using Institutional Clarity
```

Update an installed version:

```text
/plugin marketplace update md-export-skills
/plugin update md-export-skills@md-export-skills
```

Terminal equivalent:

```bash
claude plugin marketplace update md-export-skills
claude plugin update md-export-skills@md-export-skills
```

Restart Claude Code after updating.

Tell an agent to install it:

```text
Install MD Export Skills for Claude Code. Run:
claude plugin marketplace add https://github.com/jeremy193a/md-to-artifacts.git
claude plugin install md-export-skills@md-export-skills
Then restart Claude Code and verify /md-artifacts appears in /help.
```

Local development:

```bash
claude --plugin-dir .
```

For public demos:

```text
Use $md-export-suite to convert examples/training-handout/worksheet.md into a DOCX using a generated reference.docx.
```

```text
Use $md-export-suite to create a 4:5 social carousel from examples/social-carousel/ai-agent-export.md using Broadsheet Analysis style.
```
