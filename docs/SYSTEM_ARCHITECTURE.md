# System Architecture

## Goal

Build a repeatable decision system that answers:

> What content is the market reacting to, and what can W.RINES answer from its own point of view?

## Data flow

```text
Metricool ---------> W.RINES owned performance
Sociality.io ------> competitor public posts/stats + promoted flags
Instagram API -----> public post backup where available
        \            /
         \          /
           Make
            |
            v
     Google Sheets (operational database)
            |
            v
     GitHub (versioned intelligence layer)
            |
            +--> baselines
            +--> weekly snapshots
            +--> winner reports
            +--> pattern library
            +--> content ideas
```

## Responsibilities

### Metricool
Use for W.RINES owned account metrics that public competitor APIs cannot provide reliably: reach, 3-second view rate, average watch, saves, shares, profile actions and similar owned-account data.

### Sociality.io
Use as the primary competitor intelligence source. It is especially important for:
- tracked-account stats
- recent public posts
- promoted/paid indication
- competitor content review

### Make
Automation/orchestration only. It should collect and move data; it should not silently become the source of truth for interpretation.

### Google Sheets
Operational database for daily inspection, sorting, notes and manual corrections.

### GitHub
Versioned source of truth for system rules, baselines, taxonomy, code and weekly archived snapshots.

## Data-quality rule

A zero returned by an external connector is not automatically a real zero. If an account is known to have incomplete metrics, mark the field/status as missing or unreliable.

## Privacy / copying rule

Do not copy competitor scripts verbatim. Store public metadata and abstract learnings. The reusable unit is the Pattern, not the competitor's wording.
