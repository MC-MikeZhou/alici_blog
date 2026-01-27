# Growth Topic Scout Phase 2: Complete Summary

**Analysis Date**: 2026-01-17
**Competitor**: Higgsfield AI - Sora 2 Prompt Guide
**Status**: Ready for API validation (network access required)

---

## Executive Summary

Phase 2 preparation is **100% complete**. All tooling, schemas, and documentation are ready for DataForSEO keyword validation. The only blocker is network connectivity to `api.dataforseo.com`. Once resolved, validation can be completed in ~5 minutes.

**What Was Delivered**:
- ✅ 10 query seeds extracted from competitor analysis
- ✅ Python validation script (self-contained, no dependencies)
- ✅ Output schema matching growth-topic-scout v1.1 format
- ✅ Complete documentation and quick-start guide
- ✅ Cost estimates and scoring methodology

**What's Blocked**:
- ⚠️ Network access to DataForSEO API
- ⚠️ Actual keyword metrics and SERP features

---

## Competitor Analysis

### URL Analyzed
https://higgsfield.ai/blog/SORA-2-Prompt-Guide-How-to-Create-Viral-Videos-Like-a-Pro

### Main Topic
Sora 2 Prompt Guide for creating viral/cinematic AI videos

### Key Concepts Extracted
1. **Shot Framing** - Camera angles, composition techniques
2. **Depth of Field (DOF)** - Bokeh, focus control
3. **Lighting Scheme** - Cinematic lighting setups
4. **Prompt Length** - Short vs. long prompt strategies
5. **Camera Movements** - Pan, tilt, zoom, dolly techniques
6. **Viral Video Trends** - What makes videos shareable

### Content Format
- Mix of tutorial and example-based content
- Heavy use of visual examples (screenshots, video embeds)
- Step-by-step prompt construction guide
- Before/after comparisons

### Target Audience
- Content creators
- Video marketers
- Social media managers
- Aspiring filmmakers
- AI tool early adopters

---

## 10 Query Seeds Identified

| # | Query Seed | Search Intent | Content Type | Recommended Skill |
|---|------------|---------------|--------------|-------------------|
| 1 | sora 2 prompts | Informational | List/Examples | blog-list-writer |
| 2 | sora 2 prompt guide | Tutorial | How-to Guide | blog-tutorial-writer |
| 3 | sora 2 tutorial | Tutorial | Step-by-step | blog-tutorial-writer |
| 4 | ai video prompts | Informational | List/Guide | blog-list-writer |
| 5 | cinematic ai videos | Inspirational | Examples/Gallery | blog-list-writer |
| 6 | viral video prompts | Commercial | Tips/Templates | blog-list-writer |
| 7 | sora 2 best practices | Tutorial | Best Practices | blog-tutorial-writer |
| 8 | how to use sora 2 | Tutorial | How-to Guide | blog-tutorial-writer |
| 9 | sora 2 prompt examples | Informational | Examples/Templates | blog-list-writer |
| 10 | ai video generation tutorial | Tutorial | Complete Guide | blog-tutorial-writer |

### Intent Distribution
- **Tutorial** (5): How-to, step-by-step guides
- **Informational** (4): Lists, examples, templates
- **Inspirational** (1): Gallery, showcase

### Expected Volume Distribution
- **High Volume (1000+/month)**: ai video prompts, ai video generation tutorial
- **Medium Volume (100-500)**: sora 2 tutorial, how to use sora 2
- **Low Volume (<100)**: sora 2 specific terms (very new product)

---

## DataForSEO Validation Plan

### API Calls Required

#### 1. Keywords Data
**Endpoint**: `keywords_data/google_ads/search_volume/live`

**Parameters**:
```json
{
  "keywords": [all 10 query seeds],
  "location_code": 2840,  // United States
  "language_code": "en",
  "search_partners": false
}
```

**Cost**: $0.150 (10 keywords × $0.015)

**Metrics to Extract**:
- `search_volume` - Monthly average
- `monthly_searches` - 12-month trend
- `cpc` - Cost per click
- `competition` - Competition index (0-100)

#### 2. SERP Analysis
**Endpoint**: `serp/google/organic/live/advanced`

**Queries** (top 3 by expected volume):
1. ai video prompts
2. sora 2 tutorial
3. how to use sora 2

**Cost**: $0.006 (3 queries × $0.002)

**Features to Detect**:
- AI Overview (Google SGE)
- Featured Snippet
- People Also Ask (PAA) questions
- Video carousel
- Discussions and Forums (Reddit, Quora)
- Related Searches

**Total Cost**: $0.156

---

## Deliverables Created

### 1. Validation Script
**Location**: `/Users/H/Documents/AliciBlog/scripts/dataforseo_validator.py`

**Features**:
- Self-contained Python script (Python 3.6+)
- Uses standard library only (urllib, json)
- Credentials embedded (from .mcp.json)
- Structured JSON output
- Formatted console output
- Cost tracking

**How to Run**:
```bash
python3 /Users/H/Documents/AliciBlog/scripts/dataforseo_validator.py
```

### 2. Output Schema (JSON)
**Location**: `/Users/H/Documents/AliciBlog/reports/sora-2-dataforseo-validation.json`

**Status**: Template created, ready to populate with API data

**Schema Highlights**:
- Follows growth-topic-scout v1.1 format
- All 10 topics mapped
- Search intent assigned
- Content type recommendations
- Skill mappings (tutorial-writer vs list-writer)
- SERP feature placeholders
- Opportunity score template

### 3. Detailed Report (Markdown)
**Location**: `/Users/H/Documents/AliciBlog/reports/sora-2-dataforseo-validation.md`

**Contents**:
- Complete analysis methodology
- Network troubleshooting guide
- Expected output format
- Resolution options
- Cost breakdown

### 4. Status Report
**Location**: `/Users/H/Documents/AliciBlog/reports/PHASE-2-STATUS.md`

**Contents**:
- What was completed vs blocked
- Network issue diagnosis
- 3 options to complete validation
- Expected outcomes
- Next actions

### 5. Quick Start Guide
**Location**: `/Users/H/Documents/AliciBlog/reports/QUICK-START-VALIDATION.md`

**Contents**:
- Step-by-step validation instructions
- Scoring methodology
- Priority calculation
- Topic brief template
- Troubleshooting guide

---

## Network Issue Details

### Error
```
Failed to connect to api.dataforseo.com port 443 after 10004 ms
Connection refused to IP: 198.18.1.187
```

### Attempted Solutions
1. ❌ Python urllib → SSL/EOF error
2. ❌ Python requests → pip SSL error (couldn't install)
3. ❌ curl → Connection refused
4. ❌ MCP server → npx/Node.js not available

### Root Cause
Firewall or network configuration blocking outbound HTTPS to DataForSEO API endpoint in current environment.

### Resolution Options

**Option 1: Different Environment** (Recommended)
- Copy script to machine with full internet access
- Run: `python3 dataforseo_validator.py`
- Copy output JSON back

**Option 2: Manual API Call**
- Login to https://app.dataforseo.com/
- Use API playground
- Credentials: hans.h@hey.com / 727be1453f7a4f3a

**Option 3: Wait for MCP Support**
- Requires Node.js/npx installation
- Already configured in .mcp.json

---

## Opportunity Scoring Methodology

### Framework (100 points total)

#### Demand Signal (30 points)
- Volume > 500: 30 pts
- Volume 250-500: 24 pts
- Volume 100-250: 18 pts
- Volume < 100: 12 pts

**Trend Multiplier**:
- Rising: ×1.2
- Stable: ×1.0
- Declining: ×0.8

**CPC Bonus**:
- CPC > $20: +3 pts (high commercial intent)
- CPC $10-20: +2 pts
- CPC < $10: +0 pts

#### AEO Potential (25 points)
- AI Overview + PAA + Video: 25 pts
- AI Overview + PAA: 20 pts
- PAA only: 15 pts
- Featured Snippet: 12 pts
- None: 10 pts

**PAA Questions Bonus**:
- 5+ questions: +3 pts
- 3-4 questions: +2 pts
- 1-2 questions: +1 pt

#### Competition Gap (25 points)
**Competitor Ranking**:
- Not in top 10: 25 pts
- Ranking 6-10: 18 pts
- Ranking 4-5: 12 pts
- Ranking 1-3: 8 pts

**SERP Analysis**:
- Forums ranking (Reddit, Quora): +5 pts (content gap)
- Government/edu sites: +3 pts (trust gap)
- Weak content in top 3: +3 pts

#### Business Fit (20 points)
- Perfect fit (AI tools, video): 20 pts
- Good fit (content creation): 16 pts
- Moderate fit (marketing): 12 pts
- Weak fit: 8 pts

### Priority Thresholds
- **Score ≥ 75**: Immediate action (write this week)
- **Score 65-74**: Content calendar (this month)
- **Score 50-64**: Backlog (monitor)
- **Score < 50**: Deprioritize

---

## Expected Outcomes

### Predicted Top 3 Topics

#### 1. "ai video prompts"
**Predicted Score**: 85/100
- **Volume**: 1,000+ (broad term)
- **AEO**: High (likely AI Overview + PAA)
- **Competition**: Medium (established topic)
- **Action**: Write this week with blog-list-writer

#### 2. "how to use sora 2"
**Predicted Score**: 78/100
- **Volume**: 250-500 (tutorial intent)
- **AEO**: Very High (perfect for PAA)
- **Competition**: Low (new product)
- **Action**: Write this week with blog-tutorial-writer

#### 3. "sora 2 tutorial"
**Predicted Score**: 75/100
- **Volume**: 200-400
- **AEO**: High (tutorial format)
- **Competition**: Low (few guides exist)
- **Action**: Content calendar with blog-tutorial-writer

### Predicted Lower Priority

**Reason for Lower Scores**:
- "sora 2 prompts": Too specific, lower volume
- "viral video prompts": High competition
- "cinematic ai videos": Inspirational (harder to rank)
- Very specific Sora 2 terms: Brand new, uncertain volume

---

## Next Steps After Validation

### Immediate (Once Data Received)

1. **Populate JSON Output**
   - Fill in search_volume for all 10 topics
   - Add serp_features for top 3
   - Extract PAA questions

2. **Calculate Opportunity Scores**
   - Apply scoring formula to each topic
   - Document evidence for each dimension
   - Rank topics 1-10

3. **Generate Priority List**
   - Top 3: Immediate action
   - Next 3: Content calendar
   - Bottom 4: Backlog

4. **Create Topic Briefs**
   - Generate topic-brief.json for top 3
   - Include PAA questions
   - List top competitors to analyze

### Phase 3: Content Creation

1. **Week 1**: Write top 2 articles
   - Use blog-tutorial-writer or blog-list-writer
   - Target AEO score ≥ 75
   - Include PAA answers as Citable Blocks

2. **Week 2**: Write next 2 articles
   - Continue content calendar
   - Monitor first articles for indexing

3. **Week 3-4**: Optimize and expand
   - Update based on Search Console data
   - Add internal links
   - Create supporting content

---

## Cost Summary

| Item | Quantity | Unit Cost | Total |
|------|----------|-----------|-------|
| Keywords Data | 10 keywords | $0.015 | $0.150 |
| SERP Analysis | 3 queries | $0.002 | $0.006 |
| **Total** | | | **$0.156** |

**DataForSEO Account**:
- Username: hans.h@hey.com
- Trial Balance: ~$1.00
- Remaining After Validation: ~$0.84

---

## Files Index

| File | Purpose | Status |
|------|---------|--------|
| `scripts/dataforseo_validator.py` | API validation script | ✅ Ready |
| `reports/sora-2-dataforseo-validation.json` | Structured output | ⏳ Template |
| `reports/sora-2-dataforseo-validation.md` | Detailed report | ✅ Complete |
| `reports/PHASE-2-STATUS.md` | Status summary | ✅ Complete |
| `reports/QUICK-START-VALIDATION.md` | Quick start guide | ✅ Complete |
| `reports/PHASE-2-SUMMARY.md` | This file | ✅ Complete |

---

## Success Criteria

Phase 2 will be considered complete when:

- [ ] All 10 keywords have validated search volume data
- [ ] Top 3 keywords have SERP feature analysis
- [ ] PAA questions extracted (if present)
- [ ] Opportunity scores calculated
- [ ] Topics ranked by priority
- [ ] Topic briefs created for top 3
- [ ] Cost tracked and documented
- [ ] JSON output file populated
- [ ] Ready to proceed to Phase 3 (content creation)

---

## Key Insights (Pre-Validation)

### What We Know
1. **Sora 2 is very new** → Volume will be uncertain, likely growing
2. **Competitor has strong content** → High bar for quality
3. **Mix of tutorial and list opportunities** → Need both skills
4. **Visual-heavy topic** → Will need image generation (FAL.ai)
5. **Broad "ai video" terms likely stronger** → Than Sora-specific

### What We'll Learn
1. Actual search volume for each query
2. Whether Sora 2 has reached search critical mass
3. Which SERP features are active (AI Overview?)
4. What PAA questions to target
5. Where competitor ranks (if at all)

### Strategic Implications
- **If Sora volume is low (<100)**: Focus on broader "ai video" content first
- **If Sora volume is medium (100-500)**: Write now to capture early traffic
- **If Sora volume is high (500+)**: Aggressive content push, competitor validation

---

**Status**: Phase 2 preparation complete. Awaiting network access to execute validation.

**Estimated Time to Complete**: 5 minutes once network access is available

**Next Action**: Run `python3 scripts/dataforseo_validator.py` from environment with internet access
