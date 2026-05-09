#!/usr/bin/env python3
"""Resolve public style-guide IDs to deterministic token styles."""

from __future__ import annotations

import json
from pathlib import Path


STYLE_DIR = Path(__file__).resolve().parents[1] / "styles"

STYLE_ALIASES = {
    "regulated-ledger": "institutional-clarity",
    "human-workshop": "warm-editorial",
    "swiss-protocol": "monochrome-precision",
    "terminal-operator": "dark-console",
    "aurora-product": "gradient-intelligence",
    "metrics-command": "data-command",
    "broadsheet-intelligence": "broadsheet-analysis",
    "black-label-cinema": "cinematic-luxury",
    "playful-systems": "playful-productivity",
    "image-market": "visual-lifestyle",
    "spatial-canvas": "playful-productivity",
    "blueprint-infra": "dark-console",
    "commerce-editorial": "warm-editorial",
    "motion-premiere": "cinematic-luxury",
    "performance-machine": "cinematic-luxury",
}


def token_style_id(style_id: str) -> str:
    return STYLE_ALIASES.get(style_id, style_id)


def style_choices() -> str:
    token_ids = sorted(p.stem for p in STYLE_DIR.glob("*.json") if p.name != "style_index.json")
    guide_ids = sorted(STYLE_ALIASES)
    return ", ".join([*guide_ids, *token_ids])


def load_style(style_id: str) -> tuple[dict, str]:
    resolved = token_style_id(style_id)
    path = STYLE_DIR / f"{resolved}.json"
    if not path.exists():
        raise SystemExit(f"Unknown style '{style_id}'. Available styles: {style_choices()}")
    return json.loads(path.read_text(encoding="utf-8")), resolved
