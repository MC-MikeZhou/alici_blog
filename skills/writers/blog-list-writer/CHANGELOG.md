# blog-list-writer Changelog

All notable changes to the Blog List Writer skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.0] - 2026-02-04

### Added

- **Listicle profiles + enforced blueprints (A/B/C/D)**:
  - `standard | prompt_workflow | mega | alternatives`
  - Fixed H2 order + required tables + fixed table column names + lintable CTA markers
- **Plan Pack bundle outputs** for listicles:
  - `01-article-draft.md` + `02-plan.json` + `03-assets.json`
  - Optional: `01-article.md` (copy) + `04-listicle-validator-report.json`
- **Listicle Validator gate**:
  - New lint step: `python3 scripts/listicle_validator.py --dir <output_dir>`
  - Structure is PASS/FAIL; evidence gaps are WARNINGS (non-blocking) per policy
- **Methodology guardrails** via `methodology_level`:
  - `research_only | hybrid | hands_on`
  - Prevents trust failures (e.g., research_only cannot claim “we tested”)
- **Assets queue contract**:
  - `03-assets.json` includes `recommended_generate_max=5` (editor-safe default)
  - Requires featured image + ≥2 diagrams (comparison infographic + decision tree recommended)
- **Regression fixtures** for validator:
  - `skills/writers/blog-list-writer/testdata/standard`
  - `skills/writers/blog-list-writer/testdata/prompt_workflow`
  - `skills/writers/blog-list-writer/testdata/mega`

### Changed

- **Listicle word-count strategy**:
  - v2 list default 2,500–3,500 → v3 profile-based 4,500–10,000
- **AEO structure tightened**:
  - `## Quick Answer` must be 120–180 words
  - `## Key Takeaways` mandated
  - `## FAQ + Final Verdict` requires ≥6 FAQs (2–4 sentence answers)
- **Tables become machine-parsable**:
  - Required tables must exist
  - Column names are fixed (validator enforces exact headers)
- **CTA becomes lintable**:
  - `<!-- CTA:1 --> ... <!-- /CTA -->` at end of Quick Answer
  - `<!-- CTA:2 --> ... <!-- /CTA -->` at end of Final Verdict (or Category Winners for mega)
- **Tool entries become lintable**:
  - Tool Card required fields + order enforcement

### Fixed

- **Unstable first drafts for large listicles**:
  - Reduced “structure drift” by making the output compile-like (Blueprint + Validator)
- **Domain-unfamiliar empty content failure mode**:
  - Forces planning artifacts (plan.json) before writing long-form body
- **“Fake testing” trust risk**:
  - Methodology-level guardrails prevent unsupported “we tested X+” claims

### Upgrade Notes (v2 list → v3 listicle)

Breaking changes for `content_type=list`:
- Outputs are now a required bundle: `01-article-draft.md` + `02-plan.json` + `03-assets.json`
- Downstream pipeline must run validator gate first:
  - `python3 scripts/listicle_validator.py --dir <output_dir>`
- Headings/tables/CTAs/tool cards are now **strictly enforced** by blueprint + validator

Tool Showdown (`content_type=tool_showdown`) is unchanged in v3.0.

---

## [2.4] - 2026-01-26 (Implicit)

This version did not have a dedicated changelog entry at the time. The date is used as a **documentation snapshot** aligned with the broader v2.2/v2.3 ecosystem updates.

### Added / Changed
- List listicles with:
  - Year-in-title rules + title formulas
  - Evaluation methodology section (5-dimension framework)
  - Comparison table with one-line “Core Positioning”

### Limitations (known)
- List mode structure was still **guideline-based**, not blueprint-enforced
- No plan-pack outputs; downstream steps often had to reverse-infer structure
- No lint gate; large listicles frequently needed editor “structural rescue”

---

## [2.3] - 2026-01-21

### Added
- Strategic principles for `tool_showdown`:
  - Beginner-first positioning
  - Conversion-oriented CTA philosophy (“try before you commit” framing)

---

## [2.2] - 2026-01-21

### Added
- `content_type=tool_showdown` mode
- Version verification integration (`verified_tools` from smart-root)
- Enforced showdown structure (template-driven tables/CTAs/decision tree)

---

## [2.1] - 2026-01-18

### Added
- Dependency validation for required docs (writing principles + product catalog)

---

## [2.0] - 2026-01-18

### Added
- Mandatory year + number in title (strict validation rules)
- Evaluation Methodology section template (5-dimension framework)
- Enhanced comparison table with “Core Positioning” column

---

## [1.0] - 2025-XX-XX

### Initial Release
- Basic list article structure and templated tool entries
- Compatible with downstream editor/AEO/export steps (v1 pipeline)

