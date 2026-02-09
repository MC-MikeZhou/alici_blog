#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import html
import re
import urllib.parse
from dataclasses import dataclass
from typing import List, Optional, Tuple

from http_fetch import fetch_text_via_curl


DDG_HTML_BASES = [
    "https://html.duckduckgo.com/html/",
    "https://safe.duckduckgo.com/html/",
    "https://duckduckgo.com/html/",
]

DDG_LITE_BASES = [
    "https://lite.duckduckgo.com/lite/",
    "https://duckduckgo.com/lite/",
]


@dataclass(frozen=True)
class DDGResult:
    rank: int
    url: str
    title: str
    snippet: str


def hash_query(q: str) -> str:
    return hashlib.sha1(q.encode("utf-8")).hexdigest()[:12]


def _strip_tags(s: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", " ", s or "")).strip()


def _decode_ddg_redirect(href: str) -> str:
    """
    DDG often uses /l/?uddg=<encoded> redirects.
    """
    href = (href or "").strip()
    if not href:
        return ""
    if href.startswith("//"):
        href = "https:" + href
    if href.startswith("/l/") or "duckduckgo.com/l/" in href:
        try:
            u = urllib.parse.urlparse(href if href.startswith("http") else "https://duckduckgo.com" + href)
            qs = urllib.parse.parse_qs(u.query)
            uddg = (qs.get("uddg") or [""])[0]
            if uddg:
                return urllib.parse.unquote(uddg)
        except Exception:
            return href
    return href


def make_ddg_url(query: str, *, s: int = 0) -> str:
    # POST endpoint; URL is constant.
    _ = query
    _ = s
    return DDG_HTML_BASES[0]


def _fetch_ddg_lite_page(
    post_fields: dict, *, retries_per_base: int = 6, max_time_s: int = 22
) -> Tuple[str, int]:
    post_data = urllib.parse.urlencode({k: str(v) for k, v in (post_fields or {}).items()})
    last_status = 0
    for base in DDG_LITE_BASES:
        fr = fetch_text_via_curl(
            base,
            max_time_s=max_time_s,
            connect_timeout_s=6,
            retries=retries_per_base,
            post_data=post_data,
        )
        last_status = int(fr.status or 0)
        if fr.ok and fr.text and "<html" in fr.text.lower():
            return fr.text, last_status
    return "", last_status


def _parse_ddg_lite_next_fields(html_text: str) -> Optional[dict]:
    """
    DDG Lite uses a "Next Page" form with hidden fields. We replay that form to paginate.
    """
    m = re.search(r'(?is)<form[^>]+class="next_form"[^>]*>(.*?)</form>', html_text or "")
    if not m:
        return None
    form = m.group(1)
    fields = {}
    for im in re.finditer(r'(?is)<input[^>]+type="hidden"[^>]+name="([^"]+)"[^>]+value="([^"]*)"', form):
        fields[html.unescape(im.group(1))] = html.unescape(im.group(2))
    if not fields.get("q"):
        return None
    return fields


def parse_ddg_lite_html(html_text: str, *, max_results: int = 50) -> Tuple[List[DDGResult], Optional[dict]]:
    """
    Returns: (results, next_page_post_fields)
    """
    t = html_text or ""
    results: List[DDGResult] = []

    # Split into chunks by result-link anchors to keep snippets local.
    parts = re.split(r"(?is)(<a[^>]+class=['\"]result-link['\"][^>]*>.*?</a>)", t)
    if len(parts) < 3:
        return [], _parse_ddg_lite_next_fields(t)

    # parts alternates: [prefix, anchor1, rest1, anchor2, rest2, ...]
    for i in range(1, len(parts), 2):
        anchor = parts[i]
        rest = parts[i + 1] if i + 1 < len(parts) else ""
        ma = re.search(r'(?is)href="([^"]+)"[^>]*>(.*?)</a>', anchor)
        if not ma:
            continue
        url = html.unescape(ma.group(1)).strip()
        if url.startswith("//"):
            url = "https:" + url
        if not url.startswith("http"):
            continue
        title = _strip_tags(ma.group(2))
        ms = re.search(r"(?is)<td[^>]+class=['\"]result-snippet['\"][^>]*>(.*?)</td>", rest)
        snippet = _strip_tags(ms.group(1)) if ms else ""

        results.append(DDGResult(rank=len(results) + 1, url=url, title=title, snippet=snippet))
        if len(results) >= max_results:
            break

    return results, _parse_ddg_lite_next_fields(t)


def _fetch_ddg_html(query: str, *, offset: int, retries_per_base: int = 6) -> Tuple[str, int]:
    post_data = urllib.parse.urlencode({"q": query, "s": str(int(offset))})
    last_status = 0
    for base in DDG_HTML_BASES:
        fr = fetch_text_via_curl(
            base,
            max_time_s=18,
            connect_timeout_s=5,
            retries=retries_per_base,
            post_data=post_data,
        )
        last_status = int(fr.status or 0)
        if fr.ok and fr.text and "<html" in fr.text.lower():
            return fr.text, last_status
    return "", last_status


def parse_ddg_html(html_text: str, *, max_results: int = 50) -> List[DDGResult]:
    # Result blocks are div.result; title link is a.result__a.
    blocks = re.findall(r'<div class="result[^"]*".*?</div>\s*</div>\s*</div>', html_text or "", flags=re.S)
    if not blocks:
        # Fallback: split by result__a links if markup differs.
        blocks = re.findall(r'(<a[^>]+class="result__a"[^>]+>.*?</a>.*?)(?=<a[^>]+class="result__a"|$)', html_text or "", flags=re.S)

    out: List[DDGResult] = []
    for b in blocks:
        ma = re.search(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', b, flags=re.S)
        if not ma:
            continue
        href = _decode_ddg_redirect(ma.group(1))
        if not href.startswith("http"):
            continue
        title = _strip_tags(ma.group(2))

        ms = re.search(r'<a[^>]+class="result__snippet"[^>]*>(.*?)</a>', b, flags=re.S)
        if not ms:
            ms = re.search(r'<div[^>]+class="result__snippet"[^>]*>(.*?)</div>', b, flags=re.S)
        snippet = _strip_tags(ms.group(1)) if ms else ""

        out.append(DDGResult(rank=len(out) + 1, url=href, title=title, snippet=snippet))
        if len(out) >= max_results:
            break
    return out


def ddg_search(query: str, *, max_results: int = 50) -> Tuple[str, List[DDGResult]]:
    """
    Returns: (raw_html_combined, parsed_results)
    """
    all_results: List[DDGResult] = []
    raw_pages: List[str] = []

    # Prefer Lite: more stable + simpler HTML in many restricted environments.
    next_fields: Optional[dict] = {"q": query}
    lite_guard = 0
    while next_fields and len(all_results) < max_results and lite_guard < 6:
        html_text, status = _fetch_ddg_lite_page(next_fields, retries_per_base=8, max_time_s=22)
        _ = status
        if not html_text:
            break
        raw_pages.append(html_text)
        page_results, next_fields = parse_ddg_lite_html(html_text, max_results=max_results - len(all_results))
        if not page_results:
            break
        for r in page_results:
            all_results.append(DDGResult(rank=len(all_results) + 1, url=r.url, title=r.title, snippet=r.snippet))
        lite_guard += 1

    # Fallback: DDG HTML endpoint.
    if not all_results:
        offset = 0
        while len(all_results) < max_results and offset <= 200:
            html_text, status = _fetch_ddg_html(query, offset=offset, retries_per_base=8)
            _ = status
            if not html_text:
                break
            raw_pages.append(html_text)
            page_results = parse_ddg_html(html_text, max_results=max_results - len(all_results))
            if not page_results:
                break
            for r in page_results:
                all_results.append(
                    DDGResult(rank=len(all_results) + 1, url=r.url, title=r.title, snippet=r.snippet)
                )
            offset += 30  # DDG html pagination step

    return ("\n\n<!--PAGE-->\n\n".join(raw_pages), all_results)
