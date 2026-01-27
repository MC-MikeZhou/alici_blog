# AEO Analysis Report Template

Use this template to structure the output of every AEO analysis.

---

## Report Structure

```
═══════════════════════════════════════════════════════════════════════════════
                              AEO ANALYSIS REPORT
═══════════════════════════════════════════════════════════════════════════════
URL: [target URL]
Title: [page title]
Analysis Date: [current date]

OVERALL SCORE: [XX]/100  [Rating Emoji] [Rating Text]

Rating Scale:
  90-100: Excellent - Highly optimized for AI citation
  75-89:  Good - Solid foundation, minor improvements needed
  60-74:  Fair - Functional but missing key AEO elements
  40-59:  Poor - Significant gaps in AEO readiness
  0-39:   Critical - Not optimized for AI answer engines
═══════════════════════════════════════════════════════════════════════════════
```

---

## Module Scoring Display

For each module, use this format:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ MODULE 1: CONTENT STRUCTURE & PARSABILITY                        [XX/30]   │
├─────────────────────────────────────────────────────────────────────────────┤
│ Progress: ████████████████████░░░░░░░░░░                                   │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐│
│ │ 1.1 Title/H1/Description Alignment                              [X/4]  ││
│ │ Status: ✓ Pass | ⚠️ Partial | ✗ Fail                                    ││
│ │                                                                         ││
│ │ Finding: [Specific observation about this item]                         ││
│ │                                                                         ││
│ │ 💡 AEO Expert Insight:                                                  ││
│ │ [Educational explanation of why this matters for AI engines.            ││
│ │  Keep it concise but informative - this is the learning moment.]       ││
│ └─────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐│
│ │ 1.2 Heading Hierarchy                                           [X/4]  ││
│ │ ... (repeat for each item)                                              ││
│ └─────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Score Summary Table

After all modules, include:

```
═══════════════════════════════════════════════════════════════════════════════
                              SCORE SUMMARY
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────┬─────────┬─────────┬──────────────────┐
│ Module                              │ Score   │ Max     │ Visual           │
├─────────────────────────────────────┼─────────┼─────────┼──────────────────┤
│ 1. Content Structure & Parsability  │ XX      │ 30      │ ████████░░░░░░░░ │
│ 2. Technical Indexability           │ XX      │ 25      │ ██████████████░░ │
│ 3. Citation & E-E-A-T Signals       │ XX      │ 25      │ ██████░░░░░░░░░░ │
│ 4. Visibility & Measurement Design  │ XX      │ 20      │ ████████████░░░░ │
├─────────────────────────────────────┼─────────┼─────────┼──────────────────┤
│ TOTAL                               │ XX      │ 100     │                  │
└─────────────────────────────────────┴─────────┴─────────┴──────────────────┘

Positioning: [One-sentence summary of content's AEO readiness]
Example: "SEO-oriented content with moderate AEO readiness; key gaps in Schema and E-E-A-T signals."
```

---

## Citable Blocks Section

Identify content pieces most likely to be quoted by AI:

```
═══════════════════════════════════════════════════════════════════════════════
                           CITABLE BLOCKS IDENTIFIED
═══════════════════════════════════════════════════════════════════════════════
Content pieces with highest AI citation potential:

┌─────┬────────────────────────────────────────┬───────────┬──────────────────┐
│ #   │ Content Block                          │ Potential │ Schema Candidate │
├─────┼────────────────────────────────────────┼───────────┼──────────────────┤
│ 1   │ "[Exact quote or description]"         │ ⭐⭐⭐⭐⭐    │ HowTo            │
│     │ Location: [Section name]               │           │                  │
│     │ Why citable: [Reason]                  │           │                  │
├─────┼────────────────────────────────────────┼───────────┼──────────────────┤
│ 2   │ "[Exact quote or description]"         │ ⭐⭐⭐⭐     │ ItemList         │
│     │ Location: [Section name]               │           │                  │
│     │ Why citable: [Reason]                  │           │                  │
├─────┼────────────────────────────────────────┼───────────┼──────────────────┤
│ ... │ (Continue for 3-5 most citable blocks) │           │                  │
└─────┴────────────────────────────────────────┴───────────┴──────────────────┘

💡 AEO Expert Insight:
Citable blocks are self-contained statements that AI can quote without needing
surrounding context. The best citable blocks include: specific data, clear
definitions, step-by-step instructions, or definitive answers to common questions.
```

---

## Priority Recommendations Section

```
═══════════════════════════════════════════════════════════════════════════════
                        PRIORITY IMPROVEMENT RECOMMENDATIONS
═══════════════════════════════════════════════════════════════════════════════

🔴 HIGH PRIORITY (Do First - Highest ROI)
───────────────────────────────────────────────────────────────────────────────

┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. [Recommendation Title]                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ Current State:                                                              │
│ [What's wrong or missing now]                                               │
│                                                                             │
│ Recommended Action:                                                         │
│ [Specific, actionable steps to fix]                                         │
│                                                                             │
│ 📊 ROI & Growth Value:                                                      │
│ • Impact: [Quantified improvement, e.g., "+17% AI result scores"]           │
│ • Effort: [Low/Medium/High]                                                 │
│ • Timeline: [How quickly results may appear]                                │
│ • Business Value: [Connection to traffic/citations/conversions]             │
│                                                                             │
│ 💡 Why This Matters:                                                        │
│ [Brief explanation of the AEO principle behind this recommendation]         │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. [Next High Priority Recommendation]                                      │
│ ...                                                                         │
└─────────────────────────────────────────────────────────────────────────────┘


🟡 MEDIUM PRIORITY (Do Next - Good ROI)
───────────────────────────────────────────────────────────────────────────────

┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. [Recommendation Title]                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ Current State: [...]                                                        │
│ Recommended Action: [...]                                                   │
│ 📊 ROI & Growth Value: [...]                                                │
│ 💡 Why This Matters: [...]                                                  │
└─────────────────────────────────────────────────────────────────────────────┘


🟢 LOW PRIORITY (Nice to Have - Incremental Gains)
───────────────────────────────────────────────────────────────────────────────

┌─────────────────────────────────────────────────────────────────────────────┐
│ 5. [Recommendation Title]                                                   │
│ Quick win: [One-line description and expected small improvement]            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Benchmark Comparison (Optional)

If analyzing content for a specific niche, include competitive context:

```
═══════════════════════════════════════════════════════════════════════════════
                           BENCHMARK COMPARISON
═══════════════════════════════════════════════════════════════════════════════

Industry AEO Benchmarks (AI Video Tools Content):

┌─────────────────────────────────────┬─────────────┬─────────────┬──────────┐
│ Metric                              │ This Page   │ Top 10 Avg  │ Gap      │
├─────────────────────────────────────┼─────────────┼─────────────┼──────────┤
│ Schema Implementation               │ FAQ only    │ Article+FAQ │ -1 type  │
│ Author Visibility                   │ Brand only  │ Named+Bio   │ Missing  │
│ Source Citations                    │ 0           │ 3-5         │ -3 to -5 │
│ FAQ Questions (Topic-Relevant)      │ 0           │ 5-8         │ -5 to -8 │
│ Content Freshness                   │ 35 days     │ <90 days    │ ✓ Good   │
└─────────────────────────────────────┴─────────────┴─────────────┴──────────┘
```

---

## Quick Reference Key

```
Status Indicators:
  ✓  = Pass (meets AEO standards)
  ⚠️  = Partial (room for improvement)
  ✗  = Fail (needs immediate attention)

Priority Levels:
  🔴 High   = Critical for AEO success, highest ROI
  🟡 Medium = Important, good returns on effort
  🟢 Low    = Nice to have, incremental improvements

Citation Potential:
  ⭐⭐⭐⭐⭐ = Very High - Likely to be quoted verbatim
  ⭐⭐⭐⭐  = High - Strong candidate for AI extraction
  ⭐⭐⭐   = Medium - May be cited with improvements
  ⭐⭐    = Low - Needs restructuring to be citable
  ⭐     = Very Low - Unlikely to be cited as-is
```

---

## Report Footer

```
═══════════════════════════════════════════════════════════════════════════════
                              METHODOLOGY NOTE
═══════════════════════════════════════════════════════════════════════════════

This analysis is based on the AEO Evaluation Framework v1.0, synthesizing
guidance from official sources (Google, Microsoft, Bing) and industry research
(Forrester, Semrush, Ahrefs, SurferSEO).

Key quantitative benchmarks used:
• 78% of AI answers contain lists (SurferSEO)
• 95% of ChatGPT citations from content <10 months old (Semrush)
• +11.4% citation rate for semantic URLs (Perplexity research)
• +17.46% AI result scores for definition content (SurferSEO)
• +19.95% AI result scores for clear subheadings (SurferSEO)

For framework details, see: EVALUATION_FRAMEWORK.md
═══════════════════════════════════════════════════════════════════════════════
```

---

## Language Adaptation

### For Chinese Content, adapt labels:

```
═══════════════════════════════════════════════════════════════════════════════
                              AEO 分析报告
═══════════════════════════════════════════════════════════════════════════════
URL: [目标网址]
标题: [页面标题]
分析日期: [当前日期]

综合评分: [XX]/100  [评级 Emoji] [评级文本]

评级标准:
  90-100: 优秀 - AI 引用高度优化
  75-89:  良好 - 基础扎实，需要小幅改进
  60-74:  一般 - 功能性内容，缺少关键 AEO 元素
  40-59:  较差 - AEO 准备度存在显著差距
  0-39:   严重不足 - 未针对 AI 答案引擎优化
═══════════════════════════════════════════════════════════════════════════════

模块标题翻译:
• Content Structure & Parsability → 内容结构与可解析性
• Technical Indexability → 技术可索引性
• Citation & E-E-A-T Signals → 引用与 E-E-A-T 信号
• Visibility & Measurement Design → 可见性与度量设计

标签翻译:
• AEO Expert Insight → 💡 AEO 专家解读
• ROI & Growth Value → 📊 ROI 与增长价值
• Citable Blocks Identified → 可引用内容块识别
• Priority Improvement Recommendations → 优先改进建议
• High Priority → 🔴 高优先级
• Medium Priority → 🟡 中优先级
• Low Priority → 🟢 低优先级
```
