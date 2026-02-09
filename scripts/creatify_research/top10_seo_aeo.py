#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.parse
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Local imports (no package install)
THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(THIS_DIR))

from ddg_serp import DDGResult, hash_query, parse_ddg_html, parse_ddg_lite_html  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "research 竞品分析" / "creatify-ai"
DATA_DIR = OUT_DIR / "data"


def _mkdir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def _write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")


def _slug(url: str) -> str:
    try:
        p = urllib.parse.urlparse(url)
        return (p.path or "").strip("/").split("/")[-1]
    except Exception:
        return ""


def _guess_date_from_snippet(snippet: str) -> Optional[str]:
    s = (snippet or "").strip()
    m = re.match(
        r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2}),\s+(20\d{2})",
        s,
    )
    if not m:
        return None
    mon_map = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }
    mon = mon_map.get(m.group(1))
    day = int(m.group(2))
    year = int(m.group(3))
    if not mon:
        return None
    try:
        return dt.date(year, mon, day).isoformat()
    except Exception:
        return None


def _is_blog_post(url: str) -> bool:
    try:
        p = urllib.parse.urlparse(url)
        if p.netloc.lower() != "creatify.ai":
            return False
        if not p.path.startswith("/blog/"):
            return False
        return p.path.strip("/") != "blog"
    except Exception:
        return False


def build_inventory(max_urls: int = 500) -> List[Dict[str, Any]]:
    """
    Offline inventory from pre-fetched Wayback CDX dumps (recommended).

    Network fetching from Python is intentionally avoided in this repo environment. Use
    `scripts/creatify_research/fetch_top10_artifacts.sh` to fetch CDX + SERP + Wayback HTML first.
    """
    cdx_asc = sorted(DATA_DIR.glob("wayback_cdx_*_asc.json"))
    cdx_desc = sorted(DATA_DIR.glob("wayback_cdx_*_desc.json"))
    if not cdx_asc or not cdx_desc:
        raise SystemExit(
            "Missing Wayback CDX dumps. Run `scripts/creatify_research/fetch_top10_artifacts.sh` first "
            "(or fetch CDX JSONs into `research 竞品分析/creatify-ai/data/`)."
        )

    def _load_cdx_rows(p: Path) -> List[Tuple[str, str]]:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return []
        if not isinstance(data, list) or len(data) < 2:
            return []
        rows: List[Tuple[str, str]] = []
        for r in data[1:]:
            if not isinstance(r, list) or len(r) < 2:
                continue
            ts, orig = str(r[0]), str(r[1])
            if ts and orig:
                rows.append((ts, orig))
        return rows

    first_by_orig: Dict[str, str] = {}
    last_by_orig: Dict[str, str] = {}

    for p in cdx_asc:
        for ts, orig in _load_cdx_rows(p):
            first_by_orig.setdefault(orig, ts)
    for p in cdx_desc:
        for ts, orig in _load_cdx_rows(p):
            last_by_orig.setdefault(orig, ts)

    by_url: Dict[str, Dict[str, Any]] = {}
    for orig, last_ts in last_by_orig.items():
        first_ts = first_by_orig.get(orig)
        try:
            u = urllib.parse.urlparse(orig)
        except Exception:
            continue
        netloc = (u.netloc or "").lower()
        if netloc not in {"creatify.ai", "www.creatify.ai"}:
            continue
        path = (u.path or "").strip()
        if not path.startswith("/blog/") or path.rstrip("/") == "/blog":
            continue
        if any(
            x in path.lower()
            for x in [
                "/blog/tag/",
                "/blog/category/",
                "/blog/author/",
                "/blog/page/",
                "/blog/wp-",
                "/blog/feed",
                "/blog/sitemap",
            ]
        ):
            continue
        if re.search(r"\.(xml|json|txt|png|jpg|jpeg|webp|gif|svg|css|js)$", path.lower()):
            continue

        canon = urllib.parse.urlunparse(("https", "creatify.ai", path.rstrip("/"), "", "", ""))
        publish_guess = None
        if first_ts and re.match(r"^\d{14}$", first_ts):
            publish_guess = dt.date(int(first_ts[0:4]), int(first_ts[4:6]), int(first_ts[6:8])).isoformat()

        by_url[canon] = {
            "url": canon,
            "title_serp": "",
            "snippet_serp": "",
            "publish_date_guess": publish_guess,
            "slug": _slug(canon),
            "wayback_first_seen_ts": first_ts,
            "wayback_last_seen_ts": last_ts,
            "discovered_by": ["wayback_cdx_dump"],
        }

        if len(by_url) >= max_urls:
            break

    return sorted(by_url.values(), key=lambda x: x["url"])


def candidate_filter(inv: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    today = dt.date.today()
    evergreen_re = re.compile(
        r"\b(ultimate|guide|cost|pricing|template|checklist|best|vs\.?|compare|comparison|ads?|seo|tiktok|youtube)\b",
        re.I,
    )

    out_scored: List[Tuple[int, Dict[str, Any]]] = []
    for it in inv:
        title = it.get("title_serp") or it.get("slug") or ""
        keep = False
        d = it.get("publish_date_guess")
        if d:
            try:
                dd = dt.date.fromisoformat(d)
                months = (today.year - dd.year) * 12 + (today.month - dd.month)
                if months <= 12:
                    keep = True
            except Exception:
                keep = False
        if not keep and evergreen_re.search(title):
                keep = True
        if keep:
            pre = _freshness_score(it.get("publish_date_guess")) + _commercial_intent_score(title)
            if evergreen_re.search(title):
                pre += 8
            out_scored.append((pre, it))

    # best-effort dedup by slug
    seen: Dict[str, int] = {}
    dedup: List[Dict[str, Any]] = []
    for _, it in sorted(out_scored, key=lambda x: x[0], reverse=True):
        s = it.get("slug") or it["url"]
        seen[s] = seen.get(s, 0) + 1
        if seen[s] <= 2:
            dedup.append(it)
    return dedup


def _core_query_from_title(title: str) -> str:
    t = (title or "").strip()
    t = re.sub(r"\bCreatify\b", "", t, flags=re.I).strip()
    t = re.sub(r"\b20\d{2}\b", "", t).strip()
    t = re.sub(r"[\|\-–—:]+", " ", t).strip()
    t = re.sub(r"\s+", " ", t).strip()
    words = t.split()
    return " ".join(words[:10])


def generate_queries(item: Dict[str, Any]) -> List[str]:
    title = item.get("title_serp") or ""
    core = _core_query_from_title(title) or item.get("slug") or ""
    core = core.strip()
    queries: List[str] = []
    if core:
        queries.append(core)
    m = re.search(r"\b(20\d{2})\b", title)
    yr = m.group(1) if m else str(dt.date.today().year)
    if core:
        queries.append(f"{core} {yr}")
    lc = core.lower()
    if not lc.startswith(("how", "what", "best")):
        if any(k in lc for k in ["seo", "ads", "pricing", "cost", "template", "generator", "agency"]):
            queries.append(f"how to {core}")
        else:
            queries.append(f"what is {core}")
    uniq: List[str] = []
    seen = set()
    for q in queries:
        q = q.strip()
        if not q or q in seen:
            continue
        seen.add(q)
        uniq.append(q)
    return uniq[:3]


def _rank_of_url(results: List[DDGResult], target_url: str) -> Optional[int]:
    tu = target_url.rstrip("/")
    for r in results:
        if r.url.rstrip("/") == tu:
            return r.rank
    return None


def _serp_position_score(best_rank: Optional[int]) -> int:
    if best_rank is None:
        return 0
    if best_rank <= 3:
        return 40
    if best_rank <= 10:
        return 30
    if best_rank <= 20:
        return 20
    if best_rank <= 50:
        return 10
    return 0


def _freshness_score(publish_date_guess: Optional[str]) -> int:
    if not publish_date_guess:
        return 10
    try:
        d = dt.date.fromisoformat(publish_date_guess)
    except Exception:
        return 10
    today = dt.date.today()
    months = (today.year - d.year) * 12 + (today.month - d.month)
    if months <= 6:
        return 20
    if months <= 12:
        return 10
    return 5


def _commercial_intent_score(title: str) -> int:
    t = (title or "").lower()
    score = 0
    if any(k in t for k in ["pricing", "cost", "ads", "advertis", "agency", "template", "best", "vs", "compare"]):
        score += 10
    if any(k in t for k in ["tiktok", "youtube", "meta", "facebook", "google ads", "shopify"]):
        score += 5
    if any(k in t for k in ["generator", "ai avatar", "ugc", "video ad", "creative"]):
        score += 5
    return min(20, score)


def _load_semrush_keyword_samples() -> Dict[str, int]:
    semrush_path = DATA_DIR / "traffic_seo_semrush.json"
    samples: Dict[str, int] = {}
    if not semrush_path.exists():
        return samples
    try:
        d = json.loads(semrush_path.read_text(encoding="utf-8"))
        for m in d.get("observed_months") or []:
            for it in (m.get("top_organic_keywords_sample") or []):
                kw = str(it.get("keyword") or "").lower().strip()
                vol = int(it.get("volume") or 0)
                if kw and vol:
                    samples[kw] = max(vol, samples.get(kw, 0))
    except Exception:
        return {}
    return samples


def _demand_proxy_score(title: str, samples: Dict[str, int]) -> Tuple[int, Optional[Dict[str, Any]]]:
    t = (title or "").lower()
    best: Optional[Tuple[str, int]] = None
    for kw, vol in samples.items():
        if kw and kw in t:
            if best is None or vol > best[1]:
                best = (kw, vol)
    if best:
        kw, vol = best
        if vol >= 10000:
            return 20, {"matched_keyword": kw, "volume": vol}
        if vol >= 5000:
            return 16, {"matched_keyword": kw, "volume": vol}
        if vol >= 1000:
            return 12, {"matched_keyword": kw, "volume": vol}
        return 8, {"matched_keyword": kw, "volume": vol}
    return 10, None


def seo_validate(
    candidates: List[Dict[str, Any]], *, max_candidates: int = 80
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    serp_dir = DATA_DIR / "serp_snapshots"
    _mkdir(serp_dir)

    semrush_samples = _load_semrush_keyword_samples()

    def _load_serp_results(q: str) -> Tuple[Optional[str], List[DDGResult]]:
        snap_path = serp_dir / f"serp_{hash_query(q)}.html"
        if not snap_path.exists():
            return None, []
        raw = snap_path.read_text(encoding="utf-8", errors="ignore")
        # Multi-page snapshots are concatenated with <!--PAGE--> markers.
        pages = [p for p in raw.split("<!--PAGE-->") if p.strip()]
        allr: List[DDGResult] = []
        for p in pages:
            rs, _next = parse_ddg_lite_html(p, max_results=60)
            if not rs:
                rs = parse_ddg_html(p, max_results=60)
            for r in rs:
                allr.append(DDGResult(rank=len(allr) + 1, url=r.url, title=r.title, snippet=r.snippet))
            if len(allr) >= 50:
                break
        return str(snap_path.relative_to(ROOT)), allr[:50]

    serp_evidence: List[Dict[str, Any]] = []
    seo_rows: List[Dict[str, Any]] = []

    for c in candidates[:max_candidates]:
        url = c["url"]
        title = c.get("title_serp") or c.get("slug") or ""
        queries = generate_queries(c)

        best_rank = None
        best_query = None
        best_snapshot = None
        any_serp_parsed = False

        for q in queries:
            qh = hash_query(q)
            snapshot_rel, results = _load_serp_results(q)

            rank = _rank_of_url(results, url)
            if rank is not None and (best_rank is None or rank < best_rank):
                best_rank = rank
                best_query = q
                best_snapshot = snapshot_rel

            serp_status = "missing" if snapshot_rel is None else "ok"
            serp_blocked_hint = None
            if snapshot_rel is not None and not results:
                # DDG Lite can return anomaly/bot pages; mark explicitly for transparency.
                try:
                    raw = (serp_dir / f"serp_{qh}.html").read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    raw = ""
                if "anomaly.js" in raw or "cc=botnet" in raw or "anomaly-modal" in raw:
                    serp_status = "blocked"
                    serp_blocked_hint = "duckduckgo_anomaly_botnet"
                else:
                    serp_status = "empty"
            if results:
                any_serp_parsed = True

            serp_evidence.append(
                {
                    "query": q,
                    "captured_at": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
                    "target_url": url,
                    "target_rank": rank,
                    "snapshot_path": snapshot_rel,
                    "serp_status": serp_status,
                    "blocked_hint": serp_blocked_hint,
                    "top10": [
                        {"rank": r.rank, "url": r.url, "title": r.title, "snippet": r.snippet}
                        for r in results[:10]
                    ],
                }
            )

        pos_score = _serp_position_score(best_rank)
        demand_score, demand_evidence = _demand_proxy_score(title, semrush_samples)
        intent_score = _commercial_intent_score(title)
        fresh_score = _freshness_score(c.get("publish_date_guess"))
        seo_score = min(100, pos_score + demand_score + intent_score + fresh_score)

        seo_rows.append(
            {
                "url": url,
                "title": title,
                "publish_date_guess": c.get("publish_date_guess"),
                "wayback_last_seen_ts": c.get("wayback_last_seen_ts"),
                "queries": queries,
                "best_query": best_query,
                "best_rank": best_rank,
                "serp_parsed_any": any_serp_parsed,
                "serp_position_score": pos_score,
                "demand_proxy_score": demand_score,
                "demand_proxy_evidence": demand_evidence,
                "commercial_intent_score": intent_score,
                "freshness_score": fresh_score,
                "seo_score": seo_score,
                "serp_snapshot_best": best_snapshot,
            }
        )

    return seo_rows, serp_evidence


def _extract_text_words(html_text: str, limit_words: int = 180) -> str:
    t = re.sub(r"(?is)<script.*?>.*?</script>", " ", html_text or "")
    t = re.sub(r"(?is)<style.*?>.*?</style>", " ", t)
    t = re.sub(r"(?is)<[^>]+>", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return " ".join(t.split()[:limit_words])


def _count_tags(html_text: str, tag: str) -> int:
    return len(re.findall(rf"(?is)<{tag}\b", html_text or ""))


def _find_faq_questions(html_text: str, limit: int = 12) -> List[str]:
    t = html_text or ""
    idx = t.lower().find("faq")
    if idx < 0:
        idx = t.lower().find("frequently asked")
    if idx < 0:
        return []
    window = t[idx : idx + 60000]
    qs: List[str] = []
    for m in re.finditer(r"(?is)<h[23][^>]*>(.*?)</h[23]>", window):
        q = re.sub(r"<[^>]+>", " ", m.group(1))
        q = re.sub(r"\s+", " ", q).strip()
        if not q or "faq" in q.lower() or len(q) > 140:
            continue
        qs.append(q)
        if len(qs) >= limit:
            break
    return qs


def _extract_outbound_domains(html_text: str) -> List[str]:
    hrefs = re.findall(r'(?is)href="(https?://[^"]+)"', html_text or "")
    domains: List[str] = []
    for h in hrefs:
        try:
            net = urllib.parse.urlparse(h).netloc.lower()
        except Exception:
            continue
        if not net or net.endswith("creatify.ai"):
            continue
        domains.append(net)
    return domains


def _authority_domain_ratio(domains: List[str]) -> float:
    if not domains:
        return 0.0
    auth = 0
    for d in domains:
        if any(
            d.endswith(x)
            for x in [
                "google.com",
                "youtube.com",
                "tiktok.com",
                "meta.com",
                "facebook.com",
                "instagram.com",
                "microsoft.com",
                "openai.com",
                "apple.com",
                "hubspot.com",
                "ahrefs.com",
                "semrush.com",
                "statista.com",
                "pewresearch.org",
                ".gov",
                ".edu",
            ]
        ):
            auth += 1
    return auth / max(1, len(domains))


def _aeo_score_from_cache(html_text: str) -> Tuple[int, Dict[str, Any]]:
    first150 = _extract_text_words(html_text, limit_words=170)

    answer_first = 0
    if re.search(
        r"(?i)in this guide|you will learn|here(?:'s| is) (?:how|what)|step[- ]by[- ]step|we'll cover",
        first150,
    ):
        answer_first = 18
    if re.search(r"(?i)^what is |^how to |^tiktok seo|^youtube ads", first150.strip()):
        answer_first = max(answer_first, 20)
    if re.search(r"(?i)\b(a checklist|key takeaways|tl;dr)\b", first150):
        answer_first = 25

    h2 = _count_tags(html_text, "h2")
    h3 = _count_tags(html_text, "h3")
    lists = _count_tags(html_text, "ul") + _count_tags(html_text, "ol")
    tables = _count_tags(html_text, "table")
    structure = 0
    if h2 >= 6:
        structure += 10
    if h3 >= 4:
        structure += 5
    if lists >= 3:
        structure += 6
    if tables >= 1:
        structure += 4
    structure = min(25, structure)

    faq_qs = _find_faq_questions(html_text)
    faq = 0
    if faq_qs:
        faq = 12
        if len(faq_qs) >= 5:
            faq = 18
        if len(faq_qs) >= 8:
            faq = 20

    domains = _extract_outbound_domains(html_text)
    auth_ratio = _authority_domain_ratio(domains)
    citations = 0
    if len(domains) >= 5:
        citations = 8
    if len(domains) >= 10:
        citations = 12
    if auth_ratio >= 0.35:
        citations = min(15, citations + 3)

    cta = 0
    if re.search(r"(?i)try creatify|get started|sign up|pricing", html_text):
        cta = 10
    if re.search(r"(?i)free trial|start for free|generate (?:your|a) ad", html_text):
        cta = 15

    score = min(100, answer_first + structure + faq + citations + cta)
    evidence = {
        "first_words": first150,
        "h2": h2,
        "h3": h3,
        "lists": lists,
        "tables": tables,
        "faq_questions": faq_qs,
        "outbound_domains_count": len(domains),
        "authority_domain_ratio": round(auth_ratio, 3),
        "subscores": {
            "answer_first": answer_first,
            "structure": structure,
            "faq": faq,
            "citations": citations,
            "cta": cta,
        },
    }
    return score, evidence


def aeo_audit(seo_rows: List[Dict[str, Any]], *, max_audits: int = 60) -> List[Dict[str, Any]]:
    cache_dir = DATA_DIR / "wayback_cache"
    _mkdir(cache_dir)

    out: List[Dict[str, Any]] = []
    for r in seo_rows[:max_audits]:
        url = r["url"]
        ts = str(r.get("wayback_last_seen_ts") or "")
        cache_status = None
        cache_path = cache_dir / f"wayback_{hash_query(url)}.html"
        aeo_score = 0
        evidence: Dict[str, Any] = {}
        extracted_title: Optional[str] = None
        extracted_date: Optional[str] = None

        snap_url = None
        if ts and re.match(r"^\\d{14}$", ts):
            snap_url = f"https://web.archive.org/web/{ts}id_/{url}"

        if cache_path.exists():
            html_text = cache_path.read_text(encoding="utf-8", errors="ignore")
            if html_text:
                aeo_score, evidence = _aeo_score_from_cache(html_text)
                evidence["has_ld_json"] = bool(re.search(r'(?is)type="application/ld\+json"', html_text))
                evidence["has_faqpage_schema"] = bool(re.search(r'(?is)"@type"\s*:\s*"FAQPage"', html_text))
                evidence["has_howto_schema"] = bool(re.search(r'(?is)"@type"\s*:\s*"HowTo"', html_text))
                mt = re.search(r'(?is)<meta[^>]+property="og:title"[^>]+content="([^"]+)"', html_text)
                if mt:
                    extracted_title = re.sub(r"\s+", " ", mt.group(1)).strip()
                if not extracted_title:
                    tt = re.search(r"(?is)<title[^>]*>(.*?)</title>", html_text)
                    if tt:
                        extracted_title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", tt.group(1))).strip()
                mdp = re.search(r'(?is)"datePublished"\\s*:\\s*"([^"]+)"', html_text)
                if mdp:
                    extracted_date = mdp.group(1)[:10]
                if not extracted_date:
                    mp = re.search(
                        r'(?is)<meta[^>]+property="article:published_time"[^>]+content="([^"]+)"', html_text
                    )
                    if mp:
                        extracted_date = mp.group(1)[:10]

        out.append(
            {
                "url": url,
                "title": (r.get("title") or "").strip(),
                "wayback_snapshot_url": snap_url,
                "wayback_status": cache_status,
                "wayback_path": str(cache_path.relative_to(ROOT)) if cache_path.exists() else None,
                "aeo_score": aeo_score,
                "aeo_evidence": evidence,
                "extracted_title": extracted_title,
                "extracted_publish_date": extracted_date,
            }
        )
    return out


def confidence_label(seo_row: Dict[str, Any], aeo_row: Dict[str, Any]) -> str:
    has_serp = seo_row.get("best_rank") is not None
    serp_parsed = bool(seo_row.get("serp_parsed_any"))
    has_cache = bool(aeo_row.get("wayback_path"))
    if has_serp and has_cache:
        return "High"
    if serp_parsed and has_cache:
        return "Med"
    if has_serp or has_cache:
        return "Med"
    return "Low"


def _make_aeo_highlights(ev: Dict[str, Any]) -> List[str]:
    if not ev:
        return []
    subs = ev.get("subscores") or {}
    out: List[str] = []
    if subs.get("answer_first", 0) >= 20:
        out.append("Answer-first 开篇信号强")
    if int(ev.get("h2") or 0) >= 6:
        out.append(f"H2 结构密（H2={ev.get('h2')}）")
    if int(ev.get("lists") or 0) >= 3:
        out.append(f"列表/步骤块充足（lists={ev.get('lists')}）")
    if int(ev.get("tables") or 0) >= 1:
        out.append("包含表格（利于对比/摘录）")
    if ev.get("faq_questions"):
        out.append(f"包含 FAQ（Q={len(ev.get('faq_questions') or [])}）")
    if int(ev.get("outbound_domains_count") or 0) >= 8:
        out.append(f"外部引用较多（outlinks={ev.get('outbound_domains_count')}）")
    if float(ev.get("authority_domain_ratio") or 0) >= 0.35:
        out.append("权威来源占比不错")
    if ev.get("has_faqpage_schema"):
        out.append("检测到 FAQPage schema")
    if ev.get("has_howto_schema"):
        out.append("检测到 HowTo schema")
    return out[:6]


def build_top10_report(seo_rows: List[Dict[str, Any]], aeo_rows: List[Dict[str, Any]]) -> None:
    by_url_aeo = {r["url"]: r for r in aeo_rows}
    combined: List[Dict[str, Any]] = []

    for s in seo_rows:
        a = by_url_aeo.get(s["url"]) or {}
        title_seo = (s.get("title") or "").strip()
        title_ex = (a.get("extracted_title") or "").strip()
        is_slug_like = (" " not in title_seo) and ("-" in title_seo) and (len(title_seo) >= 18)
        if title_ex and (not title_seo or is_slug_like):
            title = title_ex
        else:
            title = title_seo or title_ex
        if not title:
            title = _slug(s["url"]) or s["url"]
        seo_score = int(s.get("seo_score") or 0)
        aeo_score = int(a.get("aeo_score") or 0)
        total = round(0.7 * seo_score + 0.3 * aeo_score, 2)
        combined.append(
            {
                "url": s["url"],
                "title": title,
                "publish_date_guess": (a.get("extracted_publish_date") or s.get("publish_date_guess")),
                "seo_score": seo_score,
                "aeo_score": aeo_score,
                "total_score": total,
                "best_query": s.get("best_query"),
                "best_rank": s.get("best_rank"),
                "demand_proxy_evidence": s.get("demand_proxy_evidence"),
                "serp_snapshot_best": s.get("serp_snapshot_best"),
                "wayback_path": a.get("wayback_path"),
                "aeo_highlights": _make_aeo_highlights((a.get("aeo_evidence") or {})),
                "confidence": confidence_label(s, a),
            }
        )

    combined.sort(key=lambda x: x["total_score"], reverse=True)
    top10 = combined[:10]
    top20 = combined[:20]

    md: List[str] = []
    md.append("# Creatify Blog Top 10（SEO 优先 + AEO 加分）: 数据验证与解读（EN）")
    md.append("")
    md.append(f"> 生成时间: {dt.date.today().isoformat()}")
    md.append(
        "> 方法：SERP 快照（如可用）+ Wayback Machine（公开缓存）结构审计 + Semrush 公共快照关键词样本（需求代理）。"
        " 注：部分搜索引擎会返回反爬/异常页（如 DDG anomaly），已在 evidence pack 中标注 `serp_status`。"
    )
    md.append("")

    md.append("## 1) Top 10 结果总表")
    md.append("")
    md.append("| Rank | Title | Total | SEO | AEO | Best SERP | Demand Proxy | Confidence |")
    md.append("|---:|---|---:|---:|---:|---|---|---|")
    for i, it in enumerate(top10, start=1):
        if it.get("best_rank"):
            best_serp = f"#{it['best_rank']} ({it['best_query']})"
        else:
            best_serp = "— (blocked/unavailable or not in Top results)"
        dp = it.get("demand_proxy_evidence") or {}
        demand = f"{dp.get('matched_keyword')} ({dp.get('volume')})" if dp else "N/A"
        title = (it.get("title") or "").replace("|", " ")
        md.append(
            f"| {i} | {title[:70]} | {it['total_score']:.2f} | {it['seo_score']} | {it['aeo_score']} | {best_serp[:48].replace('|',' ')} | {demand} | {it['confidence']} |"
        )

    md.append("")
    md.append("## 2) Top 10 逐篇：SEO 证据 + AEO 结构亮点")
    md.append("")
    for i, it in enumerate(top10, start=1):
        md.append(f"### {i}. {it['title']}")
        md.append("")
        md.append(f"- URL: {it['url']}")
        if it.get("publish_date_guess"):
            md.append(f"- Publish (guess): {it['publish_date_guess']}")
        md.append(f"- Score: Total **{it['total_score']:.2f}** (SEO {it['seo_score']} / AEO {it['aeo_score']}) | Confidence: **{it['confidence']}**")
        if it.get("best_rank"):
            md.append(f"- Best SERP evidence: rank **#{it['best_rank']}** for query: `{it['best_query']}`")
        else:
            md.append("- SERP evidence: **not found / blocked / unavailable** for generated queries (see evidence pack `serp_status`).")
        if it.get("serp_snapshot_best"):
            md.append(f"- SERP snapshot: `{it['serp_snapshot_best']}`")
        if it.get("wayback_path"):
            md.append(f"- Wayback snapshot: `{it['wayback_path']}`")
        if it.get("aeo_highlights"):
            md.append("- AEO highlights:")
            for h in it["aeo_highlights"]:
                md.append(f"  - {h}")
        md.append("")

    md.append("## 3) Top 20 备选（用于扩展或做 Hub-and-Spoke）")
    md.append("")
    md.append("| Rank | Title | Total | Best SERP | AEO | Confidence |")
    md.append("|---:|---|---:|---|---:|---|")
    for i, it in enumerate(top20, start=1):
        best_serp = f"#{it['best_rank']}" if it.get("best_rank") else "—"
        title = (it.get("title") or "").replace("|", " ")
        md.append(f"| {i} | {title[:78]} | {it['total_score']:.2f} | {best_serp} | {it['aeo_score']} | {it['confidence']} |")

    md.append("")
    md.append("## 4) 两种角色的启发（结构化解读）")
    md.append("")
    md.append("### A) 站在 AEO 专家的角度：Top 10 的共性")
    md.append("")
    md.append("- **答案块优先（Answer-first）**：把定义/结论/步骤承诺放在首屏前 120–150 词，降低模型抽取成本。")
    md.append("- **结构化可摘录**：H2/H3 层级清晰 + 列表/表格/步骤块充足，比长段落更容易被 AI 与 PAA 抽取。")
    md.append("- **FAQ = PAA 工程**：FAQ 的问题本身就是长尾查询，应标准化问题句式并复用到站内多个页面形成“问题库”。")
    md.append("- **引用 = 可信度杠杆**：外链不仅是 SEO 信号，也是 AI 引擎判断“可核验性”的核心证据。")
    md.append("- **Schema 是可选但高 ROI**：若缓存页中能观察到 FAQPage/HowTo 结构化数据，AEO 适配会更强；没有也应列为下一阶段工程化目标。")

    md.append("")
    md.append("### B) 站在 Creatify Blog 负责人的角度：如何反推策略")
    md.append("")
    md.append("- **内容矩阵是否均衡**：Top 10 若以平台/投放/SEO 指南与对比评测为主，说明内容更偏中后段承接；需要补齐“认知型”的统计/趋势文章做引用与扩散。")
    md.append("- **Evergreen vs 借势热点**：把 Top 10 分成“可常年排名”与“短周期热点”，决定编辑排期与更新频率。")
    md.append("- **Hub-and-Spoke 内链蓝图**：用 Top 10 做 3–5 个 Hub（例如 TikTok / YouTube / UGC Ads / AI avatar），每个 Hub 连接 8–20 篇长尾 Spoke。")
    md.append("- **KPI 从发文数转到排名/答案引用**：建议组合 KPI：`Top10 query 覆盖率` + `Top20 排名数` + `AI referral（域级）` + `CTA 点击/试用转化`。")

    (OUT_DIR / "04-top10-seo-aeo.md").write_text("\n".join(md), encoding="utf-8")
    _write_json(
        DATA_DIR / "top10_ranking.json",
        {"generated_at": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z", "items": combined},
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?", default="all", choices=["prepare", "score", "all"])
    ap.add_argument("--max-urls", type=int, default=5000)
    ap.add_argument("--max-candidates", type=int, default=80)
    ap.add_argument("--max-audits", type=int, default=60)
    args = ap.parse_args()

    _mkdir(OUT_DIR)
    _mkdir(DATA_DIR)

    if args.cmd in {"prepare", "all"}:
        inv = build_inventory(max_urls=args.max_urls)
        _write_jsonl(DATA_DIR / "blog_inventory_en.jsonl", inv)

        candidates = candidate_filter(inv)
        selected = candidates[: args.max_candidates]
        _write_jsonl(DATA_DIR / "selected_candidates.jsonl", selected)
        _write_json(
            DATA_DIR / "candidate_pool_meta.json",
            {
                "count_total": len(candidates),
                "count_selected": len(selected),
                "generated_at": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
            },
        )

        # Export fetch plans for shell-based fetching (network outside Python).
        serp_plan: Dict[str, str] = {}
        for c in selected:
            for q in generate_queries(c):
                serp_plan[hash_query(q)] = q
        (DATA_DIR / "serp_fetch_plan.tsv").write_text(
            "\n".join(f"{h}\t{q}" for h, q in sorted(serp_plan.items())) + "\n",
            encoding="utf-8",
        )
        (DATA_DIR / "wayback_fetch_plan.tsv").write_text(
            "\n".join(
                f"{hash_query(c['url'])}\t{c['url']}\t{(c.get('wayback_last_seen_ts') or '')}"
                for c in selected
            )
            + "\n",
            encoding="utf-8",
        )
        print("OK: prepared inventory + fetch plans.")

    if args.cmd in {"score", "all"}:
        selected_path = DATA_DIR / "selected_candidates.jsonl"
        if selected_path.exists():
            candidates = [
                json.loads(l)
                for l in selected_path.read_text(encoding="utf-8").splitlines()
                if l.strip()
            ]
        else:
            inv = build_inventory(max_urls=args.max_urls)
            candidates = candidate_filter(inv)[: args.max_candidates]

        seo_rows, serp_evidence = seo_validate(candidates, max_candidates=args.max_candidates)
        _write_jsonl(DATA_DIR / "seo_serp_evidence.jsonl", serp_evidence)
        _write_jsonl(DATA_DIR / "seo_scores.jsonl", seo_rows)

        aeo_rows = aeo_audit(seo_rows, max_audits=args.max_audits)
        _write_jsonl(DATA_DIR / "aeo_audit.jsonl", aeo_rows)

        build_top10_report(seo_rows, aeo_rows)
        print(f"OK: wrote Top10 report to: {OUT_DIR / '04-top10-seo-aeo.md'}")


if __name__ == "__main__":
    main()
