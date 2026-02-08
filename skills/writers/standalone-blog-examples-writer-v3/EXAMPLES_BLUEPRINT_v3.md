# EXAMPLES_BLUEPRINT_v3 (Standalone)

This is the structure contract for Standalone Blog Examples & Ideas Writer v3.0. All profiles share global rules; profile-specific rules are listed in separate sections.

## Global Rules (All Profiles)

### Required Outputs (same folder)
- `01-article-draft.md` (required)
- `02-plan.json` (required)
- `03-assets.json` (required)
- `04-examples-validator-report.json` (required)

### Opening (H1 + AIDA)

Article must start with:
1) `# {Title}` (H1)
2) An AIDA opening block:
   - Attention: statistical data hook + direct answer (40–60 words)
   - Interest: pain point (20–30 words)
   - Desire: value promise (20–30 words)
   - Action: navigation hint (10–20 words)

Quick Answer must be **120–180 words** total.

### Concept Card (lintable fields)

Every concept must be wrapped in boundary markers:

```md
<!-- CONCEPT_CARD_START id="concept-{rank}" profile="{profile}" -->
### {rank}. {Concept Name}

**Scenario:** ...

**Why it works:** ...

<!-- EMBED_PLACEHOLDER
  id: "concept-{rank}-embed"
  type: "youtube|instagram|tiktok|screenshot"
  alt: "descriptive alt text"
  source_hint: "brand name or source"
-->

**Key elements:**
- Element 1
- Element 2
- Element 3

**Script:** (Profile B required / Profile A optional)
> Hook: ...
> Claim: ...
> Proof: ...
> CTA: ...

**Variations:** (Profile B required / Profile A optional)
- Variation 1: ...
- Variation 2: ...

**Try it:** [CTA text](URL)
<!-- CONCEPT_CARD_END -->
```

#### Concept Card Field Requirements by Profile

| Field | Profile A (Showcase) | Profile B (Ideas+Templates) | Profile C (Mega) |
|-------|---------------------|----------------------------|-----------------|
| Concept Name | Required | Required | Required |
| Scenario | Required (50–100 words) | Required (50–100 words) | Required (20–40 words) |
| Why it works | Required (30–60 words) | Required (30–60 words) | Optional |
| EMBED_PLACEHOLDER | Required | Required | Recommended |
| Key elements (≥3 bullets) | Required | Required | Not required |
| Script (Hook/Claim/Proof/CTA) | Optional | **Required** | Not required |
| Variations (≥2) | Optional | **Required** | Not required |
| Try it CTA | Required | Required | Required |

### Citable Blocks (taxonomy v3.0)

Format (must be exact):
```md
<!-- CITABLE_BLOCK type="statistic|definition|comparison|recommendation|methodology|case_study|key_takeaway" id="unique-kebab-id" -->
Standalone, quotable content (40–120 words).
<!-- /CITABLE_BLOCK -->
```

Rules:
- Minimum: **5** blocks
- Minimum distinct `type`s: **3**
- Each open marker must have a corresponding close marker

### Image Placeholders (v2.0)

```md
![Alt text](placeholder)
<!-- IMAGE_PLACEHOLDER
  id: "kebab-case-id"
  type: "hero|screenshot|diagram|comparison"
  priority: "required|recommended|optional"
  alt: "descriptive alt text"
  where: "placement description"
-->
```

Required keys: `id`, `type`, `priority`, `alt`, `where`
Minimum: **2** (1 hero + 1 diagram/comparison)

### CTA Cards (v2.0 friction-aligned)

```md
<!-- CTA_CARD
  position: "after-overview|mid-article|end"
  trigger: "friction_point|achievement|decision"
  friction_context: "50-100 words describing user mental state"
  product: "video_studio|image_studio|video_prompt|..."
  cta_type: "try_free|learn_more|see_pricing"
  url: "https://..."
  headline: "Short headline"
  body: "1-3 sentences"
-->
```

Rules:
- Minimum: **2** CTA_CARD blocks (1 mid-article + 1 closing)

### Embed Placeholders (NEW in v3.0)

```md
<!-- EMBED_PLACEHOLDER
  id: "concept-{rank}-embed"
  type: "youtube|instagram|tiktok|screenshot"
  alt: "descriptive alt text"
  source_hint: "brand name or source"
-->
```

Required keys: `id`, `type`, `alt`, `source_hint`
Rules: **1 per Concept Card** (for Profiles A and B; recommended for C)

### Source Attribution Rules (All Profiles)

Examples articles reference real brands, campaigns, and content. Every external reference must be attributed.

#### Concept-Level Attribution

Each Concept Card that references a real brand/campaign MUST include:
- The brand name in the **Scenario** field
- A `source_hint` value in its `EMBED_PLACEHOLDER` marker
- If the concept is from a specific campaign, name it (e.g., "Nike's 'Just Do It' 50th Anniversary TikTok campaign")

#### Article-Level Attribution

Two options depending on profile and brand density:

**Option A — Inline (preferred for Profiles A and B):**
Attribution is embedded in concept cards via `source_hint` and the plan's `brand_sources` array. No separate section needed if every concept card with `source_type != "original_concept"` has proper attribution.

**Option B — Dedicated Section (required for Profile C Mega, or when >50% of concepts reference external brands):**

Add before FAQ:
```md
## Sources and Credits

This article references campaigns, content, and strategies from the following brands and creators:

- **[Brand 1]** — [What we referenced] ([Source URL])
- **[Brand 2]** — [What we referenced] ([Source URL])

*All brand names, logos, and campaign materials belong to their respective owners.*
```

#### Do NOT
- Fabricate campaign names or statistics
- Claim brand endorsement of alici.ai
- Use brand logos without attribution
- Present competitor content as original

### "How to Recreate" Section Specification (All Profiles)

This section connects examples to alici.ai products. It is NOT a full tutorial — it is a **quick-start bridge**.

#### Structure (Profile A — Showcase, Profile B — Ideas+Templates)

Target: **150–300 words**

```md
## How to Recreate These with {Product Name}

{Product context: 1-2 sentences explaining what the product does, from PRODUCT_CATALOG.md}

1. **Choose your concept** — Pick an example from above that matches your [use case].
2. **Open {Product Name}** — [Brief action with link to product URL].
3. **Set your parameters** — [1-2 specific settings relevant to the article topic].
4. **Generate and iterate** — [Brief action].
5. **Export and publish** — [Brief final action].

> **Pro tip:** [One actionable tip that references a specific concept from the article, e.g., "Take the 'Unboxing Reaction' concept from #3 above and..."]

<!-- CTA_CARD position="end" trigger="achievement" ... -->
```

#### Structure (Profile C — Mega)

Target: **100–200 words**

```md
## How to Get Started with {Product Name}

{Product context: 1 sentence}

1. [Step 1 — 1 sentence]
2. [Step 2 — 1 sentence]
3. [Step 3 — 1 sentence]

> Start free: [CTA link]
```

#### Product Selection Rules

1. Read `references/PRODUCT_CATALOG.md` keyword-product mapping
2. Match the article's `primary_keyword` against product feature tags
3. Use the **primary product** for the section title and steps
4. If the article covers multiple product areas (e.g., video + image), use the one most aligned with the majority of concepts

#### Internal Reference Requirement

- Reference at least **2 specific concept names** from the article (e.g., "Take the 'Unboxing Reaction' concept from #3 above")
- This creates an internal reference loop that improves engagement and time-on-page

### FAQ Requirements (lintable)

In `## FAQ`:
- ≥6 FAQ questions
- Each answer is **2–4 sentences**
- Schema.org FAQPage markup recommended

### Tables (lintable)

All required tables must be valid Markdown tables (header row + separator row).

---

## Profile A — Showcase (`showcase`)

**Typical size**: 10–25 concepts
**Target words**: 3,500–7,000

### Required H2 Order
1. `## Key Takeaways`
2. `## Quick Overview` (Table)
3. Category sections (H2): `## {Category Name}` — concepts as H3 inside
4. `## How to Recreate These with {Product}`
5. `## Pro Tips for {Topic}`
6. `## FAQ`
7. `## Conclusion`

### Quick Overview Table

Columns must be exactly:
- `# | Concept | Type/Category | Best For | {Flex Column}`

The 5th column is selected by the Planner based on topic fit:

| Column Option | Slug | Use When | Example Values |
|---------------|------|----------|----------------|
| Difficulty | `difficulty` | Tutorials, DIY, maker topics | Easy, Medium, Advanced |
| Budget Level | `budget` | Ads, marketing, campaigns | Free, $50-200, $500+ |
| Engagement Type | `engagement` | Social media, content ideas | Likes, Shares, Saves |
| Production Effort | `effort` | Video, photo, creative content | Quick (<1h), Half-day, Multi-day |
| Industry | `industry` | Cross-industry showcases | E-commerce, SaaS, Beauty |

Default: `difficulty`. The Planner records its choice in `02-plan.json` → `tables.overview_flex_column`.

### Categorization
If concepts are categorized (recommended for 15+), use H2 category headings with H3 concept cards inside. If flat (no categories), list all concepts under a single `## {N} {Topic} Examples` H2.

### CTA Positions
- CTA#1: after **Quick Overview** section
- CTA#2: at the end of **Conclusion**

---

## Profile B — Ideas + Templates (`ideas_templates`)

**Typical size**: 5–15 concepts
**Target words**: 3,000–5,500

### Required H2 Order
1. `## Key Takeaways`
2. `## {N} {Topic} Ideas` — concepts as H3 inside (each with Script + Variations)
3. `## How to Prompt for {Topic}` (optional, include if concepts involve AI prompting)
4. `## Pro Tips for {Topic}`
5. `## FAQ`
6. `## Conclusion`

### Additional Requirements
- Every Concept Card MUST include **Script** field (Hook → Claim → Proof → CTA)
- Every Concept Card MUST include **Variations** field (≥2 variations)
- `How to Prompt` section should contain copy-paste prompt templates if applicable

### CTA Positions
- CTA#1: after 3rd or 4th concept card
- CTA#2: at the end of **Conclusion**

---

## Profile C — Mega Gallery (`mega`)

**Typical size**: 25–60+ concepts
**Target words**: 6,000–10,000

### Required H2 Order
1. `## Key Takeaways`
2. `## Master List` (Table)
3. Category sections (H2): `## {Category Name}` — concepts as H3 inside (lightweight cards)
4. `## How to Get Started with {Product}`
5. `## FAQ`
6. `## Conclusion`

### Master List Table
Columns must be exactly:
- `# | Concept | Category | Platform | Quick Description`

### Lightweight Card Format
Mega profile uses minimal cards:
```md
<!-- CONCEPT_CARD_START id="concept-{rank}" profile="mega" -->
### {rank}. {Concept Name}
{Scenario: 20–40 words}

<!-- EMBED_PLACEHOLDER ... --> (recommended, not required)

**Try it:** [CTA text](URL)
<!-- CONCEPT_CARD_END -->
```

### Categorization
Mandatory for Mega profile. Must have ≥3 categories.

### CTA Positions
- CTA#1: after **Master List** table
- CTA#2: at the end of **Conclusion**
