#!/usr/bin/env python3
"""Crawl and organize the getdesign.md DESIGN.md corpus.

The public getdesign.md directory is backed by VoltAgent/awesome-design-md.
This script keeps that raw corpus in .work/ and creates an ordered local
working copy grouped by the collection categories from the upstream README.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


REPO_URL = "https://github.com/VoltAgent/awesome-design-md.git"
ROOT = Path(__file__).resolve().parents[1]
WORK_ROOT = ROOT / ".work" / "getdesign-md"
SOURCE_DIR = WORK_ROOT / "source"
ORGANIZED_DIR = WORK_ROOT / "organized"


def run(cmd: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(
        cmd,
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def slugify(value: str) -> str:
    slug = value.lower()
    slug = slug.replace("&", "and")
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def sync_source(refresh: bool) -> None:
    WORK_ROOT.mkdir(parents=True, exist_ok=True)
    if not (SOURCE_DIR / ".git").exists():
        run(["git", "clone", "--depth", "1", REPO_URL, str(SOURCE_DIR)])
        return
    if refresh:
        run(["git", "fetch", "--depth", "1", "origin", "main"], cwd=SOURCE_DIR)
        run(["git", "reset", "--hard", "origin/main"], cwd=SOURCE_DIR)


def parse_collection(readme: Path) -> list[dict[str, object]]:
    categories: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    in_collection = False
    item_pattern = re.compile(
        r"^- \[\*\*(?P<name>.+?)\*\*\]\(https://getdesign\.md/(?P<slug>[^/]+)/design-md\) - (?P<description>.+)$"
    )

    for line in readme.read_text(encoding="utf-8").splitlines():
        if line.strip() == "## Collection":
            in_collection = True
            continue
        if in_collection and line.startswith("## "):
            break
        if not in_collection:
            continue
        if line.startswith("### "):
            title = line.removeprefix("### ").strip()
            current = {
                "title": title,
                "slug": slugify(title),
                "entries": [],
            }
            categories.append(current)
            continue
        if current is None:
            continue
        match = item_pattern.match(line.strip())
        if not match:
            continue
        current["entries"].append(
            {
                "name": match.group("name"),
                "slug": match.group("slug"),
                "description": match.group("description"),
            }
        )

    return categories


def copy_entry(slug: str, target: Path) -> bool:
    source = SOURCE_DIR / "design-md" / slug
    design = source / "DESIGN.md"
    if not design.exists():
        return False

    target.mkdir(parents=True, exist_ok=True)
    shutil.copy2(design, target / "DESIGN.md")
    readme = source / "README.md"
    if readme.exists():
        shutil.copy2(readme, target / "README.md")
    return True


def organize(categories: list[dict[str, object]]) -> dict[str, object]:
    if ORGANIZED_DIR.exists():
        shutil.rmtree(ORGANIZED_DIR)
    ORGANIZED_DIR.mkdir(parents=True)

    used_slugs: set[str] = set()
    index_categories: list[dict[str, object]] = []
    missing: list[dict[str, str]] = []

    for category_index, category in enumerate(categories, start=1):
        category_dir = ORGANIZED_DIR / f"{category_index:02d}-{category['slug']}"
        category_dir.mkdir(parents=True)
        organized_entries = []

        entries = category["entries"]
        assert isinstance(entries, list)
        for item_index, item in enumerate(entries, start=1):
            slug = str(item["slug"])
            entry_dir = category_dir / f"{item_index:02d}-{slug}"
            found = copy_entry(slug, entry_dir)
            used_slugs.add(slug)
            entry = {
                "name": item["name"],
                "slug": slug,
                "description": item["description"],
                "source_url": f"https://getdesign.md/{slug}/design-md",
                "organized_path": str(entry_dir.relative_to(WORK_ROOT)),
                "status": "present" if found else "missing-in-source",
            }
            organized_entries.append(entry)
            if not found:
                missing.append(entry)

        index_categories.append(
            {
                "title": category["title"],
                "slug": category["slug"],
                "count": len(organized_entries),
                "entries": organized_entries,
            }
        )

    source_slugs = sorted(
        path.parent.name for path in (SOURCE_DIR / "design-md").glob("*/DESIGN.md")
    )
    uncategorized_slugs = [slug for slug in source_slugs if slug not in used_slugs]
    uncategorized_entries = []
    if uncategorized_slugs:
        category_dir = ORGANIZED_DIR / "99-uncategorized"
        for item_index, slug in enumerate(uncategorized_slugs, start=1):
            entry_dir = category_dir / f"{item_index:02d}-{slug}"
            copy_entry(slug, entry_dir)
            uncategorized_entries.append(
                {
                    "name": slug,
                    "slug": slug,
                    "description": "Present in upstream source but not listed in the getdesign.md category order.",
                    "source_url": f"https://getdesign.md/{slug}/design-md",
                    "organized_path": str(entry_dir.relative_to(WORK_ROOT)),
                    "status": "uncategorized",
                }
            )
        index_categories.append(
            {
                "title": "Uncategorized",
                "slug": "uncategorized",
                "count": len(uncategorized_entries),
                "entries": uncategorized_entries,
            }
        )

    commit = run(["git", "rev-parse", "HEAD"], cwd=SOURCE_DIR)
    index = {
        "source": "getdesign.md via VoltAgent/awesome-design-md",
        "repo_url": REPO_URL,
        "source_commit": commit,
        "crawled_at": datetime.now(timezone.utc).isoformat(),
        "organized_dir": str(ORGANIZED_DIR.relative_to(ROOT)),
        "source_design_count": len(source_slugs),
        "categorized_count": sum(
            1
            for category in index_categories
            for entry in category["entries"]
            if entry["status"] == "present"
        ),
        "missing_count": len(missing),
        "uncategorized_count": len(uncategorized_entries),
        "categories": index_categories,
    }

    (WORK_ROOT / "index.json").write_text(
        json.dumps(index, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    write_markdown_index(index)
    return index


def write_markdown_index(index: dict[str, object]) -> None:
    lines = [
        "# getdesign.md Working Corpus",
        "",
        f"- Source: {index['source']}",
        f"- Repo: {index['repo_url']}",
        f"- Commit: `{index['source_commit']}`",
        f"- Source DESIGN.md files: {index['source_design_count']}",
        f"- Categorized files: {index['categorized_count']}",
        f"- Missing from source: {index['missing_count']}",
        f"- Uncategorized source files: {index['uncategorized_count']}",
        "",
    ]
    categories = index["categories"]
    assert isinstance(categories, list)
    for category in categories:
        lines.append(f"## {category['title']}")
        lines.append("")
        for entry in category["entries"]:
            status = "" if entry["status"] == "present" else f" [{entry['status']}]"
            lines.append(
                f"- {entry['name']} (`{entry['slug']}`){status}: {entry['description']}"
            )
        lines.append("")

    (WORK_ROOT / "index.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Fetch the latest upstream main before organizing.",
    )
    args = parser.parse_args()

    sync_source(refresh=args.refresh)
    categories = parse_collection(SOURCE_DIR / "README.md")
    index = organize(categories)
    print(
        "Organized "
        f"{index['categorized_count']} categorized DESIGN.md files "
        f"from {index['source_design_count']} source files into {ORGANIZED_DIR}"
    )
    if index["missing_count"] or index["uncategorized_count"]:
        print(
            f"Notes: {index['missing_count']} missing, "
            f"{index['uncategorized_count']} uncategorized. See {WORK_ROOT / 'index.md'}"
        )


if __name__ == "__main__":
    main()
