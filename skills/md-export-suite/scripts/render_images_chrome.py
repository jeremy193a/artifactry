#!/usr/bin/env python3
"""Render fixed-canvas slide HTML files to PNG or JPG using Chrome/Chromium."""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

from PIL import Image


ASPECT_PIXELS = {
    "16:9": (1920, 1080),
    "4:5": (1638, 2048),
    "1:1": (1800, 1800),
    "9:16": (1080, 1920),
}


CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome",
    "chromium",
    "chromium-browser",
]


def find_chrome(explicit: str | None) -> str:
    if explicit:
        return explicit
    for candidate in CHROME_CANDIDATES:
        if candidate.startswith("/") and Path(candidate).exists():
            return candidate
        if not candidate.startswith("/"):
            return candidate
    raise SystemExit("Chrome/Chromium not found. Pass --chrome /path/to/chrome.")


def render_one(chrome: str, html_file: Path, output: Path, width: int, height: int, image_format: str) -> None:
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = Path(tmp.name)

    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={width},{height + 120}",
        f"--screenshot={tmp_path}",
        html_file.resolve().as_uri(),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    with Image.open(tmp_path) as image:
        cropped = image.crop((0, 0, width, height))
        output.parent.mkdir(parents=True, exist_ok=True)
        if image_format in {"jpg", "jpeg"}:
            cropped.convert("RGB").save(output, quality=92, optimize=True)
        else:
            cropped.save(output)
    tmp_path.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render slide HTML files to images.")
    parser.add_argument("slides_dir", help="Directory containing slide-*.html files.")
    parser.add_argument("--output-dir", "-o", required=True, help="Output image directory.")
    parser.add_argument("--aspect", default="16:9", choices=ASPECT_PIXELS.keys())
    parser.add_argument("--format", default="png", choices=["png", "jpg", "jpeg"])
    parser.add_argument("--chrome", help="Path to Chrome/Chromium binary.")
    args = parser.parse_args()

    chrome = find_chrome(args.chrome)
    width, height = ASPECT_PIXELS[args.aspect]
    slides = sorted(Path(args.slides_dir).glob("slide-*.html"))
    if not slides:
        raise SystemExit(f"No slide-*.html files found in {args.slides_dir}")

    out = Path(args.output_dir)
    ext = "jpg" if args.format == "jpeg" else args.format
    for slide in slides:
        render_one(chrome, slide, out / f"{slide.stem}.{ext}", width, height, ext)
    print(f"Rendered {len(slides)} images to {out}")


if __name__ == "__main__":
    main()
