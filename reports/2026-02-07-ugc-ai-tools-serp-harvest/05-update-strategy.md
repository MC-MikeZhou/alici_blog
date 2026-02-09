# Update Strategy (UGC AI Tools SERP Harvest)

> Generated: `2026-02-07T03:37:49Z` | Market: US + EN | Cadence: Biweekly

This strategy turns SERP evidence into a repeatable refresh process for listicles and guides.

## Biweekly Runbook (Fixed Actions)

1. Re-run the harvest script with the same `00-mission-config.json`.
2. Compare outputs vs last run:
   - Query metrics delta (volume/CPC/competition).
   - SERP feature delta (AI Overview / PAA appearing or disappearing).
   - New URLs entering Top20 (strong targets) and URLs dropping out.
3. Record a delta summary and decide update level (L1/L2/L3).

## Trigger Rules (Hard Gates)

- **Primary keyword decay**: if the primary keyword’s `search_volume` drops by >=30% for 2 consecutive runs, trigger a primary-keyword re-selection.
- **Intent drift**: if SERP Top10 shifts from listicle to definition/how-to majority, switch title formula and restructure plan for the next version.
- **AIO/PAA concentration**: if AIO appears and PAA questions cluster on a specific sub-intent, upgrade that sub-intent into a new page or rewrite the FAQ to match PAA phrasing.

## Update Levels (Operational)

- **L1 (30 min)**: update pricing links, tool list, disclosures, and freshness date.
- **L2 (2-3 hours)**: rewrite Quick Answer, strengthen tables for extraction, replace FAQ with PAA-style questions.
- **L3 (1 day)**: change primary keyword, rewrite title/slug, reorder tool pool, possibly expand list size; re-run validator + AEO scoring.

## Compatibility Note (Listicle Validator)

- Do NOT add extra H2 sections into the article body for `standard` profile listicles.
- Keep update strategy as a separate file (`08-update-strategy.md`) unless switching to `mega` profile where an in-article update module is allowed.

## Current Evidence Snapshot

- Queries generated: **40** (max 40)
- Queries passing volume gate: **23**
- SERP calls made: **23**
- Kept candidate URLs: **179**

## Where to Look

- `01-query-universe.json`: validated demand per query
- `02-serp-snapshots.jsonl`: SERP features + top organic evidence
- `03-candidate-urls.jsonl`: deduped off-site URLs (traceable to query + rank)
- `04-competitor-url-pack.md`: curated link pack for editors
