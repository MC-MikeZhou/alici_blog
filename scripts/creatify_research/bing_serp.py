#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import html
import re
import urllib.parse
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from http_fetch import fetch_text_via_curl


@dataclass(frozen=True)
class BingResult:
    rank: int
    url: str
    title: str
    snippet: str
    cache_url: Optional[str] = None


def _strip_tags(s: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", " ", s or "")).strip()


def _decode_bing_click_url(href: str) -> str:
    """
    Bing SERP often uses redirect links like https://www.bing.com/ck/a?...&u=a1....
    We decode the base64-ish 'u' param to get the real target URL.
    """
    href = (href or "").strip()
    if not href:
        return ""
    if "bing.com/ck/a" not in href:
        return href

    try:
        u = urllib.parse.urlparse(href)
        qs = urllib.parse.parse_qs(u.query)
        uu = (qs.get("u") or [""])[0]
        if not uu.startswith("a1"):
            return href
        b = uu[2:]
        pad = "=" * ((4 - (len(b) % 4)) % 4)
        decoded = base64.b64decode(b + pad).decode("utf-8", "ignore")
        return decoded.strip() or href
    except Exception:
        return href


def make_bing_search_url(query: str, *, count: int = 10, first: int = 1) -> str:
    q = urllib.parse.quote(query)
    # setlang/mkt to reduce localized SERP changes
    return f"https://www.bing.com/search?q={q}&count={int(count)}&first={int(first)}&setlang=en-US&mkt=en-US"


def parse_bing_serp(html_text: str, *, max_results: int = 50) -> List[BingResult]:
    blocks = re.findall(r'<li class="b_algo".*?</li>', html_text or "", flags=re.S)
    results: List[BingResult] = []
    for b in blocks:
        m = re.search(r'href="([^"]+)"', b)
        href = _decode_bing_click_url(m.group(1) if m else "")
        if not href.startswith("http"):
            continue
        mt = re.search(r"<a[^>]*>(.*?)</a>", b, flags=re.S)
        title = _strip_tags(mt.group(1)) if mt else ""
        mp = re.search(r"<p>(.*?)</p>", b, flags=re.S)
        snippet = _strip_tags(mp.group(1)) if mp else ""
        mc = re.search(r'(https?://cc\.bingj\.com/cache\.aspx[^"\s<]+)', b)
        cache_url = mc.group(1) if mc else None
        results.append(BingResult(rank=len(results) + 1, url=href, title=title, snippet=snippet, cache_url=cache_url))
        if len(results) >= max_results:
            break
    return results


def bing_search(query: str, *, max_results: int = 50) -> Tuple[str, List[BingResult]]:
    """
    Returns: (raw_html, parsed_results)
    """
    # Bing returns 10 per page; we page through.
    all_results: List[BingResult] = []
    raw_pages: List[str] = []
    first = 1
    while len(all_results) < max_results and first <= 200:
        url = make_bing_search_url(query, count=10, first=first)
        fr = fetch_text_via_curl(url, max_time_s=18, retries=10)
        if not fr.ok or not fr.text:
            break
        raw_pages.append(fr.text)
        page_results = parse_bing_serp(fr.text, max_results=max_results - len(all_results))
        if not page_results:
            break
        # Adjust ranks across pages
        for r in page_results:
            all_results.append(
                BingResult(
                    rank=len(all_results) + 1,
                    url=r.url,
                    title=r.title,
                    snippet=r.snippet,
                    cache_url=r.cache_url,
                )
            )
        first += 10

    return ("\n\n<!--PAGE-->\n\n".join(raw_pages), all_results)


def hash_query(q: str) -> str:
    return hashlib.sha1(q.encode("utf-8")).hexdigest()[:12]

