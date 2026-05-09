---
title: "Agent Command Center"
doctype: "slides"
outputs: ["pptx", "png"]
style: "dark-console"
tone: "technical product demo"
aspect: "16:9"
---

# Agent Command Center

## Slide 1: Route The Work

The agent should identify the artifact before touching the renderer.

- doctype: slides | document | carousel | docs
- outputs: pptx | docx | pdf | png | jpg
- aspect: 16:9 | 4:5 | 1:1 | 9:16

## Slide 2: Execute With Tools

The skill gives the agent a deterministic path from source Markdown to final files.

- Normalize Markdown
- Render fixed-canvas HTML
- Capture images with Chrome
- Assemble PPTX from verified frames

## Slide 3: Validate Before Delivery

Every artifact should pass checks before the final answer.

- Correct file count
- Correct dimensions
- No clipped text
- Editable source preserved
