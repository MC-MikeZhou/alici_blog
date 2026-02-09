# UGC Ads (2026-02-08) Seed Portfolio

## Inputs

- Basecamp root todolist:
  - https://3.basecamp.com/3135399/buckets/42744895/todolists/9536725297
  - linked: https://3.basecamp.com/3135399/buckets/45547714/todolists/9546306218
- Context pack output:
  - `tmp/basecamp-context/2026-02-08-ugc-ads-v2/`

## Files

- `02-team-research-report.md`
- `03-team-directions.json`
- `04-decision-brief.md`
- `05-basecamp-mapping.json`

## Rebuild Commands

Rebuild Basecamp context pack:

```bash
python3 scripts/basecamp_pull_todolist.py \
  --app-url "https://3.basecamp.com/3135399/buckets/42744895/todolists/9536725297" \
  --out "tmp/basecamp-context/2026-02-08-ugc-ads-v2" \
  --follow-linked-todolists \
  --follow-linked-depth 1 \
  --allow-bucket 42744895 \
  --allow-bucket 45547714 \
  --max-linked 3
```

Rebuild mapping:

```bash
python3 scripts/basecamp_map_directions.py \
  --context tmp/basecamp-context/2026-02-08-ugc-ads-v2/02-basecamp-normalized/context.json \
  --directions "research 竞品分析/team-research/2026-02-08-ugc-ads/03-team-directions.json" \
  --out "research 竞品分析/team-research/2026-02-08-ugc-ads/05-basecamp-mapping.json" \
  --min-confidence 0.55 \
  --top-k 8
```

