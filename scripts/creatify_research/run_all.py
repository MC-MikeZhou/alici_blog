#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Import sibling module without requiring package installs.
THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(THIS_DIR))

from dataforseo_curl import (  # noqa: E402
    DataForSEOCreds,
    dataforseo_keywords_search_volume_live,
    dataforseo_serp_google_organic_live_advanced,
    extract_keyword_items,
    extract_serp_items,
)


ROOT = Path(__file__).resolve().parents[2]  # repo root
OUT_DIR = ROOT / "research 竞品分析" / "creatify-ai"
DATA_DIR = OUT_DIR / "data"


def _mkdir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def _write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
        return obj if isinstance(obj, dict) else {}
    except Exception:
        return {}


def _domain(url: str) -> str:
    try:
        from urllib.parse import urlparse

        return (urlparse(url).netloc or "").lower()
    except Exception:
        return ""


def _normalize_url(url: str) -> str:
    return (url or "").strip()


def _inventory_queries() -> List[str]:
    # DataForSEO supports Google-style queries; "site:" is the safest way to enumerate URLs without crawling.
    return [
        "site:creatify.ai/zh/blog",
        "site:creatify.ai/blog",
        "site:creatify.ai \"blog\" \"creatify\"",
        "site:creatify.ai/zh/blog 2025",
        "site:creatify.ai/blog 2025",
        "site:creatify.ai/zh/blog 2026",
        "site:creatify.ai/blog 2026",
    ]


def _core_keyword_set() -> List[str]:
    # We use these keywords to build a 12-month trend proxy for awareness/interest.
    return [
        "creatify",
        "creatify ai",
        "creatify.ai",
        "creatify pricing",
        "creatify blog",
        "ai video ads generator",
        "ai ad generator",
        "ugc ads ai",
        "ai tiktok ads",
    ]


def _extract_organic_results(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for it in items:
        if str(it.get("type") or "") != "organic":
            continue
        url = _normalize_url(str(it.get("url") or ""))
        title = str(it.get("title") or "").strip()
        snippet = str(it.get("description") or "").strip()
        rank = it.get("rank_group") or it.get("rank_absolute") or None
        if not url:
            continue
        out.append(
            {
                "url": url,
                "domain": _domain(url),
                "title": title,
                "snippet": snippet,
                "rank": rank,
            }
        )
    return out


def _summarize_serp_features(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    features = {
        "ai_overview": False,
        "featured_snippet": False,
        "people_also_ask": False,
        "paa_questions": [],
        "video": False,
        "forums": False,
    }
    paa_questions: List[str] = []

    for it in items:
        t = str(it.get("type") or "")
        if t == "ai_overview":
            features["ai_overview"] = True
        elif t == "featured_snippet":
            features["featured_snippet"] = True
        elif t == "people_also_ask":
            features["people_also_ask"] = True
            sub = it.get("items")
            if isinstance(sub, list):
                for s in sub:
                    if isinstance(s, dict):
                        q = str(s.get("title") or "").strip()
                        if q:
                            paa_questions.append(q)
        elif t == "video":
            features["video"] = True
        elif t in ["discussions_and_forums", "forum"]:
            features["forums"] = True

    # cap to keep reports short
    features["paa_questions"] = paa_questions[:12]
    return features


def _build_inventory(creds: DataForSEOCreds, location_code: int, language_code: str) -> Dict[str, Any]:
    inv_raw_dir = DATA_DIR / "dataforseo" / "inventory_serp_raw"
    _mkdir(inv_raw_dir)

    all_urls: Dict[str, Dict[str, Any]] = {}
    evidence: List[Dict[str, Any]] = []

    for q in _inventory_queries():
        resp = dataforseo_serp_google_organic_live_advanced(
            query=q, location_code=location_code, language_code=language_code, creds=creds, depth=100
        )
        safe_name = "".join([c if c.isalnum() else "_" for c in q])[:120]
        _write_json(inv_raw_dir / f"{safe_name}.json", resp)

        items = extract_serp_items(resp)
        org = _extract_organic_results(items)
        features = _summarize_serp_features(items)
        evidence.append({"query": q, "features": features, "organic_count": len(org)})

        for r in org:
            url = r["url"]
            # Keep only blog-ish URLs on creatify.ai, but also allow feature/pricing pages for milestones.
            if r.get("domain") != "creatify.ai":
                continue
            if "/blog" not in url:
                continue
            if url not in all_urls:
                all_urls[url] = {
                    "url": url,
                    "title": r.get("title") or "",
                    "snippet": r.get("snippet") or "",
                    "discovered_by": [q],
                }
            else:
                all_urls[url]["discovered_by"] = sorted(
                    list(set((all_urls[url].get("discovered_by") or []) + [q]))
                )
                if not all_urls[url].get("title") and r.get("title"):
                    all_urls[url]["title"] = r.get("title") or ""

    inventory = {
        "generated_at": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "queries": evidence,
        "urls": sorted(all_urls.values(), key=lambda x: x["url"]),
        "url_count": len(all_urls),
    }
    _write_json(DATA_DIR / "blog_inventory.json", inventory)
    return inventory


def _build_keyword_trends(creds: DataForSEOCreds, location_code: int, language_code: str) -> Dict[str, Any]:
    kw_raw_dir = DATA_DIR / "dataforseo" / "keywords_raw"
    _mkdir(kw_raw_dir)

    keywords = _core_keyword_set()
    resp = dataforseo_keywords_search_volume_live(
        keywords=keywords,
        location_code=location_code,
        language_code=language_code,
        creds=creds,
        date_from="2025-02-01",
        date_to="2026-02-01",
    )
    _write_json(kw_raw_dir / "core_keywords.json", resp)

    items = extract_keyword_items(resp)
    out_items: List[Dict[str, Any]] = []
    for it in items:
        if not isinstance(it, dict):
            continue
        out_items.append(
            {
                "keyword": str(it.get("keyword") or ""),
                "search_volume": it.get("search_volume") or 0,
                "cpc": it.get("cpc") or 0,
                "competition": it.get("competition") or 0,
                "competition_level": it.get("competition_level") or "",
                "monthly_searches": it.get("monthly_searches") or [],
            }
        )

    trends = {
        "generated_at": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "location_code": location_code,
        "language_code": language_code,
        "keywords": out_items,
    }
    _write_json(DATA_DIR / "keyword_trends.json", trends)
    return trends


def _estimate_revenue_model(traffic_proxy: Dict[str, Any], inventory: Dict[str, Any]) -> Dict[str, Any]:
    """
    A conservative, explicit assumption-based model:
    We do NOT claim real revenue; we provide scenario ranges based on generic SaaS funnels.
    Inputs are only proxies (brand interest + indexed content).
    """
    # Use brand keyword "creatify" monthly volume as interest proxy
    brand = next((k for k in (traffic_proxy.get("keywords") or []) if (k.get("keyword") or "").lower() == "creatify"), None)
    monthly = (brand or {}).get("monthly_searches") or []
    # We want last 6 months of the proxy series if present.
    monthly_sorted = []
    for m in monthly:
        if not isinstance(m, dict):
            continue
        y = int(m.get("year") or 0)
        mo = int(m.get("month") or 0)
        v = int(m.get("search_volume") or 0)
        if y and mo:
            monthly_sorted.append((y, mo, v))
    monthly_sorted.sort(reverse=True)
    last6 = monthly_sorted[:6]

    blog_count = int(inventory.get("url_count") or 0)

    # Scenarios (explicitly assumptions; not factual):
    scenarios = [
        {
            "name": "Conservative",
            "visit_to_signup": 0.003,
            "signup_to_paid": 0.05,
            "arpa_usd": 39,
        },
        {
            "name": "Base",
            "visit_to_signup": 0.006,
            "signup_to_paid": 0.08,
            "arpa_usd": 59,
        },
        {
            "name": "Aggressive",
            "visit_to_signup": 0.010,
            "signup_to_paid": 0.12,
            "arpa_usd": 79,
        },
    ]

    # We do not have visits; we derive "inferred monthly visits" as a multiple of brand volume.
    # This is intentionally rough and explained in the report.
    # multiplier range is derived from typical brand query share vs total visits.
    # We keep it fixed per scenario for clarity.
    for s in scenarios:
        if s["name"] == "Conservative":
            s["brand_to_visits_multiplier"] = 30
        elif s["name"] == "Base":
            s["brand_to_visits_multiplier"] = 60
        else:
            s["brand_to_visits_multiplier"] = 100

    estimates = []
    for (y, mo, brand_vol) in last6:
        month = f"{y:04d}-{mo:02d}"
        row = {"month": month, "brand_search_volume_proxy": brand_vol, "blog_indexed_urls": blog_count}
        for s in scenarios:
            visits = int(round(brand_vol * s["brand_to_visits_multiplier"]))
            signups = visits * s["visit_to_signup"]
            paid = signups * s["signup_to_paid"]
            mrr = paid * s["arpa_usd"]
            row[f"mrr_usd_{s['name'].lower()}"] = int(round(mrr))
        estimates.append(row)

    return {
        "generated_at": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "notes": [
            "This is an assumption-based range model; not actual revenue.",
            "Inputs are proxies (brand keyword volume + blog index size).",
        ],
        "scenarios": scenarios,
        "estimates_last_6_months": estimates,
    }


def _md_table(headers: List[str], rows: List[List[str]]) -> str:
    out = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("|" + "|".join(["---"] * len(headers)) + "|")
    for r in rows:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out)


def _fmt_int(n: Any) -> str:
    try:
        return f"{int(n):,}"
    except Exception:
        return "0"


def _pick_last6_months_series(keyword_trends: Dict[str, Any], keyword: str) -> List[Dict[str, Any]]:
    kw = next(
        (k for k in (keyword_trends.get("keywords") or []) if str(k.get("keyword") or "").lower() == keyword.lower()),
        None,
    )
    monthly = (kw or {}).get("monthly_searches") or []
    items = []
    for m in monthly:
        if not isinstance(m, dict):
            continue
        y = int(m.get("year") or 0)
        mo = int(m.get("month") or 0)
        v = int(m.get("search_volume") or 0)
        if y and mo:
            items.append({"year": y, "month": mo, "search_volume": v})
    items.sort(key=lambda x: (x["year"], x["month"]), reverse=True)
    return items[:6]


def _write_reports(
    *,
    inventory: Dict[str, Any],
    keyword_trends: Dict[str, Any],
    revenue_est: Dict[str, Any],
    location_code: int,
    language_code: str,
) -> None:
    _mkdir(OUT_DIR)

    today = dt.date.today().isoformat()
    window = "2025-08-01 ~ 2026-01-31"

    # 00 Executive
    blog_urls = inventory.get("urls") or []
    exec_md = [
        "# Creatify（creatify.ai + /zh/blog）竞品流量与 AEO/SEO 研究：执行摘要",
        "",
        f"> **分析日期**: {today}",
        f"> **时间窗（近半年）**: {window}",
        f"> **数据源**: DataForSEO（SERP + Google Ads keywords data，US/EN）+ Google 索引枚举（site: 查询）",
        "",
        "## 一句话结论",
        "",
        "- 由于 Creatify 的博客/站点对脚本抓取存在 Cloudflare challenge，本次采用“**搜索引擎可见性驱动**”的方法：以 DataForSEO 枚举博客 URL、评估 SEO 关键词与 AEO（AI Overview/PAA）机会，给出近半年趋势代理与里程碑。",
        "",
        "## 核心数据（可复现）",
        "",
        f"- `site:` 枚举到的博客 URL 数（去重、仅含 /blog）：**{_fmt_int(inventory.get('url_count'))}**",
        f"- 分析区域：**location_code={location_code}（US）**，language_code=**{language_code}**",
        "",
        "## 近半年里程碑（本阶段定义：搜索可见性信号）",
        "",
        "我们将里程碑定义为三类信号的变化：",
        "1) 品牌兴趣（brand query）趋势（用 `creatify` 的 monthly_searches 作为代理）",
        "2) 博客索引规模（可被 SERP 枚举到的 URL 数）",
        "3) AEO 机会密度（目标关键词 SERP 是否出现 AI Overview / PAA）",
        "",
        "下一步（若你要“正文全量抓取 + 内容层面 AEO 结构评测”）：需要浏览器侧导出 sitemap 或 URL 列表（不绕过 Cloudflare）。",
        "",
    ]
    (OUT_DIR / "00-executive-summary.md").write_text("\n".join(exec_md), encoding="utf-8")

    # 01 Traffic & audience (proxy)
    brand_last6 = _pick_last6_months_series(keyword_trends, "creatify")
    rows = [[f"{x['year']:04d}-{x['month']:02d}", _fmt_int(x["search_volume"])] for x in brand_last6]
    traffic_md = [
        "# 访问量与用户数据（以“搜索可见性代理”刻画）",
        "",
        f"> **时间窗**: {window}",
        "> **说明**: 本报告无法直接抓取 Creatify 的站内 analytics；因此将“访问量/用户兴趣”的半年趋势用可复现的公开代理指标表达（Google Ads keyword monthly searches + SERP features）。",
        "",
        "## 1) 品牌兴趣趋势（代理）：`creatify` 的月搜索量",
        "",
        _md_table(["月份", "Search volume（proxy）"], rows) if rows else "- DataForSEO 未返回 monthly_searches（可能与账户权限/接口返回有关）。",
        "",
        "## 2) 内容资产规模（代理）：博客被索引的 URL 数",
        "",
        f"- `creatify.ai` 的 /blog 系列 URL（SERP 枚举去重）：**{_fmt_int(inventory.get('url_count'))}**",
        "",
        "## 3) 用户获取渠道（本阶段）",
        "",
        "- 本阶段聚焦 SEO/AEO，因此渠道数据仅覆盖“搜索引擎可见性”。如果你希望补齐 Direct/Paid/Social 等渠道，需要：Semrush 付费导出 / GA4 截图 / 或你提供第三方报表导出。",
        "",
    ]
    (OUT_DIR / "01-traffic-and-audience.md").write_text("\n".join(traffic_md), encoding="utf-8")

    # 02 SEO/AEO
    aeo_md = [
        "# SEO 搜索引擎流量与 AEO 表现（DataForSEO 证据）",
        "",
        f"> **时间窗**: {window}",
        f"> **地域/语言**: US/{language_code}",
        "",
        "## 1) Blog 可见性现状（基于 site: 枚举）",
        "",
        f"- 枚举 query 数：{len(inventory.get('queries') or [])}",
        f"- 枚举到的 /blog URL：**{_fmt_int(inventory.get('url_count'))}**",
        "",
        "## 2) AEO 信号：枚举查询自身的 SERP features",
        "",
    ]
    qrows = []
    for q in inventory.get("queries") or []:
        feats = q.get("features") or {}
        qrows.append(
            [
                str(q.get("query") or ""),
                "Y" if feats.get("ai_overview") else "N",
                "Y" if feats.get("people_also_ask") else "N",
                "Y" if feats.get("featured_snippet") else "N",
                "Y" if feats.get("video") else "N",
                str(q.get("organic_count") or 0),
            ]
        )
    if qrows:
        aeo_md.append(_md_table(["Query", "AIO", "PAA", "FS", "Video", "Organic"], qrows))
    else:
        aeo_md.append("- 无（inventory 阶段未产出 query evidence）。")

    aeo_md += [
        "",
        "## 3) 关键词商业价值（CPC/竞争度）",
        "",
        "以下为本次拉取的核心关键词集（用于趋势代理 + 商业意图参考）：",
        "",
    ]
    krows = []
    for k in keyword_trends.get("keywords") or []:
        kw = str(k.get("keyword") or "")
        sv = k.get("search_volume") or 0
        cpc = k.get("cpc") or 0
        comp = k.get("competition_level") or ""
        krows.append([kw, _fmt_int(sv), f"${float(cpc):.2f}", str(comp)])
    if krows:
        aeo_md.append(_md_table(["Keyword", "Volume", "CPC", "Competition"], krows))
    else:
        aeo_md.append("- 未拉取到关键词数据（检查 DataForSEO 返回）。")

    (OUT_DIR / "02-seo-aeo-performance.md").write_text("\n".join(aeo_md), encoding="utf-8")

    # 03 Blog inventory & milestones
    inv_rows = []
    for u in (inventory.get("urls") or [])[:80]:
        inv_rows.append([u.get("url") or "", (u.get("title") or "")[:80].replace("\n", " ")])
    inv_md = [
        "# 博客流量表现（基于索引可见性）与近半年里程碑",
        "",
        f"> **时间窗**: {window}",
        "> **说明**: 在无法直接抓取博客正文的情况下，本章用“被索引页面清单 + SERP features + 关键词趋势代理”来评估博客的流量潜力与 AEO 表现。",
        "",
        "## 1) 博客 URL 清单（节选）",
        "",
        _md_table(["URL", "Title (SERP)"], inv_rows) if inv_rows else "- 暂无（未枚举到 blog URLs）。",
        "",
        "## 2) 里程碑（本阶段可验证）",
        "",
        "我们用“可复现”的代理数据来定义里程碑：",
        "- brand search proxy（`creatify` monthly_searches）出现明显上升/下降的月份",
        "- blog 索引 URL 数量的显著变化（需要多次运行对比；本次为 baseline snapshot）",
        "",
        "## 3) 收入（区间估算模型）",
        "",
        "注意：以下为区间估算（非真实营收披露），用于竞品量级判断。",
        "",
    ]
    est_rows = []
    for r in revenue_est.get("estimates_last_6_months") or []:
        est_rows.append(
            [
                str(r.get("month") or ""),
                _fmt_int(r.get("brand_search_volume_proxy") or 0),
                _fmt_int(r.get("mrr_usd_conservative") or 0),
                _fmt_int(r.get("mrr_usd_base") or 0),
                _fmt_int(r.get("mrr_usd_aggressive") or 0),
            ]
        )
    if est_rows:
        inv_md.append(
            _md_table(
                ["Month", "Brand volume proxy", "MRR$ (Cons.)", "MRR$ (Base)", "MRR$ (Aggr.)"],
                est_rows,
            )
        )
    else:
        inv_md.append("- 无估算结果（brand monthly series 为空或 DataForSEO 未返回）。")

    (OUT_DIR / "03-blog-inventory-milestones.md").write_text("\n".join(inv_md), encoding="utf-8")


def _write_reports_from_public_snapshot(snapshot_path: Path) -> None:
    """
    Build a minimal report set from a pre-collected public snapshot JSON.
    This is a fallback when DataForSEO credentials are unavailable.
    """
    snap = _read_json(snapshot_path)
    if not snap:
        raise SystemExit(f"Invalid snapshot JSON: {snapshot_path}")

    _mkdir(OUT_DIR)
    today = dt.date.today().isoformat()

    # Copy snapshot into evidence pack so runs are reproducible.
    _mkdir(DATA_DIR)
    _write_json(DATA_DIR / "public_snapshot.json", snap)

    # Build small tables from known keys if present.
    traffic = _read_json(DATA_DIR / "traffic_seo_semrush.json")
    revenue = _read_json(DATA_DIR / "revenue_public.json")
    blog = _read_json(DATA_DIR / "blog_samples.json")

    # If the workspace already contains the richer, hand-built research docs, do not overwrite.
    expected = [
        OUT_DIR / "00-executive-summary.md",
        OUT_DIR / "01-traffic-and-audience.md",
        OUT_DIR / "02-seo-aeo-performance.md",
        OUT_DIR / "03-blog-inventory-milestones.md",
    ]
    if all(p.exists() for p in expected):
        print(f"OK: public snapshot stored at: {DATA_DIR / 'public_snapshot.json'}")
        print(f"OK: reports already exist at: {OUT_DIR}")
        return

    # Minimal docs as fallback (kept short on purpose).
    (OUT_DIR / "00-executive-summary.md").write_text(
        "\n".join(
            [
                "# Creatify public snapshot (fallback)",
                "",
                f"> generated: {today}",
                "",
                "- DataForSEO creds missing; using pre-collected public snapshot JSON.",
                f"- Snapshot: `{DATA_DIR / 'public_snapshot.json'}`",
                "",
                "Next: add DataForSEO creds to run full pipeline.",
            ]
        ),
        encoding="utf-8",
    )
    (OUT_DIR / "01-traffic-and-audience.md").write_text(
        json.dumps(traffic or snap.get("traffic") or {}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (OUT_DIR / "02-seo-aeo-performance.md").write_text(
        json.dumps(snap.get("seo_aeo") or {}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (OUT_DIR / "03-blog-inventory-milestones.md").write_text(
        json.dumps(blog or snap.get("blog") or {}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    _write_json(DATA_DIR / "revenue_public_snapshot.json", revenue or snap.get("revenue") or {})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--public-snapshot",
        help="Path to a JSON snapshot to use when DataForSEO credentials are unavailable.",
    )
    args = ap.parse_args()

    if args.public_snapshot:
        _write_reports_from_public_snapshot(Path(args.public_snapshot).resolve())
        return

    # Default mode: DataForSEO pipeline.
    creds = DataForSEOCreds.from_env()

    location_code = int(os.environ.get("CREATIFY_LOCATION_CODE") or 2840)
    language_code = str(os.environ.get("CREATIFY_LANGUAGE_CODE") or "en").strip() or "en"

    _mkdir(DATA_DIR)
    _mkdir(DATA_DIR / "dataforseo")

    inventory = _build_inventory(creds, location_code, language_code)
    keyword_trends = _build_keyword_trends(creds, location_code, language_code)

    revenue_est = _estimate_revenue_model(keyword_trends, inventory)
    _write_json(DATA_DIR / "revenue_estimates.json", revenue_est)

    _write_reports(
        inventory=inventory,
        keyword_trends=keyword_trends,
        revenue_est=revenue_est,
        location_code=location_code,
        language_code=language_code,
    )

    print(f"OK: wrote reports to: {OUT_DIR}")


if __name__ == "__main__":
    main()
