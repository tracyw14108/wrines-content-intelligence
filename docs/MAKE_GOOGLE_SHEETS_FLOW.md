# Make + Google Sheets Flow

## Current operational database

Google Sheet: `W.RINES Content Intelligence`

Sheets:
- `RAW_POSTS`
- `ACCOUNT_BASELINE`
- `WEEKLY_WINNERS`
- `PATTERN_LIBRARY`
- `CONTENT_IDEAS`

## Current Make role

The Make scenario collects the latest data from W.RINES / public IG sources and writes operational data into Google Sheets. Sociality remains the preferred source for competitor promoted/organic interpretation and any fields that public Instagram APIs do not expose reliably.

## Intended weekly loop

```text
1. Collect latest posts
2. Normalize fields
3. Write/update RAW_POSTS
4. Read account baseline
5. Calculate Performance Multiple
6. Flag Normal / Watch / Winner / Breakout
7. Human/AI review of Hook, Pattern, CTA and W.RINES angle
8. Archive weekly snapshot to GitHub
9. Update Pattern Library only when evidence is meaningful
```

## Google Sheet -> GitHub handoff

Recommended snapshot columns:

```text
CapturedAt,Category,Account,PostID,PublishedAt,Type,Views,Likes,Comments,Reposts,Permalink,Caption,Source,Promoted,DataQuality
```

Save weekly exports to:

```text
data/weekly-snapshots/YYYY-MM-DD.csv
```

The GitHub scripts can then generate a versioned Winner report.

## Safety / data quality

- Do not commit credentials, tokens or private API responses.
- Do not infer `Promoted=false` when the source did not provide a promoted flag; store `unknown`.
- Preserve missing values as blank/null, not zero.
