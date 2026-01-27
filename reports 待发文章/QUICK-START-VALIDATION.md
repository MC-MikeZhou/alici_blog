# Quick Start: Complete DataForSEO Validation

**Time Required**: 5 minutes
**Cost**: ~$0.16 USD
**Prerequisites**: Network access to api.dataforseo.com

---

## Step 1: Test API Connectivity

```bash
# Test if you can reach DataForSEO API
curl --user 'hans.h@hey.com:727be1453f7a4f3a' \
  'https://api.dataforseo.com/v3/appendix/user_data'
```

**Expected Output**: JSON with account info and remaining balance

**If Failed**: You're in the same network environment as the original issue. Try from:
- Different WiFi network
- Different computer
- Disable VPN if active
- Use mobile hotspot

---

## Step 2: Run Validation Script

```bash
# Navigate to project directory
cd /Users/H/Documents/AliciBlog

# Run the validator
python3 scripts/dataforseo_validator.py
```

**What It Does**:
1. Fetches keyword metrics for 10 queries
2. Analyzes SERP features for top 3 queries
3. Generates structured JSON output
4. Displays formatted table and cost summary

**Runtime**: ~30 seconds

---

## Step 3: Verify Output

### Console Output Should Show:

```
================================================================================
DataForSEO Keyword Validation - Phase 2
================================================================================

Step 1: Fetching keyword metrics...
Keywords: 10

✓ Retrieved metrics for 10 keywords

Keyword Metrics:
--------------------------------------------------------------------------------
Keyword                                     Volume      CPC   Comp
--------------------------------------------------------------------------------
sora 2 prompts                                 XXX  $XX.XX     XX
sora 2 prompt guide                            XXX  $XX.XX     XX
...

Step 2: Fetching SERP features for top queries...
  Analyzing: [keyword]
    Features: AI Overview, PAA (4), Video

================================================================================
API Cost Summary
================================================================================
Keywords Data (10 keywords): $0.150
SERP Analysis (3 queries): $0.006
Total: $0.156
```

### File Output:
**Location**: `/Users/H/Documents/AliciBlog/reports/sora-2-dataforseo-validation.json`

**Key Fields to Check**:
```json
{
  "topics": [
    {
      "primary_keyword": "...",
      "search_volume": {
        "monthly_avg": 260,  // Should have real number
        "cpc": 18.70,        // Should have real number
        "trend": "stable"    // Should be "rising|stable|declining"
      },
      "serp_features": {
        "ai_overview": true,      // Should be true/false
        "paa_questions": ["..."]  // Should have questions if true
      }
    }
  ]
}
```

---

## Step 4: Analyze Results

### Questions to Answer:

1. **Which keyword has highest volume?**
   - Sort by `search_volume.monthly_avg`
   - Likely winner: "ai video prompts" (broader term)

2. **Which keywords have AI Overview?**
   - Check `serp_features.ai_overview: true`
   - These are AEO opportunities

3. **Which have People Also Ask?**
   - Check `serp_features.paa_questions` length
   - Target these questions in content

4. **What's the trend?**
   - "rising" = Act fast
   - "stable" = Evergreen opportunity
   - "declining" = Lower priority

5. **Commercial intent?**
   - CPC > $10 = High commercial intent
   - CPC < $5 = Informational

---

## Step 5: Calculate Priority

### Scoring Formula (for top 3-5 keywords):

**Demand Signal (30 points)**:
- Volume > 500: 30 pts
- Volume 250-500: 24 pts
- Volume 100-250: 18 pts
- Volume < 100: 12 pts

**AEO Potential (25 points)**:
- AI Overview + PAA + Video: 25 pts
- AI Overview + PAA: 20 pts
- PAA only: 15 pts
- None: 10 pts

**Competition Gap (25 points)**:
- Check if competitor ranks in top 10
  - Not ranking: 25 pts
  - Ranking 6-10: 18 pts
  - Ranking 1-5: 12 pts

**Business Fit (20 points)**:
- Perfect fit (AI tools): 20 pts
- Good fit: 16 pts
- Moderate: 12 pts

**Total Score**: Sum all dimensions (max 100)

---

## Step 6: Create Priority List

### Template:

| Rank | Keyword | Volume | Score | Action |
|------|---------|--------|-------|--------|
| 1 | [keyword] | XXX | 85 | Write this week |
| 2 | [keyword] | XXX | 78 | Write this week |
| 3 | [keyword] | XXX | 72 | Content calendar |
| 4 | [keyword] | XXX | 65 | Content calendar |
| 5 | [keyword] | XXX | 58 | Backlog |

**Decision Rules**:
- Score ≥ 75: Immediate action
- Score 65-74: Content calendar (this month)
- Score < 65: Backlog (deprioritize)

---

## Step 7: Generate Topic Briefs

For each top 3 keyword, create:

```json
{
  "primary_keyword": "how to use sora 2",
  "search_intent": "tutorial",
  "target_audience": "Content creators new to Sora 2",
  "content_type": "How-to Guide",
  "recommended_skill": "blog-tutorial-writer",
  "target_length": "1,800-2,500 words",
  "paa_questions": [
    "How do I get started with Sora 2?",
    "What are the best practices for Sora 2?",
    "How much does Sora 2 cost?"
  ],
  "key_sections": [
    "Getting started with Sora 2",
    "Basic prompt structure",
    "Advanced techniques",
    "Common mistakes to avoid"
  ],
  "competitors_to_analyze": [
    "https://higgsfield.ai/blog/SORA-2-Prompt-Guide-..."
  ]
}
```

Save to: `/reports/sora-2-topic-briefs/[keyword-slug].json`

---

## Troubleshooting

### Error: "Invalid credentials"
**Fix**: Double-check `.mcp.json` credentials match script

### Error: "Insufficient funds"
**Fix**: Check DataForSEO balance at https://app.dataforseo.com/

### Error: "Rate limit exceeded"
**Fix**: Wait 60 seconds and retry

### No SERP features found
**Possible**: Very new topic, Google hasn't added features yet
**Action**: Focus on traditional SEO, monitor for feature emergence

---

## What to Do After Validation

### If High Volume Found (>500/month)
1. **Immediate**: Run `/write-tutorial` or `/write-list` for top keyword
2. **This Week**: Write top 3 articles
3. **Track**: Add to content calendar

### If Medium Volume (100-500/month)
1. **This Month**: Add to content calendar
2. **Optimize**: Focus on AEO (answer PAA questions directly)
3. **Diversify**: Mix with other high-volume topics

### If Low Volume (<100/month)
1. **Wait**: Sora 2 is new, volume will grow
2. **Alternative**: Write broader "ai video" content first
3. **Monitor**: Re-validate in 30 days

---

## Final Checklist

Before moving to Phase 3 (Content Creation):

- [ ] All 10 keywords have search_volume.monthly_avg populated
- [ ] Top 3 keywords have serp_features analyzed
- [ ] Opportunity scores calculated for all topics
- [ ] Topics ranked by priority
- [ ] Topic briefs created for top 3
- [ ] Cost tracked (should be ~$0.156)
- [ ] Results saved to JSON file
- [ ] Content calendar updated

---

## Commands Reference

```bash
# Quick validation (if network works)
python3 /Users/H/Documents/AliciBlog/scripts/dataforseo_validator.py

# Test single keyword (manual curl)
curl --user 'hans.h@hey.com:727be1453f7a4f3a' \
  -X POST 'https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live' \
  -H 'Content-Type: application/json' \
  -d '[{"keywords":["sora 2 tutorial"],"location_code":2840,"language_code":"en"}]'

# Check account balance
curl --user 'hans.h@hey.com:727be1453f7a4f3a' \
  'https://api.dataforseo.com/v3/appendix/user_data' | grep "money"
```

---

**Ready to Execute**: All preparation complete. Just run the script once network access is available.
