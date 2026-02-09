# Writer Shared Components Index

> Registry of shared components used across all Writer Skills.
> **Version**: 1.0
> **Updated**: 2026-02-07

---

## Component Registry

| Component | Version | File | Purpose |
|-----------|---------|------|---------|
| **CTA_CARD** | v2.0 | `_shared/CTA_CARD_v2.0.md` | Friction-aligned CTA placement system |
| **IMAGE_PLACEHOLDER** | v2.0 | `_shared/IMAGE_PLACEHOLDER_v2.0.md` | Structured image placeholder system |

---

## Usage by Skill

| Skill | CTA_CARD v2.0 | IMAGE_PLACEHOLDER v2.0 |
|-------|---------------|------------------------|
| **blog-tutorial-writer** v3.1 | ✅ Context-aware, friction-aligned | ✅ 5-7 images per article |
| **blog-list-writer** v3.1 | ✅ Blueprint-driven CTA markers | ✅ 10-15 images per article |
| **blog-showdown-writer** v1.0 | ✅ 3 fixed positions | ✅ 4-8 images per article |

---

## How to Reference

In each Writer's SKILL.md, reference shared components like this:

```markdown
### CTA Placement

> **Shared Component**: See `_shared/CTA_CARD_v2.0.md` for full CTA_CARD v2.0 format,
> attributes, copy patterns, and product mapping.
>
> This skill uses the **[Tutorial/Listicle/Showdown]** placement strategy defined there.
```

```markdown
### Image Placeholders

> **Shared Component**: See `_shared/IMAGE_PLACEHOLDER_v2.0.md` for full IMAGE_PLACEHOLDER v2.0
> format, type definitions, priority guidelines, and asset pipeline integration.
>
> This skill uses the **[Tutorial/Listicle/Showdown]** placement strategy defined there.
```

---

## Non-Shared Components (Skill-Specific)

These components remain in their respective SKILL.md files:

| Component | Owner | Why Not Shared |
|-----------|-------|----------------|
| Citable Block Taxonomy v3.0 | blog-tutorial-writer | Tutorial-specific, 7 types with complex rules |
| Self-Check JSON | blog-tutorial-writer | Tutorial-specific schema |
| Listicle Validator Gate | blog-list-writer | Listicle-specific PASS/FAIL |
| Blueprint Profiles (A/B/C/D) | blog-list-writer | Listicle-specific structure |
| Plan Pack Bundle | blog-list-writer | Listicle-specific output |
| methodology_level guardrails | blog-list-writer | Listicle-specific trust rules |
| Showdown Validator Gate | blog-showdown-writer | Showdown-specific PASS/FAIL |
| P4 Reframe opening | blog-showdown-writer | Showdown-specific opening |
| L4 Integrator positioning | blog-showdown-writer | Showdown-specific positioning |
| Source Attribution section | blog-showdown-writer | Showdown-specific evidence |
| evidence_level guardrails | blog-showdown-writer | Showdown-specific trust rules |

---

## Shared Documents (Already Existing)

These documents are already shared across skills via `/skills/_docs/`:

| Document | Path | Used By |
|----------|------|---------|
| BLOG_WRITING_PRINCIPLES_v2.md | `/skills/_docs/` | All Writers |
| PRODUCT_CATALOG.md | `/skills/_docs/` | All Writers |
| LISTICLE_BLUEPRINTS_v3.md | `/skills/_docs/` | blog-list-writer |

---

## Version History

### v1.0 (2026-02-07)
- Initial component registry
- Extracted CTA_CARD v2.0 and IMAGE_PLACEHOLDER v2.0 from tutorial/list writers
- Documented skill-specific vs shared components
