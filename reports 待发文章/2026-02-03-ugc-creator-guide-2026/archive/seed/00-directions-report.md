# Seed Mode — UGC Creator (Video) Beginner Guide — Directions Report
**Date**: 2026-02-03  
**Mode**: growth-topic-scout v2.2 — Seed Mode (Mode D)  
**Language / Geo**: en / US (2840)  
**Seed**: `ugc creator`  

---

## Phase 0 — Mission Config ✅

**Audience**: UGC creator beginners (video UGC: Reels/TikTok/Shorts)  
**Goal**: traffic_and_conversion  
**Primary product**: `script_to_video` (secondary: `video_prompt`, `video_studio`)  
**Validation depth**: standard  

**Hard constraints**
- Must cover this reference as a *reference* (not a rewrite): `https://invideo.io/blog/ai-ugc-strategy-guide/`
- Scope: creator workflow for **video UGC** (image/review UGC only as a small supporting section)
- Title must include **2026** (editor v2.9.3 blocking rule)

**Mission Config file**: `00-mission-config.json`

---

## Phase 0.5 — Competitor Intent Pattern Discovery ✅

### Competitor anchors (attempted)
| # | Competitor | Status | Titles pulled |
|---:|---|---|---:|
| 1 | https://invideo.io/blog | OK (html fallback) | 20 |
| 2 | https://later.com/blog | OK (feed: https://later.com/rss.xml) | 20 |
| 3 | https://sproutsocial.com/insights | OK (feed: https://sproutsocial.com/insights/feed) | 10 |
| 4 | https://www.shopify.com/blog | OK (html fallback) | 20 |
| 5 | https://grin.co/blog | OK (feed: https://grin.co/blog/feed) | 12 |

### Discovered intent patterns (target: 5–8)

| Pattern | Name | Count | Example titles |
|---|---|---:|---|
| P1 | Become a UGC creator (beginner path) | 17 | How to Make Commercial Ads in 2026: A Director’s Guide to Studio-Grade Results #howtoguides #marketers; How to Create a Real Estate Video Using AI (Invideo+Kling 2.6/Kling O1/Veo 3.1) #videomarketing #realestate; How to Build “Soul” Into AI-Generated Ads #marketers; Reshoot Without the Reshoot: How to Swap Faces and Scenes in Your Videos Instantly with Performances #instagram #creators; How to Create a Commercial Product Video? #youtube #marketers |
| P2 | Portfolio / examples | 2 | New video ideas 44 posts; Find an Idea |
| P3 | Rates / pricing / usage rights | 1 | What Is Automated Affiliate Marketing (and Is It Right for Small Teams?) |
| P4 | Outreach / pitching / platforms | 2 | What is Shopify? . How our commerce platform works; Affiliate Marketing Software Explained: Choosing the Best Platform for Your Brand |
| P5 | Brief / script / shot list (deliverables) | 1 | Business plan template . |
| P6 | Editing workflow (short-form) | 0 | - |
| P7 | Compliance / disclosures (FTC, platform policies) | 0 | - |

---

## Phase 1 — Intent Pattern Expansion (60–80 keywords) ✅

- Output: `01-keywords-to-validate.json` (80 keywords)

---

## Phase 2 — DataForSEO Validation (SEO + AEO) ✅

- Output: `02-validated-keywords.json`
- Output: `03-top-directions.json`
- Note: LLM Mentions is commonly subscription-gated; this run uses Keywords Data + SERP features as AEO proxies.

Top direction candidates (after Gate 1/2/3):

| Rank | Pattern | Primary keyword | Total vol | SEO | AEO | Priority |
|---:|---|---|---:|---:|---:|---|
| 1 | P1 | what is a ugc creator | 3720 | 67 | 75 | high_aeo_first |
| 2 | P2 | ugc portfolio examples | 1140 | 25 | 55 | low |
| 3 | P3 | ugc usage rights | 80 | 20 | 95 | high_aeo_first |
| 4 | P5 | ugc brief template | 20 | 14 | 75 | high_aeo_first |
| 5 | P4 | ugc creator pitch | 30 | 11 | 95 | high_aeo_first |
| 6 | P7 | ftc disclosure ugc | 0 | 10 | 75 | high_aeo_first |
| 7 | P6 | how to edit ugc videos | 20 | 4 | 95 | high_aeo_first |

---

## Phase 3 — Title Lock (final 2 directions) ✅

### D01 (Rank 1)

**Locked title**: How to Become a UGC Creator in 2026: A Beginner Video Workflow (Step-by-Step)

- Primary keyword: `what is a ugc creator`
- SEO score: 67 / AEO score: 75 / Priority: high_aeo_first
- SERP Top 3 titles:
  - New to UGC- is it worth it? : r/UGCcreators
  - Start Making Money As A UGC Creator In 7 Easy Steps
  - UGC Content Creator: Role, Skills, and How to Get Started

### D02 (Rank 2)

**Locked title**: UGC Creator Portfolio in 2026: Templates, Examples, and What Brands Want

- Primary keyword: `ugc portfolio examples`
- SEO score: 25 / AEO score: 55 / Priority: low
- SERP Top 3 titles:
  - 13 UGC Portfolio Examples & How to Create ...
  - Can i see your portfolio? : r/UGCcreators
  - Katie UGC Portfolio

---

## Deterministic Direction Selection (final pick) ✅

Selected: **D01**

- Title: How to Become a UGC Creator in 2026: A Beginner Video Workflow (Step-by-Step)
- Slug: `ugc-creator-guide-2026`
- Rationale: max(combined_priority, seo_score, aeo_score, beginner-breadth)

