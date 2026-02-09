# Evidence Gap Plan

Purpose: document what is still missing after standard-depth competitor benchmarking and define concrete actions to close gaps.

## Current Coverage

- Competitors covered: InVideo, Higgsfield, OpusClip
- Sample size: 18 pages total (6 each)
- Artifacts available:
  - `competitor-benchmark-matrix.md`
  - `sources.jsonl`
  - local benchmark research for InVideo and Opus

## Gaps

### Gap 1: Traffic confidence is directional, not measured

Issue:
- We have intent-based and format-based quality signals, but not reliable page-level traffic estimates.

Impact:
- Prioritization of article updates is still heuristic.

Closure action:
1. Run keyword and SERP capture for each sampled URL with DataForSEO (or equivalent).
2. Add fields: `est_monthly_clicks`, `keyword_cluster_size`, `serp_feature_presence`.
3. Re-score backlog priorities using measured demand.

### Gap 2: Publish-date precision is incomplete

Issue:
- Several benchmark pages do not expose dates in quick scrape summaries.

Impact:
- Freshness/cadence scoring has uncertainty.

Closure action:
1. Run deterministic metadata extraction for each URL (`article:published_time`, JSON-LD date fields).
2. Backfill `sources.jsonl` publish dates.
3. Recalculate freshness subscore.

### Gap 3: Higgsfield local archive is missing

Issue:
- No dedicated local research folder equivalent to `invideo-blog` and `opus-pro-blog`.

Impact:
- Harder to run repeatable offline comparisons.

Closure action:
1. Create local folder: `research 竞品分析/higgsfield-blog/`.
2. Save page snapshots + extracted framework notes + benchmark file.
3. Add to monthly refresh pipeline.

### Gap 4: No measured experiment_pack in canonical v3 draft

Issue:
- `SELF_TEST_PLACEHOLDER` remains in `01-article-draft.md`.

Impact:
- Proof density and citation trust are capped.

Closure action:
1. Execute 30-run prompt test protocol.
2. Replace placeholder with measured table and mini case outcomes.
3. Add at least 3 `case_study` CITABLE_BLOCK entries.

### Gap 5: Internal-link graph is not yet implemented

Issue:
- Canonical page exists, but satellite pages and interlinks are not published.

Impact:
- Query breadth and topical authority growth are limited.

Closure action:
1. Produce satellite page A: template vault.
2. Produce satellite page B: alternatives showdown.
3. Add bidirectional links between canonical and satellites.

## Priority Order to Close Gaps

1. Gap 4 (experiment evidence) - strongest impact on trust and AEO citation probability.
2. Gap 1 (traffic confidence) - strongest impact on roadmap prioritization.
3. Gap 5 (internal linking) - strongest impact on organic growth compounding.
4. Gap 2 (date precision) - medium impact, quick win.
5. Gap 3 (Higgsfield local archive) - medium impact, infrastructure benefit.

