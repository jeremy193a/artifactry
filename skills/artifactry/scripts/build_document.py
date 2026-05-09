#!/usr/bin/env python3
"""Export Markdown documents to styled DOCX, HTML, and PDF."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from build_reference_docx import build as build_reference
from normalize_markdown import expand_includes, normalize
from render_images_chrome import find_chrome
from style_resolver import load_style


CSS_TEMPLATE = """
@page {
  size: __PAGE_SIZE__;
  margin: __MARGIN_TOP__cm __MARGIN_RIGHT__cm __MARGIN_BOTTOM__cm __MARGIN_LEFT__cm;
}
:root {
  --primary: __PRIMARY__;
  --ink: __INK__;
  --body: __BODY__;
  --muted: __MUTED__;
  --line: __LINE__;
  --surface: __SURFACE__;
  --background: __BACKGROUND__;
  --display: __DISPLAY__;
  --body-font: __BODY_FONT__;
  --mono: __MONO__;
}
* { box-sizing: border-box; }
html { background: #d8dde6; }
body {
  margin: 0 auto;
  color: var(--body);
  background: var(--background);
  font-family: var(--body-font), -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 10.8pt;
  line-height: 1.5;
}
main {
  max-width: 100%;
}
h1, h2, h3, h4 {
  color: var(--ink);
  font-family: var(--display), var(--body-font), sans-serif;
  line-height: 1.08;
  page-break-after: avoid;
}
h1 {
  margin: 0 0 18pt;
  padding-bottom: 10pt;
  border-bottom: 2pt solid var(--primary);
  font-size: 28pt;
  font-weight: 760;
}
h2 {
  margin: 24pt 0 8pt;
  font-size: 19pt;
  font-weight: 740;
}
h3 {
  margin: 18pt 0 6pt;
  font-size: 14pt;
  font-weight: 720;
}
p { margin: 0 0 8pt; }
a { color: var(--primary); text-decoration: none; }
strong { color: var(--ink); }
blockquote {
  margin: 14pt 0;
  padding: 12pt 14pt;
  border-left: 4pt solid var(--primary);
  background: var(--surface);
  color: var(--ink);
}
code {
  font-family: var(--mono), ui-monospace, SFMono-Regular, Consolas, monospace;
  font-size: .92em;
  color: var(--ink);
}
pre {
  margin: 12pt 0;
  padding: 12pt 14pt;
  border: 1pt solid var(--line);
  border-radius: 6pt;
  background: var(--surface);
  white-space: pre-wrap;
  page-break-inside: avoid;
}
pre code { font-size: 8.8pt; }
table {
  width: 100%;
  margin: 14pt 0;
  border-collapse: collapse;
  page-break-inside: avoid;
  font-size: 9.4pt;
}
th, td {
  padding: 8pt 9pt;
  border: 1pt solid var(--line);
  vertical-align: top;
}
th {
  color: var(--ink);
  background: var(--surface);
  font-weight: 760;
}
ul, ol { margin: 0 0 10pt 18pt; padding: 0; }
li { margin: 3pt 0; }
hr {
  margin: 20pt 0;
  border: 0;
  border-top: 1pt solid var(--line);
}
img {
  max-width: 100%;
  height: auto;
  page-break-inside: avoid;
}
.artifactry-cover {
  margin-bottom: 24pt;
  color: var(--muted);
  font-size: 8.8pt;
  font-weight: 760;
  text-transform: uppercase;
  letter-spacing: .06em;
}
.writing-line {
  display: block;
  min-height: 28pt;
  border-bottom: 1pt solid var(--line);
}
"""


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print(" ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)


def pandoc_available() -> bool:
    try:
        subprocess.run(["pandoc", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def css_for_style(style_id: str, page_size: str) -> str:
    style, _ = load_style(style_id)
    colors = style["colors"]
    typography = style["typography"]
    margins = style.get("document", {}).get("margins_cm", [2.2, 2.0, 2.2, 2.2])
    replacements = {
        "__PAGE_SIZE__": "Letter" if page_size == "letter" else "A4",
        "__MARGIN_TOP__": str(float(margins[0])),
        "__MARGIN_BOTTOM__": str(float(margins[1])),
        "__MARGIN_LEFT__": str(float(margins[2])),
        "__MARGIN_RIGHT__": str(float(margins[3])),
        "__PRIMARY__": colors["primary"],
        "__INK__": colors["ink"],
        "__BODY__": colors["body"],
        "__MUTED__": colors["muted"],
        "__LINE__": colors["line"],
        "__SURFACE__": colors["surface"],
        "__BACKGROUND__": colors["background"],
        "__DISPLAY__": typography.get("display", "Inter"),
        "__BODY_FONT__": typography.get("body", "Inter"),
        "__MONO__": typography.get("mono", "JetBrains Mono"),
    }
    css = CSS_TEMPLATE
    for key, value in replacements.items():
        css = css.replace(key, value)
    return css


def pandoc_html(normalized_md: Path, output_html: Path, title: str, style_id: str, page_size: str) -> None:
    if not pandoc_available():
        raise SystemExit("pandoc is required for document HTML/PDF export.")

    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as css_file:
        css_file.write("<style>\n")
        css_file.write(css_for_style(style_id, page_size))
        css_file.write("\n</style>\n")
        css_path = Path(css_file.name)
    cover_path = write_cover(title, style_id)

    try:
        run(
            [
                "pandoc",
                str(normalized_md),
                "--from=markdown+smart",
                "--to=html5",
                "--standalone",
                "--metadata",
                f"title={title}",
                "--include-in-header",
                str(css_path),
                "--include-before-body",
                str(cover_path),
                "--output",
                str(output_html),
            ]
        )
    finally:
        css_path.unlink(missing_ok=True)
        cover_path.unlink(missing_ok=True)


def write_cover(title: str, style_id: str) -> Path:
    cover = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8")
    cover.write(f'<main><div class="artifactry-cover">Artifactry · {style_id}</div>\n')
    cover.close()
    return Path(cover.name)


def close_main(output_html: Path) -> None:
    text = output_html.read_text(encoding="utf-8")
    if "</body>" in text and "</main>" not in text:
        text = text.replace("</body>", "</main>\n</body>")
        output_html.write_text(text, encoding="utf-8")


def chrome_pdf(html_path: Path, output_pdf: Path, chrome: str | None = None) -> None:
    chrome_bin = find_chrome(chrome)
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            chrome_bin,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={output_pdf}",
            html_path.resolve().as_uri(),
        ]
    )


def soffice_pdf(docx_path: Path, output_pdf: Path) -> None:
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    out_dir = output_pdf.parent
    run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(out_dir), str(docx_path)])
    generated = out_dir / f"{docx_path.stem}.pdf"
    if generated != output_pdf and generated.exists():
        generated.replace(output_pdf)


def build(input_path: Path, output_dir: Path, outputs: list[str], style_id: str, company: str, page_size: str, pdf_route: str, worksheet_lines: bool, chrome: str | None) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = input_path.stem
    normalized_md = output_dir / f"{stem}.normalized.md"
    normalized_md.write_text(normalize(expand_includes(input_path), worksheet_lines=worksheet_lines), encoding="utf-8")

    built: list[Path] = []
    docx_path = output_dir / f"{stem}.docx"
    html_path = output_dir / f"{stem}.html"
    pdf_path = output_dir / f"{stem}.pdf"

    if "docx" in outputs or pdf_route == "soffice":
        reference = output_dir / "reference.docx"
        build_reference(reference, company, style_id, page_size=page_size)
        run(
            [
                "pandoc",
                str(normalized_md),
                "--from=markdown+smart",
                "--to=docx",
                f"--reference-doc={reference}",
                "--output",
                str(docx_path),
            ]
        )
        if "docx" in outputs:
            built.append(docx_path)

    if "html" in outputs or ("pdf" in outputs and pdf_route == "chrome"):
        pandoc_html(normalized_md, html_path, input_path.stem.replace("-", " ").title(), style_id, page_size)
        close_main(html_path)
        if "html" in outputs:
            built.append(html_path)

    if "pdf" in outputs:
        if pdf_route == "soffice":
            soffice_pdf(docx_path, pdf_path)
        elif pdf_route == "pandoc":
            run(["pandoc", str(normalized_md), "--from=markdown+smart", "--pdf-engine=xelatex", "--output", str(pdf_path)])
        else:
            if not html_path.exists():
                pandoc_html(normalized_md, html_path, input_path.stem.replace("-", " ").title(), style_id, page_size)
                close_main(html_path)
            chrome_pdf(html_path, pdf_path, chrome)
        built.append(pdf_path)

    return built


def main() -> None:
    parser = argparse.ArgumentParser(description="Build styled DOCX/HTML/PDF from Markdown.")
    parser.add_argument("input", help="Input Markdown file.")
    parser.add_argument("--output-dir", "-o", default="output/document", help="Output directory.")
    parser.add_argument("--outputs", nargs="+", default=["docx", "pdf"], choices=["docx", "pdf", "html"])
    parser.add_argument("--style", default="regulated-ledger", help="Artifactry style guide or token style ID.")
    parser.add_argument("--company", default="Artifactry")
    parser.add_argument("--page-size", default="a4", choices=["a4", "letter"])
    parser.add_argument("--pdf-route", default="chrome", choices=["chrome", "soffice", "pandoc"])
    parser.add_argument("--worksheet-lines", action="store_true")
    parser.add_argument("--chrome", help="Path to Chrome/Chromium binary.")
    args = parser.parse_args()

    built = build(
        Path(args.input),
        Path(args.output_dir),
        args.outputs,
        args.style,
        args.company,
        args.page_size,
        args.pdf_route,
        args.worksheet_lines,
        args.chrome,
    )
    for path in built:
        print(path)


if __name__ == "__main__":
    main()
