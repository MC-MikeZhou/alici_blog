# CTA_CARD v2.0 — Shared Component

> Friction-Aligned CTA Placement System for all Writer Skills.
> **Version**: 2.0
> **Updated**: 2026-02-07
> **Used by**: blog-tutorial-writer, blog-list-writer, blog-showdown-writer

---

## Philosophy

CTAs should appear at **friction points** where users naturally seek solutions, not arbitrary fixed positions.

---

## CTA_CARD v2.0 Format

```markdown
<!-- CTA_CARD
  position: "after-step-3|after-troubleshooting|end|after-quick-answer|after-category-winners"
  trigger: "friction_point|achievement|decision"
  friction_context: "User's mental state at this point (50-100 words)"
  product: "alici-ai|specific-product-id"
  cta_type: "try_free|learn_more|see_pricing"
-->

[CTA Card Content Here - Generated based on friction_context]

<!-- /CTA_CARD -->
```

## Attributes

| Attribute | Required | Values | Purpose |
|-----------|----------|--------|---------|
| `position` | ✅ Yes | after-step-N, after-troubleshooting, after-quick-answer, after-category-winners, end | Physical placement in article |
| `trigger` | ✅ Yes | friction_point, achievement, decision | Why CTA appears here |
| `friction_context` | ✅ Yes | Free text (50-100 words) | Explains user's mental state at this point |
| `product` | ✅ Yes | alici-ai, specific-product-id | Which product to promote |
| `cta_type` | ✅ Yes | try_free, learn_more, see_pricing | CTA action type |

---

## Friction Points by Trigger Type

| Friction Point | User Mental State | CTA Trigger | Example Context |
|----------------|-------------------|-------------|-----------------|
| **Just learned complex workflow** | "This seems hard..." | `friction_point` | After Step 3 (7-element prompt structure) |
| **Completed key milestone** | "I did it! What's next?" | `achievement` | After successfully generating first video |
| **Facing tool choice** | "Which should I use?" | `decision` | Before tool selection step |
| **Hit troubleshooting** | "Something's broken..." | `friction_point` | In troubleshooting section |
| **Finished reading comparison** | "OK, now what?" | `achievement` | End of category winners |

---

## Placement Strategies (Per Skill)

### Tutorial (blog-tutorial-writer)

Context-aware, friction-aligned CTAs (not fixed positions):

| Position | CTA Type | Trigger | Frequency |
|----------|----------|---------|-----------|
| After Introduction (optional) | Quick Start | `decision` | 0-1x |
| After Complex Step | Simplification Offer | `friction_point` | 1-2x |
| After Achievement | Upgrade/Next Step | `achievement` | 0-1x |
| Conclusion | Strong CTA | `achievement` | 1x (mandatory) |

### Listicle (blog-list-writer)

Blueprint-driven CTA markers (lintable):

| Position | CTA Marker | Trigger | Frequency |
|----------|------------|---------|-----------|
| End of Quick Answer | `<!-- CTA:1 -->` | `decision` | 1x (mandatory) |
| End of Final Verdict (Profile A/B/D) | `<!-- CTA:2 -->` | `achievement` | 1x (mandatory) |
| End of Category Winners (Profile C mega) | `<!-- CTA:2 -->` | `achievement` | 1x (mandatory) |

### Showdown (blog-showdown-writer)

3 fixed positions in 11-heading structure:

| Position | CTA # | Trigger | Frequency |
|----------|-------|---------|-----------|
| After Quick Answer | CTA #1 | `decision` | 1x (mandatory) |
| After Category Winners | CTA #2 | `achievement` | 1x (mandatory) |
| In Final Verdict | CTA #3 | `achievement` | 1x (mandatory) |

---

## CTA Copy Patterns

### Soft CTA (after Quick Answer / early in article)

```markdown
> 💡 **Not sure which to pick?** Try them all free on alici.ai first.
> [Try All Models Free →](https://app.alici.ai)
```

### Contextual CTA (after comparison / category winners)

```markdown
> **Skip the signup chaos** — compare all [N] models in one platform.
> [Compare Side by Side →](https://app.alici.ai/pages/videoGen)
```

### Strong CTA (final verdict / conclusion)

```markdown
Ready to create your own professional AI videos? alici.ai gives you access to
**Kling 2.0, Runway Gen-4, and Google Veo 3** in one platform—no switching between tools.

**[Create AI Videos Now →](https://app.alici.ai/pages/videoGen)**
```

### Friction Point CTA (after complex step)

```markdown
**Feeling overwhelmed by prompt engineering?** alici.ai simplifies the process—just
describe what you want, and our AI handles the complexity automatically.

> 💡 **Skip the complexity**: Generate professional prompts in 1 click
> [Try AI Prompt Studio Free →](https://app.alici.ai/pages/promptStudio)
```

---

## Product Mapping

CTAs must reference products from `/skills/_docs/PRODUCT_CATALOG.md`.

**Common products**:

| Product ID | Name | URL | Default CTA Text |
|------------|------|-----|-------------------|
| `video_studio` | AI Video Studio | `https://app.alici.ai/pages/videoGen` | Create AI Videos Now |
| `image_studio` | AI Image Studio | `https://app.alici.ai/pages/imageGen` | Generate AI Images Free |
| `alici-ai` | alici.ai (general) | `https://alici.ai` | Try alici.ai Free |

---

## Version History

### v2.0 (2026-02-05)
- Friction-aligned placement system
- Structured CTA_CARD format with 5 attributes
- Per-skill placement strategies
- Extracted as shared component (v2.0.1, 2026-02-07)

### v1.0 (Prior)
- Fixed-position CTAs
- No friction context
