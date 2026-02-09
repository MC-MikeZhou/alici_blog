# Tutorial Blueprint v3.0 (Structure Contract)

This blueprint defines the **lintable** structure and marker requirements for Standalone Blog Tutorial Writer v3.0.

## 1) Tier System (mandatory)

Tier selection determines word range and required conditional sections:

| Tier | Word Range | Use Case | Must Include |
|------|------------|----------|--------------|
| Tier 1 | 1,800–2,200 | Single tool/feature | Troubleshooting + FAQ |
| Tier 2 | 2,200–2,800 | Workflow/multi-step | Prerequisites + Troubleshooting + FAQ |
| Tier 3 | 2,800–3,500 | Composite/monetization | Market Context + Monetization (if triggered) + Prerequisites + Troubleshooting + FAQ |

## 2) Required Markers (mandatory)

### 2.1 Citable Blocks (taxonomy v3.0)

Format (must be exact):
```md
<!-- CITABLE_BLOCK type="statistic|definition|comparison|recommendation|methodology|case_study|key_takeaway" id="unique-kebab-id" -->
Standalone, quotable content (40–120 words).
<!-- /CITABLE_BLOCK -->
```

Rules:
- Minimum: **5** blocks
- Minimum distinct `type`s: **3**
- Types must be from the allowed set above
- Each open marker must have a corresponding close marker

### 2.2 Image placeholders (v2.0)

Provide images using a Markdown image line plus structured metadata block:
```md
![Alt text](placeholder)
<!-- IMAGE_PLACEHOLDER
  id: "kebab-case-id"
  type: "hero|screenshot|diagram|comparison"
  priority: "required|recommended|optional"
  alt: "descriptive alt text"
  where: "placement description"
  context: "optional user context to guide generation"
  size_hint: "optional WxH"
-->
```

Required keys: `id`, `type`, `priority`, `alt`, `where`

### 2.3 CTA cards (v2.0 friction-aligned)

Format:
```md
<!-- CTA_CARD
  position: "after-step-3|after-troubleshooting|end"
  trigger: "friction_point|achievement|decision"
  friction_context: "50-100 words describing user mental state and why this CTA helps now"
  product: "video_studio|image_studio|video_prompt|..."
  cta_type: "try_free|learn_more|see_pricing"
  url: "https://..."
  headline: "Short headline"
  body: "1-3 sentences"
-->
```

Required keys: `position`, `trigger`, `friction_context`, `product`, `cta_type`

Rules:
- Minimum: **2** CTA_CARD blocks per tutorial (1 mid-article + 1 closing)

### 2.4 Self-Test placeholder

If **no** `experiment_pack` is provided, you must include:
```md
<!-- SELF_TEST_PLACEHOLDER: Replace with real testing data -->
...
<!-- /SELF_TEST_PLACEHOLDER -->
```

## 3) Required Headings (order + triggers)

### 3.1 Opening (H1 + AIDA)

Article must start with:
1) `# {Title}` (H1)
2) An AIDA opening block (comment markers recommended, but content is mandatory):
   - Attention: direct answer (40–60 words)
   - Interest: pain point (20–30)
   - Desire: value promise (20–30)
   - Action: navigation hint (10–20)

### 3.2 Main H2 order (mandatory)

The article must contain the following H2 sections in this order:

1. `## Background`
2. `## Market Context: Why {Topic} Is Exploding Right Now` (Tier 3 only; include if market_data exists)
3. `## Prerequisites Check` (Tier 2/3 only)
4. `## Choose Your Path: {N} Workflows Compared` (only if the tutorial has multiple workflows/paths)
5. Steps: `## Step 1: ...` through `## Step N: ...` (N ≥ 5)
6. `## Understanding Prompt Structure for {Tool}` (only for prompt-driven AI generation tutorials)
7. `## Troubleshooting: Quick Fixes for Common Issues` (all tiers)
8. `## Pro Tips for {Topic}` (optional)
9. `## Monetization Framework: How to Make Money with {Topic}` (Tier 3 only; include if monetization is in scope)
10. `## Conclusion`
11. `## FAQ`

Notes:
- Conditional sections must appear exactly where listed above if triggered.
- If a conditional section is not triggered, it must not appear.

## 4) Required Tables (by section)

### 4.1 Prerequisites Check table (Tier 2/3)

Must include a Markdown table with header columns:
`Item | Required? | Why | Alternatives`

### 4.2 Workflow Selector table (if multi-path)

Must include a Markdown table with header columns:
`Goal | Workflow | Time | Difficulty | Jump To`

### 4.3 Troubleshooting table (all tiers)

Must include a Markdown table with header columns:
`Symptom | Likely Cause | Fix`

And at least **5** data rows (issues).

