# Claude / Claude Code Guide

For browser-based Claude Chat, use [CLAUDE_CHAT.md](CLAUDE_CHAT.md). This file focuses on Claude Code.

## Agent

This repo includes a Claude Code agent:

```text
.claude/agents/export-designer.md
```

Use it when the task is more than a simple conversion:

```text
Use the export-designer agent to turn this Markdown into a 16:9 presentation and 4:5 carousel using Regulated Ledger style.
```

The agent follows:

```text
diagnose -> ask -> search -> route -> refactor -> render -> validate -> deliver
```

When using this project with Claude or Claude Code, ask explicitly:

```text
Use the local skill at skills/artifactry to convert this Markdown into a polished export.
```

Recommended prompt:

```text
Use $artifactry. Ask me which output, style, and size I want first if I have not specified them. Then read my Markdown, apply local DESIGN.md if present, generate the files, and validate before answering.
```

Claude Code plugin install:

```text
/plugin marketplace add https://github.com/jeremy193a/artifactry.git
/plugin install md-export-skills@md-export-skills
```

Restart Claude Code after installing.

Use the bundled slash command:

```text
/artifactry examples/showcase/board-brief.md as a 16:9 PPTX and PNG deck using Regulated Ledger
```

`/md-artifacts` is also available as a legacy alias for backwards compatibility. Prefer `/artifactry` in new usage.

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
Install Artifactry for Claude Code. Run:
claude plugin marketplace add https://github.com/jeremy193a/artifactry.git
claude plugin install md-export-skills@md-export-skills
Then restart Claude Code and verify /artifactry appears in /help.
```

Local development:

```bash
claude --plugin-dir .
```

For public demos:

```text
Use $artifactry to convert examples/training-handout/worksheet.md into a DOCX using a generated reference.docx.
```

```text
Use $artifactry to create a 4:5 social carousel from examples/social-carousel/ai-agent-export.md using Broadsheet Intelligence style.
```
