# AEO Evaluation Framework

## Scoring Overview

| Module | Weight | Focus |
|--------|--------|-------|
| Content Structure & Parsability | 30% | Can AI easily extract and quote? |
| Technical Indexability | 25% | Can AI crawlers access and understand? |
| Citation & E-E-A-T Signals | 25% | Why would AI trust and cite this? |
| Visibility & Measurement Design | 20% | Is content designed to be found? |

---

## Module 1: Content Structure & Parsability (30 points)

### 1.1 Title/H1/Description Alignment (4 points)

| Score | Criteria |
|-------|----------|
| 4 | All three aligned, clearly describe content, include target keywords |
| 2 | Partial alignment, some mismatch between elements |
| 0 | Significant mismatch or missing elements |

**AEO Expert Insight:**
> AI uses these three elements as "content fingerprint" to understand page topic. Microsoft explicitly states AI systems check if Title, H1, and meta description tell a consistent story. Misalignment confuses the parsing algorithm and reduces citation probability.

### 1.2 Heading Hierarchy (H2/H3 as Chapters) (4 points)

| Score | Criteria |
|-------|----------|
| 4 | Clear hierarchy, headings define distinct content sections |
| 2 | Some structure, but hierarchy unclear or inconsistent |
| 0 | No meaningful heading structure or all same level |

**AEO Expert Insight:**
> AI parses pages into "chunks" using headings as boundaries. Microsoft's guide calls H2/H3 "chapter titles that define clear content slices." Without them, AI cannot identify where one idea ends and another begins—making extraction unreliable.

### 1.3 Opening Direct Answer (4 points)

| Score | Criteria |
|-------|----------|
| 4 | First 50 words directly answer the core question/promise |
| 2 | First 100 words contain answer but buried in context |
| 0 | Opening is background/hook only, no direct answer |

**AEO Expert Insight:**
> AI answer engines prioritize content that "leads with the answer." SurferSEO research shows pages with direct opening answers score 17.46% higher in AI results. The inverted pyramid structure (answer first, details later) is the AEO gold standard.

### 1.4 Q&A Format Presence (4 points)

| Score | Criteria |
|-------|----------|
| 4 | Dedicated FAQ section + Q&A format in body, topic-relevant |
| 2 | Some Q&A elements but not systematic or topic-mismatched |
| 0 | No Q&A format anywhere |

**AEO Expert Insight:**
> Q&A format mirrors how users query AI ("How do I...?", "What is...?"). Microsoft states this format "mirrors the way people search." FAQ sections with proper Schema are the most extractable content type—AI can literally copy-paste the answer.

### 1.5 List/Table Usage (4 points)

| Score | Criteria |
|-------|----------|
| 4 | Strategic use of lists AND tables for key information |
| 2 | Some lists OR tables, but not optimally used |
| 0 | Wall-of-text, no structured data presentation |

**AEO Expert Insight:**
> 78% of AI-generated answers contain either ordered or unordered lists (SurferSEO). Lists are "machine-readable by default"—they break complex information into discrete, quotable units. Tables enable comparison-style answers that AI loves to synthesize.

### 1.6 Paragraph Length (3 points)

| Score | Criteria |
|-------|----------|
| 3 | Paragraphs ≤3 sentences, high scannability |
| 1 | Mixed lengths, some dense paragraphs |
| 0 | Wall-of-text paragraphs (200+ words each) |

**AEO Expert Insight:**
> Long paragraphs "blur ideas together" (Microsoft). AI struggles to extract clean quotes from dense text—it may skip your content entirely for a competitor's cleaner structure. Short paragraphs = higher extraction confidence.

### 1.7 Key Information Visibility (4 points)

| Score | Criteria |
|-------|----------|
| 4 | All critical content visible without interaction |
| 2 | Some content in tabs/accordions but duplicated in visible areas |
| 0 | Key information hidden in collapsed elements |

**AEO Expert Insight:**
> Microsoft explicitly warns: content in tabs, accordions, or expandable menus may not be parsed. AI crawlers often don't execute JavaScript interactions. If your best answer is behind a "click to expand," AI will never see it.

### 1.8 Text-Based Facts (3 points)

| Score | Criteria |
|-------|----------|
| 3 | All key facts/data in text format |
| 1 | Some facts in images but with alt text |
| 0 | Critical information only in images/PDFs |

**AEO Expert Insight:**
> AI cannot read images or PDFs reliably. Microsoft lists "key information only in images or PDFs" as a critical mistake. If your killer statistic is in an infographic, AI will cite your competitor who wrote it as text.

---

## Module 2: Technical Indexability (25 points)

### 2.1 Page Indexability (4 points)

| Score | Criteria |
|-------|----------|
| 4 | No blocking directives, confirmed indexable |
| 0 | noindex, robots.txt blocking, or login-required |

**AEO Expert Insight:**
> Google states: pages must "be indexed by Google" and "qualify for snippet display" to appear in AI features. This is the absolute baseline—no index = no AI visibility, period.

### 2.2 Snippet Eligibility (4 points)

| Score | Criteria |
|-------|----------|
| 4 | No nosnippet, content qualifies for rich snippets |
| 2 | max-snippet restrictions but content available |
| 0 | nosnippet tag present |

**AEO Expert Insight:**
> AI Overviews and similar features pull from snippet-eligible content. Using nosnippet to "protect" your content also hides it from AI answer engines. You cannot be cited if AI cannot quote you.

### 2.3 JavaScript Rendering Dependency (5 points)

| Score | Criteria |
|-------|----------|
| 5 | Core content renders without JavaScript |
| 2 | Some content requires JS but critical info is static |
| 0 | Content primarily JS-rendered |

**AEO Expert Insight:**
> Forrester explicitly warns: "Unlike traditional search crawlers, answer engine bots struggle with JavaScript rendering." This is a KEY differentiator from SEO. Many AI crawlers are simpler than Googlebot—they may not execute your React app.

### 2.4 Schema Markup Presence (4 points)

| Score | Criteria |
|-------|----------|
| 4 | Appropriate Schema (Article, FAQ, HowTo, etc.) with complete fields |
| 2 | Schema present but incomplete or wrong type |
| 0 | No Schema markup |

**AEO Expert Insight:**
> Schema contributes ~10% to Perplexity's ranking algorithm. It's "the language AI models speak" (industry research). Schema tells AI: "This is an article by [author] published on [date] about [topic]"—explicit context that plain HTML cannot provide.

### 2.5 Schema-Content Consistency (4 points)

| Score | Criteria |
|-------|----------|
| 4 | Schema data exactly matches visible page content |
| 2 | Minor discrepancies between Schema and content |
| 0 | Schema claims things not on page, or vice versa |

**AEO Expert Insight:**
> Google explicitly states: "all the content in your markup [must be] visible on your web page." Inconsistent Schema is treated as spam signal. AI trusts Schema only when it matches reality.

### 2.6 Semantic HTML Structure (4 points)

| Score | Criteria |
|-------|----------|
| 4 | Proper use of article, section, nav, header, lists, tables |
| 2 | Some semantic elements but inconsistent |
| 0 | "Div soup"—no semantic meaning in HTML |

**AEO Expert Insight:**
> Semantic HTML provides "explicit context about content structure" (industry research). `<article>` tells AI "this is the main content." `<nav>` tells AI "skip this." Without semantics, AI must guess—and may guess wrong.

---

## Module 3: Citation & E-E-A-T Signals (25 points)

> **UPDATED in v2.3**: Reorganized to separate **structural signals** (can AI parse?) from **content depth** (does author have real expertise?). This addresses the gap where articles score high on structure but lack genuine experience evidence.

---

### **Part A: Structural Signals (12 points)**

These check if E-E-A-T signals are **present** and **accessible** to AI.

#### 3.1 Self-Contained Information Blocks (4 points)

| Score | Criteria |
|-------|----------|
| 4 | Key conclusions can be quoted without surrounding context |
| 2 | Some standalone statements but most need context |
| 0 | All content requires reading full article to understand |

**AEO Expert Insight:**
> Perplexity's mechanism: retrieve → summarize → cite with numbers. If your insight requires reading 3 paragraphs to understand, AI will skip it for a competitor's clean one-liner. Write conclusions that work as standalone quotes.

#### 3.2 Specific Data & Statistics (4 points)

| Score | Criteria |
|-------|----------|
| 4 | Multiple specific numbers, percentages, data points |
| 2 | Some specifics but mostly vague claims |
| 0 | Only qualitative claims ("innovative," "powerful") |

**AEO Expert Insight:**
> Forrester recommends "short, simple answers full of unique quotes and stats." Specific data is inherently more citable—"reduces costs by 47%" beats "significantly reduces costs." AI prefers precision.

#### 3.3 Source Attribution & Citations (4 points)

| Score | Criteria |
|-------|----------|
| 4 | External sources linked for key claims |
| 2 | Some attribution but incomplete |
| 0 | Claims without any source indication |

**AEO Expert Insight:**
> Perplexity emphasizes "transparency" and "verifiability." AI prefers citing content that itself cites sources—it's a trust chain. Unsourced claims are risky for AI to quote because they cannot be verified.

---

### **Part B: Content Depth (13 points)** - NEW in v2.3

These check if E-E-A-T signals are **demonstrated** through actual content, not just claimed in metadata.

#### 3.4 Experience Evidence (5 points)

| Score | Criteria |
|-------|----------|
| 5 | **2+ original case studies** with specific outcomes + **first-person testing** methodology described |
| 4 | 1 detailed case study + first-person testing description |
| 3 | Generic examples OR claims testing without specific methodology |
| 2 | Only cites external examples, no original contribution |
| 1 | Implies expertise but provides zero evidence |
| 0 | No examples or evidence of hands-on experience |

**NEW AEO Expert Insight:**
> **The Gap**: Previous scoring gave full marks for "We tested 50 tools" statements. Real experience requires **demonstrated methodology**—what did you test? How? What failed? What succeeded?
>
> **What to look for:**
> - Original case studies with before/after results
> - First-person narratives ("In our testing...", "We found that...")
> - Iteration examples (prompt v1 → v2, what changed and why)
> - Failed attempts disclosed honestly
>
> **Anti-pattern**: "5+ years experience" in bio but zero evidence in article content.

#### 3.5 Author Credibility (4 points)

| Score | Criteria |
|-------|----------|
| 4 | **Named author** + verifiable background + **content demonstrates deep domain knowledge** |
| 3 | Named author + stated credentials in bio |
| 2 | Named author but generic bio OR team attribution with specific members listed |
| 1 | Generic team attribution ("Content Team", "Editorial Staff") |
| 0 | No author information |

**NEW AEO Expert Insight:**
> **The Gap**: Previous scoring accepted "alici.ai Content Team + 5+ years experience" as credible. Real credibility requires **demonstrable expertise in the content itself**.
>
> **What to look for:**
> - Named individual (not team)
> - Bio includes: specific role + company/projects + quantified achievements
> - author.url points to verifiable LinkedIn/Twitter/personal site
> - **Article content shows technical depth** beyond surface-level aggregation
>
> **Anti-pattern**: Author claims expertise but article content is shallow/aggregated from other sources.

#### 3.6 Transparency & Trustworthiness (4 points)

| Score | Criteria |
|-------|----------|
| 4 | **All data sourced** + internal tests labeled ("alici.ai testing, date, n=X") + **conflicts disclosed** + limitations acknowledged |
| 3 | Most data sourced + dates on time-sensitive info |
| 2 | Partial sourcing OR some outdated/unverified claims |
| 1 | Multiple unsourced statistics OR misleading product claims |
| 0 | Provably false information OR hidden conflicts of interest |

**NEW AEO Expert Insight:**
> **The Gap**: Previous scoring checked if sources existed, not if they were **trustworthy or relevant**.
>
> **What to look for:**
> - Statistics cite original sources (official docs > third-party research > anecdotes)
> - Internal testing transparently labeled: "alici.ai testing, Jan 2026, n=50 prompts"
> - Time-sensitive info dated: "as of Jan 2026"
> - Self-promotion disclosed: "alici.ai is our product"
> - Honest limitations: "This approach fails when..."
>
> **Anti-pattern**:
> - "89% adherence rate" with no source
> - Competitor product info possibly outdated
> - Recommending own product without disclosure

---

### M3 Scoring Summary

| Category | Points | What It Checks |
|----------|--------|----------------|
| **Structural Signals** | 12 | E-E-A-T metadata present and accessible |
| **Content Depth** | 13 | E-E-A-T demonstrated through actual expertise |
| **Total** | **25** | Real authority, not just claims |

**Critical Change**: An article can no longer score 22/25 on M3 without demonstrating real experience. The new content depth checks (13 points) require **showing** expertise, not just **stating** it.

---

## Module 4: Visibility & Measurement Design (20 points)

### 4.1 Semantic URL (4 points)

| Score | Criteria |
|-------|----------|
| 4 | URL contains 5-7 descriptive words matching content |
| 2 | Partially descriptive URL |
| 0 | Generic URL (/post/12345) or parameter-heavy |

**AEO Expert Insight:**
> Perplexity research shows semantic URLs get 11.4% more citations. `/blog/sora-2-viral-video-prompts` tells AI what the page is about before parsing. `/p/28374` tells AI nothing.

### 4.2 Meta Description with Direct Answer (4 points)

| Score | Criteria |
|-------|----------|
| 4 | Meta description contains concise answer to main query |
| 2 | Descriptive but doesn't answer the implied question |
| 0 | Keyword-stuffed or generic description |

**AEO Expert Insight:**
> Meta descriptions are often used as snippet sources. Microsoft advises: "explain value without keyword stuffing." A meta description that answers "What will I learn?" is more extractable than one that just lists keywords.

### 4.3 Brand/Entity Consistency (4 points)

| Score | Criteria |
|-------|----------|
| 4 | Consistent brand/product naming throughout |
| 2 | Minor variations in naming |
| 0 | Inconsistent names that could confuse entity recognition |

**AEO Expert Insight:**
> AI needs to recognize entities. If you call your product "AliciAI," "Alici.ai," and "Alici AI" interchangeably, AI may treat these as different entities. Consistency helps AI build accurate knowledge graph entries.

### 4.4 Query Variant Coverage (4 points)

| Score | Criteria |
|-------|----------|
| 4 | Content addresses multiple phrasings of the same question |
| 2 | Covers main query but not variants |
| 0 | Single narrow phrasing only |

**AEO Expert Insight:**
> Forrester advises creating "multiple content pieces addressing semantically similar prompts." Users ask "how to make viral Sora videos" and "best Sora 2 prompts"—same intent, different words. Cover variants to catch more AI queries.

### 4.5 Topic-Relevant FAQ Section (4 points)

| Score | Criteria |
|-------|----------|
| 4 | FAQ directly addresses topic-specific questions |
| 2 | FAQ exists but questions are generic/off-topic |
| 0 | No FAQ section |

**AEO Expert Insight:**
> FAQ Schema is the most AI-extractable format—questions map directly to user queries. BUT the questions must match your topic. Generic "What is AI?" on a Sora 2 prompts article wastes the FAQ opportunity and may confuse AI about page topic.

---

## Scoring Interpretation

| Total Score | Rating | Interpretation |
|-------------|--------|----------------|
| 90-100 | Excellent | Highly optimized for AI citation |
| 75-89 | Good | Solid foundation, minor improvements needed |
| 60-74 | Fair | Functional but missing key AEO elements |
| 40-59 | Poor | Significant gaps in AEO readiness |
| 0-39 | Critical | Not optimized for AI answer engines |

---

## Authority Sources

This framework synthesizes guidance from:

### Official Sources (Foundation)
- [Google Search Central: AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)
- [Google Blog: Succeeding in AI Search](https://developers.google.com/search/blog/2025/05/succeeding-in-ai-search)
- [Microsoft: Optimizing Content for AI Search Answers](https://about.ads.microsoft.com/en/blog/post/october-2025/optimizing-your-content-for-inclusion-in-ai-search-answers)
- [Bing: How AI Search Is Changing Conversions](https://blogs.bing.com/webmaster/November-2025/How-AI-Search-Is-Changing-the-Way-Conversions-are-Measured)

### Platform Mechanics
- [Perplexity Help: How does Perplexity work?](https://www.perplexity.ai/help-center/en/articles/10352895-how-does-perplexity-work)

### Industry Methods
- [Forrester: How To Master Answer Engine Optimization](https://www.forrester.com/blogs/how-to-master-answer-engine-optimization/)
- [Semrush: What Is Answer Engine Optimization?](https://www.semrush.com/blog/answer-engine-optimization/)
- [Ahrefs: Answer Engine Optimization](https://ahrefs.com/blog/answer-engine-optimization/)
- [SurferSEO: 7 AEO Strategies](https://surferseo.com/blog/answer-engine-optimization/)
- [Digital Elevator: AEO Strategic Framework](https://thedigitalelevator.com/blog/answer-engine-optimization-aeo/)
