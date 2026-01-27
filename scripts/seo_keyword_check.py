#!/usr/bin/env python3
"""
SEO Keyword Verification Script
Query DataForSEO for alternative keywords search volumes
"""

import urllib.request
import urllib.error
import json
from base64 import b64encode

# DataForSEO credentials
USERNAME = "hans.h@hey.com"
PASSWORD = "727be1453f7a4f3a"

# Keywords to query
keywords = [
    "kling ai",
    "kling ai video",
    "kling ai tutorial",
    "ai video camera control",
    "cinematic ai video",
    "cinematic ai video tutorial",
    "ai video stabilization",
    "ai video motion control",
    "kling motion brush",
    "ai video tools"
]

# Create auth header
credentials = USERNAME + ":" + PASSWORD
auth_header = b64encode(credentials.encode()).decode()

# Make request
url = "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live"
headers = {
    "Authorization": "Basic " + auth_header,
    "Content-Type": "application/json"
}

payload = [{
    "keywords": keywords,
    "location_code": 2840,  # US
    "language_code": "en",
    "search_partners": False
}]

data = json.dumps(payload).encode("utf-8")
request = urllib.request.Request(url, data=data, headers=headers, method="POST")

def safe_float(val):
    if val is None:
        return 0.0
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0

def safe_int(val):
    if val is None:
        return 0
    try:
        return int(val)
    except (ValueError, TypeError):
        return 0

try:
    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    if result.get("status_code") == 20000:
        tasks = result.get("tasks", [])
        for task in tasks:
            if task.get("status_code") == 20000:
                items = task.get("result", [])
                print("=" * 80)
                print("SEO Alternative Keywords Verification")
                print("=" * 80)
                print("%-40s %10s %10s %8s" % ("Keyword", "Volume", "CPC", "Comp"))
                print("-" * 80)

                sorted_items = sorted(items, key=lambda x: safe_int(x.get("search_volume", 0)), reverse=True)

                for item in sorted_items:
                    keyword = str(item.get("keyword", ""))
                    volume = safe_int(item.get("search_volume", 0))
                    cpc = safe_float(item.get("cpc", 0))
                    comp = safe_float(item.get("competition", 0))

                    cpc_str = "$%.2f" % cpc
                    comp_str = "%.2f" % comp

                    print("%-40s %10d %10s %8s" % (keyword, volume, cpc_str, comp_str))
                print()

                # Output JSON for further analysis
                output = {
                    "query_date": "2026-01-24",
                    "location": "US (2840)",
                    "keywords": []
                }
                for item in sorted_items:
                    output["keywords"].append({
                        "keyword": str(item.get("keyword", "")),
                        "search_volume": safe_int(item.get("search_volume", 0)),
                        "cpc": safe_float(item.get("cpc", 0)),
                        "competition": safe_float(item.get("competition", 0))
                    })

                # Save to file
                with open("/Users/H/Documents/AliciBlog/reports/kling-keyword-verification.json", "w") as f:
                    json.dump(output, f, indent=2)
                print("Saved to: /Users/H/Documents/AliciBlog/reports/kling-keyword-verification.json")

except Exception as e:
    import traceback
    print("Error: " + str(e))
    traceback.print_exc()
