#!/usr/bin/env python3
"""Search local Artifactry reference patterns."""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus" / "export_patterns.json"


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9:]+", text.lower())


def load_docs() -> list[dict]:
    return json.loads(CORPUS.read_text(encoding="utf-8"))


def score(query_tokens: list[str], doc: dict, idf: dict[str, float]) -> float:
    haystack = " ".join(
        [
            doc.get("id", ""),
            doc.get("title", ""),
            doc.get("doctype", ""),
            " ".join(doc.get("outputs", [])),
            " ".join(doc.get("styles", [])),
            " ".join(doc.get("keywords", [])),
            doc.get("route", ""),
            doc.get("notes", ""),
        ]
    )
    counts = Counter(tokenize(haystack))
    total = sum(counts.values()) or 1
    value = 0.0
    for token in query_tokens:
        tf = counts[token] / total
        if counts[token]:
            value += (1.0 + math.log(1 + counts[token])) * idf.get(token, 1.0) + tf
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description="Search export reference patterns.")
    parser.add_argument("query", help="Search query, e.g. 'institutional clarity 16:9 presentation'")
    parser.add_argument("--limit", type=int, default=3, help="Number of results.")
    args = parser.parse_args()

    docs = load_docs()
    query_tokens = tokenize(args.query)
    doc_tokens = [set(tokenize(json.dumps(doc))) for doc in docs]
    idf = {}
    for token in set().union(*doc_tokens):
        containing = sum(1 for tokens in doc_tokens if token in tokens)
        idf[token] = math.log((1 + len(docs)) / (1 + containing)) + 1

    ranked = sorted(((score(query_tokens, doc, idf), doc) for doc in docs), reverse=True, key=lambda x: x[0])
    for rank, (value, doc) in enumerate(ranked[: args.limit], 1):
        print(f"{rank}. {doc['title']} [{doc['id']}] score={value:.3f}")
        print(f"   doctype: {doc['doctype']}")
        print(f"   outputs: {', '.join(doc['outputs'])}")
        print(f"   styles: {', '.join(doc['styles'])}")
        print(f"   route: {doc['route']}")
        print(f"   notes: {doc['notes']}")


if __name__ == "__main__":
    main()
