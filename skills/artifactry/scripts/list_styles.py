#!/usr/bin/env python3
"""List available generic export styles."""

from __future__ import annotations

import json
from pathlib import Path


STYLE_INDEX = Path(__file__).resolve().parents[1] / "styles" / "style_index.json"


def main() -> None:
    styles = json.loads(STYLE_INDEX.read_text(encoding="utf-8"))
    for style in styles:
        print(f"{style['name']} ({style['id']})")
        print(f"  {style['summary']}")
        print(f"  Best for: {', '.join(style['best_for'])}")


if __name__ == "__main__":
    main()
