# DESIGN.md Adapter

Use this when a project has a local `DESIGN.md` or when the user asks for a style from https://getdesign.md/.

## Goal

Translate a UI/web design system into export rules for documents, decks, and social images. Do not copy website sections directly. Preserve the mood, hierarchy, color logic, typography direction, and component behavior in the format being exported.

## Acquisition

If the user names a style and no `DESIGN.md` exists, use:

```bash
npx getdesign@latest add <style-name>
```

Use any design name available in getdesign.md. Convert it into one of the generic style archetypes before exposing it to users.

If network or npm access is blocked, ask for approval or proceed with existing local style references.

## Translation Model

Read `DESIGN.md` and extract:

- Brand adjectives: e.g. institutional, warm, cinematic, developer-centric, editorial.
- Core colors: primary, background, surface, text, muted, semantic colors.
- Typography roles: display, body, mono, caption.
- Shape system: radii, pills, cards, dividers, buttons, panels.
- Density: sparse editorial, dense dashboard, document-like, cinematic.
- Motion/media guidance if relevant, but translate static exports into composition and visual rhythm.

Then map to medium-specific tokens.

## Generic Style Schema

The bundled styles in `styles/` are not simple palettes. Treat each style as an export design system derived from the local getdesign.md corpus:

- `style_dna`: philosophy, visual signature, surface logic, density.
- `palette`: color roles, accent policy, semantic color policy.
- `typography.scale`: display/body/label size, weight, line height, letter spacing, label casing.
- `shape`: corner scale, default radius, border weight.
- `layout`: grid, whitespace, image treatment.
- `components`: buttons, cards, tables, callouts.
- `slides`: deterministic CSS/PPTX tokens such as background, title rhythm, card shadow, border width, and accent geometry.
- `document`: Word/PDF translation rules such as title size, margins, heading logic, table header treatment.
- `guardrails`: do/don't rules that prevent generic model output.
- `export_translation`: format-specific instructions for PPTX, DOCX, and carousel/image exports.

When generating an artifact, inherit from the whole schema. Do not stop at `colors` and `typography`.

## Document Tokens

For Word/PDF:

- Page size and margins.
- Title, Heading 1/2/3, Normal, Code, Blockquote styles.
- Table header fill, border color, cell padding.
- Header/footer treatment.
- Link/accent color.

Rules:

- Documents must remain printable and editable.
- Use brand fonts only when likely installed; otherwise choose portable fallbacks.
- Avoid dark full-page documents unless the user explicitly asks for a designed PDF, because Word editing/printing suffers.

## Slide Tokens

For PPTX/presentation:

- Canvas size and safe margin.
- Background rotation: white, soft surface, dark chapter slide.
- Display headline size/weight.
- Body and label size.
- Card/table radius, row height, divider weight.
- Footer/page number location.
- Accent usage rules.

Rules:

- One idea per slide.
- Deterministic text with HTML/CSS/PPTX text boxes.
- Avoid copying website hero layouts unless the requested output is a landing-page mockup.

## Image Tokens

For PNG/JPG carousel:

- Pixel canvas: usually `1638x2048` for 4:5 or `1920x1080` for 16:9.
- Safe margin.
- Text scale.
- Compression target.
- Background and footer treatment.

Rules:

- Text must stay readable on mobile.
- Export high resolution first, then downscale only if requested.
- Use JPG for photo-heavy outputs, PNG for text-heavy/carousel outputs.

## Generic Style Mapping

Map `DESIGN.md` findings to one of the 10 generic style archetypes in `styles/`.

### Institutional Clarity

White canvas, restrained accent, black text, gray surfaces, mono numbers, rounded cards, institutional trust, minimal ornament.

### Warm Editorial

Warm off-white canvas, terracotta or earthy accent, editorial calm, generous whitespace, softer document feel.

### Monochrome Precision

Black-and-white minimalism, tight hierarchy, crisp dividers, technical confidence, little to no color.

### Dark Console

Dark developer surface, monospace labels, code panels, command-line rhythm, sharp contrast.

### Gradient Intelligence

Controlled purple/blue or aurora gradients, modern AI/product polish, luminous but structured.

### Data Command

Dashboard density, metric cards, tables, status colors, analytical hierarchy.

### Visual Lifestyle

Photo-led, friendly, consumer-facing, soft cards, large imagery, simple captions.

### Cinematic Luxury

Black canvas, high contrast, dramatic spacing, uppercase or serif display, premium accent.

### Playful Productivity

Friendly SaaS modules, colorful structure, approachable forms, onboarding rhythm.

### Broadsheet Analysis

Paper-white editorial density, serif display, mono kickers, hairline rules, research-led layout.

## Anti-patterns

- Averaging multiple brands into a muddy palette.
- Using app dashboard density for a presentation slide.
- Rendering Word documents as screenshots.
- Using generated images for text.
- Ignoring print/editability for DOCX.
- Using many accent colors just because a design system lists them.
