#!/usr/bin/env python3
"""Normalize exported RAW_POSTS CSV into a stable schema.

Uses only Python standard library.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

FIELDS = [
    "CapturedAt", "Category", "Account", "PostID", "PublishedAt", "Type",
    "Views", "Likes", "Comments", "Reposts", "Permalink", "Caption",
    "Source", "Promoted", "DataQuality",
]

NUMERIC_FIELDS = {"Views", "Likes", "Comments", "Reposts"}


def clean_number(value: str) -> str:
    value = (value or "").strip().replace(",", "")
    if not value:
        return ""
    try:
        return str(float(value)).rstrip("0").rstrip(".")
    except ValueError:
        return ""


def normalize_row(row: dict[str, str]) -> dict[str, str]:
    out = {field: (row.get(field) or "").strip() for field in FIELDS}
    for field in NUMERIC_FIELDS:
        out[field] = clean_number(out[field])
    if not out["DataQuality"]:
        out["DataQuality"] = "ok"
    if not out["Promoted"]:
        out["Promoted"] = "unknown"
    return out


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python scripts/normalize_posts.py INPUT.csv OUTPUT.csv", file=sys.stderr)
        return 2
    src, dst = map(Path, sys.argv[1:])
    dst.parent.mkdir(parents=True, exist_ok=True)
    with src.open("r", encoding="utf-8-sig", newline="") as f_in, dst.open("w", encoding="utf-8", newline="") as f_out:
        reader = csv.DictReader(f_in)
        writer = csv.DictWriter(f_out, fieldnames=FIELDS)
        writer.writeheader()
        for row in reader:
            writer.writerow(normalize_row(row))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
