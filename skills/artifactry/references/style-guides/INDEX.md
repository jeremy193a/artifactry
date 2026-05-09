# Artifactry Style Guides

This folder contains Artifactry's public style guide layer. These files are not brand clones. They are generic, reusable art directions synthesized from the local `.work/getdesign-md/organized` corpus.

Use these Markdown guides before rendering any visual artifact. The existing JSON files are token fallbacks for deterministic scripts; these Markdown guides are the primary creative direction for agents.

## How Agents Should Use This

1. Ask the user for desired artifact type, audience, tone, output format, and aspect ratio.
2. Select one style guide below by intent, not by color preference.
3. Read the chosen style guide before writing HTML/CSS, SVG, PPTX, or DOCX layout code.
4. Choose slide/document roles from the guide instead of rendering every page with one generic template.
5. Translate the guide into deterministic layout: real text, fixed canvas, CSS/SVG/PPTX shapes, validation.
6. Do not average styles. Pick one dominant guide and borrow at most one secondary trait only when the user asks.

## 15 Public Styles

| ID | Name | Best For | Visual Signature |
|---|---|---|---|
| `regulated-ledger` | Regulated Ledger | Executive decks, finance reports, board memos | White trust canvas, blue signal, mono figures, quiet cards |
| `human-workshop` | Human Workshop | Training, education, worksheets, team enablement | Warm paper, human reading rhythm, workbook modules |
| `swiss-protocol` | Swiss Protocol | Technical memos, founder briefs, product specs | Black-white discipline, hard grid, exact hierarchy |
| `terminal-operator` | Terminal Operator | Agent workflows, API guides, developer decks | Dark console surfaces, command blocks, status accents |
| `aurora-product` | Aurora Product | AI launches, product announcements, feature decks | Luminous gradients, glass panels, low-weight display type |
| `metrics-command` | Metrics Command | KPI reviews, analytics, ops reporting | Dense dashboard language, metric strips, status systems |
| `broadsheet-intelligence` | Broadsheet Intelligence | Research, market analysis, thought leadership | Newspaper density, serif voice, footnotes, rules |
| `black-label-cinema` | Black Label Cinema | Premium pitches, portfolio, hero presentations | Black canvas, cinematic scale, scarce metallic accents |
| `playful-systems` | Playful Systems | SaaS onboarding, internal tools, team workflows | Modular cards, friendly color, diagram-first clarity |
| `image-market` | Image Market | Social stories, consumer campaigns, product narratives | Photo-led layouts, caption systems, commerce rhythm |
| `spatial-canvas` | Spatial Canvas | Workshops, collaboration maps, brainstorm outputs | Infinite-canvas boards, sticky logic, connector systems |
| `blueprint-infra` | Blueprint Infra | Architecture, infrastructure, technical strategy | Blueprint grids, system maps, structured code evidence |
| `commerce-editorial` | Commerce Editorial | Retail, catalog, brand/product explainers | Product tiles, warm editorial surfaces, confident CTAs |
| `motion-premiere` | Motion Premiere | Creative AI, media decks, launch trailers | Film-festival pacing, dark heroes, frame marks |
| `performance-machine` | Performance Machine | Automotive, sports, hardware, high-stakes demos | Precision dark surfaces, velocity bands, spec-sheet drama |

## Selection Heuristics

- If trust and decision quality matter most, choose `regulated-ledger`.
- If teaching and adoption matter most, choose `human-workshop`.
- If exactness and restraint matter most, choose `swiss-protocol`.
- If the artifact is for developers or agents, choose `terminal-operator` or `blueprint-infra`.
- If the artifact must feel like a modern AI/product launch, choose `aurora-product`.
- If the artifact is numbers-heavy, choose `metrics-command`.
- If the artifact needs editorial authority, choose `broadsheet-intelligence`.
- If the artifact must impress immediately, choose `black-label-cinema`, `motion-premiere`, or `performance-machine`.
- If the artifact is for social/product storytelling, choose `image-market` or `commerce-editorial`.
- If the artifact explains a messy process, choose `spatial-canvas` or `playful-systems`.

## Shared Quality Bar

- Use real text. Never ask an image model to render final text-heavy slides.
- Pick page roles before designing: cover, thesis, big-number, timeline, comparison, map, table, dashboard, quote, checklist, closer.
- Keep each slide/page anchored by one dominant hierarchy.
- Do not add decorative shapes that do not explain the content.
- Validate output dimensions, clipping, contrast, and file integrity.
- Vietnamese text must preserve diacritics and remain legible at social preview size.
