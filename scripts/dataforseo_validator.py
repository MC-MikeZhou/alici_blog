#!/usr/bin/env python3
"""
DataForSEO Keyword Validation Script
Calls DataForSEO REST API to get keyword metrics and SERP features
"""

import urllib.request
import urllib.error
import json
import sys
from typing import List, Dict, Any
from base64 import b64encode

class DataForSEOClient:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.base_url = "https://api.dataforseo.com/v3"

        # Create basic auth header
        credentials = f"{username}:{password}"
        self.auth_header = b64encode(credentials.encode()).decode()

    def _make_request(self, endpoint: str, payload: List[Dict]) -> Dict:
        """Make POST request to DataForSEO API"""
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Authorization": f"Basic {self.auth_header}",
            "Content-Type": "application/json"
        }

        data = json.dumps(payload).encode('utf-8')
        request = urllib.request.Request(url, data=data, headers=headers, method='POST')

        try:
            with urllib.request.urlopen(request) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            raise Exception(f"HTTP {e.code}: {error_body}")

    def get_keywords_data(self, keywords: List[str], location_code: int = 2840, language_code: str = "en") -> Dict:
        """
        Get search volume and metrics for keywords
        Endpoint: keywords_data/google_ads/search_volume/live
        Cost: ~0.015 per keyword
        """
        payload = [{
            "keywords": keywords,
            "location_code": location_code,
            "language_code": language_code,
            "search_partners": False,
            "date_from": "2025-01-01",  # Last 12 months
            "date_to": "2026-01-01"
        }]

        return self._make_request("keywords_data/google_ads/search_volume/live", payload)

    def get_serp_data(self, keyword: str, location_code: int = 2840, language_code: str = "en") -> Dict:
        """
        Get SERP features and rankings for a keyword
        Endpoint: serp/google/organic/live/advanced
        Cost: ~0.002 per query
        """
        payload = [{
            "keyword": keyword,
            "location_code": location_code,
            "language_code": language_code,
            "device": "desktop",
            "os": "windows",
            "depth": 100  # Get top 100 results
        }]

        return self._make_request("serp/google/organic/live/advanced", payload)

def extract_keyword_metrics(api_response: Dict) -> List[Dict]:
    """Extract clean metrics from keywords_data response"""
    results = []

    if api_response.get("status_code") != 20000:
        raise Exception(f"API Error: {api_response.get('status_message')}")

    tasks = api_response.get("tasks", [])
    for task in tasks:
        if task.get("status_code") != 20000:
            continue

        result = task.get("result", [])
        if not result:
            continue

        for item in result:
            keyword = item.get("keyword")
            search_volume = item.get("search_volume", 0)
            competition = item.get("competition", 0)
            cpc = item.get("cpc", 0)

            # Monthly searches breakdown
            monthly_searches = item.get("monthly_searches", [])

            results.append({
                "keyword": keyword,
                "search_volume": search_volume,
                "competition_index": competition,
                "cpc": cpc,
                "monthly_searches": monthly_searches
            })

    return results

def extract_serp_features(api_response: Dict) -> Dict:
    """Extract SERP features from serp response"""
    features = {
        "ai_overview": False,
        "featured_snippet": False,
        "people_also_ask": False,
        "paa_questions": [],
        "video": False,
        "discussions_forums": False,
        "top_organic": []
    }

    if api_response.get("status_code") != 20000:
        return features

    tasks = api_response.get("tasks", [])
    for task in tasks:
        result = task.get("result", [])
        if not result:
            continue

        for item in result:
            items_list = item.get("items", [])

            for serp_item in items_list:
                item_type = serp_item.get("type")

                # Check for different SERP features
                if item_type == "ai_overview":
                    features["ai_overview"] = True
                elif item_type == "featured_snippet":
                    features["featured_snippet"] = True
                elif item_type == "people_also_ask":
                    features["people_also_ask"] = True
                    # Extract PAA questions
                    paa_items = serp_item.get("items", [])
                    for paa in paa_items:
                        question = paa.get("title")
                        if question:
                            features["paa_questions"].append(question)
                elif item_type == "video":
                    features["video"] = True
                elif item_type in ["discussions_and_forums", "forum"]:
                    features["discussions_forums"] = True
                elif item_type == "organic":
                    # Collect top organic results
                    rank_group = serp_item.get("rank_group")
                    if rank_group and rank_group <= 10:
                        features["top_organic"].append({
                            "rank": rank_group,
                            "domain": serp_item.get("domain"),
                            "title": serp_item.get("title"),
                            "url": serp_item.get("url")
                        })

    return features

def main():
    # DataForSEO credentials
    USERNAME = "hans.h@hey.com"
    PASSWORD = "727be1453f7a4f3a"

    # Phase 2 Priority Keywords from phase-1-keyword-expansion.json
    keywords = [
        "AI video prompts",
        "best AI video prompts 2026",
        "AI video prompt engineering",
        "Sora AI prompts",
        "ChatGPT prompts for video creation",
        "text to video AI prompts",
        "how to write prompts for AI videos",
        "AI video prompt examples",
        "AI video prompt templates",
        "AI video generation prompts",
        "AI video prompts for social media",
        "AI video prompts for YouTube",
        "AI video prompts for TikTok",
        "AI video prompts for Instagram",
        "AI video prompts for ads",
        "AI animation prompts",
        "image to video AI prompts",
        "Runway Gen-3 prompts",
        "AI video prompts 2026",
        "best prompts for AI video generators",
        "AI video prompt guide",
        "free AI video prompts",
        "AI video prompts for beginners",
        "AI video marketing prompts",
        "AI product video prompts"
    ]

    client = DataForSEOClient(USERNAME, PASSWORD)

    print("=" * 80)
    print("DataForSEO Keyword Validation - Phase 2")
    print("=" * 80)
    print()

    # Step 1: Get keyword metrics
    print("Step 1: Fetching keyword metrics...")
    print(f"Keywords: {len(keywords)}")
    print()

    try:
        keywords_response = client.get_keywords_data(keywords)
        keyword_metrics = extract_keyword_metrics(keywords_response)

        # Display results
        print(f"✓ Retrieved metrics for {len(keyword_metrics)} keywords")
        print()
        print("Keyword Metrics:")
        print("-" * 80)
        print(f"{'Keyword':<40} {'Volume':>10} {'CPC':>8} {'Comp':>6}")
        print("-" * 80)

        for metric in keyword_metrics:
            comp = metric['competition_index'] if metric['competition_index'] is not None else 0
            # Handle both string and numeric competition values
            if isinstance(comp, str):
                comp_str = comp[:6]
            else:
                comp_str = f"{comp:.2f}"
            cpc_val = metric['cpc'] if metric['cpc'] is not None else 0
            vol = metric['search_volume'] if metric['search_volume'] is not None else 0
            print(f"{metric['keyword']:<40} {vol:>10} ${cpc_val:>7.2f} {comp_str:>6}")

        print()

    except Exception as e:
        print(f"✗ Error fetching keyword metrics: {e}")
        sys.exit(1)

    # Step 2: Get SERP features for top 3 keywords
    print("Step 2: Fetching SERP features for top queries...")
    print()

    # Sort by volume and get top 3 (handle None values)
    top_keywords = sorted(keyword_metrics, key=lambda x: x['search_volume'] if x['search_volume'] is not None else 0, reverse=True)[:3]

    serp_results = {}
    for kw_data in top_keywords:
        keyword = kw_data['keyword']
        print(f"  Analyzing: {keyword}")

        try:
            serp_response = client.get_serp_data(keyword)
            serp_features = extract_serp_features(serp_response)
            serp_results[keyword] = serp_features

            # Display features
            features_found = []
            if serp_features['ai_overview']:
                features_found.append("AI Overview")
            if serp_features['featured_snippet']:
                features_found.append("Featured Snippet")
            if serp_features['people_also_ask']:
                features_found.append(f"PAA ({len(serp_features['paa_questions'])})")
            if serp_features['video']:
                features_found.append("Video")
            if serp_features['discussions_forums']:
                features_found.append("Forums")

            print(f"    Features: {', '.join(features_found) if features_found else 'None'}")

        except Exception as e:
            print(f"    ✗ Error: {e}")

    print()

    # Step 3: Generate structured output
    print("=" * 80)
    print("Structured Output (JSON)")
    print("=" * 80)
    print()

    output = {
        "phase": "2_dataforseo_validation",
        "analysis_date": "2026-01-26",
        "validation_method": "dataforseo_rest_api",
        "seed": "The ONLY 7 Prompts You Need to Create Any AI Video",
        "total_keywords_validated": len(keywords),
        "keywords": []
    }

    # Process each keyword and assign tier
    for metric in keyword_metrics:
        keyword = metric['keyword']
        volume = metric['search_volume'] if metric['search_volume'] is not None else 0
        cpc = metric['cpc'] if metric['cpc'] is not None else 0

        # Tier classification
        if volume >= 1000 and cpc >= 3.0:
            tier = 1
        elif volume >= 500 and cpc >= 2.0:
            tier = 2
        elif volume >= 100:
            tier = 3
        else:
            tier = 4

        keyword_data = {
            "keyword": keyword,
            "search_volume": volume,
            "cpc": cpc,
            "competition_index": metric['competition_index'],
            "tier": tier
        }

        # Add SERP features if available
        if keyword in serp_results:
            keyword_data["serp_features"] = {
                "ai_overview": serp_results[keyword]['ai_overview'],
                "featured_snippet": serp_results[keyword]['featured_snippet'],
                "people_also_ask": serp_results[keyword]['people_also_ask'],
                "paa_questions": serp_results[keyword]['paa_questions'][:5] if serp_results[keyword]['paa_questions'] else [],
                "video": serp_results[keyword]['video'],
                "discussions_forums": serp_results[keyword]['discussions_forums']
            }

            # Add top competitors
            if serp_results[keyword]['top_organic']:
                keyword_data["top_competitors"] = serp_results[keyword]['top_organic'][:5]

        output["keywords"].append(keyword_data)

    # Save to file
    output_file = "/Users/H/Documents/AliciBlog/reports 待发文章/2026-01-26-ai-video-prompts/phase-2-validation-results.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(json.dumps(output, indent=2))
    print()
    print(f"✓ Output saved to: {output_file}")
    print()

    # Calculate cost
    keywords_cost = len(keywords) * 0.015
    serp_cost = len(top_keywords) * 0.002
    total_cost = keywords_cost + serp_cost

    print("=" * 80)
    print("API Cost Summary")
    print("=" * 80)
    print(f"Keywords Data ({len(keywords)} keywords): ${keywords_cost:.3f}")
    print(f"SERP Analysis ({len(top_keywords)} queries): ${serp_cost:.3f}")
    print(f"Total: ${total_cost:.3f}")
    print()

if __name__ == "__main__":
    main()
