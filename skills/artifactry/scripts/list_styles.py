#!/usr/bin/env python3
"""List available Artifactry style guides and token fallbacks."""

from __future__ import annotations

import json
from pathlib import Path


STYLE_INDEX = Path(__file__).resolve().parents[1] / "styles" / "style_index.json"
STYLE_GUIDES = Path(__file__).resolve().parents[1] / "references" / "style-guides"


def main() -> None:
    guide_files = sorted(p for p in STYLE_GUIDES.glob("*.md") if p.name != "INDEX.md")
    if guide_files:
        print("Creative style guides")
        print("---------------------")
        for guide in guide_files:
            title = guide.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
            print(f"{title} ({guide.stem})")
            print(f"  {guide.relative_to(Path(__file__).resolve().parents[1])}")
        print()

    print("Deterministic token fallbacks")
    print("-----------------------------")
    styles = json.loads(STYLE_INDEX.read_text(encoding="utf-8"))
    for style in styles:
        print(f"{style['name']} ({style['id']})")
        print(f"  {style['summary']}")
        print(f"  Best for: {', '.join(style['best_for'])}")


if __name__ == "__main__":
    main()
