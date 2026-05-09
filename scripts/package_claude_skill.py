#!/usr/bin/env python3
"""Package artifactry as a Claude Chat custom Skill ZIP."""

from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "artifactry"
DIST = ROOT / "dist"
ZIP_PATH = DIST / "artifactry.zip"


def main() -> None:
    DIST.mkdir(parents=True, exist_ok=True)
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()

    with ZipFile(ZIP_PATH, "w", ZIP_DEFLATED) as zf:
        for path in sorted(SKILL_DIR.rglob("*")):
            if path.is_dir():
                continue
            if "__pycache__" in path.parts:
                continue
            if path.name == ".DS_Store" or path.suffix == ".pyc":
                continue
            arcname = Path(SKILL_DIR.name) / path.relative_to(SKILL_DIR)
            zf.write(path, arcname)

    print(ZIP_PATH)


if __name__ == "__main__":
    main()
