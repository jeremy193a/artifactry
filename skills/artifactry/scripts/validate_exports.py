#!/usr/bin/env python3
"""Validate exported DOCX, PPTX, PDF, PNG, JPG, or directories."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from zipfile import BadZipFile, ZipFile


def validate_docx(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        with ZipFile(path) as z:
            names = set(z.namelist())
            if "word/document.xml" not in names:
                errors.append("missing word/document.xml")
            if "word/styles.xml" not in names:
                errors.append("missing word/styles.xml")
    except BadZipFile:
        errors.append("not a valid docx zip")
    return errors


def validate_pptx(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        with ZipFile(path) as z:
            names = z.namelist()
            slide_files = [n for n in names if n.startswith("ppt/slides/slide") and n.endswith(".xml")]
            if not slide_files:
                errors.append("no slides found")
            if "[Content_Types].xml" not in names:
                errors.append("missing content types")
    except BadZipFile:
        errors.append("not a valid pptx zip")
    return errors


def validate_pdf(path: Path) -> list[str]:
    data = path.read_bytes()[:5]
    return [] if data == b"%PDF-" else ["missing PDF header"]


def validate_image(path: Path) -> list[str]:
    try:
        from PIL import Image

        with Image.open(path) as image:
            image.verify()
        return []
    except Exception as exc:
        return [f"invalid image: {exc}"]


def validate_path(path: Path) -> list[str]:
    if not path.exists():
        return ["missing"]
    if path.is_file() and path.stat().st_size == 0:
        return ["zero-byte file"]
    if path.is_dir():
        files = [p for p in path.iterdir() if p.is_file()]
        if not files:
            return ["empty directory"]
        errors = []
        for file in files:
            errors.extend(f"{file.name}: {err}" for err in validate_path(file))
        return errors

    suffix = path.suffix.lower()
    if suffix == ".docx":
        return validate_docx(path)
    if suffix == ".pptx":
        return validate_pptx(path)
    if suffix == ".pdf":
        return validate_pdf(path)
    if suffix in {".png", ".jpg", ".jpeg"}:
        return validate_image(path)
    return []


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate exported files.")
    parser.add_argument("paths", nargs="+", help="Files or directories to validate.")
    args = parser.parse_args()

    failed = False
    for raw in args.paths:
        path = Path(raw)
        errors = validate_path(path)
        if errors:
            failed = True
            print(f"FAIL {path}")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"OK   {path}")

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
