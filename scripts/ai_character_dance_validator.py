#!/usr/bin/env python3
"""
DataForSEO Keyword Validation Script for AI Character Dance Keywords
Fetches real search volume data for 25 keywords
"""

import urllib.request
import urllib.error
import json
import sys
from typing import List, Dict, Any
from base64 import b64encode
from datetime import datetime

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
            "date_from": "2025-01-01",
            "date_to": "2026-01-01"
        }]

        return self._make_request("keywords_data/google_ads/search_volume/live", payload)

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
            search_volume = item.get("search_volume", 0) or 0
            competition_raw = item.get("competition", 0)
            cpc_raw = item.get("cpc", 0)

            # Convert to proper types
            try:
                competition = float(competition_raw) if competition_raw else 0.0
            except (ValueError, TypeError):
                competition = 0.0

            try:
                cpc = float(cpc_raw) if cpc_raw else 0.0
            except (ValueError, TypeError):
                cpc = 0.0

            # Estimate keyword difficulty (simplified formula)
            # Using competition index as proxy: 0-0.3 = easy (20-40), 0.3-0.7 = medium (40-60), 0.7-1.0 = hard (60-80)
            if competition <= 0.3:
                keyword_difficulty = 20 + int(competition * 66)
            elif competition <= 0.7:
                keyword_difficulty = 40 + int((competition - 0.3) * 50)
            else:
                keyword_difficulty = 60 + int((competition - 0.7) * 66)

            results.append({
                "keyword": keyword,
                "search_volume": search_volume,
                "keyword_difficulty": keyword_difficulty,
                "competition": competition,
                "cpc": round(cpc, 2)
            })

    return results

def main():
    # DataForSEO credentials
    USERNAME = "hans.h@hey.com"
    PASSWORD = "727be1453f7a4f3a"

    # All 25 keywords for AI character dance topic
    keywords = [
        "AI character animation",
        "how to make AI character dance videos",
        "AI character dance videos for TikTok",
        "animated mascot videos for brands",
        "AI character animation for marketing",
        "create animated character videos",
        "Instagram character animation ideas",
        "best AI character animation tools",
        "character animation for product demos",
        "AI character animation tutorial",
        "professional AI character animation",
        "bulk create character animations",
        "automate character video production",
        "realistic character dance movements",
        "TikTok mascot dance trends",
        "AI character animation trends 2026",
        "fast AI character animation",
        "high quality AI mascot videos",
        "AI mascot creator comparison",
        "make money with AI character videos",
        "character video marketing trends",
        "monetize character animation content",
        "AI dance videos for social media marketing",
        "animate characters with AI",
        "character dance video maker reviews"
    ]

    client = DataForSEOClient(USERNAME, PASSWORD)

    print("=" * 80)
    print("DataForSEO Keyword Validation - AI Character Dance")
    print("=" * 80)
    print()

    print(f"Fetching metrics for {len(keywords)} keywords...")
    print()

    try:
        # Call API
        keywords_response = client.get_keywords_data(keywords)
        keyword_metrics = extract_keyword_metrics(keywords_response)

        print(f"✓ Retrieved metrics for {len(keyword_metrics)} keywords")
        print()

        # Display summary
        print("Keyword Metrics Summary:")
        print("-" * 100)
        print(f"{'Keyword':<50} {'Volume':>10} {'KD':>5} {'CPC':>8} {'Comp':>6}")
        print("-" * 100)

        for metric in sorted(keyword_metrics, key=lambda x: x['search_volume'], reverse=True):
            print(f"{metric['keyword']:<50} {metric['search_volume']:>10} {metric['keyword_difficulty']:>5} "
                  f"${metric['cpc']:>7.2f} {metric['competition']:>6.2f}")

        print()

        # Save raw response
        output_file = "/Users/H/Documents/AliciBlog/reports 待发文章/2026-01-26-ai-character-dance/dataforseo-raw-response.json"
        with open(output_file, 'w') as f:
            json.dump({
                "fetched_at": datetime.now().isoformat(),
                "total_keywords": len(keyword_metrics),
                "metrics": keyword_metrics
            }, f, indent=2)

        print(f"✓ Raw data saved to: dataforseo-raw-response.json")
        print()

        # Calculate statistics
        total_volume = sum(m['search_volume'] for m in keyword_metrics)
        avg_volume = total_volume // len(keyword_metrics)
        avg_kd = sum(m['keyword_difficulty'] for m in keyword_metrics) // len(keyword_metrics)

        print("=" * 80)
        print("Statistics:")
        print("=" * 80)
        print(f"Total Monthly Searches: {total_volume:,}")
        print(f"Average Volume: {avg_volume:,}")
        print(f"Average Keyword Difficulty: {avg_kd}")
        print()

        # Calculate cost
        keywords_cost = len(keywords) * 0.015

        print("=" * 80)
        print("API Cost Summary")
        print("=" * 80)
        print(f"Keywords Data ({len(keywords)} keywords): ${keywords_cost:.3f}")
        print()

    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
