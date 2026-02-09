# Creatify competitor research (traffic + SEO/AEO)

This folder contains a small, repeatable pipeline to research:
- `https://creatify.ai/`
- `https://creatify.ai/zh/blog`

Constraints observed on 2026-02-04/05:
- `creatify.ai` blocks automated fetching for `/blog`, `/zh/blog`, `/sitemap.xml` with Cloudflare challenge.
- In this environment, network access from Python subprocesses is unreliable; we fetch via top-level `curl` and then score offline in Python.

## Run (Top 10 blog: EN only, SEO-first + AEO bonus)

From repo root (fetches public artifacts via `curl`, then scores offline):

```bash
zsh scripts/creatify_research/fetch_top10_artifacts.sh
```

If you are running in a restricted runner where network is only allowed for direct `curl` invocations
(and child-process `curl` calls are blocked), use the explicit 4-step flow:

```bash
# 1) Fetch Wayback CDX dumps
curl -4 -sS -L --retry 12 --retry-all-errors --retry-delay 1 -A 'Mozilla/5.0' \
  'https://web.archive.org/cdx/search/cdx?url=creatify.ai/blog/&matchType=prefix&output=json&fl=timestamp,original&filter=statuscode:200&collapse=urlkey&from=2020&to=2026&limit=8000&sort=asc' \
  -o 'research 竞品分析/creatify-ai/data/wayback_cdx_creatify_ai_blog_asc.json'

curl -4 -sS -L --retry 12 --retry-all-errors --retry-delay 1 -A 'Mozilla/5.0' \
  'https://web.archive.org/cdx/search/cdx?url=creatify.ai/blog/&matchType=prefix&output=json&fl=timestamp,original&filter=statuscode:200&collapse=urlkey&from=2020&to=2026&limit=8000&sort=desc' \
  -o 'research 竞品分析/creatify-ai/data/wayback_cdx_creatify_ai_blog_desc.json'

# 2) Prepare inventory + fetch plans (offline)
python3 scripts/creatify_research/top10_seo_aeo.py prepare --max-candidates 20

# 3) Generate a multi-request curl config and fetch SERP + Wayback snapshots
python3 scripts/creatify_research/make_fetch_curl_config.py \
  --data-dir 'research 竞品分析/creatify-ai/data' \
  --out /tmp/creatify_fetch.cfg
curl -K /tmp/creatify_fetch.cfg

# 4) Score + write report (offline)
python3 scripts/creatify_research/top10_seo_aeo.py score --max-candidates 20 --max-audits 20
```

If you already fetched artifacts, you can re-score without refetching:

```bash
python3 scripts/creatify_research/top10_seo_aeo.py score
```

Outputs (workspace relative):
- `research 竞品分析/creatify-ai/00-executive-summary.md`
- `research 竞品分析/creatify-ai/01-traffic-and-audience.md`
- `research 竞品分析/creatify-ai/02-seo-aeo-performance.md`
- `research 竞品分析/creatify-ai/03-blog-inventory-milestones.md`
- `research 竞品分析/creatify-ai/data/` (evidence pack: API request/response JSON)

Additional output:
- `research 竞品分析/creatify-ai/04-top10-seo-aeo.md`
- `research 竞品分析/creatify-ai/data/blog_inventory_en.jsonl`
- `research 竞品分析/creatify-ai/data/seo_serp_evidence.jsonl`
- `research 竞品分析/creatify-ai/data/aeo_audit.jsonl`
