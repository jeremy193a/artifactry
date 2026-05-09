#!/usr/bin/env python3
"""Render a simple Markdown deck/carousel into fixed-canvas HTML slides."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path


ASPECTS = {
    "16:9": (1920, 1080, "wide"),
    "4:5": (1638, 2048, "portrait"),
    "1:1": (1800, 1800, "square"),
    "9:16": (1080, 1920, "story"),
}

STYLE_DIR = Path(__file__).resolve().parents[1] / "styles"
INCLUDE_RE = re.compile(r"^\s*\{\{\s*include:\s*([^}]+?)\s*\}\}\s*$")


def load_style(style_id: str) -> dict:
    path = STYLE_DIR / f"{style_id}.json"
    if not path.exists():
        choices = ", ".join(sorted(p.stem for p in STYLE_DIR.glob("*.json") if p.name != "style_index.json"))
        raise SystemExit(f"Unknown style '{style_id}'. Available styles: {choices}")
    return json.loads(path.read_text(encoding="utf-8"))


def expand_includes(path: Path, seen: set[Path] | None = None) -> str:
    """Expand {{ include: relative/path.md }} directives recursively."""
    source = path.resolve()
    seen = seen or set()
    if source in seen:
        chain = " -> ".join(str(p) for p in [*seen, source])
        raise ValueError(f"Circular include detected: {chain}")
    seen.add(source)

    expanded: list[str] = []
    for raw in source.read_text(encoding="utf-8").splitlines():
        match = INCLUDE_RE.match(raw)
        if not match:
            expanded.append(raw)
            continue
        include_path = (source.parent / match.group(1).strip()).resolve()
        if not include_path.exists():
            raise FileNotFoundError(f"Include not found: {include_path}")
        expanded.append(expand_includes(include_path, seen.copy()).rstrip())
    return "\n".join(expanded) + "\n"


def strip_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end].strip().splitlines()
    meta: dict[str, str] = {}
    for line in raw:
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta, text[end + 5 :]


def parse_slides(markdown: str) -> tuple[str, list[dict[str, object]]]:
    lines = markdown.strip().splitlines()
    deck_title = "Markdown Export"
    slides: list[dict[str, object]] = []
    current: dict[str, object] | None = None

    def finish() -> None:
        nonlocal current
        if current and (current.get("title") or current.get("body")):
            slides.append(current)
        current = None

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("# "):
            deck_title = line[2:].strip()
            continue
        if line == "---":
            finish()
            continue
        if line.startswith("## "):
            finish()
            title = re.sub(r"^Slide\s+\d+\s*[:—-]\s*", "", line[3:].strip(), flags=re.I)
            current = {"title": title, "body": [], "bullets": []}
            continue
        if current is None:
            if line.strip():
                current = {"title": deck_title, "body": [], "bullets": []}
            else:
                continue
        if line.startswith("- "):
            current.setdefault("bullets", []).append(line[2:].strip())
        elif line.strip():
            current.setdefault("body", []).append(line.strip())

    finish()
    if not slides:
        slides = [{"title": deck_title, "body": ["No slide content found."], "bullets": []}]
    return deck_title, slides


def slide_body(slide: dict[str, object]) -> str:
    paragraphs = "".join(f"<p>{html.escape(str(p))}</p>" for p in slide.get("body", []))
    bullets = "".join(f"<li>{html.escape(str(b))}</li>" for b in slide.get("bullets", []))
    bullet_html = f"<ul>{bullets}</ul>" if bullets else ""
    return paragraphs + bullet_html


BASE_CSS = """
:root {
  --primary: __PRIMARY__;
  --ink: __INK__;
  --body: __BODY__;
  --muted: __MUTED__;
  --line: __LINE__;
  --soft: __SURFACE__;
  --canvas: __BACKGROUND__;
  --display-font: __DISPLAY_FONT__;
  --body-font: __BODY_FONT__;
  --mono-font: __MONO_FONT__;
  --card-radius: __CARD_RADIUS__px;
  --headline-weight: __HEADLINE_WEIGHT__;
}
* { box-sizing: border-box; }
html, body { margin: 0; font-family: var(--body-font), Arial, sans-serif; color: var(--ink); background: #d8dde6; }
body.single { width: var(--w); height: var(--h); overflow: hidden; background: var(--canvas); }
body.deck { padding: 40px; }
.deck-wrap { display: grid; gap: 40px; justify-content: center; }
body.single .deck-wrap { width: var(--w); height: var(--h); display: block; overflow: hidden; }
.slide { position: relative; width: var(--w); height: var(--h); overflow: hidden; background: var(--canvas); box-shadow: 0 12px 48px rgba(10,11,13,.16); }
body.single .slide { position: absolute; inset: 0; box-shadow: none; }
.pad { position: absolute; inset: var(--pad-y) var(--pad-x); }
.header, .footer { position: absolute; left: var(--pad-x); right: var(--pad-x); display: flex; justify-content: space-between; color: var(--muted); font-weight: 650; font-size: var(--meta); }
.header { top: var(--pad-y); }
.footer { bottom: var(--footer-y); }
.kicker { display: flex; align-items: center; gap: 14px; }
.dot { width: 13px; height: 13px; border-radius: 50%; background: var(--primary); }
.content { position: absolute; left: var(--pad-x); right: var(--pad-x); top: var(--content-top); bottom: var(--footer-y); display: grid; align-content: center; }
.title { max-width: var(--title-width); margin: 0; font-family: var(--display-font), Arial, sans-serif; font-size: var(--title); line-height: .98; letter-spacing: -1px; font-weight: var(--headline-weight); }
.blue { color: var(--primary); }
.body { margin-top: var(--gap); max-width: var(--body-width); color: var(--body); font-size: var(--copy); line-height: 1.28; }
.body p { margin: 0 0 .7em; }
.body ul { margin: 0; padding: 0; list-style: none; display: grid; gap: var(--bullet-gap); }
.body li { padding: var(--bullet-pad); border: 1px solid var(--line); border-radius: var(--card-radius); background: var(--soft); font-weight: 650; color: var(--ink); }
body.wide { --w: 1920px; --h: 1080px; --pad-x: 92px; --pad-y: 76px; --footer-y: 52px; --content-top: 150px; --title: 82px; --copy: 30px; --meta: 22px; --gap: 34px; --bullet-gap: 18px; --bullet-pad: 24px 28px; --radius: 24px; --title-width: 1320px; --body-width: 980px; }
body.portrait { --w: 1638px; --h: 2048px; --pad-x: 132px; --pad-y: 132px; --footer-y: 96px; --content-top: 260px; --title: 104px; --copy: 40px; --meta: 26px; --gap: 48px; --bullet-gap: 24px; --bullet-pad: 34px 40px; --radius: 38px; --title-width: 1220px; --body-width: 1180px; }
body.square { --w: 1800px; --h: 1800px; --pad-x: 120px; --pad-y: 110px; --footer-y: 88px; --content-top: 230px; --title: 98px; --copy: 38px; --meta: 25px; --gap: 44px; --bullet-gap: 22px; --bullet-pad: 32px 38px; --radius: 34px; --title-width: 1240px; --body-width: 1120px; }
body.story { --w: 1080px; --h: 1920px; --pad-x: 76px; --pad-y: 96px; --footer-y: 80px; --content-top: 230px; --title: 78px; --copy: 32px; --meta: 21px; --gap: 38px; --bullet-gap: 20px; --bullet-pad: 28px 30px; --radius: 30px; --title-width: 880px; --body-width: 860px; }
"""


def css_for_style(style: dict) -> str:
    colors = style["colors"]
    typography = style["typography"]
    slides = style.get("slides", {})
    replacements = {
        "__PRIMARY__": colors["primary"],
        "__INK__": colors["ink"],
        "__BODY__": colors["body"],
        "__MUTED__": colors["muted"],
        "__LINE__": colors["line"],
        "__SURFACE__": colors["surface"],
        "__BACKGROUND__": colors["background"],
        "__DISPLAY_FONT__": typography.get("display", "Arial"),
        "__BODY_FONT__": typography.get("body", "Arial"),
        "__MONO_FONT__": typography.get("mono", "Courier New"),
        "__CARD_RADIUS__": str(slides.get("card_radius", 24)),
        "__HEADLINE_WEIGHT__": str(slides.get("headline_weight", 500)),
    }
    css = BASE_CSS
    for key, value in replacements.items():
        css = css.replace(key, value)
    return css


def render_slide(deck_title: str, slide: dict[str, object], index: int, total: int) -> str:
    title = html.escape(str(slide.get("title", ""))).replace("AI", "<span class='blue'>AI</span>")
    return f"""
<section class="slide" id="slide-{index:02d}">
  <div class="header">
    <div class="kicker"><span class="dot"></span>{html.escape(deck_title)}</div>
    <div>{index:02d} / {total:02d}</div>
  </div>
  <main class="content">
    <h1 class="title">{title}</h1>
    <div class="body">{slide_body(slide)}</div>
  </main>
  <div class="footer">
    <span>MD Export Suite</span>
    <span>designed from markdown</span>
  </div>
</section>
"""


def render_html(deck_title: str, slides: list[dict[str, object]], aspect_class: str, css: str, single: int | None = None) -> str:
    selected = [slides[single]] if single is not None else slides
    start = single + 1 if single is not None else 1
    body_class = f"{aspect_class} {'single' if single is not None else 'deck'}"
    slide_html = "\n".join(
        render_slide(deck_title, slide, start + idx, len(slides)) for idx, slide in enumerate(selected)
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(deck_title)}</title>
  <style>{css}</style>
</head>
<body class="{body_class}">
  <div class="deck-wrap">{slide_html}</div>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Render Markdown into fixed-canvas HTML slides.")
    parser.add_argument("input", help="Input Markdown file.")
    parser.add_argument("--output-dir", "-o", required=True, help="Output directory.")
    parser.add_argument("--aspect", default="16:9", choices=ASPECTS.keys())
    parser.add_argument("--style", default=None, help="Generic style ID. Defaults to frontmatter style or institutional-clarity.")
    args = parser.parse_args()

    meta, markdown = strip_frontmatter(expand_includes(Path(args.input)))
    deck_title, slides = parse_slides(markdown)
    deck_title = meta.get("title", deck_title)
    style_id = args.style or meta.get("style", "institutional-clarity")
    style = load_style(style_id)
    css = css_for_style(style)
    _, _, aspect_class = ASPECTS[args.aspect]

    out = Path(args.output_dir)
    slides_dir = out / "slides-html"
    slides_dir.mkdir(parents=True, exist_ok=True)
    (out / "deck.html").write_text(render_html(deck_title, slides, aspect_class, css), encoding="utf-8")
    for idx in range(len(slides)):
        (slides_dir / f"slide-{idx+1:02d}.html").write_text(
            render_html(deck_title, slides, aspect_class, css, idx),
            encoding="utf-8",
        )
    print(f"Generated {len(slides)} HTML slides in {out} using style {style_id}")


if __name__ == "__main__":
    main()
