# Analytics & A/B Tests — Alici UGC Ads Hub

## 1) Event taxonomy (minimum viable)
### Required events
- `view_hub_ugc_ads`
- `click_cta_generate_script`
- `script_generated`
- `signup_started`
- `signup_completed`
- `export_video`

### Recommended properties
Common:
- `page_path` (e.g., `/solutions/ugc-ads/`)
- `referrer`
- `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`
- `device_type` (mobile/desktop)

Script generation:
- `format_selected` (testimonial, product_demo, unboxing, before_after, problem_solution)
- `variant_count_requested`
- `industry` (optional, if captured)

Export:
- `platform_preset` (tiktok, reels, shorts)
- `aspect_ratio` (9:16, 1:1, 16:9)

## 2) Funnel definition (what “good” looks like)
Primary funnel:
`view_hub_ugc_ads` → `click_cta_generate_script` → `script_generated`

Monetization funnel:
`script_generated` → `signup_completed` → `export_video`

## 3) CTA gating (recommended)
- No-login: allow 1 script preview (text only)
- Signup required for:
  - exporting video
  - generating multi-variant packs beyond a small limit

## 4) A/B tests (2 rounds)
### Test 1: Hero layout
Variants:
- A: Key Takeaways-first hero (bullets above the fold)
- B: Demo-first hero (short demo video above the fold)

Primary success metric:
- `click_cta_generate_script` rate

Guardrail metrics:
- `script_generated` rate
- bounce/exit rate

### Test 2: CTA wording
Variants:
- A: “Generate a UGC script”
- B: “Generate a UGC video ad”

Primary metric:
- `script_generated` rate

Guardrail:
- `signup_completed` rate (ensure downstream intent doesn’t drop)

## 5) QA checklist (before shipping)
- [ ] All events fire once per page view/action (no double fires)
- [ ] UTM captured on first page, persisted through signup/export
- [ ] Subpages fire `view_hub_ugc_ads` equivalent event with page-specific name (e.g., `view_ugc_ads_for_tiktok`)
- [ ] Consent/analytics policy respected (region-dependent)

