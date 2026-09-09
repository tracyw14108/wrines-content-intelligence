# Baseline Rules

## Core principle

Every account is compared with itself, not with larger or smaller accounts.

## Default windows

- Weekly scan: latest 7 days.
- Baseline reference: previous 28 days when enough data is available.
- Initial baseline may use the best available 60–90 day sample until rolling data accumulates.

## Reels

Preferred baseline: median Views for recent Reels.

Fallback order when Views are unavailable/unreliable:
1. Engagement median
2. Comments
3. Reposts / shares where available

## Carousel / Photo

Preferred baseline: median Engagement for the same format.

Engagement should use the fields actually provided by the source. Do not invent missing likes, saves or shares.

## Long-tail accounts

If one account has extreme viral outliers, do not use a simple average as its primary baseline. Median and topic-specific breakout analysis are preferred.

## Paid content

`is_promoted=true` or other paid evidence must be stored separately. A paid breakout can be a **Topic Signal**, but cannot be called an Organic Winner.

## Data-quality statuses

- `confirmed`: enough usable data for a numeric baseline.
- `provisional`: sample is still small.
- `long_tail`: extreme outliers require special interpretation.
- `content_signal`: useful content examples exist but baseline is not yet stable.
- `data_incomplete`: connector fields are known to be unreliable/missing.

## Update rule

Never overwrite historical baselines without versioning. Add a new baseline file when the reference distribution changes materially.
