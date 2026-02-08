# Standalone Blog List Writer v3.0 (Listicle)

This folder is a **self-contained** packaging of AliciBlog’s `blog-list-writer` **v3.0 listicle** workflow, designed to be runnable in **non-repo environments** (e.g., **Claude Web** chat) while preserving the v3 guarantees:

- Blueprint-enforced headings + required tables + CTA markers + tool-card fields
- Outputs as a **3-file bundle** (+ optional validator report)
- Methodology-level guardrails (no “we tested” unless allowed)
- A lint gate that yields **PASS/FAIL** on structure (plus evidence warnings)

## What’s Inside

- `PROMPT_CLAUDE_WEB.md` — paste this into Claude Web as the “skill” prompt.
- `LISTICLE_BLUEPRINTS_v3.md` — lintable blueprint spec (A/B/C/D).
- `PLAN_SCHEMA_MIN_v3.json` — minimal plan.json schema (for reference).
- `ASSETS_SCHEMA_MIN_v3.json` — minimal assets.json schema (for reference).
- `listicle_validator.py` — standalone validator script (optional, for local CI / CLI use).

## How to Use (Claude Web)

### Option A — Claude Web “Skills” upload (recommended if you see the SKILL.md error)

Upload `standalone-blog-list-writer-v3/SKILL.md` (it starts with YAML frontmatter `---`, which the Skills loader requires).

### Option B — Normal chat (no upload)

1) Open `standalone-blog-list-writer-v3/PROMPT_CLAUDE_WEB.md`  
2) Copy-paste the entire content into Claude Web chat.
3) Then provide one of:
   - A topic (required), e.g. “best AI UGC tools”
   - Optional competitor URL(s), e.g. `https://invideo.io/blog/best-ai-ugc-tools/`

### Example input (Claude Web)

```
Topic: best AI UGC tools
Competitor URL: https://invideo.io/blog/best-ai-ugc-tools/
Must-include tools: alici.ai
Desired list size: 12
```

Claude should produce **four code blocks** named:
- `01-article-draft.md`
- `02-plan.json`
- `03-assets.json`
- `04-listicle-validator-report.json` (self-check result)

## How to Use (Local CLI / CI)

If you have the three outputs in a folder:

```bash
python3 standalone-blog-list-writer-v3/listicle_validator.py --dir /path/to/output_dir
```

It will write `04-listicle-validator-report.json` and exit:
- `0` on PASS
- `1` on FAIL

## Preconditions / Postconditions

### Preconditions (inputs + allowed behavior)
- Input: topic + optional competitor URLs
- Allowed: normal public web browsing; **no paywalled/login-only scraping**; no access-control bypassing
- Default assumptions: `methodology_level=research_only`, `freshness_date=today`, `geo=US`, `language=en`

### Postconditions (guaranteed outputs)
- Blueprint-compliant listicle draft
- Machine-checkable plan + assets queue
- Validator PASS/FAIL result (structure), with evidence Warnings allowed
