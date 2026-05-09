#!/usr/bin/env python3
"""Normalize Markdown before DOCX/PDF export."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


UNDERLINE_RE = re.compile(r"^_{5,}\s*$")
INCLUDE_RE = re.compile(r"^\s*\{\{\s*include:\s*([^}]+?)\s*\}\}\s*$")


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


def normalize(text: str, worksheet_lines: bool = False) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    out: list[str] = []
    blank_count = 0

    for raw in lines:
        line = raw.rstrip()

        if worksheet_lines and UNDERLINE_RE.match(line):
            line = '<span class="writing-line">&nbsp;</span>'

        if not line:
            blank_count += 1
            if blank_count <= 2:
                out.append("")
            continue

        blank_count = 0

        # Keep checkbox Markdown portable for Pandoc and Word.
        line = line.replace("- [ ]", "- ☐")
        line = line.replace("- [x]", "- ☑")
        line = line.replace("- [X]", "- ☑")

        # Avoid accidental multiple H1s in document exports by demoting
        # subsequent H1 headings after the first visible title.
        if line.startswith("# "):
            h1_seen = any(existing.startswith("# ") for existing in out)
            if h1_seen:
                line = "#" + line

        out.append(line)

    result = "\n".join(out).strip() + "\n"
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize Markdown for export.")
    parser.add_argument("input", help="Input Markdown file.")
    parser.add_argument("--output", "-o", help="Output Markdown file. Defaults to stdout.")
    parser.add_argument(
        "--worksheet-lines",
        action="store_true",
        help="Convert underscore-only writing lines into stable spans.",
    )
    args = parser.parse_args()

    source = Path(args.input)
    result = normalize(expand_includes(source), worksheet_lines=args.worksheet_lines)

    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(result, encoding="utf-8")
        print(output)
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
