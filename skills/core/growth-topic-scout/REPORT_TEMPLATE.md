# Growth Topic Scout Report Templates v2.1

Use these templates to structure the output of competitive topic analysis (Mode A), keyword matrix analysis (Mode B), and AEO validation (Mode C).

**v2.1 Changes**: Added Mode C (AEO Validation) templates, dual scoring (SEO + AEO), and LLM citation analysis sections.

---

## Mode Detection

| Input Type | Mode | Template |
|------------|------|----------|
| Competitor URL(s) | Mode A + C | URL Analysis Report + AEO Validation |
| Seed keyword + trigger words | Mode B + C | Keyword Matrix Report + AEO Validation |
| "AEO验证", "AI visibility" | Mode C only | AEO Validation Report |

**Note**: Mode C (AEO Validation) is enabled by default for all analyses in v2.1.

---

# Mode A: URL Analysis Report Template

## Report Structure

```
===============================================================================
                         GROWTH TOPIC SCOUT REPORT
                              Mode A: URL Analysis
===============================================================================
Analysis Date: [YYYY-MM-DD]
Competitor URLs Analyzed: [N]
Topics Discovered: [N]
Validated Opportunities: [N]

EXECUTIVE SUMMARY
-------------------------------------------------------------------------------
- [Key finding 1 - most important opportunity]
- [Key finding 2 - competitive gap discovered]
- [Key finding 3 - quick win identified]
- [Key finding 4 - AEO opportunity highlight]
- [Recommended next action]
===============================================================================
```

---

## Competitor Content Analysis

For each competitor URL analyzed:

```
+-----------------------------------------------------------------------------+
| COMPETITOR ANALYSIS #1                                                       |
+-----------------------------------------------------------------------------+
| URL: [competitor URL]                                                        |
| Title: [article title]                                                       |
| Type: [Tutorial / List / News / Comparison / Guide]                          |
| Est. Word Count: [X,XXX words]                                               |
+-----------------------------------------------------------------------------+
| TOPIC TREE                                                                   |
| +-- Primary: [main topic]                                                    |
| +-- Sub-topic 1: [H2 section theme]                                          |
| +-- Sub-topic 2: [H2 section theme]                                          |
| +-- Sub-topic N: [H2 section theme]                                          |
+-----------------------------------------------------------------------------+
| KEY ENTITIES IDENTIFIED                                                      |
| - Products/Tools: [list]                                                     |
| - Concepts: [list]                                                           |
| - Competitors mentioned: [list]                                              |
+-----------------------------------------------------------------------------+
| QUERY SEEDS EXTRACTED: [N total]                                             |
| - How-to: [N] queries                                                        |
| - What-is: [N] queries                                                       |
| - Best/List: [N] queries                                                     |
| - Comparison: [N] queries                                                    |
| - Problem-solving: [N] queries                                               |
+-----------------------------------------------------------------------------+
```

---

## Top 10 Topic Opportunities

```
===============================================================================
                       TOP 10 TOPIC OPPORTUNITIES
===============================================================================
Ranked by Opportunity Score (Demand x AEO Potential x Gap x Fit)
```

For each opportunity:

```
+-----------------------------------------------------------------------------+
| #1 * EXCELLENT OPPORTUNITY                              Score: [XX]/100     |
+-----------------------------------------------------------------------------+
| PRIMARY KEYWORD                                                              |
| "[target keyword/query]"                                                     |
|                                                                              |
| SEARCH INTENT: [How-to / What-is / Best-List / Comparison / Problem-solving]|
+-----------------------------------------------------------------------------+
| RECOMMENDED TITLES                                                           |
| 1. "[Title option 1]"                                                        |
| 2. "[Title option 2]"                                                        |
| 3. "[Title option 3]"                                                        |
+-----------------------------------------------------------------------------+
| CONTENT TYPE: [Tutorial / List / News / Comparison]                          |
| RECOMMENDED SKILL: [blog-tutorial-writer / blog-list-writer / blog-news-writer]|
+-----------------------------------------------------------------------------+
| OUTLINE (H2/H3 Structure)                                                    |
|                                                                              |
| H1: [Recommended title]                                                      |
| +-- H2: [Section 1]                                                          |
| |   +-- H3: [Subsection]                                                     |
| |   +-- H3: [Subsection]                                                     |
| +-- H2: [Section 2]                                                          |
| +-- H2: [Section 3]                                                          |
| +-- H2: FAQ / Key Takeaways                                                  |
+-----------------------------------------------------------------------------+
| AEO ANSWER BLOCK (40-60 words)                                               |
|                                                                              |
| Target Question: "[Question this content should answer]"                     |
|                                                                              |
| Direct Answer Draft:                                                         |
| "[40-60 word answer that could be quoted by AI engines. Should be           |
|   self-contained, factual, and directly address the question.]"             |
+-----------------------------------------------------------------------------+
| EVIDENCE & SCORING                                                           |
|                                                                              |
| +-------------------+--------+---------------------------------------------+ |
| | Dimension         | Score  | Evidence                                    | |
| +-------------------+--------+---------------------------------------------+ |
| | Demand Signal     | XX/30  | [SERP features found, search suggest, etc.] | |
| | AEO Potential     | XX/25  | [PAA presence, answer box opportunity]      | |
| | Competition Gap   | XX/25  | [How AliciBlog can differentiate]           | |
| | Business Fit      | XX/20  | [Relevance to AI tools focus]               | |
| +-------------------+--------+---------------------------------------------+ |
| | TOTAL             | XX/100 |                                             | |
| +-------------------+--------+---------------------------------------------+ |
+-----------------------------------------------------------------------------+
| ALICIBLOG DIFFERENTIATION ANGLE                                              |
|                                                                              |
| "[How AliciBlog should approach this differently than the competitor.       |
|   Specific angle, unique value proposition, or gap to exploit.]"            |
+-----------------------------------------------------------------------------+
```

---

## Opportunity Summary Table

```
===============================================================================
                         OPPORTUNITY SUMMARY
===============================================================================

+-----+------------------------------+-------+----------+---------------------+
| #   | Primary Keyword              | Score | Type     | Recommended Skill   |
+-----+------------------------------+-------+----------+---------------------+
| 1   | [keyword]                    | XX    | Tutorial | blog-tutorial-writer|
| 2   | [keyword]                    | XX    | List     | blog-list-writer    |
| 3   | [keyword]                    | XX    | How-to   | blog-tutorial-writer|
| ...                                                                         |
| 10  | [keyword]                    | XX    | News     | blog-news-writer    |
+-----+------------------------------+-------+----------+---------------------+

QUICK WINS (High potential, low effort):
- [Topic] - [Why it's a quick win]
- [Topic] - [Why it's a quick win]

CONTENT GAPS (Topics competitor covers that AliciBlog doesn't):
- [Gap 1]
- [Gap 2]
```

---

## Next Actions

```
===============================================================================
                            NEXT ACTIONS
===============================================================================

IMMEDIATE (This Week):
+-----------------------------------------------------------------------------+
| 1. [Action] - [Topic] -> [Skill to use]                                     |
| 2. [Action] - [Topic] -> [Skill to use]                                     |
+-----------------------------------------------------------------------------+

SHORT-TERM (This Month):
+-----------------------------------------------------------------------------+
| 3. [Action] - [Topic] -> [Skill to use]                                     |
| 4. [Action] - [Topic] -> [Skill to use]                                     |
+-----------------------------------------------------------------------------+

BACKLOG (When Resources Allow):
- [Topic] - [Brief reason]
- [Topic] - [Brief reason]

===============================================================================
```

---

# Mode B: Keyword Matrix Report Template (NEW in v2.0)

## Matrix Report Structure

```
===============================================================================
                    KEYWORD MATRIX ANALYSIS REPORT
                         Mode B: Scale SEO
===============================================================================
Seed Keyword: [seed keyword]
Analysis Date: [YYYY-MM-DD]
Total Keywords Generated: [N]
After Validation: [N]
Top 20 Opportunities Identified: [N]

EXECUTIVE SUMMARY
-------------------------------------------------------------------------------
- Total Keywords Analyzed: [N]
- High Priority (Score 80+): [N]
- Medium Priority (Score 60-79): [N]
- Top Opportunity: "[keyword]" (Score: [XX])
- Estimated Content Production Cost: ~$[X.XX] (DataForSEO)
-------------------------------------------------------------------------------
Key Insights:
- [Insight 1 - market opportunity]
- [Insight 2 - competitor weakness pattern]
- [Insight 3 - differentiation strategy]
===============================================================================
```

---

## Matrix Expansion Summary

```
+-----------------------------------------------------------------------------+
| MATRIX EXPANSION SUMMARY                                                     |
+-----------------------------------------------------------------------------+
| Seed Keyword: "[seed keyword]"                                               |
+-----------------------------------------------------------------------------+
| EXPANSION STRATEGIES USED                                                    |
| +-- Modifiers (best, free, top, etc.): [N] keywords                         |
| +-- Intent Words (how to, vs, tutorial, etc.): [N] keywords                 |
| +-- Use Cases (for YouTube, for TikTok, etc.): [N] keywords                 |
| +-- Time Markers (2026, latest, new): [N] keywords                          |
| +-- Tool Names (specific tools): [N] keywords                               |
| +-- DataForSEO API Expansion: [N] keywords                                  |
+-----------------------------------------------------------------------------+
| DEDUPLICATION                                                                |
| - Keywords before dedup: [N]                                                 |
| - Keywords after dedup: [N]                                                  |
| - Duplicates removed: [N]                                                    |
+-----------------------------------------------------------------------------+
```

---

## Top 20 Priority Topics

```
===============================================================================
                       TOP 20 PRIORITY TOPICS
===============================================================================
Ranked by Opportunity Score (Volume x Trend x Gap x CPC)

TIER 1: HIGH PRIORITY (Score 80+)
-------------------------------------------------------------------------------
| #  | Topic                              | Volume  | Trend | Type      | Score |
|----|------------------------------------|---------+-------+-----------+-------|
| 1  | [keyword]                          | [X,XXX] | [up]  | [Listicle]| [XX]  |
| 2  | [keyword]                          | [X,XXX] | [up]  | [Tutorial]| [XX]  |
| 3  | [keyword]                          | [X,XXX] | [up]  | [Showdown]| [XX]  |
-------------------------------------------------------------------------------

TIER 2: MEDIUM-HIGH PRIORITY (Score 70-79)
-------------------------------------------------------------------------------
| #  | Topic                              | Volume  | Trend | Type      | Score |
|----|------------------------------------|---------+-------+-----------+-------|
| 4  | [keyword]                          | [X,XXX] | [->]  | [Tutorial]| [XX]  |
| 5  | [keyword]                          | [X,XXX] | [up]  | [List]    | [XX]  |
| 6  | [keyword]                          | [X,XXX] | [->]  | [How-to]  | [XX]  |
-------------------------------------------------------------------------------

TIER 3: MEDIUM PRIORITY (Score 60-69)
-------------------------------------------------------------------------------
| #  | Topic                              | Volume  | Trend | Type      | Score |
|----|------------------------------------|---------+-------+-----------+-------|
| 7  | [keyword]                          | [X,XXX] | [->]  | [Guide]   | [XX]  |
| 8  | [keyword]                          | [X,XXX] | [down]| [News]    | [XX]  |
| ... (remaining topics)                                                       |
-------------------------------------------------------------------------------

Trend Legend: [up] = Rising, [->] = Stable, [down] = Declining
```

---

## Gap Analysis Summary

```
===============================================================================
                         GAP ANALYSIS SUMMARY
===============================================================================

COMMON COMPETITOR WEAKNESSES
-------------------------------------------------------------------------------
| Weakness                      | Occurrence | Avg Score Impact |
|-------------------------------|------------|------------------|
| Outdated content (>6 months)  | [XX]%      | +25              |
| No FAQ section                | [XX]%      | +10              |
| Word count < 1500             | [XX]%      | +15              |
| No author bio                 | [XX]%      | +15              |
| Poor H2/H3 structure          | [XX]%      | +15              |
| No data/statistics            | [XX]%      | +15              |
-------------------------------------------------------------------------------

AGGREGATE COMPETITOR INSIGHTS
-------------------------------------------------------------------------------
| Metric                        | Average    | Target (Beat)    |
|-------------------------------|------------|------------------|
| Word Count                    | [X,XXX]    | [X,XXX+]         |
| H2 Count                      | [X.X]      | [X+]             |
| FAQ Presence Rate             | [XX]%      | 100%             |
| Author Presence Rate          | [XX]%      | 100%             |
| Average Content Age           | [X.X] mo   | < 3 months       |
-------------------------------------------------------------------------------

RECOMMENDED DIFFERENTIATION STRATEGIES
-------------------------------------------------------------------------------
1. **Freshness**: [Strategy 1]
2. **Depth**: [Strategy 2]
3. **E-E-A-T**: [Strategy 3]
4. **AEO**: [Strategy 4]
5. **Unique Data**: [Strategy 5]
===============================================================================
```

---

## Per-Topic Gap Analysis

For each of the Top 20 topics:

```
+-----------------------------------------------------------------------------+
| #1: "[keyword]"                                         Score: [XX]/100     |
+-----------------------------------------------------------------------------+
| SERP ANALYSIS                                                                |
| - AI Overview: [Yes/No]                                                      |
| - Featured Snippet: [Yes/No]                                                 |
| - PAA Questions: [N] found                                                   |
|   - "[PAA question 1]"                                                       |
|   - "[PAA question 2]"                                                       |
+-----------------------------------------------------------------------------+
| TOP 3 COMPETITORS                                                            |
| +-- #1: [domain.com]                                                         |
|     | Title: "[title]"                                                       |
|     | Word Count: [X,XXX] | H2s: [X] | FAQ: [Y/N] | Author: [Y/N]            |
|     | Published: [YYYY-MM-DD] ([X] months ago)                               |
| +-- #2: [domain.com]                                                         |
|     | Title: "[title]"                                                       |
|     | Word Count: [X,XXX] | H2s: [X] | FAQ: [Y/N] | Author: [Y/N]            |
|     | Published: [YYYY-MM-DD] ([X] months ago)                               |
| +-- #3: [domain.com]                                                         |
|     | Title: "[title]"                                                       |
|     | Word Count: [X,XXX] | H2s: [X] | FAQ: [Y/N] | Author: [Y/N]            |
|     | Published: [YYYY-MM-DD] ([X] months ago)                               |
+-----------------------------------------------------------------------------+
| GAP OPPORTUNITIES                                                            |
| - Gap Score: [XX]/100                                                        |
| - Weaknesses Found: [weakness1], [weakness2], [weakness3]                    |
| - Recommended Word Count: [X,XXX]+                                           |
+-----------------------------------------------------------------------------+
| DIFFERENTIATION ANGLES                                                       |
| 1. [Angle 1]                                                                 |
| 2. [Angle 2]                                                                 |
| 3. [Angle 3]                                                                 |
+-----------------------------------------------------------------------------+
| RECOMMENDED TITLE                                                            |
| "[Title with year]"                                                          |
| Type: [Listicle/Tutorial/Showdown] | Skill: [blog-list-writer/etc.]         |
+-----------------------------------------------------------------------------+
```

---

## Batch Execution Plan

```
===============================================================================
                       BATCH EXECUTION PLAN
===============================================================================

EXECUTION READY: [Yes/No]
Total Topics: [N]
Estimated Total Cost: $[X.XX]

PHASE 1: HIGH PRIORITY (Score 80+) - Execute First
-------------------------------------------------------------------------------
| Order | Topic                    | Type      | Writer Skill        | Status |
|-------|--------------------------|-----------|---------------------|--------|
| 1     | [keyword]                | Listicle  | blog-list-writer    | Ready  |
| 2     | [keyword]                | Tutorial  | blog-tutorial-writer| Ready  |
| 3     | [keyword]                | Showdown  | blog-list-writer    | Ready  |
-------------------------------------------------------------------------------

PHASE 2: MEDIUM-HIGH PRIORITY (Score 70-79) - Execute Second
-------------------------------------------------------------------------------
| Order | Topic                    | Type      | Writer Skill        | Status |
|-------|--------------------------|-----------|---------------------|--------|
| 4     | [keyword]                | Tutorial  | blog-tutorial-writer| Ready  |
| 5     | [keyword]                | List      | blog-list-writer    | Ready  |
-------------------------------------------------------------------------------

PHASE 3: MEDIUM PRIORITY (Score 60-69) - Execute If Resources Allow
-------------------------------------------------------------------------------
| Order | Topic                    | Type      | Writer Skill        | Status |
|-------|--------------------------|-----------|---------------------|--------|
| 6     | [keyword]                | Guide     | blog-tutorial-writer| Ready  |
| ...                                                                          |
-------------------------------------------------------------------------------

To execute: Use `/batch-workflow` with topic-brief.json
===============================================================================
```

---

## JSON Output Block

At the end of every report, include the machine-readable JSON:

```
===============================================================================
                         MACHINE-READABLE OUTPUT
===============================================================================
The following JSON files have been generated in the output directory:

1. keyword_matrix.json    - Full keyword matrix with all metrics
2. gap_analysis.json      - Competitor gap analysis data
3. 00-topic-brief.json    - Ready for downstream Writer skills

Output Directory: /reports/YYYY-MM-DD-{seed-slug}/

```json
{
  "mode": "keyword_matrix",
  "seed_keyword": "...",
  "analysis_date": "YYYY-MM-DD",
  "total_keywords": N,
  "priority_topics": [...],
  "batch_execution_ready": true
}
```
===============================================================================
```

---

# Mode C: AEO Validation Report Template (NEW in v2.1)

## AEO Validation Summary

```
===============================================================================
                      AEO VALIDATION REPORT
                        Mode C: AI Visibility Analysis
===============================================================================
Analysis Date: [YYYY-MM-DD]
Keywords Analyzed: [N]
Competitors Analyzed: [N]
LLM Queries Tested: [N]

EXECUTIVE SUMMARY
-------------------------------------------------------------------------------
- Average AI Search Volume: [X,XXX]
- alici.ai LLM Citation Rate: [X.X]%
- Top Competitor Citation Rate: [XX.X]%
- Citation Gap: [XX.X]%
- Content Gaps Found: [N]
-------------------------------------------------------------------------------
Key Insights:
- [Insight 1 - AI visibility opportunity]
- [Insight 2 - LLM citation gap]
- [Insight 3 - content differentiation strategy]
===============================================================================
```

---

## Phase C1: AI Keyword Data Results

```
+-----------------------------------------------------------------------------+
| AI KEYWORD DATA ANALYSIS                                                     |
+-----------------------------------------------------------------------------+
| Keywords Analyzed: [N] | Avg AI Volume: [X,XXX] | AI Volume Trend: [Rising] |
+-----------------------------------------------------------------------------+

TOP AI KEYWORDS BY VOLUME
-------------------------------------------------------------------------------
| #  | Keyword                        | Trad Vol | AI Vol | AI Trend | AI Score |
|----|--------------------------------|----------|--------|----------|----------|
| 1  | [keyword]                      | [X,XXX]  | [X,XXX]| [up]     | [XX]     |
| 2  | [keyword]                      | [X,XXX]  | [X,XXX]| [up]     | [XX]     |
| 3  | [keyword]                      | [X,XXX]  | [X,XXX]| [->]     | [XX]     |
| 4  | [keyword]                      | [X,XXX]  | [X,XXX]| [up]     | [XX]     |
| 5  | [keyword]                      | [X,XXX]  | [X,XXX]| [->]     | [XX]     |
-------------------------------------------------------------------------------

AI VOLUME VS TRADITIONAL VOLUME INSIGHTS
-------------------------------------------------------------------------------
- Keywords with AI > Traditional: [N] ([XX]%)
- Keywords with AI Trend Rising: [N] ([XX]%)
- Best AI Opportunity: "[keyword]" (AI Score: [XX])
-------------------------------------------------------------------------------
```

---

## Phase C2: LLM Mentions Analysis

```
+-----------------------------------------------------------------------------+
| LLM CITATION RATE ANALYSIS                                                   |
+-----------------------------------------------------------------------------+
| Competitors Analyzed: [N] | alici.ai Mention Rate: [X.X]%                   |
| Top Competitor: [domain.com] at [XX.X]% | Citation Gap: [XX.X]%             |
+-----------------------------------------------------------------------------+

COMPETITOR LLM CITATION BREAKDOWN
-------------------------------------------------------------------------------
| #  | Domain               | ChatGPT | AI Overview | Total   | Share  |
|----|----------------------|---------|-------------|---------|--------|
| 1  | [competitor1.com]    | [X,XXX] | [XXX]       | [X,XXX] | [XX]%  |
| 2  | [competitor2.com]    | [X,XXX] | [XXX]       | [X,XXX] | [XX]%  |
| 3  | [competitor3.com]    | [X,XXX] | [XXX]       | [X,XXX] | [XX]%  |
| 4  | [competitor4.com]    | [X,XXX] | [XXX]       | [X,XXX] | [XX]%  |
| 5  | [alici.ai]           | [XX]    | [X]         | [XX]    | [X.X]% |
-------------------------------------------------------------------------------

CITATION GAP ANALYSIS
-------------------------------------------------------------------------------
Gap Insight: alici.ai is [XX.X]% behind the top competitor in LLM citations.

Top Keywords Triggering Competitor Citations:
- "[keyword 1]" → [competitor.com] mentioned [XX] times
- "[keyword 2]" → [competitor.com] mentioned [XX] times
- "[keyword 3]" → [competitor.com] mentioned [XX] times

Opportunity: Target these keywords to increase alici.ai LLM visibility
-------------------------------------------------------------------------------
```

---

## Phase C3: LLM Response Analysis

```
+-----------------------------------------------------------------------------+
| LLM RESPONSE CONTENT ANALYSIS                                                |
+-----------------------------------------------------------------------------+
| Queries Analyzed: [N] | alici.ai Mentioned: [N] ([X]%)                      |
| Content Gaps Found: [N]                                                      |
+-----------------------------------------------------------------------------+

QUERY-BY-QUERY ANALYSIS
-------------------------------------------------------------------------------

Query 1: "[What are the best AI video generators in 2026?]"
+-----------------------------------------------------------------------------+
| Tools Mentioned: [Sora 2, Runway Gen-4, Kling 2.6, Veo 3]                   |
| Top Recommendation: [Sora 2]                                                 |
| alici.ai Mentioned: [No]                                                     |
+-----------------------------------------------------------------------------+
| Content Gaps Identified:                                                     |
| - No mention of one-platform multi-model access                             |
| - Missing pricing comparison                                                 |
| - No real testing methodology cited                                          |
+-----------------------------------------------------------------------------+
| Opportunity Type: HIGH                                                       |
+-----------------------------------------------------------------------------+

Query 2: "[How to create AI videos for free?]"
+-----------------------------------------------------------------------------+
| Tools Mentioned: [Runway Free Tier, Pika Labs, Leonardo AI]                 |
| Top Recommendation: [Runway Free Tier]                                       |
| alici.ai Mentioned: [No]                                                     |
+-----------------------------------------------------------------------------+
| Content Gaps Identified:                                                     |
| - No mention of free model access through aggregators                       |
| - Watermark limitations not discussed                                        |
+-----------------------------------------------------------------------------+
| Opportunity Type: MEDIUM                                                     |
+-----------------------------------------------------------------------------+

[... additional queries ...]

CONTENT GAP SUMMARY
-------------------------------------------------------------------------------
| Gap Category                          | Occurrence | Priority |
|---------------------------------------|------------|----------|
| Multi-model platform positioning      | [X]/[N]    | HIGH     |
| Pricing/cost comparison               | [X]/[N]    | HIGH     |
| Testing methodology citation          | [X]/[N]    | MEDIUM   |
| Use case specificity                  | [X]/[N]    | MEDIUM   |
| Free tier/trial information           | [X]/[N]    | LOW      |
-------------------------------------------------------------------------------
```

---

## Dual Scoring Summary (v2.1)

```
===============================================================================
                         DUAL SCORING SUMMARY
===============================================================================

+-----------------------------------------------------------------------------+
| SCORE OVERVIEW                                                               |
+-----------------------------------------------------------------------------+
| SEO Score: [XX]/100                    | AEO Score: [XX]/100                |
| Combined Priority: [EXCELLENT/HIGH/GOOD/LOW]                                 |
| Priority Reason: "[explanation]"                                             |
+-----------------------------------------------------------------------------+

SEO SCORE BREAKDOWN (100 points)
-------------------------------------------------------------------------------
| Dimension        | Score  | Evidence                                        |
|------------------|--------|------------------------------------------------|
| Demand Signal    | XX/30  | Search volume [X,XXX] + trend [rising/stable]  |
| AEO Potential    | XX/25  | AI Overview [Y/N] + PAA [N] questions          |
| Competition Gap  | XX/25  | [Gap description]                              |
| Business Fit     | XX/20  | [Product match description]                     |
|------------------|--------|------------------------------------------------|
| TOTAL            | XX/100 |                                                 |
-------------------------------------------------------------------------------

AEO SCORE BREAKDOWN (100 points) - NEW in v2.1
-------------------------------------------------------------------------------
| Dimension             | Score  | Evidence                                   |
|-----------------------|--------|-------------------------------------------|
| AI Search Heat        | XX/35  | AI volume [X,XXX] + trend [rising/stable] |
| LLM Citation Potential| XX/35  | Citation gap [XX.X]% opportunity          |
| AI Answer Coverage    | XX/30  | [N] content gaps = differentiation chance |
|-----------------------|--------|-------------------------------------------|
| TOTAL                 | XX/100 |                                            |
-------------------------------------------------------------------------------

PRIORITY DECISION MATRIX
-------------------------------------------------------------------------------
| Your Scores           | SEO: [XX] | AEO: [XX]                               |
|-----------------------|-----------|------------------------------------------|
| Matrix Position       | SEO >= 80, AEO >= 70 → EXCELLENT              |
|                       | SEO >= 80, AEO < 70  → HIGH (SEO-first)       |
|                       | SEO < 80, AEO >= 70  → HIGH (AEO-first)       |
|                       | SEO >= 60, AEO >= 60 → GOOD                   |
|                       | SEO < 60, AEO < 60   → LOW                    |
|-----------------------|-----------|------------------------------------------|
| Result                | [EXCELLENT/HIGH/GOOD/LOW]                     |
| Recommendation        | [Action recommendation]                        |
-------------------------------------------------------------------------------
===============================================================================
```

---

## Cost Summary (v2.1)

```
===============================================================================
                         COST SUMMARY
===============================================================================

+-----------------------------------------------------------------------------+
| COST BREAKDOWN                                                               |
+-----------------------------------------------------------------------------+
| Category              | Operations              | Cost                       |
|-----------------------|-------------------------|----------------------------|
| SEO Analysis          |                         |                            |
|   Keywords Data       | [N] keywords × $0.015   | $[X.XX]                    |
|   SERP Analysis       | [N] queries × $0.002    | $[X.XX]                    |
|   WebFetch            | [N] pages × free        | $0.00                      |
| SEO Subtotal          |                         | $[X.XX]                    |
|-----------------------|-------------------------|----------------------------|
| AEO Analysis (NEW)    |                         |                            |
|   AI Keyword Data     | [N] keywords × $0.015   | $[X.XX]                    |
|   LLM Mentions        | [N] competitors × $0.10 | $[X.XX]                    |
|   LLM Responses       | [N] queries × $0.05     | $[X.XX]                    |
| AEO Subtotal          |                         | $[X.XX]                    |
|-----------------------|-------------------------|----------------------------|
| TOTAL                 |                         | $[X.XX]                    |
+-----------------------------------------------------------------------------+

Cost Comparison:
- Without AEO (v2.0): ~$1.54
- With AEO (v2.1):    ~$2.59
- Increase:           +$1.05 (+68%)
===============================================================================
```

---

## Score Rating Legend (All Modes - Updated v2.1)

```
SEO Score Indicators (100 points):
  80-100  * EXCELLENT   = Prioritize immediately, high confidence
  60-79   + GOOD        = Add to content calendar
  40-59   ! FAIR        = Consider if resources allow
  0-39    x LOW         = Deprioritize

AEO Score Indicators (100 points) - NEW in v2.1:
  80-100  * EXCELLENT   = High AI visibility opportunity
  60-79   + GOOD        = Moderate AI optimization potential
  40-59   ! FAIR        = Limited AI presence opportunity
  0-39    x LOW         = Low priority for AI optimization

Combined Priority Matrix (v2.1):
  SEO >= 80 + AEO >= 70  →  EXCELLENT (Execute immediately)
  SEO >= 80 + AEO < 70   →  HIGH (SEO-first approach)
  SEO < 80 + AEO >= 70   →  HIGH (AEO-first approach)
  SEO >= 60 + AEO >= 60  →  GOOD (Schedule for calendar)
  SEO < 60 + AEO < 60    →  LOW (Deprioritize)

Trend Indicators:
  [up]    = Rising trend (month-over-month growth)
  [->]    = Stable (flat or minor fluctuation)
  [down]  = Declining (month-over-month decrease)

Search Intent Types:
  How-to        = Tutorial, guide, step-by-step
  What-is       = Definition, explanation, concept
  Best-List     = Roundup, top-N, alternatives
  Comparison    = vs, difference, compare
  Problem-solve = Fix, solve, troubleshoot

Content Types -> Skills:
  Tutorial   -> blog-tutorial-writer
  List       -> blog-list-writer
  Showdown   -> blog-list-writer (tool_showdown mode)
  News       -> blog-news-writer
  Comparison -> blog-tutorial-writer (comparison template)
  Guide      -> blog-tutorial-writer (comprehensive template)
```

---

## Language Adaptation

### For Chinese Reports (Mode A & B):

```
===============================================================================
                         增长选题侦察报告
                           模式 B: 关键词矩阵
===============================================================================
种子词: [seed keyword]
分析日期: [YYYY-MM-DD]
生成关键词数: [N]
验证后关键词: [N]
Top 20 机会: [N]

执行摘要
-------------------------------------------------------------------------------
- 分析关键词总数: [N]
- 高优先级 (80+分): [N]
- 中等优先级 (60-79分): [N]
- 最佳机会: "[keyword]" (评分: [XX])
===============================================================================

Label Translations:
- Keyword Matrix Analysis Report -> 关键词矩阵分析报告
- Top 20 Priority Topics -> Top 20 优先选题
- Gap Analysis Summary -> 差距分析摘要
- Competitor Weaknesses -> 竞品弱点
- Differentiation Strategies -> 差异化策略
- Batch Execution Plan -> 批量执行计划
- Evidence & Scoring -> 证据与评分
- Demand Signal -> 需求信号
- AEO Potential -> AEO 潜力
- Competition Gap -> 竞争差距
- Business Fit -> 业务匹配度
```

---

## Version History

### v2.1 (2026-01-24)
- **Mode C: AEO Validation Report Template (NEW)**
  - Phase C1: AI Keyword Data Results section
  - Phase C2: LLM Mentions Analysis section
  - Phase C3: LLM Response Analysis section
- **Dual Scoring Summary (NEW)**
  - SEO Score breakdown (100 points)
  - AEO Score breakdown (100 points)
  - Priority Decision Matrix
- **Cost Summary (NEW)**
  - SEO vs AEO cost breakdown
  - v2.0 vs v2.1 comparison
- Updated Score Rating Legend with AEO indicators
- Updated Mode Detection table for combined modes
- All reports now include AEO validation by default

### v2.0 (2026-01-24)
- Added Mode B: Keyword Matrix Report Template
- Added Matrix Expansion Summary section
- Added Gap Analysis Summary section
- Added Per-Topic Gap Analysis section
- Added Batch Execution Plan section
- Reorganized document for dual-mode support

### v1.0 (Original)
- Initial URL Analysis report template
- Top 10 Topic Opportunities format
- Competitor Content Analysis format
