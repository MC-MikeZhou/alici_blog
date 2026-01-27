# Growth Topic Scout Analysis Report - Sora 2 Prompts

> **Skill Version**: 1.0
> **Analysis Date**: 2026-01-17
> **Validation Method**: `dataforseo` (API call required)
> **Status**: ⚠️ Network connectivity issue - Manual API validation needed

---

## Executive Summary

- **Competitor Analyzed**: [Higgsfield AI - SORA 2 Prompt Guide](https://higgsfield.ai/blog/SORA-2-Prompt-Guide-How-to-Create-Viral-Videos-Like-a-Pro)
- **Main Topic**: Sora 2 Prompt Guide for creating viral/cinematic AI videos
- **Topics Identified**: 10 keyword opportunities extracted from competitor content
- **Status**: Ready for DataForSEO API validation (requires network access)

---

## 1. Query Seeds Extracted

Based on competitor content analysis, the following 10 query seeds were identified:

| # | Query Seed | Search Intent | Expected Content Type |
|---|------------|---------------|----------------------|
| 1 | sora 2 prompts | Informational | List/Examples |
| 2 | sora 2 prompt guide | Tutorial | How-to Guide |
| 3 | sora 2 tutorial | Tutorial | Step-by-step |
| 4 | ai video prompts | Informational | List/Guide |
| 5 | cinematic ai videos | Inspirational | Examples/Gallery |
| 6 | viral video prompts | Commercial | Tips/Templates |
| 7 | sora 2 best practices | Tutorial | Best Practices |
| 8 | how to use sora 2 | Tutorial | How-to Guide |
| 9 | sora 2 prompt examples | Informational | Examples/Templates |
| 10 | ai video generation tutorial | Tutorial | Complete Guide |

---

## 2. DataForSEO Validation Requirements

### Keywords Data API Call

**Endpoint**: `keywords_data/google_ads/search_volume/live`

**Parameters**:
```json
{
  "keywords": [
    "sora 2 prompts",
    "sora 2 prompt guide",
    "sora 2 tutorial",
    "ai video prompts",
    "cinematic ai videos",
    "viral video prompts",
    "sora 2 best practices",
    "how to use sora 2",
    "sora 2 prompt examples",
    "ai video generation tutorial"
  ],
  "location_code": 2840,
  "language_code": "en",
  "search_partners": false
}
```

**Expected Cost**: ~$0.15 (10 keywords × $0.015/keyword)

**Metrics to Extract**:
- `search_volume` - Monthly average search volume
- `monthly_searches` - 12-month trend data
- `cpc` - Cost per click (commercial intent indicator)
- `competition` - Competition index (0-100)

### SERP Analysis API Calls

**Endpoint**: `serp/google/organic/live/advanced`

**Top 3 Keywords to Analyze** (based on expected volume):
1. "ai video prompts"
2. "sora 2 tutorial"
3. "how to use sora 2"

**Parameters** (per query):
```json
{
  "keyword": "[query]",
  "location_code": 2840,
  "language_code": "en",
  "device": "desktop",
  "os": "windows",
  "depth": 100
}
```

**Expected Cost**: ~$0.006 (3 queries × $0.002/query)

**SERP Features to Detect**:
- ✅ AI Overview (Google SGE)
- ✅ Featured Snippet
- ✅ People Also Ask (PAA) questions
- ✅ Video carousel
- ✅ Discussions and Forums (Reddit, Quora)
- ✅ Related Searches

---

## 3. Network Connectivity Issue

**Error Encountered**:
```
Failed to connect to api.dataforseo.com port 443 after 10004 ms: Couldn't connect to server
IP: 198.18.1.187
```

**Possible Causes**:
1. Network firewall blocking outbound HTTPS to DataForSEO
2. VPN or proxy configuration issue
3. API endpoint temporarily unavailable
4. Environment-specific network restrictions

**Resolution Options**:

### Option 1: Use Alternative Environment
Run the validation script from an environment with full network access:

```bash
python3 /Users/H/Documents/AliciBlog/scripts/dataforseo_validator.py
```

The script is located at `/Users/H/Documents/AliciBlog/scripts/dataforseo_validator.py` and uses standard library `urllib` (no external dependencies).

### Option 2: Manual API Call via Web Interface
1. Visit DataForSEO API documentation: https://docs.dataforseo.com/
2. Use their API playground or Postman
3. Credentials available in `.mcp.json`

### Option 3: Use MCP Server (Requires Node.js)
If Node.js becomes available:
```bash
npx -y dataforseo-mcp-server
```

With environment variables from `.mcp.json`:
- `DATAFORSEO_USERNAME`: hans.h@hey.com
- `DATAFORSEO_PASSWORD`: 727be1453f7a4f3a
- `ENABLED_MODULES`: SERP,KEYWORDS_DATA

---

## 4. Expected Output Schema

Once API validation is complete, the output should follow this structure (based on growth-topic-scout v1.1 validated format):

```json
{
  "analysis_date": "2026-01-17",
  "skill_version": "1.0",
  "validation_method": "dataforseo",
  "api_cost_usd": 0.156,
  "competitor_urls": [
    "https://higgsfield.ai/blog/SORA-2-Prompt-Guide-How-to-Create-Viral-Videos-Like-a-Pro"
  ],
  "topics": [
    {
      "rank": 1,
      "primary_keyword": "[highest volume keyword]",
      "search_intent": "tutorial|best-list|comparison|how-to",
      "search_volume": {
        "monthly_avg": 0,
        "trend": "rising|stable|declining",
        "cpc": 0.00,
        "competition_index": 0,
        "data_source": "dataforseo"
      },
      "serp_features": {
        "ai_overview": true|false,
        "featured_snippet": true|false,
        "people_also_ask": true|false,
        "paa_questions": [],
        "video": true|false,
        "discussions_forums": true|false
      },
      "evidence": {
        "check_url": "https://www.google.com/search?q=[keyword]",
        "top_competitors": []
      },
      "opportunity_score": {
        "demand_signal": 0,
        "aeo_potential": 0,
        "competition_gap": 0,
        "business_fit": 0,
        "total": 0
      },
      "recommended_skill": "blog-tutorial-writer|blog-list-writer"
    }
  ],
  "content_gaps": [],
  "api_calls": [
    {
      "endpoint": "keywords_data/google_ads/search_volume/live",
      "cost": 0.15
    },
    {
      "endpoint": "serp/google/organic/live/advanced",
      "cost": 0.006
    }
  ]
}
```

---

## 5. Key Concepts from Competitor Analysis

The competitor article focuses on these main concepts that should inform keyword prioritization:

### Primary Topics:
1. **Shot Framing** - Camera angles, composition techniques
2. **Depth of Field (DOF)** - Bokeh, focus techniques
3. **Lighting Scheme** - Cinematic lighting setups
4. **Prompt Length** - Short vs. long prompt strategies
5. **Camera Movements** - Pan, tilt, zoom, dolly techniques
6. **Viral Video Trends** - What makes videos shareable

### Content Format:
- Mix of tutorial and example-based content
- Heavy use of visual examples
- Step-by-step prompt construction
- Before/after comparisons

### Target Audience:
- Content creators
- Video marketers
- Social media managers
- Aspiring filmmakers

---

## 6. Recommended Next Steps

1. **Resolve Network Connectivity**
   - Test from different network environment
   - Check firewall/VPN settings
   - Verify DataForSEO account status

2. **Complete API Validation**
   - Run `/Users/H/Documents/AliciBlog/scripts/dataforseo_validator.py`
   - Save raw API responses for analysis
   - Extract monthly trend data for seasonality

3. **Calculate Opportunity Scores**
   - Demand Signal (30 points): Volume × Trend × CPC
   - AEO Potential (25 points): AI Overview + PAA + Video
   - Competition Gap (25 points): Competitor ranking + SERP difficulty
   - Business Fit (20 points): Alignment with AliciBlog focus

4. **Prioritize Topics**
   - Rank by total opportunity score
   - Identify content type (tutorial vs. list)
   - Map to appropriate blog-writer skill

5. **Create Topic Briefs**
   - Generate `topic-brief.json` for top 3 opportunities
   - Include PAA questions for AEO optimization
   - Identify top competitors to analyze

---

## 7. Technical Details

### Script Location
`/Users/H/Documents/AliciBlog/scripts/dataforseo_validator.py`

### Configuration
Credentials stored in `/Users/H/Documents/AliciBlog/.mcp.json`:
- Username: hans.h@hey.com
- Password: 727be1453f7a4f3a
- Enabled Modules: SERP, KEYWORDS_DATA

### Output Files
- JSON: `/Users/H/Documents/AliciBlog/reports/sora-2-dataforseo-validation.json`
- Markdown: This file

---

## 8. Estimated Costs

| Item | Quantity | Unit Cost | Total |
|------|----------|-----------|-------|
| Keywords Data | 10 keywords | $0.015 | $0.150 |
| SERP Analysis | 3 queries | $0.002 | $0.006 |
| **Total** | | | **$0.156** |

**Note**: Costs are estimates based on DataForSEO pricing. Actual costs may vary.

---

## Appendix: curl Command for Manual Testing

If network access is restored, test with:

```bash
# Test user info endpoint
curl --user 'hans.h@hey.com:727be1453f7a4f3a' \
  'https://api.dataforseo.com/v3/appendix/user_data'

# Get keywords data
curl --user 'hans.h@hey.com:727be1453f7a4f3a' \
  -X POST 'https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live' \
  -H 'Content-Type: application/json' \
  -d '[{
    "keywords": ["sora 2 prompts","sora 2 tutorial"],
    "location_code": 2840,
    "language_code": "en"
  }]'
```

---

*Analysis prepared for AliciBlog Content Strategy System*
*Awaiting DataForSEO API validation to complete Phase 2*
