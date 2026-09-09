#!/usr/bin/env python3
"""Build a Markdown Winner report from the newest weekly snapshot CSV."""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

from winner_detection import score

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_DIR = ROOT / "data" / "weekly-snapshots"
WINNER_DIR = ROOT / "data" / "winners"


def to_float(value: str | None) -> float | None:
    if value is None:
        return None
    value = value.strip().replace(",", "")
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def newest_snapshot() -> Path | None:
    files = sorted(SNAPSHOT_DIR.glob("*.csv"))
    return files[-1] if files else None


def main() -> int:
    snapshot = newest_snapshot()
    if snapshot is None:
        print("No weekly snapshot found; nothing to report.")
        return 0

    rows = []
    with snapshot.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            views = to_float(row.get("Views"))
            likes = to_float(row.get("Likes")) or 0
            comments = to_float(row.get("Comments")) or 0
            reposts = to_float(row.get("Reposts")) or 0
            engagement = likes + comments + reposts
            result = score(row.get("Account", ""), views=views, engagement=engagement)
            result.update({
                "published": row.get("PublishedAt", ""),
                "type": row.get("Type", ""),
                "permalink": row.get("Permalink", ""),
                "promoted": row.get("Promoted", "unknown") or "unknown",
                "data_quality": row.get("DataQuality", "ok") or "ok",
            })
            rows.append(result)

    rank = {"Breakout": 4, "Winner": 3, "Watch": 2, "Normal": 1, "Unscored": 0}
    rows.sort(key=lambda r: (rank.get(r.get("label", "Unscored"), 0), r.get("multiple") or 0), reverse=True)

    report_date = snapshot.stem
    out = WINNER_DIR / f"{report_date}.md"
    WINNER_DIR.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# Weekly Winner Report — {report_date}",
        "",
        f"Source snapshot: `{snapshot.relative_to(ROOT)}`",
        "",
        "| Label | Account | Metric | Multiple | Promoted | Data quality | Link |",
        "|---|---|---|---:|---|---|---|",
    ]
    for r in rows:
        multiple = "" if r.get("multiple") is None else f"{r['multiple']:.2f}×"
        link = r.get("permalink") or ""
        lines.append(
            f"| {r.get('label','Unscored')} | @{r.get('account','')} | {r.get('metric','')} | {multiple} | {r.get('promoted','unknown')} | {r.get('data_quality','')} | {link} |"
        )

    lines += [
        "",
        "## Interpretation rules",
        "",
        "- Promoted/paid posts are topic signals, not organic winners.",
        "- Data-incomplete rows must not be interpreted as true zero performance.",
        "- Final Hook/Pattern/W.RINES translation review should be added after reading the content context.",
        "",
    ]

    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
