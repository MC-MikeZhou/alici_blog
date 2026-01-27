#!/usr/bin/env python3
import json
import os
import re
import sys
from base64 import b64encode
from typing import List, Dict, Any
import urllib.request
import urllib.error

HARVEST_JSONL = "/Users/H/Documents/AliciBlog/Scale Mode/Demo/invideo-blog-harvest.jsonl"
OUTPUT_JSONL = "/Users/H/Documents/AliciBlog/Scale Mode/Demo/invideo-blog-validated.jsonl"
OUTPUT_SUMMARY = "/Users/H/Documents/AliciBlog/Scale Mode/Demo/invideo-blog-validation-summary.md"
OUTPUT_LOG = "/Users/H/Documents/AliciBlog/Scale Mode/Demo/invideo-blog-validation.log"
MCP_JSON = "/Users/H/Documents/AliciBlog/.mcp.json"

LOCATION_CODE = 2840  # US
LANGUAGE_CODE = "en"
SERP_TOP_K = 10

class DataForSEOClient:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.base_url = "https://api.dataforseo.com/v3"
        credentials = f"{username}:{password}"
        self.auth_header = b64encode(credentials.encode()).decode()

    def _make_request(self, endpoint: str, payload: List[Dict]) -> Dict:
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Authorization": f"Basic {self.auth_header}",
            "Content-Type": "application/json"
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def get_keywords_data(self, keywords: List[str]) -> Dict:
        payload = [{
            "keywords": keywords,
            "location_code": LOCATION_CODE,
            "language_code": LANGUAGE_CODE,
            "search_partners": False,
            "date_from": "2025-01-01",
            "date_to": "2026-01-01"
        }]
        return self._make_request("keywords_data/google_ads/search_volume/live", payload)

    def get_serp_data(self, keyword: str) -> Dict:
        payload = [{
            "keyword": keyword,
            "location_code": LOCATION_CODE,
            "language_code": LANGUAGE_CODE,
            "device": "desktop",
            "os": "windows",
            "depth": 50
        }]
        return self._make_request("serp/google/organic/live/advanced", payload)


def load_credentials() -> Dict[str, str]:
    username = os.environ.get("DATAFORSEO_USERNAME")
    password = os.environ.get("DATAFORSEO_PASSWORD")
    if username and password:
        return {"username": username, "password": password}

    if os.path.exists(MCP_JSON):
        with open(MCP_JSON, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        mcp = cfg.get("mcpServers", {}).get("dataforseo", {}).get("env", {})
        username = mcp.get("DATAFORSEO_USERNAME")
        password = mcp.get("DATAFORSEO_PASSWORD")
        if username and password:
            return {"username": username, "password": password}

    raise RuntimeError("DataForSEO credentials not found in env or .mcp.json")


def normalize_title_to_keyword(title: str) -> str:
    t = title.lower()
    t = re.sub(r"\b20\d{2}\b", "", t)
    t = re.sub(r"\b(best|top|how to|guide|statistics|report|reports|in)\b", "", t)
    t = re.sub(r"[^a-z0-9\s]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    words = t.split()
    # keep first 6 meaningful words
    return " ".join(words[:6])[:80]


def extract_keyword_metrics(api_response: Dict) -> Dict[str, Dict[str, Any]]:
    results = {}
    if api_response.get("status_code") != 20000:
        return results
    for task in api_response.get("tasks", []):
        if task.get("status_code") != 20000:
            continue
        for item in task.get("result", []) or []:
            kw = item.get("keyword")
            if not kw:
                continue
            results[kw] = {
                "search_volume": item.get("search_volume", 0),
                "competition_index": item.get("competition", 0),
                "cpc": item.get("cpc", 0),
                "monthly_searches": item.get("monthly_searches", [])
            }
    return results


def extract_serp_features(api_response: Dict) -> Dict[str, Any]:
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
    for task in api_response.get("tasks", []):
        for result in task.get("result", []) or []:
            for item in result.get("items", []) or []:
                t = item.get("type")
                if t == "ai_overview":
                    features["ai_overview"] = True
                elif t == "featured_snippet":
                    features["featured_snippet"] = True
                elif t == "people_also_ask":
                    features["people_also_ask"] = True
                    for paa in item.get("items", []) or []:
                        q = paa.get("title")
                        if q:
                            features["paa_questions"].append(q)
                elif t == "video":
                    features["video"] = True
                elif t in {"discussions_and_forums", "forum"}:
                    features["discussions_forums"] = True
                elif t == "organic":
                    rg = item.get("rank_group")
                    if rg and rg <= 10:
                        features["top_organic"].append({
                            "rank": rg,
                            "domain": item.get("domain"),
                            "title": item.get("title"),
                            "url": item.get("url")
                        })
    return features


def main():
    creds = load_credentials()
    client = DataForSEOClient(creds["username"], creds["password"])

    records = []
    with open(HARVEST_JSONL, "r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))

    # build keyword list
    keyword_map = {}
    keywords = []
    for r in records:
        kw = normalize_title_to_keyword(r.get("title", ""))
        if not kw:
            continue
        keyword_map[r["url"]] = kw
        if kw not in keywords:
            keywords.append(kw)

    # limit to 50 for demo
    keywords = keywords[:50]

    # fetch keyword metrics
    try:
        metrics_response = client.get_keywords_data(keywords)
    except urllib.error.HTTPError as e:
        with open(OUTPUT_LOG, "w", encoding="utf-8") as f:
            f.write(f"metrics_http_error: {e.code}\n")
            f.write("metrics_http_message: Payment Required or quota issue\n")
        with open(OUTPUT_SUMMARY, "w", encoding="utf-8") as f:
            f.write("# InVideo Growth Topic Validation Summary\n\n")
            f.write("Status: FAILED\n")
            f.write(f"Error: HTTP {e.code} from DataForSEO keywords_data endpoint\n")
            f.write("Reason: Payment required / quota issue\n")
        print("validation_failed_http_402")
        return 1
    metrics = extract_keyword_metrics(metrics_response)

    # pick top SERP keywords
    ranked = sorted(metrics.items(), key=lambda x: (x[1].get("search_volume") or 0), reverse=True)
    top_serp = [k for k, _ in ranked[:SERP_TOP_K]]

    serp_map = {}
    serp_errors = []
    for kw in top_serp:
        try:
            serp_resp = client.get_serp_data(kw)
            serp_map[kw] = extract_serp_features(serp_resp)
        except urllib.error.HTTPError as e:
            serp_errors.append(f"{kw}: HTTP {e.code}")
        except Exception as e:
            serp_errors.append(f"{kw}: {e}")

    # write output
    with open(OUTPUT_JSONL, "w", encoding="utf-8") as f:
        for r in records:
            kw = keyword_map.get(r["url"], "")
            r_out = dict(r)
            r_out["primary_keyword"] = kw
            r_out["validation"] = {
                "search_volume": metrics.get(kw, {}).get("search_volume"),
                "competition_index": metrics.get(kw, {}).get("competition_index"),
                "cpc": metrics.get(kw, {}).get("cpc"),
                "monthly_searches": metrics.get(kw, {}).get("monthly_searches"),
                "serp_features": serp_map.get(kw),
                "data_source": "dataforseo"
            }
            f.write(json.dumps(r_out, ensure_ascii=False) + "\n")

    # summary
    with open(OUTPUT_SUMMARY, "w", encoding="utf-8") as f:
        f.write("# InVideo Growth Topic Validation Summary\n\n")
        f.write(f"Total records: {len(records)}\n")
        f.write(f"Keywords validated: {len(metrics)}\n")
        f.write(f"SERP analyzed: {len(top_serp)}\n\n")
        f.write("Top keywords (by search volume):\n")
        for kw, m in ranked[:10]:
            f.write(f"- {kw}: {m.get('search_volume',0)} (CPC {m.get('cpc',0)})\n")

    with open(OUTPUT_LOG, "w", encoding="utf-8") as f:
        f.write("metrics_response_status_code: " + str(metrics_response.get("status_code")) + "\n")
        f.write("metrics_response_status_message: " + str(metrics_response.get("status_message")) + "\n")
        if metrics_response.get("tasks_error", 0) > 0:
            f.write("metrics_tasks_error: " + str(metrics_response.get("tasks_error")) + "\n")
        for task in metrics_response.get("tasks", []) or []:
            f.write("task_status_code: " + str(task.get("status_code")) + "\n")
            f.write("task_status_message: " + str(task.get("status_message")) + "\n")
        f.write("serp_requests: " + str(len(top_serp)) + "\n")
        if serp_errors:
            f.write("serp_errors: " + str(len(serp_errors)) + "\n")
            for err in serp_errors[:10]:
                f.write("serp_error: " + err + "\n")
        f.write("note: no raw payloads written\n")

    print(f"validated={len(records)} keywords={len(metrics)} serp={len(top_serp)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
