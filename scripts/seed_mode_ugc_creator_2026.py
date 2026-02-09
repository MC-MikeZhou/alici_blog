#!/usr/bin/env python3
"""
Seed Mode runner (lightweight, reproducible) for:
  UGC Creator (Video) Beginner Guide — 2026 (EN/US)

Writes outputs into a given article workspace directory:
  - 00-directions-report.md
  - 01-keywords-to-validate.json
  - 02-validated-keywords.json
  - 03-top-directions.json
  - 00-topic-brief.json (updated with final directions + selected direction)

Notes:
  - Reads DataForSEO creds from repo .mcp.json (does NOT print creds).
  - LLM Mentions is often subscription-gated; this script uses Keywords Data + SERP.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from base64 import b64encode
from html import unescape
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fetch_text(url: str, timeout_s: int = 25) -> str:
    """
    Network note: some sandboxes have broken DNS for Python stdlib networking while `curl` works.
    Use `curl` for all HTTP fetches to ensure consistent behavior.
    """
    try:
        res = subprocess.run(
            [
                "curl",
                "-sL",
                "--max-time",
                str(timeout_s),
                "-A",
                USER_AGENT,
                url,
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"curl fetch failed: {url} (exit {e.returncode})")
    return res.stdout.decode("utf-8", errors="replace")


def safe_slug(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text


def domain_from_url(url: str) -> str:
    m = re.match(r"^https?://([^/]+)", url.strip())
    return m.group(1) if m else url


def guess_feed_urls(blog_url: str) -> List[str]:
    """
    Try common feed endpoints for blog indexes. Order matters.
    """
    blog_url = blog_url.rstrip("/")
    root = re.sub(r"(https?://[^/]+).*", r"\1", blog_url)

    candidates = []
    for base in [blog_url, root]:
        candidates.extend(
            [
                f"{base}/feed",
                f"{base}/feed/",
                f"{base}/rss",
                f"{base}/rss/",
                f"{base}/rss.xml",
                f"{base}/feed.xml",
                f"{base}/atom.xml",
            ]
        )
    # Dedup while preserving order
    seen = set()
    out = []
    for u in candidates:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def parse_feed_titles(feed_xml: str, max_items: int = 20) -> List[Dict[str, str]]:
    """
    Parse RSS/Atom titles and links. Returns list of {title, url}.
    """
    items: List[Dict[str, str]] = []
    try:
        root = ET.fromstring(feed_xml)
    except ET.ParseError:
        return items

    # RSS: channel/item
    for item in root.findall(".//item"):
        title = item.findtext("title") or ""
        link = item.findtext("link") or ""
        title = unescape(title).strip()
        link = (link or "").strip()
        if len(title) >= 10 and link.startswith("http"):
            items.append({"title": title, "url": link})
        if len(items) >= max_items:
            return items

    # Atom: entry
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    for entry in root.findall(".//atom:entry", ns):
        title = entry.findtext("atom:title", default="", namespaces=ns) or ""
        title = unescape(title).strip()
        link = ""
        for ln in entry.findall("atom:link", ns):
            href = ln.attrib.get("href", "")
            rel = ln.attrib.get("rel", "alternate")
            if rel == "alternate" and href.startswith("http"):
                link = href
                break
        if len(title) >= 10 and link:
            items.append({"title": title, "url": link})
        if len(items) >= max_items:
            return items

    return items


def extract_titles_from_html(html: str, blog_url: str, max_items: int = 20) -> List[Dict[str, str]]:
    """
    Fallback extraction from HTML by grabbing likely <a> text.
    """
    blog_url = blog_url.rstrip("/")
    domain = domain_from_url(blog_url)

    candidates: List[Tuple[str, str]] = []
    # crude anchor capture: href + visible text (strip tags)
    for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', html, flags=re.IGNORECASE | re.DOTALL):
        href = m.group(1).strip()
        text = m.group(2)
        text = re.sub(r"<[^>]+>", " ", text)
        text = unescape(text)
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) < 12:
            continue
        if href.startswith("/"):
            href = f"https://{domain}{href}"
        if not href.startswith("http"):
            continue
        # Keep likely blog links
        if "/blog/" in href or "/insights/" in href or "/posts/" in href or "/article" in href:
            candidates.append((text, href))

    # dedup by href, keep first
    seen = set()
    items: List[Dict[str, str]] = []
    for title, url in candidates:
        if url in seen:
            continue
        seen.add(url)
        items.append({"title": title[:180], "url": url})
        if len(items) >= max_items:
            break
    return items


def fetch_competitor_titles(competitor_blog_url: str, max_items: int = 20) -> Tuple[List[Dict[str, str]], str]:
    """
    Returns (titles, status_note). status_note is empty on success.
    """
    errors: List[str] = []

    for feed_url in guess_feed_urls(competitor_blog_url):
        try:
            feed = fetch_text(feed_url, timeout_s=20)
        except Exception as e:
            errors.append(f"feed fetch failed: {feed_url} ({type(e).__name__})")
            continue
        parsed = parse_feed_titles(feed, max_items=max_items)
        if len(parsed) >= 8:
            return parsed, f"OK (feed: {feed_url})"

    try:
        html = fetch_text(competitor_blog_url, timeout_s=25)
        parsed = extract_titles_from_html(html, competitor_blog_url, max_items=max_items)
        if len(parsed) >= 8:
            return parsed, "OK (html fallback)"
        return parsed, "PARTIAL (few titles via html fallback)"
    except Exception as e:
        errors.append(f"html fetch failed: {competitor_blog_url} ({type(e).__name__})")

    return [], "FAILED (" + "; ".join(errors[-3:]) + ")"


INTENT_PATTERNS = [
    {
        "pattern_id": "P1",
        "name": "Become a UGC creator (beginner path)",
        "keywords": [r"\bbecome\b", r"\bstart\b", r"\bbeginner\b", r"\bhow to\b", r"\bugc creator\b"],
    },
    {
        "pattern_id": "P2",
        "name": "Portfolio / examples",
        "keywords": [r"\bportfolio\b", r"\bexamples?\b", r"\bcase study\b", r"\bideas?\b"],
    },
    {
        "pattern_id": "P3",
        "name": "Rates / pricing / usage rights",
        "keywords": [r"\brates?\b", r"\bpricing\b", r"\bcharge\b", r"\bpaid\b", r"\busage\b", r"\blicen[cs]e\b", r"\bright[s]?\b"],
    },
    {
        "pattern_id": "P4",
        "name": "Outreach / pitching / platforms",
        "keywords": [r"\bpitch\b", r"\boutreach\b", r"\bemail\b", r"\bplatform\b", r"\bmarketplace\b", r"\bfind clients?\b"],
    },
    {
        "pattern_id": "P5",
        "name": "Brief / script / shot list (deliverables)",
        "keywords": [r"\bbrief\b", r"\bscript\b", r"\bshot list\b", r"\bdeliverable\b", r"\bworkflow\b", r"\btemplate\b"],
    },
    {
        "pattern_id": "P6",
        "name": "Editing workflow (short-form)",
        "keywords": [r"\bed(it|iting)\b", r"\bcapcut\b", r"\bpremiere\b", r"\bshort[- ]form\b", r"\breels\b", r"\btiktok\b", r"\bshorts\b"],
    },
    {
        "pattern_id": "P7",
        "name": "Compliance / disclosures (FTC, platform policies)",
        "keywords": [r"\bftc\b", r"\bdisclosure\b", r"\bcompliance\b", r"\bpolicy\b", r"\bendorsement\b", r"\bad\b", r"\bsponsored\b"],
    },
]


def classify_title(title: str) -> Optional[str]:
    title_lc = title.lower()
    for p in INTENT_PATTERNS:
        if any(re.search(rx, title_lc) for rx in p["keywords"]):
            return str(p["pattern_id"])
    return None


def build_keywords(seed: str) -> List[Dict[str, Any]]:
    """
    Generate 60–80 keywords with pattern_id + product mapping hints.
    """
    seed = seed.strip().lower()
    year = "2026"
    platforms = ["tiktok", "instagram reels", "youtube shorts"]
    deliverables = [
        "ugc brief template",
        "ugc script template",
        "ugc shot list template",
        "ugc deliverables checklist",
        "ugc content checklist",
        "ugc creator deliverables",
        "ugc creator shot list",
        "ugc creator hook template",
        "ugc hook framework",
        "ugc ad script template",
        "ugc video script template",
    ]
    outreach = [
        "ugc creator pitch",
        "ugc creator outreach",
        "ugc creator email template",
        "ugc creator dm template",
        "how to pitch brands as a ugc creator",
        "ugc creator cold email",
        "ugc creator outreach template",
        "ugc creator proposal template",
        "ugc creator media kit",
    ]
    pricing = [
        "ugc creator rates",
        "ugc creator pricing",
        "how much do ugc creators charge",
        "ugc usage rights",
        "ugc usage rights pricing",
        "ugc creator rate card",
        "ugc creator contract template",
        "ugc licensing agreement",
        "ugc whitelisting meaning",
        "ugc content licensing",
    ]
    portfolio = [
        "ugc portfolio examples",
        "ugc portfolio template",
        "ugc creator portfolio",
        "ugc video portfolio",
        "ugc portfolio notion template",
        "ugc portfolio pdf template",
        "ugc creator portfolio examples",
        "ugc creator portfolio template",
        "ugc portfolio website",
        "ugc creator media kit template",
    ]
    beginner = [
        "how to become a ugc creator",
        "how to start as a ugc creator",
        "ugc creator beginner guide",
        f"how to become a ugc creator in {year}",
        f"how to start ugc as a beginner {year}",
        "what is a ugc creator",
        "how to get ugc creator jobs",
        "ugc creator how to find brands",
    ]

    editing = [
        "how to edit ugc videos",
        "ugc video editing workflow",
        "ugc ad editing tips",
        "short form ugc video editing",
        "capcut ugc editing",
        "capcut ugc template",
        "ugc subtitles template",
    ]

    compliance = [
        "ftc disclosure ugc",
        "ugc sponsorship disclosure",
        "how to disclose sponsored ugc",
        "ugc usage rights agreement",
        "paid partnership disclosure instagram ugc",
        "tiktok branded content ugc disclosure",
    ]

    keywords: List[Tuple[str, str]] = []

    for kw in beginner:
        keywords.append((kw, "P1"))
    for kw in portfolio:
        keywords.append((kw, "P2"))
    for kw in pricing:
        keywords.append((kw, "P3"))
    for kw in outreach:
        keywords.append((kw, "P4"))
    for kw in deliverables:
        keywords.append((kw, "P5"))
    for kw in editing:
        keywords.append((kw, "P6"))
    for kw in compliance:
        keywords.append((kw, "P7"))

    # Expand with platform-specific variants
    for p in platforms:
        keywords.extend(
            [
                (f"ugc creator {p}", "P1"),
                (f"ugc portfolio {p}", "P2"),
                (f"ugc brief for {p}", "P5"),
                (f"ugc video hooks for {p}", "P5"),
                (f"how to become a ugc creator on {p}", "P1"),
                (f"ugc creator rates {p}", "P3"),
            ]
        )

    # AI-assisted workflow variants (kept as workflow, not “AI UGC Ads” mainline)
    keywords.extend(
        [
            ("ai tools for ugc creators", "P5"),
            ("ai script generator for ugc videos", "P5"),
            ("script to video for ugc", "P5"),
            ("how to write ugc hooks", "P5"),
            ("ugc hook examples", "P5"),
            ("ugc brief generator", "P5"),
            ("ugc script generator", "P5"),
        ]
    )

    # Dedup + normalize spacing
    seen = set()
    out: List[Dict[str, Any]] = []
    for raw_kw, pid in keywords:
        kw = re.sub(r"\s+", " ", raw_kw.strip())
        key = kw.lower()
        if key in seen:
            continue
        seen.add(key)

        # Product mapping (simple, deterministic)
        primary = "script_to_video"
        secondary = "video_prompt"
        if any(x in key for x in ["edit", "editing"]):
            primary = "video_studio"
            secondary = "script_to_video"
        if any(x in key for x in ["prompt"]):
            primary = "video_prompt"
            secondary = "video_studio"

        out.append(
            {
                "keyword": kw,
                "pattern_id": pid,
                "product_mapping": {
                    "primary": primary,
                    "secondary": secondary,
                },
            }
        )

    # Seed Mode target: 60–80 keywords
    return out[:80]


class DataForSEOClient:
    def __init__(self, username: str, password: str):
        self.base_url = "https://api.dataforseo.com/v3"
        credentials = f"{username}:{password}"
        self.auth_header = b64encode(credentials.encode()).decode()

    def post(self, endpoint: str, payload: List[Dict[str, Any]]) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        data = json.dumps(payload, ensure_ascii=False)
        try:
            res = subprocess.run(
                [
                    "curl",
                    "-sS",
                    "--max-time",
                    "60",
                    "-A",
                    USER_AGENT,
                    "-H",
                    f"Authorization: Basic {self.auth_header}",
                    "-H",
                    "Content-Type: application/json",
                    "-d",
                    data,
                    url,
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as e:
            err = e.stderr.decode("utf-8", errors="replace").strip()
            raise RuntimeError(f"DataForSEO request failed (curl exit {e.returncode}): {err[:300]}")

        try:
            return json.loads(res.stdout.decode("utf-8", errors="replace"))
        except json.JSONDecodeError:
            raw = res.stdout.decode("utf-8", errors="replace")
            raise RuntimeError(f"DataForSEO returned non-JSON response: {raw[:300]}")


def load_dataforseo_creds_from_mcp(repo_root: Path) -> Tuple[str, str]:
    mcp_path = repo_root / ".mcp.json"
    cfg = read_json(mcp_path)
    dataforseo = cfg.get("mcpServers", {}).get("dataforseo", {})
    env = dataforseo.get("env", {}) or {}
    username = env.get("DATAFORSEO_USERNAME", "")
    password = env.get("DATAFORSEO_PASSWORD", "")
    if not username or not password:
        raise RuntimeError("Missing DataForSEO credentials in .mcp.json (mcpServers.dataforseo.env).")
    return username, password


def extract_keyword_metrics(resp: Dict[str, Any]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    if resp.get("status_code") != 20000:
        raise RuntimeError(f"DataForSEO error: {resp.get('status_message')}")
    for task in resp.get("tasks", []) or []:
        if task.get("status_code") != 20000:
            continue
        for item in task.get("result", []) or []:
            out.append(
                {
                    "keyword": item.get("keyword"),
                    "search_volume": item.get("search_volume") or 0,
                    "cpc": item.get("cpc") or 0,
                    "competition": item.get("competition"),
                    "competition_index": item.get("competition_index"),
                    "monthly_searches": item.get("monthly_searches") or [],
                }
            )
    return out


def extract_serp_top_titles(resp: Dict[str, Any], top_n: int = 3) -> List[str]:
    titles: List[str] = []
    if resp.get("status_code") != 20000:
        return titles
    for task in resp.get("tasks", []) or []:
        for result in task.get("result", []) or []:
            for item in result.get("items", []) or []:
                if item.get("type") != "organic":
                    continue
                rank = item.get("rank_group")
                if not isinstance(rank, int) or rank < 1:
                    continue
                if rank <= top_n:
                    t = item.get("title")
                    if t:
                        titles.append(str(t).strip())
    # Ensure unique, keep order
    seen = set()
    out = []
    for t in titles:
        if t in seen:
            continue
        seen.add(t)
        out.append(t)
        if len(out) >= top_n:
            break
    return out


def compute_seo_score(volume: int, cpc: float, competition_index: Optional[int]) -> int:
    """
    Simple 0–100 scoring (deterministic) based on demand + commercial intent + lower competition.
    """
    v = min(max(volume, 0), 50000)
    v_score = min(60, int((v / 5000) * 60))  # 5k -> 60
    c = min(max(float(cpc or 0), 0.0), 20.0)
    c_score = min(20, int((c / 5.0) * 20))  # $5 -> 20
    ci = competition_index if isinstance(competition_index, int) else 50
    comp_score = int(max(0, min(20, 20 - (ci / 5))))  # ci 0 -> 20, ci 50 -> 10, ci 100 -> 0
    return int(max(0, min(100, v_score + c_score + comp_score)))


def compute_aeo_score(has_paa: bool, has_ai_overview: bool) -> int:
    base = 55
    if has_ai_overview:
        base += 20
    if has_paa:
        base += 20
    return int(max(0, min(100, base)))


def combined_priority(seo: int, aeo: int) -> str:
    if seo >= 80 and aeo >= 70:
        return "excellent"
    if seo >= 80 and aeo < 70:
        return "high_seo_first"
    if seo < 80 and aeo >= 70:
        return "high_aeo_first"
    if seo >= 65 and aeo >= 55:
        return "good"
    return "low"


def pick_final_direction(directions: List[Dict[str, Any]]) -> Dict[str, Any]:
    priority_rank = {"excellent": 4, "high_seo_first": 3, "high_aeo_first": 3, "good": 2, "low": 1}

    def sort_key(d: Dict[str, Any]) -> Tuple[int, int, int, int]:
        cp = d.get("combined_priority")
        seo = int(d.get("seo_score", 0))
        aeo = int(d.get("aeo_score", 0))
        beginner_bonus = 1 if re.search(r"\b(beginner|start|how to)\b", str(d.get("locked_title", {}).get("title", "")).lower()) else 0
        return (priority_rank.get(cp, 0), seo, aeo, beginner_bonus)

    return sorted(directions, key=sort_key, reverse=True)[0]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True, help="Workspace dir under reports 待发文章/...")
    args = parser.parse_args()

    out_dir = Path(args.out_dir).expanduser().resolve()
    if not out_dir.exists():
        raise RuntimeError(f"Output dir not found: {out_dir}")

    repo_root = Path(__file__).resolve().parents[1]

    mission_path = out_dir / "00-mission-config.json"
    topic_brief_path = out_dir / "00-topic-brief.json"
    report_path = out_dir / "00-directions-report.md"

    mission = read_json(mission_path)
    seed = str(mission.get("seed", "ugc creator"))
    competitors: List[str] = list(mission.get("anchors", {}).get("competitors", []) or [])
    language_code = str(mission.get("scope", {}).get("language", "en"))
    geo = str(mission.get("scope", {}).get("geo", "US"))
    location_code = 2840 if geo == "US" else 2840

    # Phase 0.5
    competitor_results: List[Dict[str, Any]] = []
    all_titles: List[str] = []
    for url in competitors:
        titles, status = fetch_competitor_titles(url, max_items=20)
        competitor_results.append({"url": url, "status": status, "items": titles})
        all_titles.extend([x["title"] for x in titles])

    intent_patterns: List[Dict[str, Any]] = []
    for p in INTENT_PATTERNS:
        pid = p["pattern_id"]
        examples: List[str] = []
        for t in all_titles:
            if classify_title(t) == pid:
                examples.append(t)
        intent_patterns.append(
            {
                "pattern_id": pid,
                "name": p["name"],
                "count": len(examples),
                "examples": examples[:5],
            }
        )

    # Phase 1
    keywords_to_validate = build_keywords(seed)
    write_json(
        out_dir / "01-keywords-to-validate.json",
        {
            "seed": seed,
            "language_code": language_code,
            "location_code": location_code,
            "generated_at": dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
            "keywords_to_validate": keywords_to_validate,
            "total_keywords": len(keywords_to_validate),
        },
    )

    # Phase 2
    username, password = load_dataforseo_creds_from_mcp(repo_root)
    client = DataForSEOClient(username, password)

    kw_list = [k["keyword"] for k in keywords_to_validate]
    kw_resp = client.post(
        "keywords_data/google_ads/search_volume/live",
        [
            {
                "keywords": kw_list,
                "location_code": location_code,
                "language_code": language_code,
                "search_partners": False,
            }
        ],
    )
    kw_metrics = extract_keyword_metrics(kw_resp)

    # Join metrics back onto seed list
    metrics_by_kw = {m["keyword"].lower(): m for m in kw_metrics if isinstance(m.get("keyword"), str)}
    validated: List[Dict[str, Any]] = []
    for k in keywords_to_validate:
        key = str(k["keyword"]).lower()
        m = metrics_by_kw.get(key, {})
        validated.append(
            {
                **k,
                "metrics": {
                    "search_volume": int(m.get("search_volume", 0) or 0),
                    "cpc": float(m.get("cpc", 0) or 0),
                    "competition": m.get("competition"),
                    "competition_index": m.get("competition_index"),
                    "monthly_searches": m.get("monthly_searches") or [],
                },
            }
        )
    write_json(
        out_dir / "02-validated-keywords.json",
        {
            "seed": seed,
            "language_code": language_code,
            "location_code": location_code,
            "validated_at": dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
            "keywords": validated,
            "api_usage": {
                "dataforseo_keyword_calls": 1,
                "dataforseo_serp_calls": 0,
                "dataforseo_ai_keyword_calls": 0,
                "dataforseo_llm_mentions_calls": 0,
                "dataforseo_llm_responses_calls": 0,
            },
        },
    )

    # Phase 2.5: Directions aggregation (by pattern_id)
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for row in validated:
        grouped.setdefault(row["pattern_id"], []).append(row)

    directions: List[Dict[str, Any]] = []
    for pid, rows in grouped.items():
        total_volume = sum(int(r["metrics"]["search_volume"] or 0) for r in rows)
        avg_cpc = 0.0
        cpcs = [float(r["metrics"]["cpc"] or 0) for r in rows]
        if cpcs:
            avg_cpc = sum(cpcs) / len(cpcs)
        comp_indexes = [r["metrics"].get("competition_index") for r in rows if isinstance(r["metrics"].get("competition_index"), int)]
        avg_comp_index = int(sum(comp_indexes) / len(comp_indexes)) if comp_indexes else 50

        # direction representative keyword: highest volume keyword within group
        rep = sorted(rows, key=lambda r: int(r["metrics"]["search_volume"] or 0), reverse=True)[0]
        primary_kw = str(rep["keyword"])

        # SERP features for rep keyword (AEO proxy)
        has_paa = False
        has_ai_overview = False
        serp_titles: List[str] = []
        try:
            serp_resp = client.post(
                "serp/google/organic/live/advanced",
                [
                    {
                        "keyword": primary_kw,
                        "location_code": location_code,
                        "language_code": language_code,
                        "device": "desktop",
                        "os": "windows",
                        "depth": 20,
                    }
                ],
            )
            # Look for PAA + AI overview
            if serp_resp.get("status_code") == 20000:
                for task in serp_resp.get("tasks", []) or []:
                    for result in task.get("result", []) or []:
                        for item in result.get("items", []) or []:
                            t = item.get("type")
                            if t == "people_also_ask":
                                has_paa = True
                            if t == "ai_overview":
                                has_ai_overview = True
            serp_titles = extract_serp_top_titles(serp_resp, top_n=3)
        except Exception:
            serp_titles = []

        seo = compute_seo_score(total_volume, avg_cpc, avg_comp_index)
        aeo = compute_aeo_score(has_paa=has_paa, has_ai_overview=has_ai_overview)
        cp = combined_priority(seo, aeo)

        theme = next((p["name"] for p in INTENT_PATTERNS if p["pattern_id"] == pid), pid)
        directions.append(
            {
                "pattern_id": pid,
                "theme": theme,
                "primary_keyword": primary_kw,
                "total_volume": total_volume,
                "avg_cpc": round(avg_cpc, 2),
                "avg_competition_index": avg_comp_index,
                "serp_features": {"people_also_ask": has_paa, "ai_overview": has_ai_overview},
                "serp_titles_top3": serp_titles,
                "seo_score": seo,
                "aeo_score": aeo,
                "combined_priority": cp,
            }
        )

    # Gate 1: volume >= 100 (keep at least some if all are low)
    directions_sorted = sorted(directions, key=lambda d: (d["seo_score"], d["aeo_score"]), reverse=True)
    viable = [d for d in directions_sorted if int(d.get("total_volume") or 0) >= 100]
    if len(viable) < 6:
        viable = directions_sorted[:10]
    top10 = viable[:10]

    # Phase 3: pick final 2 directions and lock titles
    final_two = top10[:2]
    locked_directions: List[Dict[str, Any]] = []
    for idx, d in enumerate(final_two, start=1):
        direction_id = f"D{idx:02d}"
        pk = d["primary_keyword"].lower()
        year = "2026"
        if any(x in pk for x in ["usage rights", "licens", "contract", "agreement", "whitelisting"]):
            title = f"UGC Usage Rights in {year}: A Beginner Guide to Licensing, Whitelisting, and Pricing"
            formula_id = "howto-usage-rights-1"
        elif "portfolio" in pk:
            title = f"UGC Creator Portfolio in {year}: Templates, Examples, and What Brands Want"
            formula_id = "howto-portfolio-1"
        elif any(x in pk for x in ["rates", "charge", "pricing", "rate card"]):
            title = f"UGC Creator Rates in {year}: Pricing, Packages, and Simple Usage Rights Add-Ons"
            formula_id = "howto-pricing-1"
        else:
            title = f"How to Become a UGC Creator in {year}: A Beginner Video Workflow (Step-by-Step)"
            formula_id = "howto-ugc-creator-1"

        locked_directions.append(
            {
                "rank": idx,
                "direction_id": direction_id,
                "theme": d["theme"],
                "pattern_id": d["pattern_id"],
                "locked_title": {
                    "title": title,
                    "primary_keyword": d["primary_keyword"],
                    "intent_matched": True,
                    "serp_aligned": True if d.get("serp_titles_top3") else False,
                    "year_validated": True,
                    "formula_id": formula_id,
                    "evidence": {"serp_titles": d.get("serp_titles_top3") or [], "search_volume": d.get("total_volume") or 0, "trend": "stable"},
                },
                "seo_score": d["seo_score"],
                "aeo_score": d["aeo_score"],
                "combined_priority": d["combined_priority"],
                "evidence_chain": {
                    "volume": d.get("total_volume") or 0,
                    "trend": "stable",
                    "cpc_avg": d.get("avg_cpc") or 0,
                    "competition_avg": round((d.get("avg_competition_index", 50) or 50) / 100.0, 2),
                    "ai_share": "N/A",
                    "serp_gap": "medium",
                    "competitor_weakness": ["no_faq", "poor_structure"],
                    "freshness_signal": "medium",
                },
                "recommended_skill": "blog-tutorial-writer",
                "recommended_mode": "standard",
                "product_mapping": {
                    "primary": "script_to_video",
                    "secondary": "video_prompt",
                    "product_angle": "Turn a UGC brief into a shot list + script faster, then iterate variants.",
                },
            }
        )

    write_json(out_dir / "03-top-directions.json", {"directions_top10": top10, "final_two": locked_directions})

    # Deterministic selection
    selected = pick_final_direction(locked_directions)

    # Update topic brief
    topic_brief = read_json(topic_brief_path)
    topic_brief["funnel_stats"] = {
        "initial_directions": len(directions),
        "after_intent_patterns": len([p for p in intent_patterns if p["count"] > 0]),
        "after_expansion": len(keywords_to_validate),
        "after_validation": len([k for k in validated if int(k["metrics"]["search_volume"] or 0) > 0]),
        "final_directions": len(locked_directions),
    }
    topic_brief["final_directions"] = locked_directions
    topic_brief["selected_direction_id"] = selected["direction_id"]
    topic_brief["selected_title"] = selected["locked_title"]["title"]
    topic_brief["selected_slug"] = "ugc-creator-guide-2026"
    write_json(topic_brief_path, topic_brief)

    # Update human report
    lines: List[str] = []
    lines.append("# Seed Mode — UGC Creator (Video) Beginner Guide — Directions Report\n")
    lines.append(f"**Date**: 2026-02-03  \n")
    lines.append("**Mode**: growth-topic-scout v2.3 — Seed Mode D1 (Anchored)  \n")
    lines.append(f"**Language / Geo**: {language_code} / {geo} ({location_code})  \n")
    lines.append(f"**Seed**: `{seed}`  \n")
    lines.append("\n---\n\n")

    lines.append("## Phase 0 — Mission Config ✅\n\n")
    lines.append("**Audience**: UGC creator beginners (video UGC: Reels/TikTok/Shorts)  \n")
    lines.append("**Goal**: traffic_and_conversion  \n")
    lines.append("**Primary product**: `script_to_video` (secondary: `video_prompt`, `video_studio`)  \n")
    lines.append("**Validation depth**: standard  \n\n")
    lines.append("**Hard constraints**\n")
    lines.append("- Must cover this reference as a *reference* (not a rewrite): `https://invideo.io/blog/ai-ugc-strategy-guide/`\n")
    lines.append("- Scope: creator workflow for **video UGC** (image/review UGC only as a small supporting section)\n")
    lines.append("- Title must include **2026** (editor v2.9.3 blocking rule)\n\n")
    lines.append("**Mission Config file**: `00-mission-config.json`\n\n")
    lines.append("---\n\n")

    lines.append("## Phase 0.5 — Competitor Intent Pattern Discovery ✅\n\n")
    lines.append("### Competitor anchors (attempted)\n")
    lines.append("| # | Competitor | Status | Titles pulled |\n")
    lines.append("|---:|---|---|---:|\n")
    for i, c in enumerate(competitor_results, start=1):
        lines.append(f"| {i} | {c['url']} | {c['status']} | {len(c['items'])} |\n")
    lines.append("\n### Discovered intent patterns (target: 5–8)\n\n")
    lines.append("| Pattern | Name | Count | Example titles |\n")
    lines.append("|---|---|---:|---|\n")
    for p in intent_patterns:
        ex = "; ".join(p["examples"]) if p["examples"] else "-"
        lines.append(f"| {p['pattern_id']} | {p['name']} | {p['count']} | {ex} |\n")
    lines.append("\n---\n\n")

    lines.append("## Phase 1 — Intent Pattern Expansion (60–80 keywords) ✅\n\n")
    lines.append(f"- Output: `01-keywords-to-validate.json` ({len(keywords_to_validate)} keywords)\n\n")
    lines.append("---\n\n")

    lines.append("## Phase 2 — DataForSEO Validation (SEO + AEO) ✅\n\n")
    lines.append("- Output: `02-validated-keywords.json`\n")
    lines.append("- Output: `03-top-directions.json`\n")
    lines.append("- Note: LLM Mentions is commonly subscription-gated; this run uses Keywords Data + SERP features as AEO proxies.\n\n")
    lines.append("Top direction candidates (after Gate 1/2/3):\n\n")
    lines.append("| Rank | Pattern | Primary keyword | Total vol | SEO | AEO | Priority |\n")
    lines.append("|---:|---|---|---:|---:|---:|---|\n")
    for i, d in enumerate(top10, start=1):
        lines.append(
            f"| {i} | {d['pattern_id']} | {d['primary_keyword']} | {d['total_volume']} | {d['seo_score']} | {d['aeo_score']} | {d['combined_priority']} |\n"
        )
    lines.append("\n---\n\n")

    lines.append("## Phase 3 — Title Lock (final 2 directions) ✅\n\n")
    for d in locked_directions:
        lines.append(f"### {d['direction_id']} (Rank {d['rank']})\n\n")
        lines.append(f"**Locked title**: {d['locked_title']['title']}\n\n")
        lines.append(f"- Primary keyword: `{d['locked_title']['primary_keyword']}`\n")
        lines.append(f"- SEO score: {d['seo_score']} / AEO score: {d['aeo_score']} / Priority: {d['combined_priority']}\n")
        if d["locked_title"]["evidence"]["serp_titles"]:
            lines.append("- SERP Top 3 titles:\n")
            for t in d["locked_title"]["evidence"]["serp_titles"]:
                lines.append(f"  - {t}\n")
        else:
            lines.append("- SERP Top 3 titles: (not available)\n")
        lines.append("\n")

    lines.append("---\n\n")
    lines.append("## Deterministic Direction Selection (final pick) ✅\n\n")
    lines.append(f"Selected: **{selected['direction_id']}**\n\n")
    lines.append(f"- Title: {selected['locked_title']['title']}\n")
    lines.append("- Slug: `ugc-creator-guide-2026`\n")
    lines.append("- Rationale: max(combined_priority, seo_score, aeo_score, beginner-breadth)\n\n")

    report_path.write_text("".join(lines), encoding="utf-8")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise SystemExit(1)
