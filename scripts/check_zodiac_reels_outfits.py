#!/usr/bin/env python3
"""Hard quality gate for distinctive daily 12-sign fashion Reels.

Usage: python scripts/check_zodiac_reels_outfits.py
Add each proposed look to the ledger before rendering. Exit 1 = reject.
"""
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "config" / "zodiac-reels-outfit-policy.json"
LOOKS = ROOT / "data" / "zodiac-reels" / "outfits.json"
REQUIRED = ("date", "sign", "top_id", "top_category", "top_silhouette",
            "bottom_id", "bottom_category", "bottom_silhouette")

def norm(value):
    return "".join(str(value or "").strip().lower().split())

def style(row, side):
    return (norm(row[f"{side}_category"]), norm(row[f"{side}_silhouette"]))

def reject(errors, description):
    errors.append(description)

def main():
    policy = json.loads(RULES.read_text(encoding="utf-8"))
    looks = json.loads(LOOKS.read_text(encoding="utf-8"))
    if not isinstance(looks, list):
        raise SystemExit("outfits.json must contain an array")

    errors = []
    parsed = []
    for idx, row in enumerate(looks, 1):
        missing = [key for key in REQUIRED if not norm(row.get(key))]
        if missing:
            reject(errors, f"record {idx}: missing {', '.join(missing)}")
            continue
        try:
            day = dt.date.fromisoformat(row["date"])
        except (ValueError, TypeError):
            reject(errors, f"record {idx}: invalid date {row.get('date')}")
            continue
        parsed.append((day, row))
    parsed.sort(key=lambda item: (item[0], item[1]["sign"]))
    seen_keys = set()
    seen_combo = {}
    prior = []
    controls = policy["rules"]
    lookback = int(controls["same_sign_full_top_and_bottom_piece_id_cooldown_days"])
    shape_days = int(controls["same_sign_top_or_bottom_category_and_silhouette_cooldown_days"])
    for day, row in parsed:
        sign = norm(row["sign"])
        label = f"{day} {row['sign']}"
        same_key = (day, sign)
        if same_key in seen_keys:
            reject(errors, f"{label}: duplicate date + sign")
        seen_keys.add(same_key)
        top = norm(row["top_id"]); bottom = norm(row["bottom_id"])
        top_style = style(row, "top"); bottom_style = style(row, "bottom")
        signature = (top_style, bottom_style, norm(row.get("outerwear")))
        if signature in seen_combo:
            reject(errors, f"{label}: entire garment-style combination repeated from {seen_combo[signature]}")
        else:
            seen_combo[signature] = label
        for pday, prow in prior:
            gap = (day - pday).days
            psign = norm(prow["sign"])
            if gap == 0:
                if top == norm(prow["top_id"]):
                    reject(errors, f"{label}: same-day duplicate top across signs ({prow['sign']})")
                if bottom == norm(prow["bottom_id"]):
                    reject(errors, f"{label}: same-day duplicate bottom across signs ({prow['sign']})")
            if psign != sign or gap < 0:
                continue
            if gap <= lookback:
                if top == norm(prow["top_id"]):
                    reject(errors, f"{label}: repeated top from {pday} (within {lookback} days)")
                if bottom == norm(prow["bottom_id"]):
                    reject(errors, f"{label}: repeated bottom from {pday} (within {lookback} days)")
            if gap <= shape_days:
                if top_style == style(prow, "top"):
                    reject(errors, f"{label}: same top category/silhouette as {pday}; color changes do not count")
                if bottom_style == style(prow, "bottom"):
                    reject(errors, f"{label}: same bottom category/silhouette as {pday}; color changes do not count")
        prior.append((day, row))
    if errors:
        for problem in errors:
            print("REJECT:", problem, file=sys.stderr)
        print(f"{len(errors)} duplicate/missing-style violations found", file=sys.stderr)
        raise SystemExit(1)
    print(f"PASS: {len(parsed)} zodiac Reels looks; distinct tops, bottoms and garment-style combinations")

if __name__ == "__main__":
    main()
