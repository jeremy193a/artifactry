#!/usr/bin/env python3
"""Build Artifactry showcase outputs across every bundled style."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "artifactry"
STYLE_INDEX = SKILL / "styles" / "style_index.json"
CAROUSEL_MD = ROOT / "examples" / "showcase" / "artifactry-carousel.md"
README_MD = ROOT / "README.md"
ASSETS_DIR = ROOT / "assets" / "showcase" / "styles"
BUILD_DIR = ROOT / "build" / "showcase"
OUTPUT_DIR = ROOT / "output" / "showcase"


def run(cmd: list[str]) -> None:
    print(" ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=ROOT, check=True)


def style_ids() -> list[str]:
    return [item["id"] for item in json.loads(STYLE_INDEX.read_text(encoding="utf-8"))]


def build_carousel(style: str, aspect: str) -> None:
    html_dir = BUILD_DIR / "styles" / style
    image_dir = ASSETS_DIR / style
    pptx_path = OUTPUT_DIR / "pptx" / f"artifactry-{style}.pptx"

    run(
        [
            sys.executable,
            str(SKILL / "scripts" / "render_html_deck.py"),
            str(CAROUSEL_MD),
            "--aspect",
            aspect,
            "--style",
            style,
            "--output-dir",
            str(html_dir),
        ]
    )
    run(
        [
            sys.executable,
            str(SKILL / "scripts" / "render_images_chrome.py"),
            str(html_dir / "slides-html"),
            "--aspect",
            aspect,
            "--output-dir",
            str(image_dir),
        ]
    )
    run(
        [
            sys.executable,
            str(SKILL / "scripts" / "build_pptx_from_images.py"),
            str(image_dir),
            "--aspect",
            aspect,
            "--output",
            str(pptx_path),
        ]
    )


def build_docx(style: str) -> None:
    reference = BUILD_DIR / "docx" / f"reference-{style}.docx"
    output = OUTPUT_DIR / "docx" / f"artifactry-readme-{style}.docx"

    run(
        [
            sys.executable,
            str(SKILL / "scripts" / "build_reference_docx.py"),
            "--output",
            str(reference),
            "--company",
            "Artifactry",
            "--style",
            style,
        ]
    )
    run(
        [
            "pandoc",
            str(README_MD),
            "--from=markdown",
            "--to=docx",
            f"--reference-doc={reference}",
            "--output",
            str(output),
        ]
    )


def validate(styles: list[str]) -> None:
    paths = [str(ASSETS_DIR / style) for style in styles]
    paths.extend([str(OUTPUT_DIR / "docx"), str(OUTPUT_DIR / "pptx")])
    run([sys.executable, str(SKILL / "scripts" / "validate_exports.py"), *paths])


def main() -> None:
    parser = argparse.ArgumentParser(description="Build DOCX, PNG, and PPTX showcase outputs.")
    parser.add_argument("--aspect", default="4:5", choices=["16:9", "4:5", "1:1", "9:16"])
    parser.add_argument("--styles", nargs="*", default=style_ids(), help="Style IDs to build. Defaults to all.")
    parser.add_argument("--skip-docx", action="store_true")
    parser.add_argument("--skip-carousel", action="store_true")
    args = parser.parse_args()

    for style in args.styles:
        if not args.skip_carousel:
            build_carousel(style, args.aspect)
        if not args.skip_docx:
            build_docx(style)

    validate(args.styles)


if __name__ == "__main__":
    main()
