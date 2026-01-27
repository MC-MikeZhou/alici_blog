# Phase 2: DataForSEO Keyword Validation - Complete Package

**Date**: 2026-01-17
**Topic**: Sora 2 Prompt Guide Analysis
**Status**: ⚠️ Ready for execution (network access required)

---

## Quick Navigation

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **[QUICK-START-VALIDATION.md](QUICK-START-VALIDATION.md)** | Step-by-step execution guide | **Start here** when ready to validate |
| **[PHASE-2-SUMMARY.md](PHASE-2-SUMMARY.md)** | Complete overview | Understand full scope |
| **[PHASE-2-STATUS.md](PHASE-2-STATUS.md)** | Current blockers & solutions | Troubleshoot network issues |
| **[sora-2-dataforseo-validation.md](sora-2-dataforseo-validation.md)** | Detailed methodology | Deep dive into approach |
| **[sora-2-dataforseo-validation.json](sora-2-dataforseo-validation.json)** | Output schema | Validate output format |

---

## What This Package Contains

### 1. Validation Script
**File**: `/Users/H/Documents/AliciBlog/scripts/dataforseo_validator.py`

**What it does**:
- Fetches keyword metrics for 10 Sora 2 queries
- Analyzes SERP features for top 3 queries
- Generates structured JSON output
- Displays formatted results and costs

**How to run**:
```bash
python3 /Users/H/Documents/AliciBlog/scripts/dataforseo_validator.py
```

### 2. 10 Query Seeds
Extracted from competitor analysis of Higgsfield AI's Sora 2 Prompt Guide:

1. sora 2 prompts
2. sora 2 prompt guide
3. sora 2 tutorial
4. ai video prompts
5. cinematic ai videos
6. viral video prompts
7. sora 2 best practices
8. how to use sora 2
9. sora 2 prompt examples
10. ai video generation tutorial

### 3. Output Schema
**File**: `sora-2-dataforseo-validation.json`

Follows growth-topic-scout v1.1 format with:
- Search volume metrics
- SERP feature detection
- Opportunity scoring framework
- Priority rankings
- Content type recommendations

### 4. Documentation Suite
- **Quick Start**: 5-minute execution guide
- **Summary**: Complete overview and insights
- **Status**: Current blockers and solutions
- **Methodology**: Detailed validation approach

---

## Current Status

### ✅ Completed
- [x] Competitor analysis (Higgsfield AI Sora 2 guide)
- [x] Query seed extraction (10 keywords)
- [x] Validation script development
- [x] Output schema creation
- [x] Documentation suite
- [x] Cost estimation ($0.156)
- [x] Scoring methodology

### ⚠️ Blocked
- [ ] DataForSEO API access (network connectivity issue)
- [ ] Actual keyword metrics
- [ ] SERP feature detection
- [ ] Opportunity score calculation

### 🎯 Next Steps
1. Resolve network access to api.dataforseo.com
2. Run validation script (~5 minutes)
3. Calculate opportunity scores
4. Rank topics by priority
5. Generate topic briefs for top 3
6. Proceed to Phase 3 (content creation)

---

## How to Execute (When Ready)

### Prerequisites
- Network access to `https://api.dataforseo.com`
- Python 3.6+ (already available)
- DataForSEO credentials (already configured)

### Step-by-Step

1. **Test connectivity**:
   ```bash
   curl --user 'hans.h@hey.com:727be1453f7a4f3a' \
     'https://api.dataforseo.com/v3/appendix/user_data'
   ```

   If this fails, see `PHASE-2-STATUS.md` for resolution options.

2. **Run validation**:
   ```bash
   python3 /Users/H/Documents/AliciBlog/scripts/dataforseo_validator.py
   ```

3. **Review output**:
   - Console: Formatted table + cost summary
   - File: `sora-2-dataforseo-validation.json`

4. **Calculate scores**:
   - Follow methodology in `QUICK-START-VALIDATION.md`
   - Use scoring framework (100 points total)

5. **Prioritize topics**:
   - Score ≥ 75: Write this week
   - Score 65-74: Content calendar
   - Score < 65: Backlog

---

## Expected Timeline

| Phase | Duration | Action |
|-------|----------|--------|
| **Validation** | 5 minutes | Run script, get data |
| **Analysis** | 15 minutes | Calculate scores, rank topics |
| **Topic Briefs** | 30 minutes | Create briefs for top 3 |
| **Content Creation** | 2-3 hours/article | Use blog-*-writer skills |

**Total Time to First Article**: ~3-4 hours (after network access restored)

---

## Cost Breakdown

| Item | Cost |
|------|------|
| Keywords Data (10 keywords) | $0.150 |
| SERP Analysis (3 queries) | $0.006 |
| **Total** | **$0.156** |

**DataForSEO Balance**: ~$0.84 remaining (from $1.00 trial)

---

## Key Files Reference

### Input
- Competitor URL: https://higgsfield.ai/blog/SORA-2-Prompt-Guide-How-to-Create-Viral-Videos-Like-a-Pro
- Query seeds: 10 keywords (see list above)
- Credentials: `.mcp.json` (hans.h@hey.com)

### Processing
- Script: `scripts/dataforseo_validator.py`
- API: DataForSEO REST API v3
- Endpoints: keywords_data, serp

### Output
- JSON: `reports/sora-2-dataforseo-validation.json`
- Reports: `reports/sora-2-dataforseo-validation.md`
- Logs: Console output (save manually if needed)

---

## What You'll Learn

### About the Keywords
- **Search Volume**: How many people search per month
- **Trend**: Rising, stable, or declining
- **CPC**: Commercial intent indicator
- **Competition**: How hard to rank

### About the SERPs
- **AI Overview**: Is Google SGE active?
- **Featured Snippet**: Direct answer opportunity?
- **PAA Questions**: What to answer in content?
- **Video**: Need video content?
- **Forums**: Content gap indicator (Reddit ranking)?

### About Priority
- **Top 3 Topics**: Write immediately
- **Medium Priority**: Content calendar
- **Low Priority**: Backlog or deprioritize

---

## Success Criteria

Phase 2 is complete when:

1. ✅ All 10 keywords have search volume data
2. ✅ Top 3 keywords have SERP features analyzed
3. ✅ PAA questions extracted (if present)
4. ✅ Opportunity scores calculated (0-100)
5. ✅ Topics ranked by priority
6. ✅ Topic briefs created for top 3
7. ✅ Ready to run blog-tutorial-writer or blog-list-writer

---

## Troubleshooting

### Q: Network still blocked, what to do?
**A**: See `PHASE-2-STATUS.md` → 3 resolution options

### Q: Can I use estimated volume instead?
**A**: Not recommended. Estimates are often 3-5x off reality.

### Q: What if Sora 2 volume is very low?
**A**: Focus on broader "ai video" terms first, monitor Sora growth.

### Q: How do I calculate opportunity scores?
**A**: See `QUICK-START-VALIDATION.md` → Step 5: Calculate Priority

---

## Integration with AliciBlog Workflow

### Current Phase
**Phase 2**: DataForSEO Keyword Validation

### Next Phase
**Phase 3**: Content Creation
- Use `/write-tutorial` or `/write-list`
- Input: Topic brief from Phase 2
- Target: AEO score ≥ 75

### Full Workflow
```
Phase 1: Competitor Analysis ✅
  ↓
Phase 2: Keyword Validation ⏳ (you are here)
  ↓
Phase 3: Content Creation
  ↓
Phase 4: AEO Analysis & Improvement
  ↓
Phase 5: Framer CMS Publishing
```

---

## Contact & Support

### DataForSEO Account
- Email: hans.h@hey.com
- Password: 727be1453f7a4f3a
- Dashboard: https://app.dataforseo.com/
- Docs: https://docs.dataforseo.com/

### API Endpoints
- Keywords Data: `v3/keywords_data/google_ads/search_volume/live`
- SERP Analysis: `v3/serp/google/organic/live/advanced`
- User Info: `v3/appendix/user_data`

---

## Document Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-17 | Initial Phase 2 package created | Claude |
| 2026-01-17 | Added all documentation files | Claude |
| 2026-01-17 | Validation script completed | Claude |

---

## Quick Commands

```bash
# Navigate to project
cd /Users/H/Documents/AliciBlog

# Test API connectivity
curl --user 'hans.h@hey.com:727be1453f7a4f3a' \
  'https://api.dataforseo.com/v3/appendix/user_data'

# Run validation
python3 scripts/dataforseo_validator.py

# View output
cat reports/sora-2-dataforseo-validation.json | python3 -m json.tool

# Check script
cat scripts/dataforseo_validator.py | head -50
```

---

**Ready to Execute**: All preparation complete. Just need network access to api.dataforseo.com.

**Estimated Completion Time**: 5 minutes

**Next Action**: See [QUICK-START-VALIDATION.md](QUICK-START-VALIDATION.md)
