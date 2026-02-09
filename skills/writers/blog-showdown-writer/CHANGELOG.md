# blog-showdown-writer Changelog

## v1.0 (2026-02-07)

**Initial Release — Independent Showdown Skill** ⭐

Extracted from `blog-list-writer v3.0` mode=tool_showdown and upgraded into a standalone skill.

### What's New

1. **Independent Skill**:
   - Separated from blog-list-writer as standalone `blog-showdown-writer`
   - Own SKILL.md, SHOWDOWN_TEMPLATE.md, CHANGELOG.md
   - Independent routing from smart-launcher

2. **Showdown Plan (from Listicle's Plan Pack pattern)**:
   - `showdown-plan.json` output — tool pool, comparison dimensions, evidence chain, CTA plan
   - Structured planning before writing (compile-like approach)

3. **Showdown Validator Gate (from Listicle's Validator pattern)**:
   - PASS/FAIL validation before downstream processing
   - Checks: 11-heading order, table presence, CTA positions, Source Attribution

4. **evidence_level Guardrails (from Listicle's methodology_level)**:
   - `source_based` / `hybrid` / `hands_on` — controls allowed claims
   - Prevents false methodology claims

5. **Shared Components**:
   - CTA_CARD v2.0 → references `_shared/CTA_CARD_v2.0.md`
   - IMAGE_PLACEHOLDER v2.0 → references `_shared/IMAGE_PLACEHOLDER_v2.0.md`

6. **Preserved Showdown-Specific Features**:
   - P4 Reframe mandatory opening (from TOOL_SHOWDOWN_TEMPLATE v1.2)
   - L4 Integrator positioning (from TOOL_SHOWDOWN_TEMPLATE v1.2)
   - Source Attribution section (from TOOL_SHOWDOWN_TEMPLATE v1.2)
   - 11 fixed headings structure
   - Category Winners with Choose/Avoid
   - Decision Tree with If/Then
   - Citation density ≥5/千字
   - Rewrite constraints (tool_count ≤3)

### Origin

- **TOOL_SHOWDOWN_TEMPLATE.md v1.2** → Heading structure, strategic positioning, source attribution
- **blog-list-writer v3.0 mode=tool_showdown** → Execution flow, verified_tools input, AEO checklist
- **blog-list-writer v3.0 Listicle patterns** → Plan Pack, Validator Gate, methodology guardrails (adapted)

### Files

| File | Lines | Purpose |
|------|-------|---------|
| `SKILL.md` | ~900 | Complete skill specification (§1-§12) |
| `SHOWDOWN_TEMPLATE.md` | ~627 | Reference template (copied from _docs/) |
| `CHANGELOG.md` | This file | Version history |
