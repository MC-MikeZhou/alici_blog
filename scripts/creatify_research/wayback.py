#!/usr/bin/env python3
from __future__ import annotations

import json
import urllib.parse
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from http_fetch import fetch_text_via_curl


CDX_ENDPOINT = "https://web.archive.org/cdx/search/cdx"


@dataclass(frozen=True)
class WaybackSnapshot:
    timestamp: str
    original: str
    statuscode: str

    def snapshot_url(self) -> str:
        # id_ returns more raw HTML (less replay UI), but not always available; fallback is fine.
        return f"https://web.archive.org/web/{self.timestamp}id_/{self.original}"


def _cdx_query(params: Dict[str, str], *, max_time_s: int = 25, retries: int = 10) -> Optional[List]:
    full = CDX_ENDPOINT + "?" + urllib.parse.urlencode(params)
    fr = fetch_text_via_curl(full, max_time_s=max_time_s, retries=retries)
    if not fr.ok or not fr.text:
        return None
    try:
        data = json.loads(fr.text)
    except Exception:
        return None
    if not isinstance(data, list) or len(data) < 2:
        return None
    return data


def list_unique_urls(
    url_pattern: str,
    *,
    match_type: str = "prefix",
    from_year: int = 2020,
    to_year: int = 2026,
    limit: int = 5000,
) -> Dict[str, Dict[str, str]]:
    """
    Returns mapping:
      original_url -> {"first_seen_ts": "...", "last_seen_ts": "..."}

    Notes:
    - Uses two CDX queries (sort asc/desc) collapsed by urlkey for best-effort first/last seen.
    - url_pattern should typically be host + path with wildcard, e.g. "creatify.ai/blog/*".
    """
    base = {
        "url": url_pattern,
        "matchType": match_type,
        "output": "json",
        "fl": "timestamp,original",
        "filter": "statuscode:200",
        "collapse": "urlkey",
        "from": str(from_year),
        "to": str(to_year),
        "limit": str(int(limit)),
    }

    asc = dict(base)
    asc["sort"] = "asc"
    desc = dict(base)
    desc["sort"] = "desc"

    out: Dict[str, Dict[str, str]] = {}

    asc_data = _cdx_query(asc, max_time_s=30, retries=12) or []
    for row in asc_data[1:]:
        if not isinstance(row, list) or len(row) < 2:
            continue
        ts, orig = str(row[0]), str(row[1])
        if not ts or not orig:
            continue
        out.setdefault(orig, {})["first_seen_ts"] = ts

    desc_data = _cdx_query(desc, max_time_s=30, retries=12) or []
    for row in desc_data[1:]:
        if not isinstance(row, list) or len(row) < 2:
            continue
        ts, orig = str(row[0]), str(row[1])
        if not ts or not orig:
            continue
        out.setdefault(orig, {})["last_seen_ts"] = ts

    return out


def find_latest_snapshot(url: str, *, from_year: int = 2024, to_year: int = 2026) -> Optional[WaybackSnapshot]:
    q = {
        "url": url,
        "output": "json",
        "fl": "timestamp,original,statuscode",
        "filter": "statuscode:200",
        "collapse": "digest",
        "limit": "1",
        "sort": "desc",
        "from": str(from_year),
        "to": str(to_year),
    }
    data = _cdx_query(q, max_time_s=22, retries=12)
    if not data:
        return None
    row = data[1]  # type: ignore[index]
    if not isinstance(row, list) or len(row) < 3:
        return None
    ts, orig, sc = str(row[0]), str(row[1]), str(row[2])
    if not ts or not orig:
        return None
    return WaybackSnapshot(timestamp=ts, original=orig, statuscode=sc)


def fetch_snapshot_html(snapshot: WaybackSnapshot) -> Tuple[Optional[int], str]:
    fr = fetch_text_via_curl(snapshot.snapshot_url(), max_time_s=25, retries=10)
    return fr.status, fr.text if fr.ok else ""
