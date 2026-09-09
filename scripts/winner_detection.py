#!/usr/bin/env python3
"""Winner classification helpers for W.RINES Content Intelligence."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASELINE_FILE = ROOT / "data" / "baselines" / "baseline_v1.json"


def load_baselines(path: Path = BASELINE_FILE) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)["accounts"]


def classify_multiple(multiple: float | None) -> str:
    if multiple is None:
        return "Unscored"
    if multiple >= 5:
        return "Breakout"
    if multiple >= 3:
        return "Winner"
    if multiple >= 2:
        return "Watch"
    return "Normal"


def score(account: str, views: float | None = None, engagement: float | None = None) -> dict[str, Any]:
    baseline = load_baselines().get(account)
    if not baseline:
        return {"account": account, "label": "Unscored", "reason": "baseline_missing"}

    metric = baseline.get("metric")
    base = baseline.get("median")
    status = baseline.get("status")

    if not base:
        return {
            "account": account,
            "label": "Unscored",
            "reason": f"baseline_status:{status}",
            "metric": metric,
        }

    value = views if metric == "views" else engagement
    if value is None:
        return {"account": account, "label": "Unscored", "reason": f"missing_{metric}"}

    multiple = value / float(base)
    return {
        "account": account,
        "metric": metric,
        "value": value,
        "baseline": base,
        "multiple": round(multiple, 3),
        "label": classify_multiple(multiple),
        "baseline_status": status,
    }


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("account")
    p.add_argument("--views", type=float)
    p.add_argument("--engagement", type=float)
    args = p.parse_args()
    print(json.dumps(score(args.account, args.views, args.engagement), ensure_ascii=False, indent=2))
