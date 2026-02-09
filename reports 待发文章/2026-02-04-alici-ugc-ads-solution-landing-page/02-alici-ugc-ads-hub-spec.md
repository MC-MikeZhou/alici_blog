# Alici “UGC Ads” Hub — AEO/SEO Landing Page Spec (English Global)

## 0) Decision summary
- Primary hub URL: `/solutions/ugc-ads/` (preferred for scaling a “Solutions” cluster)
- First expansion: 10 subpages (platform + format + commerce)

## 1) Target queries & intent mapping
### Primary (hub-level)
- “ugc ad generator”
- “create ugc video ads”
- “how to make ugc ads”

### Secondary (subpage-level)
- platform: “ugc ads for tiktok / instagram / facebook”
- format: “testimonial ugc ad”, “product demo ugc ad”, “unboxing ugc ad”, “before and after ugc ad”
- commerce: “ugc ads for amazon / shopify”
- angle templates: “ugc ad hooks”

## 2) Page goals & success criteria
### SEO/AEO
- Ranks for hub-level intent queries
- Extractable by answer engines:
  - TL;DR paragraph
  - HowTo list
  - FAQ (query-shaped)
- Avoid thin/duplicated content across subpages (each subpage needs a unique module)

### Conversion
Primary conversion:
- `Generate a UGC script` → `script_generated` (one free preview)
Secondary conversion:
- `signup_completed` → `export_video` (paid unlock)

## 3) Information architecture (URL set)
Hub:
- `/solutions/ugc-ads/`

Initial 10 subpages:
- `/solutions/ugc-ads/for-tiktok/`
- `/solutions/ugc-ads/for-instagram/`
- `/solutions/ugc-ads/for-facebook/`
- `/solutions/ugc-ads/product-demo/`
- `/solutions/ugc-ads/testimonial/`
- `/solutions/ugc-ads/unboxing/`
- `/solutions/ugc-ads/before-after/`
- `/solutions/ugc-ads/amazon/`
- `/solutions/ugc-ads/shopify/`
- `/solutions/ugc-ads/hooks/`

## 4) On-page module order (AEO-first)
1. H1
2. Key Takeaways (5–9 bullets)
3. TL;DR (1 paragraph)
4. How it works (3-step HowTo)
5. Templates & examples (≥ 6)
6. Use cases (links to subpages)
7. Why UGC works (education) — *only citeable facts*; otherwise `[EVIDENCE NEEDED]` or rewrite as test plan
8. Problem → Alici capability table (workflow mapping)
9. Social proof (verifiable)
10. FAQ (8–12)
11. Final CTA
12. Compliance & policy notes

## 5) Copy rules (anti “empty SEO”)
- No numeric performance claims unless we can cite a public source.
- Any “capability” statement must map to a real feature Alici ships.
- Prefer concrete promises:
  - “Generate a UGC-style script + shot list”
  - “Create multiple hook/angle variants”
  - “Export versions for TikTok/Reels/Shorts”

## 6) Structured data (JSON-LD)
Required:
- `FAQPage`
- `HowTo`
- `BreadcrumbList`

Optional:
- `VideoObject` (if a real demo video exists)
- `SoftwareApplication` (only if fields are truthful and up to date)

## 7) Technical SEO requirements
- SSR or static rendering for all core copy (no login wall)
- Avoid heavy client JS above the fold
- Images/video lazy-loaded; fixed dimensions to reduce CLS
- Canonical tag set per page; hub should not canonicalize to homepage

## 8) Internal linking plan
Hub → Subpages:
- Use “Use cases” cards + in-body contextual links.

Hub ↔ Blog cluster (editorial support pages):
- “UGC ad hooks (20 templates)”
- “Testimonial ad script templates”
- “Product demo storyboard template”
- “UGC ad length & specs by platform”

Each blog post must link back to `/solutions/ugc-ads/` within the first 2 short paragraphs.

## 9) Release plan (2-week sprint)
Week 1:
- Ship hub page copy + core CTA + FAQ/HowTo schema
- Ship 3 subpages (TikTok, Testimonial, Hooks)

Week 2:
- Ship remaining 7 subpages
- Add 2 supporting blog posts (hooks + testimonial templates)
- Run first A/B tests (hero + CTA)

## 10) Evidence pack (before publishing “Why UGC works”)
Minimum requirement:
- Add 1–2 reputable industry sources for any *industry-wide* claims.
- If no high-quality citations are available, remove statistics and keep the section qualitative.

## 11) Internal reference docs (this repo)
- AEO opening patterns: `research 竞品分析/invideo-blog/03-aeo-opening-patterns.md`
- Citation techniques: `research 竞品分析/invideo-blog/02-citation-techniques.md`
