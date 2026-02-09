# Prompt Showcase Template -- Atomic Unit v1.0

> Reusable template for "visual gallery + copy-paste prompts" articles.
> First implementation: `2026-01-28-nano-banana-pro-prompt-styles`

---

## When to Use

Use this template when the article goal is: **look at the image, read the prompt, try it yourself**.

- Source material has multiple visual styles or prompt variations
- Each item needs an image + short description + copy-paste prompt
- NOT a long tutorial, NOT a case roundup -- this is a **gallery-first** format

---

## Article Structure

```markdown
---
title: "[Model/Tool]: [N] [Category] for [Use Case]"
slug: "{model}-{n}-{category}-{use-case}"
date: YYYY-MM-DD
author: "Alici AI Team"
category: "Prompt Engineering"
tags: ["{model}", "{category}", "prompt styles", "{use-case}"]
article_type: "prompt-showcase"
source_case: "{case-slug}"
word_count_target: "800-1200"
---

# {Title} (40-70 chars)

## {Hook} (30-50 words)
Viral proof or credibility signal + "here is the formula"

## The Prompt Formula (60-80 words)
Reveal the template pattern upfront:
```
[variable A], [style reference], [variable B]
```
Explain each element in 1-2 sentences.

## {N} Styles Gallery (550-700 words, ~60% of article)

### {#}. {Style Name}
![{Style Name}]({image-path})
**The Look**: 1 sentence, 15-25 words
**Try This Prompt**:
```
Full copy-paste prompt
```
---

[REPEAT x N]

## How to Try It (60-80 words)
1. Open [Alici AI {Product}]({product-url}) and select the model.
2. Copy any prompt above. Replace [variable] with your own.
3. Generate, review, iterate.

## FAQ (90-120 words)
3 questions with concise answers:
- Can I mix/combine styles?
- Do I need to describe my [subject] every time?
- Are these the exact prompts from [source]?

## Source and Attribution (30-40 words)
Credit original creator with links.

> Soft CTA to Alici AI product.
```

---

## Word Count Budget

| Section | Words | % |
|---------|-------|---|
| Hook | 30-50 | 4% |
| The Prompt Formula | 60-80 | 7% |
| Gallery (N x 50-65) | 550-700 | 60% |
| How to Try It | 60-80 | 7% |
| FAQ (3 questions) | 90-120 | 10% |
| Source + CTA | 50-70 | 6% |
| **Total** | **840-1,100** | 100% |

---

## Output Files

| File | Purpose |
|------|---------|
| `00-implementation.md` | Progress tracker |
| `01-article-draft.md` | Main article |
| `prompt_pack.md` | All prompts standalone, copy-paste ready |
| `asset_plan.json` | Maps images to article positions |

---

## Key Design Decisions

1. **Gallery = 60%** -- the gallery IS the article. Everything else is scaffolding.
2. **1 image per style** -- keeps gallery scannable. Archive extras for later use.
3. **Code block prompts** -- every prompt in a fenced code block for easy copying.
4. **3-step How to Try It** -- always exactly 3 steps. Step 1 links to product.
5. **FAQ = 3 questions** -- address mixing styles, consistency, and source attribution.
6. **Reconstructed prompts** -- if originals aren't public, note "inspired by" in FAQ.

---

## Replication Map

| Case | Gallery Items | Prompt Pattern | Product |
|------|---------------|----------------|---------|
| mitch0z-11-styles | 11 photography styles | `[person], in style of [photographer], [scene]` | Image Studio |
| 7-secret-prompts | 7 secret prompts | `[Blueprint/Vintage/Diorama/etc.] + [subject]` | Image Studio |
| machina-iphone-aesthetic | 4-6 iPhone looks | `[person], iPhone aesthetic, [params]` | Image Studio |
| midjourney-consistency | 5-8 examples | `[character] --cref [URL] [params]` | Image Studio |

---

## Checklist

Before publishing, verify:

- [ ] Title: 40-70 chars, includes model name + category
- [ ] Hook: references viral proof or credibility signal
- [ ] Formula: reveals template pattern before gallery
- [ ] Gallery: all N items present, each with image + "The Look" + prompt
- [ ] How to Try It: exactly 3 steps, step 1 links to product
- [ ] FAQ: 3 questions
- [ ] Source: credits original creator with URLs
- [ ] CTA: soft, at end
- [ ] Word count: 800-1,200
- [ ] prompt_pack.md: all prompts standalone
- [ ] asset_plan.json: all images mapped

---

*Template version: v1.0 | Created: 2026-01-28 | First use: nano-banana-pro-11-photography-styles*
