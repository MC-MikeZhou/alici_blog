#!/usr/bin/env python3
"""
UGC AI Tools SERP Harvest (DataForSEO) + Evidence Pack Generator.

Goal:
- Find off-site competitor blog URLs for queries like "AI UGC tools" / "UGC AI video generator"
- Validate demand using DataForSEO keyword metrics + SERP features
- Output an evidence pack + an update strategy document for iterative refreshes

Constraints:
- Public web only (DataForSEO SERP data)
- Prefer SaaS official blogs; de-prioritize affiliate/directories
"""

from __future__ import annotations

import base64
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


DATAFORSEO_BASE = "https://api.dataforseo.com/v3"
DEFAULT_LOCATION_CODE_US = 2840
DEFAULT_LANGUAGE_CODE_EN = "en"


@dataclass(frozen=True)
class DataForSEOCreds:
    login: str
    password: str

    def auth_header_value(self) -> str:
        token = f"{self.login}:{self.password}".encode("utf-8")
        return "Basic " + base64.b64encode(token).decode("utf-8")


def _utc_now_iso() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: Sequence[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(r, ensure_ascii=False) for r in rows]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _domain(url: str) -> str:
    try:
        return (urlparse(url).netloc or "").lower()
    except Exception:
        return ""


def _canonicalize_url(url: str) -> str:
    """
    Canonicalize for dedup:
    - strip fragments
    - remove tracking query params like utm_*, gclid, fbclid
    - normalize scheme/host case
    """
    try:
        u = urlparse(url.strip())
    except Exception:
        return url.strip()
    q = []
    for k, v in parse_qsl(u.query, keep_blank_values=True):
        kl = k.lower()
        if kl.startswith("utm_") or kl in {"gclid", "fbclid", "mc_cid", "mc_eid", "ref"}:
            continue
        q.append((k, v))
    new_query = urlencode(q, doseq=True)
    cleaned = u._replace(query=new_query, fragment="")
    # Lowercase scheme/host only
    netloc = cleaned.netloc.lower()
    scheme = cleaned.scheme.lower()
    cleaned = cleaned._replace(netloc=netloc, scheme=scheme)
    return urlunparse(cleaned)


def _safe_slug(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:80] or "query"


def _curl_post_json(
    *,
    url: str,
    payload: List[Dict[str, Any]],
    creds: DataForSEOCreds,
    timeout_s: int = 90,
    retry: int = 3,
    sleep_s: float = 0.6,
) -> Dict[str, Any]:
    """
    Use curl to POST JSON and return parsed JSON dict.
    We use curl (not requests/urllib) because Python DNS resolution is unreliable in this environment.
    """
    data = json.dumps(payload, ensure_ascii=False)
    headers = [
        "-H",
        f"Authorization: {creds.auth_header_value()}",
        "-H",
        "Content-Type: application/json",
        "-H",
        "Accept: application/json",
    ]
    last_err: Optional[str] = None
    for attempt in range(1, max(1, retry) + 1):
        cmd = [
            "curl",
            "-sS",
            "--fail-with-body",
            "--max-time",
            str(timeout_s),
            *headers,
            url,
            "-d",
            data,
        ]
        p = subprocess.run(cmd, capture_output=True, text=True)
        if p.returncode == 0:
            try:
                obj = json.loads(p.stdout)
            except Exception:
                last_err = f"Invalid JSON response (attempt {attempt}): {p.stdout[:500]}"
            else:
                if isinstance(obj, dict):
                    if sleep_s:
                        time.sleep(sleep_s)
                    return obj
                last_err = f"Unexpected response type (attempt {attempt}): {type(obj)}"
        else:
            last_err = (p.stderr or p.stdout or "").strip()[:1200]
        time.sleep(min(2.0, 0.6 * attempt))
    raise SystemExit(f"DataForSEO request failed after {retry} attempts: {last_err}")


def _extract_tasks_ok(obj: Dict[str, Any]) -> List[Dict[str, Any]]:
    tasks = obj.get("tasks")
    if not isinstance(tasks, list):
        return []
    out: List[Dict[str, Any]] = []
    for t in tasks:
        if not isinstance(t, dict):
            continue
        if int(t.get("status_code") or 0) == 20000:
            out.append(t)
    return out


def _extract_serp_items(obj: Dict[str, Any]) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for t in _extract_tasks_ok(obj):
        res = t.get("result")
        if not isinstance(res, list) or not res:
            continue
        for r in res:
            if not isinstance(r, dict):
                continue
            its = r.get("items")
            if isinstance(its, list):
                for it in its:
                    if isinstance(it, dict):
                        items.append(it)
    return items


def _extract_keyword_items(obj: Dict[str, Any]) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for t in _extract_tasks_ok(obj):
        res = t.get("result")
        if not isinstance(res, list):
            continue
        for it in res:
            if isinstance(it, dict):
                items.append(it)
    return items


def _summarize_serp_features(items: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    features = {
        "ai_overview": False,
        "featured_snippet": False,
        "people_also_ask": False,
        "video": False,
        "forums": False,
    }
    for it in items:
        t = str(it.get("type") or "")
        if t == "ai_overview":
            features["ai_overview"] = True
        elif t == "featured_snippet":
            features["featured_snippet"] = True
        elif t == "people_also_ask":
            features["people_also_ask"] = True
        elif t == "video":
            features["video"] = True
        elif t in {"discussions_and_forums", "forum"}:
            features["forums"] = True
    return features


def _extract_organic(items: Sequence[Dict[str, Any]], keep_rank_max: int, keep_rank_soft_max: int) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for it in items:
        if str(it.get("type") or "") != "organic":
            continue
        rank = it.get("rank_group") or it.get("rank_absolute")
        if not isinstance(rank, int):
            continue
        if rank > keep_rank_soft_max:
            continue
        url = str(it.get("url") or "").strip()
        if not url:
            continue
        title = str(it.get("title") or "").strip()
        desc = str(it.get("description") or "").strip()
        out.append(
            {
                "rank": rank,
                "url": url,
                "title": title,
                "description": desc,
                "domain": _domain(url),
                "strong_rank": rank <= keep_rank_max,
            }
        )
    out.sort(key=lambda r: int(r.get("rank") or 10**9))
    return out


def _load_dataforseo_creds_from_mcp(repo_root: Path) -> DataForSEOCreds:
    """
    Preferred: read from /Users/H/Documents/AliciBlog/.mcp.json
    Fallback: env vars DATAFORSEO_LOGIN/DATAFORSEO_PASSWORD or DATAFORSEO_USERNAME/DATAFORSEO_PASSWORD.
    """
    mcp_path = repo_root / ".mcp.json"
    if mcp_path.exists():
        mcp = _read_json(mcp_path)
        env = ((mcp.get("mcpServers") or {}).get("dataforseo") or {}).get("env") or {}
        login = (env.get("DATAFORSEO_USERNAME") or env.get("DATAFORSEO_LOGIN") or "").strip()
        password = (env.get("DATAFORSEO_PASSWORD") or "").strip()
        if login and password:
            return DataForSEOCreds(login=login, password=password)

    login = (os.environ.get("DATAFORSEO_LOGIN") or os.environ.get("DATAFORSEO_USERNAME") or "").strip()
    password = (os.environ.get("DATAFORSEO_PASSWORD") or "").strip()
    if not login or not password:
        raise SystemExit("Missing DataForSEO creds. Set env vars or configure .mcp.json.")
    return DataForSEOCreds(login=login, password=password)


def _gen_queries_tools_listicle() -> List[str]:
    return [
        "best ai ugc tools",
        "best ai ugc tools 2026",
        "best ugc ai video generators",
        "best ugc ai video generators 2026",
        "best ugc ai video generator",
        "best ugc ai video generator 2026",
        "best ugc video generator",
        "best ugc video generator 2026",
        "ai ugc tools",
        "ai ugc tools 2026",
        "ai ugc video generator",
        "ugc ai video generators",
    ]


def _gen_queries_generator_intent() -> List[str]:
    return [
        "ugc ai video generator",
        "ugc ai video generators",
        "ai ugc video generator",
        "ai ugc video generators",
        "ai ugc ad generator",
        "ugc video ads ai",
        "ai ugc video ads",
        "ai video ad generator ugc",
    ]


def _gen_queries_comparison_intent() -> List[str]:
    return [
        "invideo ai ugc tools",
        "invideo ai ugc tools alternatives",
        "zeely ugc ai video generators",
        "opusclip ugc ai video generator",
        "higgsfield ugc ads ai",
        "heygen ugc video ads ai",
        "best ai video ad generator",
        "ai video ad generator tools",
    ]


def _gen_queries_site_inventory(domains: Sequence[str]) -> List[str]:
    # Use google-like site queries to enumerate relevant blog URLs safely without crawling.
    seeds = [
        "ugc",
        "\"ugc\" \"ai\"",
        "\"ugc\" \"video\"",
        "\"ai\" \"ugc\" \"tools\"",
        "\"ugc\" \"ai\" \"video generator\"",
        "\"best\" \"ugc\" \"ai\"",
    ]
    out: List[str] = []
    for d in domains:
        for s in seeds:
            out.append(f"site:{d} {s}")
            if "/blog" not in d:
                out.append(f"site:{d}/blog {s}")
    # dedup in order
    seen = set()
    dedup: List[str] = []
    for q in out:
        if q in seen:
            continue
        seen.add(q)
        dedup.append(q)
    return dedup


def _dedup_keep_order(xs: Iterable[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for x in xs:
        s = re.sub(r"\s+", " ", str(x).strip())
        if not s:
            continue
        key = s.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(s)
    return out


def _looks_like_content_url(url: str) -> bool:
    try:
        p = urlparse(url)
        path = p.path.lower()
        return any(seg in path for seg in ("/blog/", "/guides/", "/resources/", "/learn/"))
    except Exception:
        return False


def _domain_quality(domain: str, preferred_domains: Sequence[str]) -> str:
    d = (domain or "").lower().strip()
    if not d:
        return "unknown"
    if d in {pd.lower() for pd in preferred_domains}:
        return "preferred_saas"
    # common affiliate/directory patterns; not perfect, but helps de-prioritize.
    if any(x in d for x in ("top10", "best", "reviews", "alternatives", "tool", "tools")) and d.endswith((".xyz", ".site")):
        return "likely_affiliate"
    if any(x in d for x in ("medium.com", "reddit.com", "quora.com", "pinterest.com")):
        return "community_or_media"
    return "other"


def run(out_dir: Path) -> None:
    mission_path = out_dir / "00-mission-config.json"
    if not mission_path.exists():
        raise SystemExit(f"Missing mission config: {mission_path}")
    mission = _read_json(mission_path)

    scope = mission.get("scope") or {}
    location_code = int(scope.get("location_code") or DEFAULT_LOCATION_CODE_US)
    language_code = str(scope.get("language_code") or DEFAULT_LANGUAGE_CODE_EN)

    competitor_domains: List[str] = list(mission.get("competitor_domains") or [])
    competitor_domains = [d.strip().lower() for d in competitor_domains if str(d).strip()]

    preferred_domains = list(mission.get("preferred_domains") or competitor_domains)
    preferred_domains = [d.strip().lower() for d in preferred_domains if str(d).strip()]

    seed_required_urls: List[str] = list(mission.get("seed_required_urls") or [])
    seed_required_urls = [u.strip() for u in seed_required_urls if str(u).strip()]

    limits = mission.get("limits") or {}
    serp_depth = int(limits.get("serp_depth") or 100)
    keep_rank_max = int(limits.get("keep_rank_max") or 20)
    keep_rank_soft_max = int(limits.get("keep_rank_soft_max") or 50)
    max_queries = int(limits.get("max_queries") or 40)

    query_modules = set([str(x) for x in (mission.get("query_modules") or [])])
    if not query_modules:
        query_modules = {"tools_listicle", "generator_intent", "comparison_intent", "site_inventory"}

    queries: List[str] = []
    modules_map: Dict[str, List[str]] = {}

    def add_module(name: str, qs: List[str]) -> None:
        nonlocal queries, modules_map
        qs = _dedup_keep_order(qs)
        modules_map[name] = qs
        queries.extend(qs)

    if "tools_listicle" in query_modules:
        add_module("tools_listicle", _gen_queries_tools_listicle())
    if "generator_intent" in query_modules:
        add_module("generator_intent", _gen_queries_generator_intent())
    if "comparison_intent" in query_modules:
        add_module("comparison_intent", _gen_queries_comparison_intent())
    if "site_inventory" in query_modules:
        add_module("site_inventory", _gen_queries_site_inventory(competitor_domains))

    queries = _dedup_keep_order(queries)[:max_queries]

    repo_root = Path(__file__).resolve().parents[1]
    creds = _load_dataforseo_creds_from_mcp(repo_root)

    raw_dir = out_dir / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    # Phase 1: keyword metrics (volume gate)
    kw_payload = [
        {
            "keywords": queries,
            "location_code": location_code,
            "language_code": language_code,
            "search_partners": False,
        }
    ]
    kw_resp = _curl_post_json(url=f"{DATAFORSEO_BASE}/keywords_data/google_ads/search_volume/live", payload=kw_payload, creds=creds)
    _write_json(raw_dir / "keywords_search_volume_live.json", kw_resp)

    kw_items = _extract_keyword_items(kw_resp)
    metrics_by_kw: Dict[str, Dict[str, Any]] = {}
    for it in kw_items:
        kw = str(it.get("keyword") or "").strip()
        if not kw:
            continue
        metrics_by_kw[kw.lower()] = it

    query_universe: List[Dict[str, Any]] = []
    gated_queries: List[str] = []
    for q in queries:
        it = metrics_by_kw.get(q.lower(), {})
        vol = int(it.get("search_volume") or 0)
        cpc = float(it.get("cpc") or 0)
        comp_level = str(it.get("competition_level") or it.get("competition") or "").strip() or "N/A"
        query_universe.append(
            {
                "query": q,
                "module": next((m for m, qs in modules_map.items() if q in qs), "mixed"),
                "metrics": {"search_volume": vol, "cpc": cpc, "competition": comp_level},
                "passes_volume_gate": vol > 0,
            }
        )
        if vol > 0:
            gated_queries.append(q)

    _write_json(
        out_dir / "01-query-universe.json",
        {
            "generated_at": _utc_now_iso(),
            "scope": {"location_code": location_code, "language_code": language_code},
            "limits": {"max_queries": max_queries, "serp_depth": serp_depth, "keep_rank_max": keep_rank_max, "keep_rank_soft_max": keep_rank_soft_max},
            "modules": modules_map,
            "queries": query_universe,
            "api_usage": {"keywords_data_calls": 1, "serp_calls": 0},
        },
    )

    # Phase 2: SERP fetch for volume-gated queries (in order of volume desc)
    gated_sorted = sorted(
        gated_queries,
        key=lambda q: int(metrics_by_kw.get(q.lower(), {}).get("search_volume") or 0),
        reverse=True,
    )

    serp_rows: List[Dict[str, Any]] = []
    candidate_rows: List[Dict[str, Any]] = []
    seen_urls: set[str] = set()

    serp_calls = 0
    for q in gated_sorted:
        serp_payload = [
            {
                "keyword": q,
                "location_code": location_code,
                "language_code": language_code,
                "device": "desktop",
                "os": "windows",
                "depth": serp_depth,
            }
        ]
        serp_resp = _curl_post_json(url=f"{DATAFORSEO_BASE}/serp/google/organic/live/advanced", payload=serp_payload, creds=creds, timeout_s=120)
        serp_calls += 1
        _write_json(raw_dir / f"serp__{_safe_slug(q)}.json", serp_resp)

        items = _extract_serp_items(serp_resp)
        feats = _summarize_serp_features(items)
        organic = _extract_organic(items, keep_rank_max=keep_rank_max, keep_rank_soft_max=keep_rank_soft_max)

        serp_rows.append(
            {
                "query": q,
                "query_metrics": {
                    "search_volume": int(metrics_by_kw.get(q.lower(), {}).get("search_volume") or 0),
                    "cpc": float(metrics_by_kw.get(q.lower(), {}).get("cpc") or 0),
                    "competition": str(metrics_by_kw.get(q.lower(), {}).get("competition_level") or metrics_by_kw.get(q.lower(), {}).get("competition") or "N/A"),
                },
                "serp_features": feats,
                "top_organic": organic[:20],
                "fetched_at": _utc_now_iso(),
            }
        )

        for r in organic:
            url = str(r.get("url") or "")
            canon = _canonicalize_url(url)
            if canon in seen_urls:
                continue
            seen_urls.add(canon)

            dom = str(r.get("domain") or "")
            dq = _domain_quality(dom, preferred_domains)
            keep = True
            keep_reason: List[str] = []

            if not _looks_like_content_url(url):
                keep = False
                keep_reason.append("path_not_content_like")
            else:
                keep_reason.append("content_path_ok")

            if dq == "likely_affiliate":
                keep = False
                keep_reason.append("domain_likely_affiliate")
            elif dq == "preferred_saas":
                keep_reason.append("preferred_domain")

            candidate_rows.append(
                {
                    "url": url,
                    "canonical_url": canon,
                    "title": str(r.get("title") or ""),
                    "domain": dom,
                    "rank": int(r.get("rank") or 0),
                    "strong_rank": bool(r.get("strong_rank")),
                    "source_query": q,
                    "query_metrics": serp_rows[-1]["query_metrics"],
                    "serp_features": feats,
                    "domain_quality": dq,
                    "keep": keep,
                    "keep_reason": keep_reason,
                }
            )

    # Ensure required seed URLs are included even if not discovered (no rank; still traceable).
    for u in seed_required_urls:
        canon = _canonicalize_url(u)
        if canon in seen_urls:
            continue
        seen_urls.add(canon)
        dom = _domain(u)
        candidate_rows.append(
            {
                "url": u,
                "canonical_url": canon,
                "title": "",
                "domain": dom,
                "rank": None,
                "strong_rank": False,
                "source_query": "seed_required",
                "query_metrics": None,
                "serp_features": None,
                "domain_quality": _domain_quality(dom, preferred_domains),
                "keep": True,
                "keep_reason": ["seed_required_url"],
            }
        )

    _write_jsonl(out_dir / "02-serp-snapshots.jsonl", serp_rows)

    kept_candidates = [c for c in candidate_rows if c.get("keep")]
    _write_jsonl(out_dir / "03-candidate-urls.jsonl", kept_candidates)

    # Backfill api_usage in query universe file
    qj = _read_json(out_dir / "01-query-universe.json")
    if isinstance(qj, dict):
        qj.setdefault("api_usage", {})["serp_calls"] = serp_calls
        _write_json(out_dir / "01-query-universe.json", qj)

    # Phase 3: Generate human-readable URL pack
    by_query: Dict[str, List[Dict[str, Any]]] = {}
    by_domain: Dict[str, List[Dict[str, Any]]] = {}
    for c in kept_candidates:
        by_query.setdefault(str(c.get("source_query") or "unknown"), []).append(c)
        by_domain.setdefault(str(c.get("domain") or "unknown"), []).append(c)

    for q in by_query:
        by_query[q].sort(key=lambda r: (0 if r.get("rank") is None else int(r.get("rank")), r.get("domain_quality") != "preferred_saas"))
    for d in by_domain:
        by_domain[d].sort(key=lambda r: (0 if r.get("rank") is None else int(r.get("rank"))))

    # "Most isomorphic" to our target: title contains these phrases (best-effort).
    iso_hits: List[Dict[str, Any]] = []
    iso_rx = re.compile(r"(ai\\s+ugc\\s+tools|ugc\\s+ai\\s+video\\s+generator|best\\s+ai\\s+ugc)", re.I)
    for c in kept_candidates:
        if iso_rx.search(str(c.get("title") or "")) or iso_rx.search(str(c.get("url") or "")):
            iso_hits.append(c)
    iso_hits.sort(key=lambda r: (0 if r.get("rank") is None else int(r.get("rank"))))

    lines: List[str] = []
    lines.append("# Off-site Competitor URL Pack (UGC AI Tools)\n\n")
    lines.append(f"- Generated at: `{_utc_now_iso()}`\n")
    lines.append(f"- Scope: location_code `{location_code}` | language_code `{language_code}`\n")
    lines.append(f"- Volume gate: `search_volume > 0` | Strong rank: `<= {keep_rank_max}`\n")
    lines.append(f"- Preferred competitor domains: {', '.join(preferred_domains)}\n\n")
    lines.append("## Required Seed URLs (Always Included)\n\n")
    for u in seed_required_urls:
        lines.append(f"- {u}\n")
    lines.append("\n")

    lines.append("## Most Isomorphic Targets (Title/URL matches: AI UGC Tools / UGC AI Video Generator)\n\n")
    if not iso_hits:
        lines.append("- (No strong matches found in the harvested top ranks; review by query sections below.)\n\n")
    else:
        for c in iso_hits[:20]:
            rk = c.get("rank")
            rk_s = f"#{rk}" if isinstance(rk, int) else "n/a"
            lines.append(f"- {rk_s} [{c.get('domain')}] {c.get('title','').strip() or '(title unavailable)'}\n")
            lines.append(f"  - {c.get('url')}\n")
            lines.append(f"  - source_query: `{c.get('source_query')}`\n")
    lines.append("\n")

    lines.append("## URLs by Query (Top results, capped)\n\n")
    for q in gated_sorted:
        # Pull snapshot row
        snap = next((r for r in serp_rows if r.get("query") == q), None)
        m = (snap or {}).get("query_metrics") or {}
        f = (snap or {}).get("serp_features") or {}
        lines.append(f"### {q}\n\n")
        lines.append(f"- search_volume: **{m.get('search_volume', 0)}** | cpc: **{m.get('cpc', 0)}** | competition: **{m.get('competition', 'N/A')}**\n")
        lines.append(f"- serp_features: AIO={bool(f.get('ai_overview'))}, PAA={bool(f.get('people_also_ask'))}, Video={bool(f.get('video'))}, Forums={bool(f.get('forums'))}\n\n")
        rows = by_query.get(q, [])
        if not rows:
            lines.append("- (no kept candidates)\n\n")
            continue
        for c in rows[:10]:
            rk = c.get("rank")
            rk_s = f"#{rk}" if isinstance(rk, int) else "n/a"
            strong = "strong" if c.get("strong_rank") else "soft"
            lines.append(f"- {rk_s} ({strong}) [{c.get('domain')}] {c.get('title','').strip()}\n")
            lines.append(f"  - {c.get('url')}\n")
            lines.append(f"  - domain_quality: `{c.get('domain_quality')}`\n")
        lines.append("\n")

    lines.append("## URLs by Domain (Most relevant first)\n\n")
    # Sort domains with preferred first
    domains_sorted = sorted(by_domain.keys(), key=lambda d: (d not in set(preferred_domains), d))
    for d in domains_sorted:
        rows = by_domain[d]
        lines.append(f"### {d}\n\n")
        for c in rows[:5]:
            rk = c.get("rank")
            rk_s = f"#{rk}" if isinstance(rk, int) else "n/a"
            lines.append(f"- {rk_s} {c.get('title','').strip()}\n")
            lines.append(f"  - {c.get('url')}\n")
            lines.append(f"  - source_query: `{c.get('source_query')}`\n")
        lines.append("\n")

    _write_text(out_dir / "04-competitor-url-pack.md", "".join(lines))

    # Phase 4: update strategy doc (evidence-driven)
    strat: List[str] = []
    strat.append("# Update Strategy (UGC AI Tools SERP Harvest)\n\n")
    strat.append(f"> Generated: `{_utc_now_iso()}` | Market: US + EN | Cadence: Biweekly\n\n")
    strat.append("This strategy turns SERP evidence into a repeatable refresh process for listicles and guides.\n\n")
    strat.append("## Biweekly Runbook (Fixed Actions)\n\n")
    strat.append("1. Re-run the harvest script with the same `00-mission-config.json`.\n")
    strat.append("2. Compare outputs vs last run:\n")
    strat.append("   - Query metrics delta (volume/CPC/competition).\n")
    strat.append("   - SERP feature delta (AI Overview / PAA appearing or disappearing).\n")
    strat.append("   - New URLs entering Top20 (strong targets) and URLs dropping out.\n")
    strat.append("3. Record a delta summary and decide update level (L1/L2/L3).\n\n")
    strat.append("## Trigger Rules (Hard Gates)\n\n")
    strat.append("- **Primary keyword decay**: if the primary keyword’s `search_volume` drops by >=30% for 2 consecutive runs, trigger a primary-keyword re-selection.\n")
    strat.append("- **Intent drift**: if SERP Top10 shifts from listicle to definition/how-to majority, switch title formula and restructure plan for the next version.\n")
    strat.append("- **AIO/PAA concentration**: if AIO appears and PAA questions cluster on a specific sub-intent, upgrade that sub-intent into a new page or rewrite the FAQ to match PAA phrasing.\n\n")
    strat.append("## Update Levels (Operational)\n\n")
    strat.append("- **L1 (30 min)**: update pricing links, tool list, disclosures, and freshness date.\n")
    strat.append("- **L2 (2-3 hours)**: rewrite Quick Answer, strengthen tables for extraction, replace FAQ with PAA-style questions.\n")
    strat.append("- **L3 (1 day)**: change primary keyword, rewrite title/slug, reorder tool pool, possibly expand list size; re-run validator + AEO scoring.\n\n")
    strat.append("## Compatibility Note (Listicle Validator)\n\n")
    strat.append("- Do NOT add extra H2 sections into the article body for `standard` profile listicles.\n")
    strat.append("- Keep update strategy as a separate file (`08-update-strategy.md`) unless switching to `mega` profile where an in-article update module is allowed.\n\n")
    strat.append("## Current Evidence Snapshot\n\n")
    strat.append(f"- Queries generated: **{len(queries)}** (max {max_queries})\n")
    strat.append(f"- Queries passing volume gate: **{len(gated_sorted)}**\n")
    strat.append(f"- SERP calls made: **{serp_calls}**\n")
    strat.append(f"- Kept candidate URLs: **{len(kept_candidates)}**\n\n")
    strat.append("## Where to Look\n\n")
    strat.append("- `01-query-universe.json`: validated demand per query\n")
    strat.append("- `02-serp-snapshots.jsonl`: SERP features + top organic evidence\n")
    strat.append("- `03-candidate-urls.jsonl`: deduped off-site URLs (traceable to query + rank)\n")
    strat.append("- `04-competitor-url-pack.md`: curated link pack for editors\n")
    _write_text(out_dir / "05-update-strategy.md", "".join(strat))


def main(argv: List[str]) -> int:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", required=True, help="Output directory containing 00-mission-config.json")
    args = ap.parse_args(argv)

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    run(out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

