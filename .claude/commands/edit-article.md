# Edit Article Command (v2.0)

Edit and polish a blog article draft with **strategic** image generation (3-5 images max), opening optimization, and AEO enhancement.

## Usage

```
/edit-article [path/to/article.md]
```

## Core Philosophy (v2.0)

> **少即是多 (Less is More)** - 3 high-quality images beat 10 mediocre ones.

### Key Changes from v1.0

| v1.0 (Old) | v2.0 (New) |
|------------|------------|
| Fill ALL placeholders | Select 3-5 strategic positions |
| Nano Banana | Nano Banana Pro (higher quality) |
| ~$0.40/article (11 images) | ~$0.45-0.75/article (3-5 images) |
| Mechanical filling | Editorial judgment |

## What This Command Does

1. **Analyzes** the article structure and identifies key visual opportunities
2. **Selects** 3-5 strategic positions for images (NOT all placeholders)
3. **Designs** ICS-framework prompts for information-dense images
4. **Generates** images via FAL.ai Nano Banana Pro API
5. **Skips** unnecessary placeholders (explains why)
6. **Optimizes** opening paragraph for direct answer
7. **Enhances** AEO elements
8. **Outputs** edited article + detailed editor report

## Prerequisites

- `FAL_API_KEY` environment variable set
- Article draft with content (placeholders optional)
- SSH access to CDN server (for image upload)

## Output Files

- `01-article-edited.md` - Polished article with strategic images
- `04-editor-report.md` - Image strategy report with justifications

## Image Quantity Limits

| Article Type | Min | Max | Recommended |
|--------------|-----|-----|-------------|
| Tutorial | 2 | 4 | 3 |
| List | 3 | 5 | 4 |
| News | 1 | 3 | 2 |

## Strategic Image Positions

```
Position:    0%          33%          66%          100%
             ↓           ↓            ↓            ↓
             Hero        Concept      Comparison   CTA
             Cover       Diagram      Visual       (optional)
             (REQUIRED)  (if needed)  (if needed)
```

## Example

```
/edit-article /reports/2026-01-15-ai-video-guide/01-article-draft.md
```

---

## Instructions for Claude

When this command is invoked, follow the **Editor Skill v2.0** philosophy:

### Phase 1: Analyze Article

1. **Read the target article** to understand its structure
2. **Detect article type** from frontmatter `category` field:
   - `tutorial` - Step-by-step guides (3 images)
   - `list` - Best/Top X rankings (4 images)
   - `news` - Announcements (2 images)
3. **Identify key turning points** where visual aids add value

### Phase 2: Strategic Image Selection

**DO NOT** mechanically fill all placeholders. Instead:

1. **Always include**: Hero cover image (required)

2. **Ask for each position**:
   - Does this add value beyond decoration?
   - Is this concept hard to understand without visual?
   - Can one image convey 3+ information points?
   - Would a table/text work better?

3. **Select 3-5 positions** based on answers

4. **Skip and document** positions that don't pass the test:
   - Individual tool screenshots → Use comparison table
   - Decorative filler → Skip entirely
   - Repetitive patterns → Consolidate into one

### Phase 3: Design ICS Prompts

For each selected position, use the ICS framework:

```
I - Image Type: What format? (infographic, diagram, editorial)
C - Content: What 3-5 elements should it show?
S - Style: What aesthetic? (cinematic, McKinsey, modern)
```

Reference templates from `prompts/image-prompt-templates.yaml`

### Phase 4: Generate Images
图片生成和图片上传，请参考 AGENTS.md / ClAUDE.md 中的相关描述
Save to `./gen_images/` with role-based names:
   - `[slug]-hero.png`
   - `[slug]-concept.png`
   - `[slug]-comparison.png`

### Phase 5: Handle Skipped Positions

For placeholders NOT selected for image generation:

1. **Remove** the placeholder syntax
2. **Or replace** with appropriate alternative:
   - Table comparison
   - Text description
   - Link to documentation
3. **Document** in editor report why it was skipped

### Phase 6: Other Optimizations

1. **Evaluate opening quality**:
   - Check first 50 words for direct answer
   - Rewrite if weak patterns detected

2. **Enhance AEO elements**:
   - Add specific data points
   - Ensure FAQ answers standalone

3. **Apply format suggestions** based on article type

### Phase 7: Generate Outputs

1. **`01-article-edited.md`**:
   - Only selected positions have images
   - Unused placeholders removed/replaced

2. **`04-editor-report.md`** must include:
   - Image Strategy Summary (total placeholders vs generated)
   - Generated Images table (with "Why This Image?" column)
   - Skipped Positions table (with reasons)
   - Cost summary

3. **Update `00-implementation.md`** with editor phase status

### Phase 8: Report to User

Summary should include:
- "Generated X images (skipped Y positions)"
- Why each image was selected
- Total cost
- Opening optimization status

---

## Skill Reference

This command invokes the `editor` skill v2.0 from:
`skills/core/editor/SKILL.md`

Template library:
`skills/core/editor/prompts/image-prompt-templates.yaml`
