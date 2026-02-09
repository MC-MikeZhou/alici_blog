#!/usr/bin/env python3
from __future__ import annotations

import base64
import json
import os
import subprocess
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


DATAFORSEO_BASE = "https://api.dataforseo.com/v3"


@dataclass(frozen=True)
class DataForSEOCreds:
    login: str
    password: str

    @staticmethod
    def from_env() -> "DataForSEOCreds":
        login = (os.environ.get("DATAFORSEO_LOGIN") or "").strip()
        password = (os.environ.get("DATAFORSEO_PASSWORD") or "").strip()
        if not login or not password:
            raise SystemExit(
                "Missing DataForSEO credentials. Set env vars: DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD."
            )
        return DataForSEOCreds(login=login, password=password)

    def auth_header_value(self) -> str:
        token = f"{self.login}:{self.password}".encode("utf-8")
        return "Basic " + base64.b64encode(token).decode("utf-8")


def curl_post_json(
    *,
    url: str,
    payload: List[Dict[str, Any]],
    creds: DataForSEOCreds,
    timeout_s: int = 60,
    retry: int = 3,
    sleep_s: float = 0.8,
) -> Dict[str, Any]:
    """
    Use curl to POST JSON and return parsed JSON dict.
    We use curl (not requests/urllib) because Python DNS resolution is unreliable in this environment.
    """
    if retry < 1:
        retry = 1

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
    for attempt in range(1, retry + 1):
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
                last_err = f"Invalid JSON response (attempt {attempt}): {p.stdout[:300]}"
            else:
                if isinstance(obj, dict):
                    if sleep_s:
                        time.sleep(sleep_s)
                    return obj
                last_err = f"Unexpected response type (attempt {attempt}): {type(obj)}"
        else:
            last_err = (p.stderr or p.stdout or "").strip()[:800]
        time.sleep(min(2.0, 0.6 * attempt))

    raise SystemExit(f"DataForSEO request failed after {retry} attempts: {last_err}")


def dataforseo_keywords_search_volume_live(
    *,
    keywords: List[str],
    location_code: int,
    language_code: str,
    creds: DataForSEOCreds,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "keywords": keywords,
        "location_code": int(location_code),
        "language_code": str(language_code),
        "search_partners": False,
    }
    if date_from:
        payload["date_from"] = date_from
    if date_to:
        payload["date_to"] = date_to
    return curl_post_json(
        url=f"{DATAFORSEO_BASE}/keywords_data/google_ads/search_volume/live",
        payload=[payload],
        creds=creds,
    )


def dataforseo_serp_google_organic_live_advanced(
    *,
    query: str,
    location_code: int,
    language_code: str,
    creds: DataForSEOCreds,
    depth: int = 100,
    device: str = "desktop",
    os_name: str = "windows",
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "keyword": query,
        "location_code": int(location_code),
        "language_code": str(language_code),
        "device": device,
        "os": os_name,
        "depth": int(depth),
    }
    return curl_post_json(
        url=f"{DATAFORSEO_BASE}/serp/google/organic/live/advanced",
        payload=[payload],
        creds=creds,
        timeout_s=90,
    )


def extract_tasks_ok(obj: Dict[str, Any]) -> List[Dict[str, Any]]:
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


def extract_serp_items(obj: Dict[str, Any]) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for t in extract_tasks_ok(obj):
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


def extract_keyword_items(obj: Dict[str, Any]) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for t in extract_tasks_ok(obj):
        res = t.get("result")
        if not isinstance(res, list):
            continue
        for it in res:
            if isinstance(it, dict):
                items.append(it)
    return items

