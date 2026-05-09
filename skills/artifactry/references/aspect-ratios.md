# Aspect Ratios

Use these defaults unless the user provides exact dimensions.

| Name | Pixel export | PPTX size | Use |
| --- | ---: | ---: | --- |
| `16:9` | `1920x1080` | `13.333333 x 7.5 in` | Presentations, YouTube thumbnails |
| `4:5` | `1638x2048` | `10 x 12.5 in` | LinkedIn/Instagram social carousel |
| `1:1` | `1800x1800` | `10 x 10 in` | Square social posts |
| `9:16` | `1080x1920` | `7.5 x 13.333333 in` | Stories, vertical presentation |
| `A4` | document page | `8.27 x 11.69 in` | Word/PDF documents |
| `Letter` | document page | `8.5 x 11 in` | US docs |

## Rendering Rules

- Render images at target pixel size or higher.
- If browser headless adds extra viewport chrome or background bands, render taller than needed and crop to the top-left target dimensions.
- Keep all text within a safe margin:
  - 16:9: 72-120 px.
  - 4:5: 120-156 px.
  - 1:1: 108-144 px.
  - 9:16: 80-120 px.
- Use fixed dimensions for repeated components so hover/loading/dynamic text cannot shift layout.

## File Naming

Use stable names:

```text
slide-01.png
slide-02.png
...
deck-16x9.pptx
carousel-4x5.zip
document.docx
document.pdf
```
