#!/usr/bin/env python3
"""
Seed Mode (Top10) — competitor blog mining + DataForSEO validation (2026).

Per run (one out-dir with 00-mission-config.json):
  1) Collect competitor blog posts (last 12 months; prefer sitemap, fallback to ?page= listing crawl)
  2) Filter competitor posts by theme (UGC Ads / AI Influencer)
  3) Generate keyword pool by pattern clusters (per theme)
  4) Validate "true traffic" via DataForSEO:
     - keywords_data/google_ads/search_volume/live (all keywords)
     - serp/google/organic/live/advanced (top directions only)
  5) Output Top10 directions with locked titles (EN) + Chinese analysis report

Outputs (written into out-dir):
  - 01-competitor-posts-all.jsonl
  - 01-competitor-posts-theme.jsonl
  - 01-keywords-to-validate.json
  - 02-validated-keywords.json
  - 03-top-directions.json
  - 00-topic-brief.json (schema_version 2.3 compatible, final_directions=Top10)
  - 00-directions-report.md
"""

from __future__ import annotations

import argparse
import datetime as dt
import gzip
import json
import re
import subprocess
import time
import xml.etree.ElementTree as ET
from base64 import b64encode
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple
from urllib.parse import urljoin, urlparse


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

US_LOCATION_CODE = 2840
TRUE_TRAFFIC_THRESHOLD = 500  # direction total volume / month


# -------------------------
# JSON helpers
# -------------------------


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: Sequence[Dict[str, Any]]) -> None:
    lines = [json.dumps(r, ensure_ascii=False) for r in rows]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def utc_now_iso() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def root_from_url(url: str) -> str:
    p = urlparse(url)
    return f"{p.scheme}://{p.netloc}"


def parse_any_date(s: Optional[str]) -> Optional[dt.date]:
    if not s:
        return None
    m = re.match(r"^(\d{4}-\d{2}-\d{2})", s.strip())
    if not m:
        return None
    try:
        return dt.date.fromisoformat(m.group(1))
    except Exception:
        return None


# -------------------------
# HTTP via curl (retry)
# -------------------------


def curl_fetch(url: str, timeout_s: int = 35) -> bytes:
    res = subprocess.run(
        [
            "curl",
            "-sS",
            "-L",
            "--max-time",
            str(timeout_s),
            "-A",
            USER_AGENT,
            url,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if res.returncode != 0:
        err = res.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"curl failed (exit {res.returncode}) for {url}: {err[:240]}")
    return res.stdout


def fetch_bytes(url: str, timeout_s: int = 35, retries: int = 3) -> bytes:
    last: Optional[Exception] = None
    candidates = [url]
    # Host fallback for heygen: sometimes www/no-www DNS flaps
    if "://www.heygen.com" in url:
        candidates.append(url.replace("://www.heygen.com", "://heygen.com"))
    elif "://heygen.com" in url:
        candidates.append(url.replace("://heygen.com", "://www.heygen.com"))

    for attempt in range(1, retries + 1):
        for u in candidates:
            try:
                return curl_fetch(u, timeout_s=timeout_s)
            except Exception as e:
                last = e
        time.sleep(min(2.0, 0.4 * attempt))
    raise RuntimeError(str(last) if last else f"fetch failed: {url}")


def fetch_text(url: str, timeout_s: int = 35, retries: int = 3) -> str:
    return fetch_bytes(url, timeout_s=timeout_s, retries=retries).decode("utf-8", errors="replace")


def fetch_xml_bytes(url: str, timeout_s: int = 35, retries: int = 3) -> bytes:
    raw = fetch_bytes(url, timeout_s=timeout_s, retries=retries)
    if raw[:2] == b"\x1f\x8b":
        return gzip.decompress(raw)
    return raw


# -------------------------
# Sitemap parsing
# -------------------------


def sitemaps_from_robots(root: str) -> List[str]:
    robots_url = urljoin(root.rstrip("/") + "/", "robots.txt")
    try:
        txt = fetch_text(robots_url, timeout_s=20, retries=2)
    except Exception:
        return []
    out = []
    for line in txt.splitlines():
        if line.lower().startswith("sitemap:"):
            sm = line.split(":", 1)[1].strip()
            if sm.startswith("http"):
                out.append(sm)
    # dedup keep order
    seen = set()
    dedup = []
    for s in out:
        if s in seen:
            continue
        seen.add(s)
        dedup.append(s)
    return dedup


def parse_sitemap(xml_bytes: bytes) -> Tuple[List[Tuple[str, Optional[str]]], List[str]]:
    urls: List[Tuple[str, Optional[str]]] = []
    nested: List[str] = []
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return urls, nested

    tag = root.tag.split("}", 1)[-1].lower()
    if tag.endswith("sitemapindex"):
        for sm in root.findall(".//{*}sitemap"):
            loc = (sm.findtext("{*}loc") or "").strip()
            if loc.startswith("http"):
                nested.append(loc)
        return urls, nested

    if tag.endswith("urlset"):
        for u in root.findall(".//{*}url"):
            loc = (u.findtext("{*}loc") or "").strip()
            lastmod = (u.findtext("{*}lastmod") or "").strip() or None
            if loc.startswith("http"):
                urls.append((loc, lastmod))
        return urls, nested

    return urls, nested


def collect_sitemap_urls(root: str, max_sitemaps: int = 80, max_urls: int = 12000) -> List[Tuple[str, Optional[str]]]:
    seeds = sitemaps_from_robots(root)
    if not seeds:
        seeds = [urljoin(root.rstrip("/") + "/", "sitemap.xml")]

    queue = list(seeds)
    seen: set[str] = set()
    urls: List[Tuple[str, Optional[str]]] = []

    while queue and len(seen) < max_sitemaps and len(urls) < max_urls:
        sm = queue.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        try:
            xml_bytes = fetch_xml_bytes(sm, timeout_s=30, retries=2)
        except Exception:
            continue
        entries, nested = parse_sitemap(xml_bytes)
        urls.extend(entries)
        for nxt in nested:
            if nxt not in seen:
                queue.append(nxt)

    # dedup URL; keep lastmod when present
    by_url: Dict[str, Optional[str]] = {}
    for loc, lastmod in urls:
        if loc not in by_url or (by_url[loc] is None and lastmod is not None):
            by_url[loc] = lastmod
    return [(u, by_url[u]) for u in by_url]


# -------------------------
# Blog listing crawl fallback
# -------------------------


def list_posts_by_paging(blog_url: str, max_pages: int = 60) -> List[str]:
    """
    Crawl blog listing via ?page=N and extract /blog/<slug> links.
    Works for Higgsfield + HeyGen.
    """
    base = root_from_url(blog_url)
    seen_urls: set[str] = set()
    posts: List[str] = []

    def page_url(page: int) -> str:
        if page == 1:
            return blog_url
        sep = "&" if "?" in blog_url else "?"
        return f"{blog_url}{sep}page={page}"

    for page in range(1, max_pages + 1):
        try:
            html = fetch_text(page_url(page), timeout_s=30, retries=3)
        except Exception:
            break
        # Extract escaped or normal hrefs
        rels = set(re.findall(r'href=\\\"(/blog/[a-zA-Z0-9-]+)', html))
        rels.update(re.findall(r'href=\"(/blog/[a-zA-Z0-9-]+)', html))
        if not rels:
            break
        new_count = 0
        for rel in rels:
            slug = rel.split("/blog/", 1)[-1].strip("/")
            # keep likely posts (requires dash to avoid /blog/Listicles)
            if "-" not in slug:
                continue
            abs_url = urljoin(base, rel)
            if abs_url in seen_urls:
                continue
            seen_urls.add(abs_url)
            posts.append(abs_url)
            new_count += 1
        if new_count == 0:
            # no new posts discovered on this page
            break
    return posts


def extract_title_and_published(html: str) -> Tuple[Optional[str], Optional[str]]:
    # OG title first
    m = re.search(r'<meta[^>]+property=\"og:title\"[^>]+content=\"([^\"]+)\"', html, flags=re.I)
    title = m.group(1).strip() if m else None
    if not title:
        m2 = re.search(r"<title>(.*?)</title>", html, flags=re.I | re.S)
        if m2:
            title = re.sub(r"\s+", " ", m2.group(1)).strip()

    published: Optional[str] = None
    # JSON-LD BlogPosting/Article
    for s in re.finditer(r'<script[^>]+type=\"application/ld\+json\"[^>]*>(.*?)</script>', html, flags=re.I | re.S):
        raw = s.group(1).strip()
        if len(raw) < 20:
            continue
        try:
            obj = json.loads(raw)
        except Exception:
            continue
        objs = obj if isinstance(obj, list) else [obj]
        for it in objs:
            if not isinstance(it, dict):
                continue
            t = str(it.get("@type") or "").lower()
            if t in {"blogposting", "article", "newsarticle"}:
                if it.get("headline") and not title:
                    title = str(it.get("headline")).strip()
                if it.get("datePublished"):
                    published = str(it.get("datePublished")).strip()
                    break
        if published:
            break

    # HeyGen sometimes embeds a "Published" label in HTML (fallback)
    if not published:
        mm = re.search(r"Published\\s*</span>\\s*<span[^>]*>\\s*([^<]{6,40})\\s*</span>", html, flags=re.I)
        if mm:
            published = mm.group(1).strip()

    return title, published


# -------------------------
# Theme + patterns
# -------------------------


THEMES: Dict[str, Dict[str, Any]] = {
    "ugc_ads": {
        "seed_hint": "ugc ads",
        "zh": "UGC Ads",
        "match_regex": [
            r"\bugc\b",
            r"\buser generated content\b",
            r"\bcreator ads?\b",
            r"\btestimonial ads?\b",
            r"\bspark ads?\b",
            r"\bwhitelisting\b",
            r"\busage rights?\b",
            r"\bpaid partnership\b",
        ],
    },
    "ai_influencer": {
        "seed_hint": "ai influencer",
        "zh": "AI Influencer",
        "match_regex": [
            r"\bai influencer(s)?\b",
            r"\bvirtual influencer(s)?\b",
            r"\bdigital influencer(s)?\b",
            r"\bvirtual model(s)?\b",
            r"\bai avatar(s)?\b",
            r"\bsynthetic influencer(s)?\b",
            r"\bspokesperson avatar\b",
        ],
    },
}


def detect_theme_key(seed: str) -> str:
    s = seed.lower()
    if "influencer" in s:
        return "ai_influencer"
    if "ugc" in s and ("ad" in s or "ads" in s):
        return "ugc_ads"
    return "ugc_ads"


def theme_match(theme_key: str, title: str, url: str) -> bool:
    text = f"{title} {url}".lower()
    for rx in THEMES[theme_key]["match_regex"]:
        if re.search(rx, text, flags=re.I):
            return True
    return False


@dataclass(frozen=True)
class Pattern:
    pattern_id: str
    name: str
    base_keywords: Tuple[str, ...]
    evidence_terms: Tuple[str, ...]
    product_primary: str
    product_secondary: str
    product_angle: str


def build_patterns(theme_key: str) -> List[Pattern]:
    year = "2026"
    if theme_key == "ugc_ads":
        return [
            Pattern("P1", "UGC ads definition", ("ugc ads", "what are ugc ads", "ugc ad meaning", "user generated content ads"), ("ugc", "user generated content", "creator ads"), "script_to_video", "video_studio", "Turn UGC ad briefs into scripts + storyboards with Alici AI."),
            Pattern("P2", "UGC ad scripts & templates", ("ugc ad script template", "ugc ad script generator", "ugc script template", "testimonial ad script template"), ("script", "template", "hooks"), "script_to_video", "video_prompt", "Generate hook/script variants and export testable cuts with Alici AI."),
            Pattern("P3", "UGC hooks & angles", ("ugc hooks", "ugc hook examples", "ugc ad hooks", "testimonial ad hooks"), ("hook", "hooks", "angles"), "video_prompt", "script_to_video", "Generate 30 hook variants and pick winners fast with Alici AI."),
            Pattern("P4", "Briefs, shot lists, storyboards", ("ugc ad brief template", "ugc shot list", "ugc storyboard template", "ugc deliverables checklist"), ("brief", "shot list", "storyboard"), "video_studio", "script_to_video", "Convert briefs into shot lists + edit plans with Alici AI."),
            Pattern("P5", "UGC ad examples & library", ("ugc ad examples", "best ugc ads", f"ugc ad examples {year}", "ugc ad ideas"), ("examples", "best ugc ads", "ideas"), "video_prompt", "video_studio", "Build a swipe file + prompt-to-variant system using Alici AI."),
            Pattern("P6", "TikTok Spark Ads & platform variants", ("spark ads ugc", "tiktok ugc ads", "ugc ads tiktok", "tiktok spark ads creator"), ("tiktok", "spark ads", "reels"), "video_studio", "script_to_video", "Create platform-native cuts from one script with Alici AI."),
            Pattern("P7", "Whitelisting, usage rights, licensing", ("ugc whitelisting", "ugc usage rights", "ugc licensing agreement", "ugc content licensing"), ("whitelisting", "usage rights", "licensing"), "video_studio", "script_to_video", "Ship usage-rights-ready deliverables checklists and variants with Alici AI."),
            Pattern("P8", "Pricing & packages for brands", ("ugc ad pricing", "ugc ad cost", "ugc creator rates for ads", "ugc ad packages"), ("pricing", "rates", "packages"), "script_to_video", "video_studio", "More variants per creator fee = better CAC; Alici AI as scale lever."),
            Pattern("P9", "Testing & metrics (creative iteration)", ("ugc creative testing framework", "ugc creative testing", "ugc ad metrics", "ugc ad iteration"), ("testing", "metrics", "iteration"), "video_studio", "video_prompt", "Generate structured A/B test plans and variant batches with Alici AI."),
            Pattern("P10", "Hiring / sourcing UGC creators", ("find ugc creators for ads", "hire ugc creators", "ugc creator marketplace for brands", "ugc creator outreach template"), ("hire", "marketplace", "outreach"), "script_to_video", "video_studio", "Standardize briefs + evaluation rubrics for faster creator sourcing with Alici AI."),
            Pattern("P11", "Compliance (FTC + platform disclosure)", ("ftc disclosure ugc ads", "paid partnership disclosure ugc", "tiktok branded content ugc disclosure", "instagram paid partnership ugc disclosure"), ("ftc", "disclosure", "policy"), "video_studio", "script_to_video", "Ship compliant UGC scripts with disclosure options using Alici AI."),
            Pattern("P12", "AI workflow for UGC ads", ("ai tools for ugc ads", "ai ugc ad script generator", "script to video ugc ad", "ai workflow for ugc ads"), ("workflow", "ai tools", "script to video"), "script_to_video", "video_prompt", "End-to-end workflow: brief → hooks → script → cuts with Alici AI."),
        ]
    return [
        Pattern("P1", "AI influencer definition", ("ai influencer", "what is an ai influencer", "ai influencer meaning", "virtual influencer"), ("ai influencer", "virtual influencer", "meaning"), "video_prompt", "video_studio", "Explain the AI influencer stack + Alici AI workflows."),
        Pattern("P2", "AI influencer examples & case studies", ("ai influencer examples", "virtual influencer examples", f"ai influencer examples {year}", "ai model influencer examples"), ("examples", "case study", "virtual influencer"), "video_prompt", "video_studio", "Build a swipe file + prompt library for consistent character content."),
        Pattern("P3", "How to create an AI influencer", ("how to create an ai influencer", "create a virtual influencer", "make an ai influencer", "build a virtual model"), ("how to", "create", "build"), "video_studio", "video_prompt", "Create repeatable character videos (scripts + scenes + captions) with Alici AI."),
        Pattern("P4", "AI influencer marketing strategy", ("ai influencer marketing", "virtual influencer marketing strategy", "ai influencer brand deals", "ai influencer campaign"), ("marketing", "campaign", "brand deals"), "script_to_video", "video_studio", "Turn campaign goals into content pillars + scripts with Alici AI."),
        Pattern("P5", "Pricing, rates, ROI", ("ai influencer rates", "virtual influencer cost", "ai influencer pricing", "virtual influencer pricing"), ("pricing", "rates", "roi"), "script_to_video", "video_studio", "Cost-down lever: more content output per campaign budget with Alici AI."),
        Pattern("P6", "Disclosure, legal, ethics", ("ai influencer disclosure", "virtual influencer disclosure", "is ai influencer legal", "ai influencer ethics"), ("disclosure", "legal", "ethics"), "video_studio", "script_to_video", "Safe-by-design disclosure templates + compliant scripts."),
        Pattern("P7", "Platforms: Instagram / TikTok", ("ai influencer on instagram", "virtual influencer instagram strategy", "ai influencer tiktok", "virtual influencer tiktok"), ("instagram", "tiktok", "reels"), "video_studio", "video_prompt", "Generate platform-native formats + cadences with Alici AI."),
        Pattern("P8", "AI avatar vs AI influencer", ("ai avatar spokesperson vs ai influencer", "ai avatar vs virtual influencer", "ai spokesperson avatar", "avatar influencer"), ("avatar", "spokesperson", "vs"), "video_studio", "script_to_video", "Clarify positioning via comparison templates + workflows."),
        Pattern("P9", "Prompts & content workflow", ("ai influencer prompts", "ai influencer content workflow", "ai influencer content calendar", "virtual influencer content ideas"), ("prompts", "workflow", "calendar"), "video_prompt", "video_studio", "Ship prompt packs + calendars for batch production."),
        Pattern("P10", "Monetization & brand deals", ("monetize ai influencer", "ai influencer brand deals", "virtual influencer sponsorships", "ai influencer affiliate"), ("monetize", "sponsorship", "affiliate"), "script_to_video", "video_studio", "Offer-driven scripts + pitch assets generated with Alici AI."),
        Pattern("P11", "Tool comparisons", ("best ai influencer tools", "virtual influencer tools", "ai influencer generator tools", "ai model generator tools"), ("best", "tools", "generator"), "video_studio", "video_prompt", "Tool-showdown content mapped to Alici AI features."),
        Pattern("P12", "AI influencer vs virtual influencer", ("ai influencer vs virtual influencer", "virtual influencer vs ai influencer", "synthetic influencer", "digital influencer ai"), ("vs", "terminology", "synthetic"), "video_prompt", "video_studio", "Own the definition space with an AEO-first explainer."),
    ]


def build_keyword_pool(theme_key: str) -> List[Dict[str, Any]]:
    patterns = build_patterns(theme_key)
    seen: set[str] = set()
    out: List[Dict[str, Any]] = []
    platform_mods = ["tiktok", "instagram reels", "youtube shorts"]

    for p in patterns:
        for kw in p.base_keywords:
            k = re.sub(r"\s+", " ", kw.strip())
            if not k or k.lower() in seen:
                continue
            seen.add(k.lower())
            out.append(
                {
                    "keyword": k,
                    "pattern_id": p.pattern_id,
                    "pattern_name": p.name,
                    "product_mapping": {"primary": p.product_primary, "secondary": p.product_secondary, "angle": p.product_angle},
                }
            )
        # platform variants for first 2 base keywords
        for plat in platform_mods:
            for kw in p.base_keywords[:2]:
                k = re.sub(r"\s+", " ", f"{kw} {plat}".strip())
                if k.lower() in seen:
                    continue
                seen.add(k.lower())
                out.append({"keyword": k, "pattern_id": p.pattern_id})

    return out


def infer_intent_from_serp_titles(titles: Sequence[str]) -> str:
    if not titles:
        return "how-to"
    t = " | ".join(titles).lower()
    if " vs " in t or "versus" in t:
        return "comparison"
    if any(w in t for w in ("best", "top", "examples", "ideas")):
        return "list"
    if any(w in t for w in ("template", "checklist", "framework", "script")):
        return "workflow"
    if "what is" in t or "meaning" in t:
        return "definition"
    if "how to" in t or "guide" in t:
        return "how-to"
    return "use-case"


def lock_title(theme_key: str, pattern_name: str, intent: str, year: str = "2026") -> Tuple[str, str]:
    p = pattern_name.lower()
    if intent == "comparison":
        if theme_key == "ai_influencer":
            return f"AI Influencer vs Virtual Influencer: What’s the Difference? ({year})", "comparison-1"
        return f"UGC Ads vs Influencer Ads: What Works Best in {year}?", "comparison-1"

    if theme_key == "ugc_ads":
        if "script" in p or "template" in p:
            return "UGC Ad Script Template (2026): 12 Proven Hooks + 3 Full Scripts", "ugc-script-1"
        if "hooks" in p:
            return "UGC Ad Hooks That Convert (2026): 50 Swipeable Examples + Rewrite Formula", "ugc-hooks-1"
        if "brief" in p or "shot" in p or "storyboard" in p:
            return "UGC Ad Brief Template (2026): Shot List, Storyboard, and Deliverables Checklist", "ugc-brief-1"
        if "whitelisting" in p or "usage" in p or "licens" in p:
            return f"UGC Ad Usage Rights in {year}: Whitelisting, Licensing, and Pricing (Beginner Guide)", "ugc-rights-1"
        if "pricing" in p or "packages" in p:
            return f"UGC Ad Pricing in {year}: Rates, Packages, and ROI Benchmarks for Brands", "ugc-pricing-1"
        if "testing" in p or "metrics" in p:
            return "UGC Creative Testing Framework (2026): What to Test, Metrics, and 7-Day Iteration Plan", "ugc-testing-1"
        if "compliance" in p or "ftc" in p or "disclosure" in p:
            return "FTC Disclosure for UGC Ads (2026): What to Say, Where to Put It, and Platform Rules", "ugc-ftc-1"
        if "examples" in p or "library" in p:
            return "Best UGC Ads (2026): 25 Examples + The Script Pattern Behind Each", "ugc-examples-1"
        return f"UGC Ads in {year}: The Complete Playbook for High-Performing Creator Ads", "ugc-playbook-1"

    # ai_influencer
    if "definition" in p:
        return "What Is an AI Influencer? (2026) Definition, Examples, and Use Cases", "ai-def-1"
    if "examples" in p or "case" in p:
        return "AI Influencer Examples (2026): 20 Virtual Creators Brands Actually Work With", "ai-examples-1"
    if "create" in p:
        return f"How to Create an AI Influencer in {year}: Step-by-Step Workflow (Tools + Templates)", "ai-create-1"
    if "marketing" in p or "strategy" in p:
        return "AI Influencer Marketing Strategy (2026): Campaign Playbook + Content Pillars", "ai-marketing-1"
    if "pricing" in p or "rates" in p or "roi" in p:
        return "How Much Does an AI Influencer Cost? 2026 Pricing, Rates, and ROI Model", "ai-pricing-1"
    if "disclosure" in p or "legal" in p or "ethic" in p:
        return "AI Influencer Disclosure (2026): Legal, Ethical, and Platform Rules (With Templates)", "ai-disclosure-1"
    if "platform" in p or "instagram" in p or "tiktok" in p:
        return "AI Influencer on Instagram/TikTok (2026): Formats, Cadence, and Growth Loops", "ai-platform-1"
    if "tool" in p or "best" in p:
        return "Best AI Influencer Tools (2026): Generators, Avatars, and Content Workflow", "ai-tools-1"
    if "prompt" in p or "workflow" in p:
        return "AI Influencer Prompts (2026): A 30-Day Content Calendar + Prompt Pack", "ai-prompts-1"
    if "monet" in p or "brand" in p:
        return "How AI Influencers Make Money (2026): Sponsorships, Affiliate, and Brand Deal Playbook", "ai-monet-1"
    return "AI Influencer Playbook (2026): Build, Grow, and Monetize a Virtual Creator", "ai-playbook-1"


# -------------------------
# DataForSEO
# -------------------------


class DataForSEOClient:
    def __init__(self, username: str, password: str):
        credentials = f"{username}:{password}"
        self.auth_header = b64encode(credentials.encode()).decode()
        self.base_url = "https://api.dataforseo.com/v3"

    def post(self, endpoint: str, payload: List[Dict[str, Any]]) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        data = json.dumps(payload, ensure_ascii=False)
        res = subprocess.run(
            [
                "curl",
                "-sS",
                "--max-time",
                "75",
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
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if res.returncode != 0:
            err = res.stderr.decode("utf-8", errors="replace").strip()
            raise RuntimeError(f"DataForSEO curl failed (exit {res.returncode}): {err[:300]}")
        try:
            return json.loads(res.stdout.decode("utf-8", errors="replace"))
        except json.JSONDecodeError:
            raw = res.stdout.decode("utf-8", errors="replace")
            raise RuntimeError(f"DataForSEO JSON parse failed (len={len(raw)}): {raw[:220]}")


def load_dataforseo_creds(repo_root: Path) -> Tuple[str, str]:
    mcp = read_json(repo_root / ".mcp.json")
    env = (mcp.get("mcpServers", {}) or {}).get("dataforseo", {}).get("env", {}) or {}
    u = str(env.get("DATAFORSEO_USERNAME") or env.get("DATAFORSEO_LOGIN") or "").strip()
    p = str(env.get("DATAFORSEO_PASSWORD") or "").strip()
    if not u or not p:
        raise RuntimeError("Missing DataForSEO creds in .mcp.json (DATAFORSEO_USERNAME/PASSWORD)")
    return u, p


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
                if not isinstance(rank, int) or rank < 1 or rank > top_n:
                    continue
                t = item.get("title")
                if t:
                    titles.append(str(t).strip())
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
    v = min(max(volume, 0), 100000)
    v_score = min(60, int((v / 8000) * 60))  # 8k -> 60
    c = min(max(float(cpc or 0), 0.0), 30.0)
    c_score = min(20, int((c / 6.0) * 20))  # $6 -> 20
    ci = competition_index if isinstance(competition_index, int) else 55
    comp_score = int(max(0, min(20, 20 - (ci / 5))))
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
    if seo >= 80:
        return "high_seo_first"
    if aeo >= 70:
        return "high_aeo_first"
    if seo >= 65 and aeo >= 55:
        return "good"
    return "low"


# -------------------------
# Competitor mining
# -------------------------


def is_blog_post_url(url: str) -> bool:
    path = urlparse(url).path.lower()
    return "/blog/" in path and not any(x in path for x in ("/tag/", "/category/", "/author/"))


def collect_competitor_posts(blog_url: str, cutoff: dt.date) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    base = root_from_url(blog_url)
    domain = urlparse(base).netloc

    # try sitemap first (works well for invideo; may be partial for others)
    sitemap_pairs = collect_sitemap_urls(base, max_sitemaps=80, max_urls=14000)
    candidates = []
    for loc, lastmod in sitemap_pairs:
        if not is_blog_post_url(loc):
            continue
        d = parse_any_date(lastmod)
        if d and d < cutoff:
            continue
        candidates.append({"url": loc, "lastmod": lastmod, "source": "sitemap"})

    # fallback listing crawl if sitemap is missing/too small
    if len(candidates) < 30 and "/blog" in urlparse(blog_url).path.lower():
        for u in list_posts_by_paging(blog_url, max_pages=60):
            candidates.append({"url": u, "source": "listing"})

    # dedup by url
    by_url: Dict[str, Dict[str, Any]] = {}
    for c in candidates:
        by_url.setdefault(c["url"], c)
    candidates = list(by_url.values())

    # fetch title+published for a capped set (the rest is likely older anyway)
    candidates = candidates[:600]
    fetched_at = utc_now_iso()

    def fetch_one(u: str) -> Tuple[str, Optional[str], Optional[str]]:
        html = fetch_text(u, timeout_s=30, retries=3)
        title, pub = extract_title_and_published(html)
        return u, title, pub

    with ThreadPoolExecutor(max_workers=10) as ex:
        futs = {ex.submit(fetch_one, c["url"]): c for c in candidates}
        for fut in as_completed(futs):
            c = futs[fut]
            try:
                u, title, pub = fut.result()
            except Exception:
                continue
            if title:
                c["title"] = title
            if pub:
                c["published_at"] = pub

    rows: List[Dict[str, Any]] = []
    for c in candidates:
        title = str(c.get("title") or "").strip()
        if len(title) < 6:
            continue
        d = parse_any_date(c.get("published_at")) or parse_any_date(c.get("lastmod"))
        if d and d < cutoff:
            continue
        rows.append(
            {
                "competitor_domain": domain,
                "blog_url": blog_url,
                "url": c["url"],
                "title": title,
                "lastmod": c.get("lastmod"),
                "published_at": c.get("published_at"),
                "fetched_at": fetched_at,
                "source": c.get("source"),
            }
        )

    meta = {"competitor": domain, "sitemap_urls": len(sitemap_pairs), "candidates": len(candidates), "kept": len(rows)}
    # sort by date desc
    rows.sort(key=lambda r: parse_any_date(r.get("published_at")) or parse_any_date(r.get("lastmod")) or dt.date(1970, 1, 1), reverse=True)
    return rows, meta


def pick_evidence_posts(theme_posts: Sequence[Dict[str, Any]], evidence_terms: Sequence[str], max_items: int = 3) -> List[Dict[str, Any]]:
    terms = [t.lower() for t in evidence_terms if t.strip()]
    scored: List[Tuple[int, Dict[str, Any]]] = []
    for p in theme_posts:
        text = f"{p.get('title','')} {p.get('url','')}".lower()
        score = sum(1 for t in terms if t in text)
        if score > 0:
            scored.append((score, p))
    scored.sort(key=lambda x: x[0], reverse=True)
    out = [p for _, p in scored[:max_items]]
    if out:
        return out
    # fallback: most recent
    recent = sorted(theme_posts, key=lambda r: parse_any_date(r.get("published_at")) or parse_any_date(r.get("lastmod")) or dt.date(1970, 1, 1), reverse=True)
    return recent[:max_items]


def md_escape(s: str) -> str:
    return str(s).replace("|", "\\|")


# -------------------------
# Main
# -------------------------


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    mission_path = out_dir / "00-mission-config.json"
    if not mission_path.exists():
        raise RuntimeError(f"Missing mission config: {mission_path}")
    mission = read_json(mission_path)

    seed = str(mission.get("seed") or "").strip() or "ugc ads"
    theme_key = detect_theme_key(seed)
    theme_name_zh = THEMES[theme_key]["zh"]

    competitors = list(((mission.get("anchors") or {}).get("competitors") or []))
    if not competitors:
        competitors = ["https://invideo.io/blog/", "https://higgsfield.ai/blog/", "https://heygen.com/blog"]

    today = dt.date.today()
    cutoff = today - dt.timedelta(days=365)

    # Phase 0: competitor posts
    all_posts: List[Dict[str, Any]] = []
    mining_meta: List[Dict[str, Any]] = []
    for blog_url in competitors:
        posts, meta = collect_competitor_posts(blog_url, cutoff=cutoff)
        all_posts.extend(posts)
        mining_meta.append(meta)

    write_jsonl(out_dir / "01-competitor-posts-all.jsonl", all_posts)
    theme_posts = [p for p in all_posts if theme_match(theme_key, str(p.get("title") or ""), str(p.get("url") or ""))]
    write_jsonl(out_dir / "01-competitor-posts-theme.jsonl", theme_posts)

    # Phase 1: keyword pool
    scope = mission.get("scope") or {}
    language_code = str(scope.get("language") or "en")
    geo = str(scope.get("geo") or "US")
    location_code = US_LOCATION_CODE if geo.upper() == "US" else US_LOCATION_CODE

    keywords = build_keyword_pool(theme_key)
    write_json(
        out_dir / "01-keywords-to-validate.json",
        {
            "seed": seed,
            "theme_key": theme_key,
            "language_code": language_code,
            "location_code": location_code,
            "generated_at": utc_now_iso(),
            "total_keywords": len(keywords),
            "keywords_to_validate": keywords,
        },
    )

    # Phase 2: DataForSEO validate
    repo_root = Path(__file__).resolve().parents[1]
    user, pw = load_dataforseo_creds(repo_root)
    client = DataForSEOClient(user, pw)

    kw_list = [k["keyword"] for k in keywords if isinstance(k.get("keyword"), str)]
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
    metrics_by_kw = {str(m.get("keyword") or "").lower(): m for m in kw_metrics}

    validated: List[Dict[str, Any]] = []
    for k in keywords:
        key = str(k.get("keyword") or "").lower()
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
            "theme_key": theme_key,
            "language_code": language_code,
            "location_code": location_code,
            "validated_at": utc_now_iso(),
            "keywords": validated,
            "api_usage": {"dataforseo_keyword_calls": 1, "dataforseo_serp_calls": 0},
        },
    )

    patterns = {p.pattern_id: p for p in build_patterns(theme_key)}
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for row in validated:
        grouped.setdefault(str(row.get("pattern_id") or "unknown"), []).append(row)

    directions: List[Dict[str, Any]] = []
    for pid, rows in grouped.items():
        vols = [int(r.get("metrics", {}).get("search_volume") or 0) for r in rows]
        total_volume = int(sum(vols))
        cpcs = [float(r.get("metrics", {}).get("cpc") or 0) for r in rows if float(r.get("metrics", {}).get("cpc") or 0) > 0]
        avg_cpc = (sum(cpcs) / len(cpcs)) if cpcs else 0.0
        comp_indexes = [r.get("metrics", {}).get("competition_index") for r in rows if isinstance(r.get("metrics", {}).get("competition_index"), int)]
        avg_comp = int(sum(comp_indexes) / len(comp_indexes)) if comp_indexes else 55
        rep = sorted(rows, key=lambda r: int(r.get("metrics", {}).get("search_volume") or 0), reverse=True)[0]
        primary_kw = str(rep.get("keyword") or "").strip()
        seo = compute_seo_score(total_volume, avg_cpc, avg_comp)
        directions.append(
            {
                "pattern_id": pid,
                "theme": patterns.get(pid).name if pid in patterns else pid,
                "primary_keyword": primary_kw,
                "total_volume": total_volume,
                "avg_cpc": round(avg_cpc, 2),
                "avg_competition_index": avg_comp,
                "seo_score": seo,
                "aeo_score": 55,
                "combined_priority": combined_priority(seo, 55),
                "serp_features": {"people_also_ask": False, "ai_overview": False},
                "serp_titles_top3": [],
            }
        )

    # SERP only for top 12 by SEO/volume
    directions.sort(key=lambda d: (int(d.get("seo_score") or 0), int(d.get("total_volume") or 0)), reverse=True)
    serp_calls = 0
    for d in directions[:12]:
        kw = str(d.get("primary_keyword") or "").strip()
        if not kw:
            continue
        has_paa = False
        has_aio = False
        titles: List[str] = []
        try:
            serp_resp = client.post(
                "serp/google/organic/live/advanced",
                [
                    {
                        "keyword": kw,
                        "location_code": location_code,
                        "language_code": language_code,
                        "device": "desktop",
                        "os": "windows",
                        "depth": 20,
                    }
                ],
            )
            serp_calls += 1
            if serp_resp.get("status_code") == 20000:
                for task in serp_resp.get("tasks", []) or []:
                    for result in task.get("result", []) or []:
                        for item in result.get("items", []) or []:
                            t = item.get("type")
                            if t == "people_also_ask":
                                has_paa = True
                            if t == "ai_overview":
                                has_aio = True
            titles = extract_serp_top_titles(serp_resp, top_n=3)
        except Exception:
            titles = []

        aeo = compute_aeo_score(has_paa=has_paa, has_ai_overview=has_aio)
        d["aeo_score"] = aeo
        d["combined_priority"] = combined_priority(int(d["seo_score"]), aeo)
        d["serp_features"] = {"people_also_ask": has_paa, "ai_overview": has_aio}
        d["serp_titles_top3"] = titles

    # rank final directions with true traffic gate
    def direction_score(d: Dict[str, Any]) -> float:
        seo = float(d.get("seo_score") or 0)
        aeo = float(d.get("aeo_score") or 0)
        vol = float(d.get("total_volume") or 0)
        return 0.55 * seo + 0.35 * aeo + 0.10 * min(100.0, vol / TRUE_TRAFFIC_THRESHOLD * 100.0)

    directions.sort(key=lambda d: (direction_score(d), int(d.get("total_volume") or 0)), reverse=True)
    above = [d for d in directions if int(d.get("total_volume") or 0) >= TRUE_TRAFFIC_THRESHOLD]
    below = [d for d in directions if int(d.get("total_volume") or 0) < TRUE_TRAFFIC_THRESHOLD]
    top10 = (above + below)[:10]

    out_dirs: List[Dict[str, Any]] = []
    for idx, d in enumerate(top10, start=1):
        pid = str(d.get("pattern_id") or "unknown")
        pat = patterns.get(pid)
        intent = infer_intent_from_serp_titles(d.get("serp_titles_top3") or [])
        locked_title, formula_id = lock_title(theme_key, d.get("theme") or "", intent=intent)
        evidence_posts = pick_evidence_posts(theme_posts, pat.evidence_terms if pat else (), max_items=3)
        out_dirs.append(
            {
                "rank": idx,
                "direction_id": f"D{idx:02d}",
                "pattern_id": pid,
                "theme": d.get("theme"),
                "intent_type": intent,
                "locked_title": {
                    "title": locked_title,
                    "primary_keyword": d.get("primary_keyword"),
                    "intent_matched": True,
                    "serp_aligned": True if d.get("serp_titles_top3") else False,
                    "year_validated": True,
                    "formula_id": formula_id,
                    "evidence": {"serp_titles": d.get("serp_titles_top3") or [], "search_volume": int(d.get("total_volume") or 0), "trend": "stable"},
                },
                "seo_score": int(d.get("seo_score") or 0),
                "aeo_score": int(d.get("aeo_score") or 0),
                "combined_priority": d.get("combined_priority"),
                "evidence_chain": {
                    "volume": int(d.get("total_volume") or 0),
                    "trend": "stable",
                    "cpc_avg": float(d.get("avg_cpc") or 0),
                    "competition_avg": round((int(d.get("avg_competition_index") or 55)) / 100.0, 2),
                    "serp_features": d.get("serp_features") or {},
                    "serp_titles_top3": d.get("serp_titles_top3") or [],
                    "below_threshold": int(d.get("total_volume") or 0) < TRUE_TRAFFIC_THRESHOLD,
                    "competitor_evidence": [
                        {"competitor": p.get("competitor_domain"), "title": p.get("title"), "url": p.get("url"), "published_at": p.get("published_at"), "lastmod": p.get("lastmod")}
                        for p in evidence_posts
                    ],
                },
                "product_mapping": {
                    "primary": pat.product_primary if pat else "video_studio",
                    "secondary": pat.product_secondary if pat else "script_to_video",
                    "product_angle": pat.product_angle if pat else "Map this topic to Alici AI workflows.",
                },
            }
        )

    write_json(out_dir / "03-top-directions.json", {"seed": seed, "theme_key": theme_key, "top_directions": out_dirs})

    # topic brief (v2.3)
    brief = {
        "mode": "seed_funnel",
        "schema_version": "2.3",
        "analysis_date": today.isoformat(),
        "seed": seed,
        "engine": "d1",
        "data_source": "competitor+dataforseo",
        "mission_config": mission,
        "funnel_stats": {
            "competitor_posts_total": len(all_posts),
            "competitor_posts_theme": len(theme_posts),
            "total_keywords": len(keywords),
            "validated_keywords": len(validated),
            "final_directions": len(out_dirs),
        },
        "final_directions": out_dirs,
        "diversity_report": None,
        "api_usage": {"dataforseo_keyword_calls": 1, "dataforseo_serp_calls": serp_calls},
        "competitor_mining": {"cutoff_date": cutoff.isoformat(), "meta": mining_meta},
    }
    write_json(out_dir / "00-topic-brief.json", brief)

    # Update validated keywords api_usage with serp calls
    vk = read_json(out_dir / "02-validated-keywords.json")
    vk.setdefault("api_usage", {})["dataforseo_serp_calls"] = serp_calls
    write_json(out_dir / "02-validated-keywords.json", vk)

    # human report
    counts: Dict[str, int] = {}
    for p in theme_posts:
        dom = str(p.get("competitor_domain") or "unknown")
        counts[dom] = counts.get(dom, 0) + 1
    below_cnt = sum(1 for d in out_dirs if d.get("evidence_chain", {}).get("below_threshold"))

    lines: List[str] = []
    lines.append(f"# Seed Mode Top10 — {theme_name_zh}\n\n")
    lines.append(f"- **Seed**: `{seed}`\n")
    lines.append(f"- **时间窗口**: 最近 12 个月（cutoff: `{cutoff.isoformat()}`）\n")
    lines.append(f"- **真流量阈值**: Direction `total_volume >= {TRUE_TRAFFIC_THRESHOLD}/月`\n")
    lines.append(f"- **数据源**: 竞品博客(sitemap/分页) + DataForSEO Keywords Data + SERP\n\n")
    lines.append("---\n\n")
    lines.append("## 1) 竞品博客覆盖与主题命中\n\n")
    lines.append(f"- 抓取到的竞品博文（近12个月）总数: **{len(all_posts)}**\n")
    lines.append(f"- 主题命中博文总数: **{len(theme_posts)}**\n")
    lines.append("- 分布（domain → count）:\n")
    for dom in sorted(counts.keys()):
        lines.append(f"  - `{dom}` → **{counts[dom]}**\n")
    lines.append("\n---\n\n")
    lines.append("## 2) Top10（英文标题 + 数据）\n\n")
    lines.append(f"> 注：Top10 中 **{below_cnt}** 个方向未达 {TRUE_TRAFFIC_THRESHOLD}/月阈值（保留用于主题覆盖/集群建设）。\n\n")
    lines.append("| # | Locked Title (EN) | Primary Keyword | Total Vol/mo | CPC | Comp | SERP (PAA/AIO) |\n")
    lines.append("|---:|---|---|---:|---:|---:|---|\n")
    for d in out_dirs:
        ef = d.get("evidence_chain", {}) or {}
        sf = ef.get("serp_features", {}) or {}
        paa = "Y" if sf.get("people_also_ask") else "N"
        aio = "Y" if sf.get("ai_overview") else "N"
        lines.append(
            f"| {d.get('rank')} | {md_escape(d.get('locked_title', {}).get('title'))} | "
            f"{md_escape(d.get('locked_title', {}).get('primary_keyword'))} | {int(ef.get('volume') or 0):,} | "
            f"${float(ef.get('cpc_avg') or 0):.2f} | {float(ef.get('competition_avg') or 0):.2f} | {paa}/{aio} |\n"
        )
    lines.append("\n---\n\n")
    lines.append("## 3) Top10 逐条拆解（中文）\n\n")
    for d in out_dirs:
        ef = d.get("evidence_chain", {}) or {}
        sf = ef.get("serp_features", {}) or {}
        lines.append(f"### {d.get('rank')}. {d.get('locked_title', {}).get('title')}\n\n")
        lines.append(f"- **Primary keyword**: `{d.get('locked_title', {}).get('primary_keyword')}`\n")
        lines.append(
            f"- **Traffic**: {int(ef.get('volume') or 0):,}/mo | CPC ${float(ef.get('cpc_avg') or 0):.2f} | Comp {float(ef.get('competition_avg') or 0):.2f}\n"
        )
        lines.append(f"- **SERP**: PAA={bool(sf.get('people_also_ask'))} | AI Overview={bool(sf.get('ai_overview'))}\n")
        if ef.get("below_threshold"):
            lines.append(f"- **⚠️ 未达真流量阈值**：仍保留用于主题覆盖。\n")
        ce = ef.get("competitor_evidence") or []
        if ce:
            lines.append("- **竞品证据（近12个月命中）**:\n")
            for p in ce[:3]:
                lines.append(f"  - {p.get('title')} ({p.get('competitor')})\n")
        pm = d.get("product_mapping") or {}
        lines.append(f"- **Alici angle**: {pm.get('product_angle')}\n\n")

    (out_dir / "00-directions-report.md").write_text("".join(lines), encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

