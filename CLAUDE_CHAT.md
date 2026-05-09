# Claude Chat Guide

This is the primary user path for non-developers who use Claude in the browser.

## What Claude Chat Supports

Claude Chat does not use Claude Code slash commands like `/plugin marketplace add`. For Claude Chat, package this as a custom Skill ZIP and upload it in Claude:

1. Open Claude.
2. Go to `Customize` -> `Skills`.
3. Click `+` -> `Create skill`.
4. Choose `Upload a skill`.
5. Upload `dist/md-export-suite.zip`.
6. Toggle the skill on.

The ZIP must contain the skill folder at the root:

```text
md-export-suite.zip
└── md-export-suite/
    ├── SKILL.md
    ├── references/
    └── scripts/
```

## Recommended User Prompt

```text
Use the MD Export Suite skill. I have a Markdown file and want to export it. First ask me which output format, visual style, and size I want. Then create the files and validate them.
```

## Style Question Claude Should Ask

Whenever the user has not specified enough detail, Claude should ask:

```text
Before I export, choose the target:
1. Output: DOCX, PDF, PPTX, PNG/JPG carousel, or bundle?
2. Style: Institutional Clarity, Warm Editorial, Monochrome Precision, Dark Console, Gradient Intelligence, Data Command, Visual Lifestyle, Cinematic Luxury, Playful Productivity, Broadsheet Analysis, or local DESIGN.md?
3. Size: A4/Letter, 16:9, 4:5, 1:1, 9:16, or custom?
4. Priority: editable file, final polished visual, or both?
```

## Prompt Examples

```text
Use MD Export Suite to turn this Markdown into a polished DOCX. Ask me which document style I want first.
```

```text
Use MD Export Suite to create a 4:5 social carousel from this Markdown. Ask me which getdesign.md style to use.
```

```text
Use MD Export Suite to export this training Markdown into both a 16:9 presentation and an A4 handout.
```

## Notes For Users

- Upload the Markdown file into the chat.
- If you have a `DESIGN.md`, upload it too.
- Choose one of the 10 generic styles, or upload a local `DESIGN.md` if you want the agent to adapt a custom visual system.
- For best results, keep one Markdown file per deliverable.
