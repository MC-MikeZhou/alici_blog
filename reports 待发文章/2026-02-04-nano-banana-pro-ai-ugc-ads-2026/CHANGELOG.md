# Changelog — Nano Banana Pro × Hyper‑Real AI UGC Ads (2026)

## v2.3 (2026-02-07)

- **Cover + image refresh**: Adopted the new selected cover image and placed the new context visuals into the article at the most relevant steps (workflow pipeline + Step 4 composite + good-vs-fake checklist).
- **Local-first media**: Switched inline image links from remote CDN URLs to local `gen_images/` assets to keep preview/export self-contained.

## v2.2 (2026-02-07)

- **Internal-link pruning (publish draft only)**: Removed most non-essential alici.ai internal links to reduce "over-linking" while keeping external evidence links intact.
- **Kept only 4 core internal links**:
  - Nano Banana Pro deep link: `https://app.alici.ai/pages/imageGen?model=google_banana_pro_1&uco=motion_blog`
  - Nano Banana Pro reference: `https://alici.ai/blog/nano-banana-pro-is-here`
  - AI video models reference: `https://alici.ai/blog/best-ai-video-generators-2026`
  - Standard VideoGen CTA: `https://app.alici.ai/pages/videoGen?model=kling_2_6_s_mc&uco=motion_blog`
- **Archive housekeeping**: Moved legacy v2.0 artifacts out of the root into `archive/v2.0/` to keep the folder "latest-only" (details preserved in `archive/v2.0/VERSION-CHANGELOG.md`).

## v2.1 (2026-02-06)

- **Title strategy update (Volume-first)**: Updated the primary title to `How to Use Nano Banana Pro for UGC Ads in 2026 (AI UGC Workflow + Prompts)` so the H1 aligns with current US query demand.
- **Live DataForSEO validation**: Confirmed API status on 2026-02-06 (`/v3/keywords_data/google_ads/search_volume/live`, `status_code=20000`) and refreshed the keyword strategy using live volumes:
  - `nano banana pro`: 49,500
  - `how to use nano banana pro`: 480
  - `nano banana prompt`: 1,900
  - `ugc ads`: 1,300
  - `ai ugc`: 1,000
  - `ugc video ads`: 70
  - `ai ugc ads`: null
  - `hyper-real ai ugc ads`: null
- **Metadata refresh**: Updated `title`, `meta_title`, `meta_description`, and `last_updated` in draft + edited markdown, with `ugc ads` and `ai ugc` prioritized in metadata wording.
- **Topic brief keyword order**: Reordered `secondary_keywords` to prioritize `how to use nano banana pro`, `ugc ads`, `ai ugc`, and `ugc video ads` before legacy long-tail variants.

## v2.0 (2026-02-05)

- Writer upgrade + structure compliance pass (prerequisites check, troubleshooting table, citable blocks, and image placeholders). Full detail archived in `archive/v2.0/VERSION-CHANGELOG.md`.

## v1.1 (2026-02-04)

- **Banana Pro deep link**: Added a one-click Nano Banana Pro link for actor generation: `https://app.alici.ai/pages/imageGen?model=google_banana_pro_1&uco=motion_blog`.
- **VideoGen CTA link update**: Switched `https://alici.ai/pages/videoGen` to `https://app.alici.ai/pages/videoGen?uco=motion_blog` for a direct app landing flow.
- **Alici AI platform note**: Added a short note in Step 5 clarifying that Veo 3 / Sora-class workflows (and adjacent building blocks) can be run in alici.ai (`https://app.alici.ai/`) to avoid over-reliance on third-party descriptions.
- **Alici Blog internal association**: Added “More Alici Blog links” near the top and a dedicated appendix section:
  - `https://alici.ai/blog/best-ai-video-generators-2026`
  - `https://alici.ai/blog/nano-banana-pro-is-here`
- **Archive**: Moved the original v1.0 outputs into `archive-v1.0/` while keeping v1.1 as the default files in the root folder.
- **Archive layout**: Old versions live under `archive/v1.0/` (and snapshots under `archive/v1.1/`) while keeping only the latest (no-suffix) files in the root folder.

## v1.0 (2026-02-04)

- Initial article generation from YouTube transcript, including edited version, AEO + competitive validation notes, Framer JSON export, and preview.

## v1.2 (2026-02-04)

- **Beginner mistakes + quick fixes**: Added a compact beginner-focused section (4 items) and kept the combined count of beginner items + FAQ at **≤ 10**.
- **FAQ refresh (6 items)**: Replaced the prior FAQ with 6 beginner questions (length, face-on camera, native feel, AI UGC effectiveness, better hooks, and what to measure first).
- **EEAT (first-person)**: Updated the author to **Noah Bennett** and added a short first-person author blurb + first-person disclosure.
- **Hook constraint rule**: Added a constraint rule (time/cost/niche/without-X) to the hook generation prompt.
- **Proof timing guidance**: Updated the assembly checklist to bring proof forward into the first **8–10 seconds**.
