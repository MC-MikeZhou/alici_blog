# Writer Feedback Template v1.0

> 用于 Human Review Checklist 的 Writer Feedback Loop
> 当 Module 3 (竞品推荐) 或 Module 6 (Promise-Delivery) 发现无法自动修复的问题时使用

---

## 模板结构

```markdown
# Writer Feedback from Human Review

**Article**: {article_title}
**Review Date**: {date}
**Feedback Type**: CONTENT_REVISION_REQUIRED
**Round**: {round_number}/2

---

## Issues Requiring Rewrite

{issues_list}

---

## Instructions for Writer

1. Address each issue above
2. Return **only the revised sections** (not the full article)
3. Maintain existing style and structure
4. Do not introduce new issues
5. Mark your changes with `<!-- REVISED -->` comment

## After Revision

The Human Review will re-run automatically on revised content.
Maximum revision rounds: 2

---

*Human Review Checklist v1.0*
```

---

## Issue Templates

### Module 3: Competitor Recommendation

```markdown
### Issue {n}: Competitor Recommendation

**Module**: 3 - Competitor Mention Scan
**Severity**: ⛔ BLOCKING
**Location**: Line {line_number}

**Original Text**:
> {original_text}

**Problem**: Direct recommendation to competitor "{competitor_name}"

**Pattern Detected**: "{pattern}"

**Required Fix** (choose one):

**Option A - Neutral Description**:
Change to objective feature description:
> "{competitor_name} offers {feature}"
> "{competitor_name} integrates with {tool}"

**Option B - Add alici.ai Alternative**:
Add alici.ai as an alternative option:
> "...or use alici.ai which provides access to multiple AI tools including {competitor_name}"

**Option C - Remove Recommendation**:
Remove the recommendation entirely and keep only factual comparison.

---

**Your Revised Text**:
```
[Paste your revised paragraph here]
```
```

### Module 6: Promise-Delivery Mismatch

```markdown
### Issue {n}: Promise-Delivery Mismatch

**Module**: 6 - Promise-Delivery Check
**Severity**: ⚠️ WARNING
**Type**: {mismatch_type}

**Title Promise**:
> {title_text}

**Actual Content**:
> {content_summary}

**Mismatch Details**:
- Expected: {expected}
- Found: {found}

**Required Fix** (choose one):

**Option A - Add Missing Content**:
{add_content_suggestion}

**Option B - Modify Title**:
Change title to accurately reflect content:
> "{suggested_title}"

---

**Your Action**:
- [ ] Option A: I will add the missing content
- [ ] Option B: Change title to: "{suggested_title}"

**If Option A, provide the additional content**:
```
[Paste additional content here]
```
```

---

## Mismatch Type Templates

### Number Mismatch

```markdown
**Type**: Number Promise Mismatch

**Title Promise**: "{n} Best AI Video Generators"
**Actual Content**: Only {actual_count} tools covered in detail

**Required Fix**:
- Option A: Add {missing_count} more tool(s) to reach {n}
- Option B: Change title to "{actual_count} Best AI Video Generators"
```

### Year Mismatch

```markdown
**Type**: Year Promise Mismatch

**Title Promise**: "...in 2026"
**Actual Content**: No 2026-specific data found

**Required Fix**:
- Option A: Add 2026 data points (pricing, features, updates)
- Option B: Remove year from title if content is evergreen
```

### Scope Mismatch

```markdown
**Type**: Scope Promise Mismatch

**Title Promise**: "Complete Guide to..."
**Actual Content**: Word count {actual_words} (expected 2000+)

**Required Fix**:
- Option A: Expand content to be more comprehensive
- Option B: Change title to "Quick Guide to..." or "Introduction to..."
```

### How-To Mismatch

```markdown
**Type**: How-To Promise Mismatch

**Title Promise**: "How to {action}"
**Actual Content**: No clear step-by-step instructions found

**Required Fix**:
- Option A: Add numbered steps showing how to {action}
- Option B: Change title to remove "How to" if article is informational
```

---

## Response Format

Writer should respond with:

```markdown
# Writer Revision Response

**Article**: {article_title}
**Feedback Round**: {round_number}

## Revisions Made

### Issue 1: {issue_title}
**Chosen Option**: {A/B/C}
**Revised Content**:
```
{revised_content}
```

### Issue 2: {issue_title}
**Chosen Option**: {A/B/C}
**Revised Content**:
```
{revised_content}
```

## Notes
{any_additional_notes}
```

---

## Feedback Loop Rules

1. **Maximum 2 rounds**: If issues persist after 2 rounds, mark as `MANUAL_REVIEW_REQUIRED`
2. **Partial revision accepted**: Writer can address some issues and mark others for human review
3. **No new issues**: Writer should not introduce new problems while fixing existing ones
4. **Preserve structure**: Revisions should maintain article structure and flow
