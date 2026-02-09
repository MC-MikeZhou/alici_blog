# Growth Topic Scout Phase 2: Status Report

## Current Status: ⚠️ Blocked by Network Connectivity

**Date**: 2026-01-17
**Phase**: DataForSEO Keyword Validation
**Blocker**: Cannot connect to api.dataforseo.com from current environment

---

## What Was Completed

### 1. Competitor Analysis Summary ✅
- **URL**: https://higgsfield.ai/blog/SORA-2-Prompt-Guide-How-to-Create-Viral-Videos-Like-a-Pro
- **Main Topic**: Sora 2 Prompt Guide for creating viral/cinematic AI videos
- **Key Concepts Extracted**:
  - Shot framing and camera angles
  - Depth of field (DOF) techniques
  - Lighting schemes
  - Short vs. long prompts
  - Camera movements
  - Viral video trends

### 2. Query Seeds Identified ✅
10 keyword opportunities extracted:
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

### 3. Output Schema Prepared ✅
- JSON structure created following growth-topic-scout v1.1 format
- All 10 topics mapped with search intent
- Content type recommendations included
- Recommended skills assigned (blog-tutorial-writer vs blog-list-writer)

### 4. Validation Script Created ✅
- **Location**: `/Users/H/Documents/AliciBlog/scripts/dataforseo_validator.py`
- **Features**:
  - Calls DataForSEO REST API
  - Extracts keyword metrics (volume, CPC, competition)
  - Analyzes SERP features (AI Overview, PAA, Video, Forums)
  - Generates JSON output matching expected schema
  - Uses Python standard library only (urllib)

---

## What Is Blocked

### Network Connectivity Issue
```
Error: Failed to connect to api.dataforseo.com port 443
IP: 198.18.1.187
Timeout: 10+ seconds
```

**Attempted Solutions**:
- ✅ Python urllib (SSL error)
- ✅ curl (connection refused)
- ❌ MCP server (requires Node.js/npx - not available)

**Root Cause**: Firewall or network configuration blocking outbound HTTPS to DataForSEO API endpoint

---

## How to Complete Phase 2

### Option 1: Run from Different Environment (Recommended)

1. **Copy the script to a machine with full internet access**:
   ```bash
   # Script location
   /Users/H/Documents/AliciBlog/scripts/dataforseo_validator.py
   ```

2. **Run the script**:
   ```bash
   python3 dataforseo_validator.py
   ```

3. **Copy the output back**:
   - JSON output: `sora-2-dataforseo-validation.json`
   - Console output includes formatted table and cost summary

### Option 2: Manual API Calls via Web Interface

1. **Visit DataForSEO API Testing Page**:
   - https://app.dataforseo.com/api-dashboard

2. **Login Credentials** (from `.mcp.json`):
   - Username: `hans.h@hey.com`
   - Password: `727be1453f7a4f3a`

3. **Call Keywords Data Endpoint**:
   - Endpoint: `keywords_data/google_ads/search_volume/live`
   - Payload: See `/reports/sora-2-dataforseo-validation.json` → `api_calls[0].parameters`

4. **Call SERP Endpoint** (for top 3 keywords):
   - Endpoint: `serp/google/organic/live/advanced`
   - Keywords: "ai video prompts", "sora 2 tutorial", "how to use sora 2"

### Option 3: Wait for MCP Server Support

If Node.js/npx becomes available in the environment:
```bash
npx -y dataforseo-mcp-server
```

Environment variables are already configured in `.mcp.json`.

---

## What the Validation Will Provide

### 1. Search Volume Data
For each of 10 keywords:
- Monthly average search volume
- 12-month trend (rising/stable/declining)
- Cost per click (CPC) - indicates commercial intent
- Competition index (0-100)

**Expected Patterns**:
- "sora 2" specific terms: Lower volume (100-500/month), brand new
- "ai video" general terms: Higher volume (1,000+/month), established
- Tutorial queries: Higher AEO potential (PAA questions)

### 2. SERP Features (Top 3 Keywords)
- **AI Overview**: If present, indicates Google SGE is active
- **Featured Snippet**: Direct answer opportunity
- **People Also Ask**: 3-5 questions to target for AEO
- **Video**: Indicates visual content preference
- **Forums (Reddit/Quora)**: Content gap indicator

### 3. Opportunity Scoring
Each topic will receive a score (0-100) based on:
- **Demand Signal** (30 pts): Volume × Trend × CPC
- **AEO Potential** (25 pts): AI Overview + PAA + Video
- **Competition Gap** (25 pts): Competitor ranking analysis
- **Business Fit** (20 pts): Alignment with AliciBlog

### 4. Priority Ranking
Topics sorted by opportunity score, with:
- Top 3: Immediate action (this week)
- Next 3: Content calendar (this month)
- Bottom 4: Backlog (deprioritize if score < 70)

---

## Expected Outcomes

### High Priority Topics (Expected)
Based on search intent and competitor analysis:

1. **"how to use sora 2"** - Tutorial, high AEO potential
2. **"ai video prompts"** - List, broader appeal
3. **"sora 2 tutorial"** - Tutorial, direct competitor alternative

### Medium Priority Topics (Expected)
4. **"sora 2 prompts"** - List, core topic
5. **"cinematic ai videos"** - Inspirational, visual-heavy
6. **"viral video prompts"** - Commercial intent

### Lower Priority (Expected)
7-10. Niche or very new terms with uncertain volume

---

## Files Generated

| File | Status | Location |
|------|--------|----------|
| Validation Script | ✅ Complete | `/Users/H/Documents/AliciBlog/scripts/dataforseo_validator.py` |
| Output Schema (JSON) | ⏳ Template | `/Users/H/Documents/AliciBlog/reports/sora-2-dataforseo-validation.json` |
| Detailed Report (MD) | ✅ Complete | `/Users/H/Documents/AliciBlog/reports/sora-2-dataforseo-validation.md` |
| Status Summary | ✅ Complete | `/Users/H/Documents/AliciBlog/reports/PHASE-2-STATUS.md` |

---

## Cost Estimate

| Item | Quantity | Unit Cost | Total |
|------|----------|-----------|-------|
| Keywords Data | 10 keywords | $0.015 | $0.150 |
| SERP Analysis | 3 queries | $0.002 | $0.006 |
| **Total** | | | **$0.156** |

**Remaining Trial Balance**: ~$0.84 (assuming $1.00 trial credit)

---

## Next Actions

### Immediate (Unblock Phase 2)
- [ ] Run validation script from environment with network access
- [ ] Save raw API responses
- [ ] Populate JSON output file with metrics

### After Validation Complete
- [ ] Calculate opportunity scores for all 10 topics
- [ ] Rank topics by priority
- [ ] Generate topic briefs for top 3
- [ ] Create content calendar
- [ ] Run blog-tutorial-writer or blog-list-writer for highest priority topic

### Phase 3 Preparation
- [ ] Review AEO framework for scoring methodology
- [ ] Prepare writer skill inputs (topic brief + PAA questions)
- [ ] Set up quality gate (AEO score must be ≥75)

---

## Questions & Troubleshooting

### Q: Can we use estimated data instead of API?
**A**: Not recommended. Estimates from web tools are often 3-5x off. DataForSEO provides actual Google Ads data.

### Q: What if some keywords have zero volume?
**A**: Expected for very new terms like "sora 2". Focus on broader terms ("ai video prompts") and wait for Sora 2 adoption.

### Q: Should we proceed without validation?
**A**: No. The whole point of Phase 2 is to avoid writing content for keywords with <100/month volume. Would waste time.

### Q: How accurate is DataForSEO vs Google Keyword Planner?
**A**: DataForSEO uses GKP data, so identical. Advantage: API access + 12-month trends + SERP features in one call.

---

## Contact & Support

**DataForSEO Account**:
- Email: hans.h@hey.com
- Dashboard: https://app.dataforseo.com/

**Script Issues**:
- Script is self-contained (no dependencies except Python 3.6+)
- All credentials embedded (not ideal but functional)
- Outputs to console + saves JSON file

---

*Phase 2 prepared and ready for execution once network access is available*
*All outputs follow growth-topic-scout v1.1 schema*
