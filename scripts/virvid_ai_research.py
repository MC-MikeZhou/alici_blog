#!/usr/bin/env python3
"""
Virvid.ai competitor research runner (crawl + AEO features + DataForSEO Labs + reports).
Outputs land in: research 竞品分析/virvid-ai/

Design goals:
- Reproducible: raw API responses + page snapshots are saved.
- Safe: no hard-coded credentials; reads DataForSEO creds from .mcp.json.
- Low-deps: stdlib only.
"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import datetime as dt
import hashlib
import json
import os
import random
import re
import sys
import time
import urllib.parse
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
import subprocess
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from threading import Lock
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed


USER_AGENT = "Mozilla/5.0 (compatible; AliciBlogResearchBot/1.0; +https://alici.ai)"
DEFAULT_BASE = "https://virvid.ai"
DEFAULT_BLOG = "https://virvid.ai/blog"
DEFAULT_NAME = "Virvid.ai"

US_LOCATION_CODE = 2840
EN_LANGUAGE_CODE = "en"

TIME_WINDOW_SINCE = dt.date(2025, 8, 1)
TIME_WINDOW_UNTIL = dt.date(2026, 1, 31)

DEFAULT_SESSIONS_PER_USER = [1.2, 1.4, 1.6]


class RateLimiter:
    def __init__(self, min_interval_s: float) -> None:
        self._min_interval_s = max(0.0, float(min_interval_s))
        self._lock = Lock()
        self._last_at = 0.0

    def wait(self) -> None:
        if self._min_interval_s <= 0:
            return
        with self._lock:
            now = time.time()
            wait_s = (self._last_at + self._min_interval_s) - now
            if wait_s > 0:
                time.sleep(wait_s)
            self._last_at = time.time()


def derive_domain_target(base: str) -> str:
    try:
        netloc = urllib.parse.urlparse(base).netloc or base
    except Exception:
        netloc = base
    netloc = netloc.strip().lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    return netloc


def geo_display(location_code: Optional[int], language_code: str) -> str:
    lc = (language_code or "").strip() or "en"
    if location_code is None:
        return f"Global/{lc}"
    if int(location_code) == US_LOCATION_CODE and lc == "en":
        return "US/en"
    return f"location_code={int(location_code)}/{lc}"


def geo_note(location_code: Optional[int], language_code: str) -> str:
    lc = (language_code or "").strip() or "en"
    if location_code is None:
        return f"Global/{lc} (location=all, language_code={lc})"
    return f"{geo_display(location_code, lc)} (location_code={int(location_code)}, language_code={lc})"


def parse_optional_int(x: Optional[str]) -> Optional[int]:
    if x is None:
        return None
    s = str(x).strip().lower()
    if s in {"", "none", "null"}:
        return None
    return int(s)


def fetch_url_with_retries(url: str, limiter: Optional[RateLimiter], timeout_s: int = 45, max_retries: int = 3) -> FetchResult:
    last = None
    for attempt in range(1, max_retries + 1):
        if limiter:
            limiter.wait()
        fr = fetch_url(url, timeout_s=timeout_s)
        last = fr
        retriable = False
        if fr.status in {0, 408, 425, 429, 500, 502, 503, 504}:
            retriable = True
        if fr.status == 200 and not fr.body:
            retriable = True
        if fr.error and "curl_error" in fr.error:
            retriable = True
        if not retriable or attempt == max_retries:
            return fr
        backoff = min(8.0, 0.6 * attempt + random.random() * 0.4)
        time.sleep(backoff)
    return last or FetchResult(url=url, status=0, final_url=url, fetched_at=utc_now_iso(), content_type="", body=b"", error="unknown")


def utc_now_iso() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            try:
                rows.append(json.loads(s))
            except Exception:
                continue
    return rows


def write_csv(path: Path, rows: Sequence[Dict[str, Any]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(fieldnames))
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def sha256_bytes(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


class LinkExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        if tag.lower() != "a":
            return
        href = None
        for k, v in attrs:
            if k.lower() == "href" and v:
                href = v
                break
        if href:
            self.links.append(href.strip())


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._buf: List[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        t = tag.lower()
        if t in {"script", "style", "noscript"}:
            self._skip_depth += 1

        if t in {"p", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6"}:
            self._buf.append("\n")

    def handle_endtag(self, tag: str) -> None:
        t = tag.lower()
        if t in {"script", "style", "noscript"} and self._skip_depth > 0:
            self._skip_depth -= 1
        if t in {"p", "li"}:
            self._buf.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip_depth > 0:
            return
        s = data.strip()
        if not s:
            return
        self._buf.append(s + " ")

    def text(self) -> str:
        out = "".join(self._buf)
        out = re.sub(r"[ \t]+\n", "\n", out)
        out = re.sub(r"\n{3,}", "\n\n", out)
        return out.strip()


@dataclass
class FetchResult:
    url: str
    status: int
    final_url: str
    fetched_at: str
    content_type: str
    body: bytes
    error: str = ""


def fetch_url(url: str, timeout_s: int = 45) -> FetchResult:
    """
    Prefer curl to avoid intermittent SSL EOF errors on some macOS Python builds.
    """
    fetched_at = utc_now_iso()
    meta_marker = b"\n__CURLMETA__"
    try:
        res = subprocess.run(
            [
                "curl",
                "-sS",
                "-L",
                "--max-time",
                str(int(timeout_s)),
                "-A",
                USER_AGENT,
                "-w",
                "\n__CURLMETA__%{http_code} %{url_effective}\n",
                url,
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out = res.stdout
        idx = out.rfind(meta_marker)
        if idx == -1:
            return FetchResult(url=url, status=0, final_url=url, fetched_at=fetched_at, content_type="", body=out, error="curl_missing_meta")
        body = out[:idx]
        meta = out[idx + len(meta_marker) :].decode("utf-8", errors="replace").strip()
        parts = meta.split(" ", 1)
        status = int(parts[0]) if parts and parts[0].isdigit() else 0
        final_url = parts[1].strip() if len(parts) > 1 else url
        return FetchResult(url=url, status=status, final_url=final_url, fetched_at=fetched_at, content_type="", body=body)
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode("utf-8", errors="replace").strip()
        return FetchResult(url=url, status=0, final_url=url, fetched_at=fetched_at, content_type="", body=b"", error=f"curl_error: {err[:300]}")
    except Exception as e:
        return FetchResult(url=url, status=0, final_url=url, fetched_at=fetched_at, content_type="", body=b"", error=f"{type(e).__name__}: {e}")


def normalize_url(base: str, href: str) -> Optional[str]:
    href = href.strip()
    if not href or href.startswith("#") or href.startswith("mailto:") or href.startswith("javascript:"):
        return None
    u = urllib.parse.urljoin(base, href)
    parsed = urllib.parse.urlparse(u)
    if parsed.scheme not in {"http", "https"}:
        return None
    # strip fragments
    parsed = parsed._replace(fragment="")
    return parsed.geturl()


def is_same_site(url: str, base_netloc: str) -> bool:
    try:
        return urllib.parse.urlparse(url).netloc == base_netloc
    except Exception:
        return False


def blog_root_and_prefix(blog_index: str) -> Tuple[str, str]:
    """
    Returns (blog_root, blog_prefix) where:
      - blog_root is the normalized path root (no trailing slash), e.g. "/blog" or "/resource"
      - blog_prefix is blog_root + "/", e.g. "/blog/" or "/resource/"
    """
    try:
        path = urllib.parse.urlparse(blog_index).path or ""
    except Exception:
        path = ""
    blog_root = (path or "").rstrip("/") or "/blog"
    blog_prefix = blog_root.rstrip("/") + "/"
    return blog_root, blog_prefix


def url_path_startswith(url: str, prefix: str) -> bool:
    try:
        return urllib.parse.urlparse(url).path.startswith(prefix)
    except Exception:
        return False


def extract_links(html: str, base_url: str) -> List[str]:
    p = LinkExtractor()
    p.feed(html)
    out: List[str] = []
    for href in p.links:
        u = normalize_url(base_url, href)
        if u:
            out.append(u)
    # keep order but unique
    seen: Set[str] = set()
    uniq: List[str] = []
    for u in out:
        if u in seen:
            continue
        seen.add(u)
        uniq.append(u)
    return uniq


def parse_sitemaps_from_robots(robots_txt: str) -> List[str]:
    sitemaps = []
    for line in robots_txt.splitlines():
        if line.lower().startswith("sitemap:"):
            s = line.split(":", 1)[1].strip()
            if s:
                sitemaps.append(s)
    return sitemaps


def parse_sitemap_xml(xml_bytes: bytes) -> List[str]:
    urls: List[str] = []
    try:
        root = ET.fromstring(xml_bytes)
    except Exception:
        return urls

    # Support sitemapindex and urlset
    ns = ""
    if root.tag.startswith("{"):
        ns = root.tag.split("}", 1)[0] + "}"

    def find_text(el: ET.Element, child: str) -> Optional[str]:
        c = el.find(f"{ns}{child}")
        if c is None or c.text is None:
            return None
        return c.text.strip()

    if root.tag.endswith("sitemapindex"):
        for sm in root.findall(f"{ns}sitemap"):
            loc = find_text(sm, "loc")
            if loc:
                urls.append(loc)
        return urls

    if root.tag.endswith("urlset"):
        for u in root.findall(f"{ns}url"):
            loc = find_text(u, "loc")
            if loc:
                urls.append(loc)
        return urls

    return urls


def load_dataforseo_creds(repo_root: Path) -> Tuple[str, str]:
    mcp_path = repo_root / ".mcp.json"
    cfg = read_json(mcp_path)
    dataforseo = cfg.get("mcpServers", {}).get("dataforseo", {})
    env = dataforseo.get("env", {}) or {}
    username = env.get("DATAFORSEO_USERNAME", "") or env.get("DATAFORSEO_LOGIN", "")
    password = env.get("DATAFORSEO_PASSWORD", "")
    if not username or not password:
        raise RuntimeError("Missing DataForSEO credentials in .mcp.json (mcpServers.dataforseo.env).")
    return str(username), str(password)


class DataForSEOClient:
    def __init__(self, username: str, password: str):
        self.base_url = "https://api.dataforseo.com/v3"
        auth = (f"{username}:{password}").encode("utf-8")
        self.auth_header = "Basic " + (base64(auth))

    def post(self, endpoint: str, payload: List[Dict[str, Any]], timeout_s: int = 60) -> Dict[str, Any]:
        """
        Use curl to avoid intermittent SSL EOF issues seen with urllib on some macOS builds.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        data = json.dumps(payload, ensure_ascii=False)
        last_err = None
        for attempt in range(1, 4):
            try:
                res = subprocess.run(
                    [
                        "curl",
                        "-sS",
                        "--max-time",
                        str(int(timeout_s)),
                        "-A",
                        USER_AGENT,
                        "-H",
                        f"Authorization: {self.auth_header}",
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
                raw = res.stdout.decode("utf-8", errors="replace")
                return json.loads(raw)
            except Exception as e:
                last_err = e
                time.sleep(0.6 * attempt)
        raise RuntimeError(f"DataForSEO request failed after retries: {last_err}")


def base64(data: bytes) -> str:
    import base64 as _b64

    return _b64.b64encode(data).decode("utf-8")


def safe_int(x: Any, default: int = 0) -> int:
    try:
        if x is None:
            return default
        return int(float(x))
    except Exception:
        return default


def safe_float(x: Any, default: float = 0.0) -> float:
    try:
        if x is None:
            return default
        return float(x)
    except Exception:
        return default


def extract_jsonld_blocks(html: str) -> List[Any]:
    blocks: List[Any] = []
    # Keep it simple: find <script ... application/ld+json ...> ... </script>
    pattern = re.compile(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.I | re.S)
    for m in pattern.finditer(html):
        raw = m.group(1).strip()
        if not raw:
            continue
        # Some sites include multiple JSON objects; try strict then lenient
        try:
            blocks.append(json.loads(raw))
            continue
        except Exception:
            pass
        # Lenient: strip HTML comments
        raw2 = re.sub(r"<!--|-->", "", raw).strip()
        try:
            blocks.append(json.loads(raw2))
        except Exception:
            continue
    return blocks


def flatten_jsonld_types(obj: Any) -> List[str]:
    out: List[str] = []

    def walk(x: Any) -> None:
        if isinstance(x, dict):
            t = x.get("@type")
            if isinstance(t, str):
                out.append(t)
            elif isinstance(t, list):
                out.extend([str(z) for z in t if isinstance(z, (str, int, float))])
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(obj)
    # unique preserve order
    seen = set()
    uniq: List[str] = []
    for t in out:
        t2 = str(t).strip()
        if not t2 or t2 in seen:
            continue
        seen.add(t2)
        uniq.append(t2)
    return uniq


def extract_meta(html: str) -> Dict[str, str]:
    # Very lightweight extraction via regex; good enough for title/date/canonical
    meta: Dict[str, str] = {}
    title_m = re.search(r"<title[^>]*>(.*?)</title>", html, flags=re.I | re.S)
    if title_m:
        meta["title_tag"] = re.sub(r"\s+", " ", title_m.group(1)).strip()

    def find_meta(prop_or_name: str) -> Optional[str]:
        # meta property="og:title" content="..."
        pat = re.compile(
            rf'<meta[^>]+(?:property|name)=["\']{re.escape(prop_or_name)}["\'][^>]+content=["\'](.*?)["\']',
            re.I | re.S,
        )
        m = pat.search(html)
        if m:
            return re.sub(r"\s+", " ", m.group(1)).strip()
        return None

    for k in ["og:title", "twitter:title", "description", "og:description", "article:published_time", "article:modified_time"]:
        v = find_meta(k)
        if v:
            meta[k] = v

    canon = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\'](.*?)["\']', html, flags=re.I | re.S)
    if canon:
        meta["canonical"] = canon.group(1).strip()
    return meta


def parse_date_any(s: str) -> Optional[dt.date]:
    s = s.strip()
    if not s:
        return None
    # common ISO
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            d = dt.datetime.strptime(s[: len(fmt)], fmt)
            return d.date()
        except Exception:
            continue
    # RFC3339-ish: 2026-01-22T12:34:56.000Z
    m = re.match(r"(\d{4}-\d{2}-\d{2})", s)
    if m:
        try:
            return dt.date.fromisoformat(m.group(1))
        except Exception:
            return None
    return None


def extract_published_date(html: str, meta: Dict[str, str], jsonld: List[Any]) -> Optional[dt.date]:
    candidates: List[str] = []
    if meta.get("article:published_time"):
        candidates.append(meta["article:published_time"])
    # <time datetime="">
    for m in re.finditer(r"<time[^>]+datetime=['\"](.*?)['\"]", html, flags=re.I):
        candidates.append(m.group(1))
    # JSON-LD datePublished
    def walk(x: Any) -> None:
        if isinstance(x, dict):
            for k, v in x.items():
                if k == "datePublished" and isinstance(v, str):
                    candidates.append(v)
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    for b in jsonld:
        walk(b)

    for c in candidates:
        d = parse_date_any(c)
        if d:
            return d
    return None


def slug_from_url(url: str) -> str:
    p = urllib.parse.urlparse(url)
    parts = [x for x in p.path.split("/") if x]
    if not parts:
        return "index"
    s = parts[-1]
    s = re.sub(r"[^a-zA-Z0-9_-]+", "-", s).strip("-").lower()
    return s or "page"


def month_bucket(date_: Optional[dt.date]) -> str:
    if not date_:
        return "unknown"
    return f"{date_.year:04d}-{date_.month:02d}"


def within_window(d: Optional[dt.date], since: dt.date, until: dt.date) -> bool:
    if not d:
        return True  # keep unknown dates, but flag later
    return since <= d <= until


def month_str_to_date(m: str) -> Optional[dt.date]:
    m = (m or "").strip()
    if not re.match(r"^\d{4}-\d{2}$", m):
        return None
    try:
        y, mo = m.split("-", 1)
        return dt.date(int(y), int(mo), 1)
    except Exception:
        return None


def filter_month_rows(rows: List[Dict[str, Any]], since: dt.date, until: dt.date) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    since_m = since.replace(day=1)
    until_m = until.replace(day=1)
    for r in rows:
        d = month_str_to_date(str(r.get("month") or ""))
        if not d:
            continue
        if since_m <= d <= until_m:
            out.append(r)
    return out


def sleep_polite(base_s: float) -> None:
    # add jitter so we don't look like a bot hammering endpoints
    jitter = random.random() * 0.25
    time.sleep(max(0.0, base_s + jitter))


def discover_blog_urls(
    base: str,
    blog_index: str,
    rate_limit_s: float,
    max_list_pages: int,
    refresh: bool,
    cache_dir: Path,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Returns:
      - blog_posts: list of {url, discovered_via, discovered_at, listing_date?, listing_title?}
      - sources: list of sources entries (for 99-sources.md)
    """
    sources: List[Dict[str, Any]] = []
    base_netloc = urllib.parse.urlparse(base).netloc
    blog_root, blog_prefix = blog_root_and_prefix(blog_index)

    # 1) robots.txt -> sitemaps
    robots_url = urllib.parse.urljoin(base, "/robots.txt")
    robots_cache = cache_dir / "robots.txt"
    robots_txt = ""
    if robots_cache.exists() and not refresh:
        robots_txt = robots_cache.read_text(encoding="utf-8", errors="replace")
        sources.append(
            {
                "kind": "robots",
                "url": robots_url,
                "retrieved_at": "",
                "status": 200,
                "local_path": str(robots_cache),
                "note": "robots.txt used to discover sitemaps (cached)",
            }
        )
    else:
        fr = fetch_url(robots_url)
        if fr.status and fr.body:
            robots_txt = fr.body.decode("utf-8", errors="replace")
            robots_cache.parent.mkdir(parents=True, exist_ok=True)
            robots_cache.write_text(robots_txt, encoding="utf-8")
        sources.append(
            {
                "kind": "robots",
                "url": robots_url,
                "retrieved_at": fr.fetched_at,
                "status": fr.status,
                "local_path": str(robots_cache),
                "note": "robots.txt used to discover sitemaps",
            }
        )
        sleep_polite(rate_limit_s)

    sitemaps = parse_sitemaps_from_robots(robots_txt)
    if not sitemaps:
        # fallback to common sitemap location
        sitemaps = [urllib.parse.urljoin(base, "/sitemap.xml")]

    blog_urls: Set[str] = set()

    # 1.5) Sitemap fetch (handles sitemapindex)
    def fetch_sitemap(u: str, depth: int = 0) -> None:
        if depth > 2:
            return
        fn = re.sub(r"[^a-zA-Z0-9_-]+", "_", urllib.parse.urlparse(u).path.strip("/")) or "sitemap_xml"
        cache_path = cache_dir / "sitemaps" / f"{fn}.xml"
        if cache_path.exists() and not refresh:
            xml_bytes = cache_path.read_bytes()
            sources.append(
                {
                    "kind": "sitemap",
                    "url": u,
                    "retrieved_at": "",
                    "status": 200,
                    "local_path": str(cache_path),
                    "note": "sitemap xml (cached)",
                }
            )
        else:
            fr = fetch_url(u)
            xml_bytes = fr.body
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            if xml_bytes:
                cache_path.write_bytes(xml_bytes)
            sources.append(
                {
                    "kind": "sitemap",
                    "url": u,
                    "retrieved_at": fr.fetched_at,
                    "status": fr.status,
                    "local_path": str(cache_path),
                    "note": "sitemap xml (may be sitemapindex or urlset)",
                }
            )
            sleep_polite(rate_limit_s)
        if not xml_bytes:
            return
        locs = parse_sitemap_xml(xml_bytes)
        if not locs:
            return
        # If sitemapindex, recurse; else it's urlset locs
        if any(x.endswith(".xml") for x in locs[: min(len(locs), 20)]):
            for sm in locs:
                fetch_sitemap(sm, depth + 1)
            return
        for loc in locs:
            if is_same_site(loc, base_netloc) and url_path_startswith(loc, blog_prefix):
                blog_urls.add(loc)

    for sm in sitemaps:
        fetch_sitemap(sm, 0)

    # 2) Crawl blog listing pages (pagination) to fill gaps + capture listing metadata if present
    listing_seen: Set[str] = set()
    listing_queue: List[str] = [blog_index]
    listing_meta_by_url: Dict[str, Dict[str, Any]] = {}
    pages_fetched = 0

    while listing_queue and pages_fetched < max_list_pages:
        u = listing_queue.pop(0)
        if u in listing_seen:
            continue
        listing_seen.add(u)
        pages_fetched += 1

        key = hashlib.sha256(u.encode("utf-8")).hexdigest()[:16]
        cache_path = cache_dir / "list_pages" / f"blog_list_{key}.html"
        meta_path = cache_dir / "list_pages" / f"blog_list_{key}.meta.json"
        if cache_path.exists() and not refresh:
            html = cache_path.read_text(encoding="utf-8", errors="replace")
            status = 200
            fetched_at = ""
            if meta_path.exists():
                try:
                    meta_obj = json.loads(meta_path.read_text(encoding="utf-8"))
                    status = safe_int(meta_obj.get("status"), status)
                    fetched_at = str(meta_obj.get("fetched_at") or "")
                except Exception:
                    pass
            sources.append(
                {
                    "kind": "blog_list",
                    "url": u,
                    "retrieved_at": fetched_at,
                    "status": status,
                    "local_path": str(cache_path),
                    "note": "blog listing page used for URL discovery (cached)",
                }
            )
        else:
            fr = fetch_url_with_retries(u, limiter=None, timeout_s=45, max_retries=3)
            status = fr.status
            fetched_at = fr.fetched_at
            html = fr.body.decode("utf-8", errors="replace") if fr.body else ""
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(html, encoding="utf-8")
            write_json(meta_path, {"url": u, "status": status, "fetched_at": fetched_at, "final_url": fr.final_url, "error": fr.error})
            sources.append(
                {
                    "kind": "blog_list",
                    "url": u,
                    "retrieved_at": fetched_at,
                    "status": status,
                    "local_path": str(cache_path),
                    "note": "blog listing page used for URL discovery",
                }
            )
            sleep_polite(rate_limit_s)

        if status < 200 or status >= 400 or not html:
            continue

        links = extract_links(html, u)
        for link in links:
            if not is_same_site(link, base_netloc):
                continue
            if url_path_startswith(link, blog_prefix) and link.rstrip("/") != blog_index.rstrip("/"):
                blog_urls.add(link)

        # pagination candidates: keep within blog root, include query ?page= or /page/
        for link in links:
            if not is_same_site(link, base_netloc):
                continue
            parsed = urllib.parse.urlparse(link)
            if not parsed.path.startswith(blog_root):
                continue
            if link == blog_index:
                continue
            if ("page=" in parsed.query) or ("/page/" in parsed.path) or (parsed.path.rstrip("/").endswith(blog_root)):
                if link not in listing_seen and link not in listing_queue:
                    listing_queue.append(link)

    # Assemble output list
    rows: List[Dict[str, Any]] = []
    now = utc_now_iso()
    for url in sorted(blog_urls):
        rows.append(
            {
                "url": url,
                "discovered_via": "sitemap_or_listing",
                "discovered_at": now,
                **listing_meta_by_url.get(url, {}),
            }
        )
    return rows, sources


def extract_internal_external_link_counts(html: str, page_url: str, base_netloc: str) -> Tuple[int, int, int, int]:
    links = extract_links(html, page_url)
    internal_links = 0
    external_links = 0
    internal_pricing = 0
    internal_tools = 0
    for u in links:
        p = urllib.parse.urlparse(u)
        if p.netloc == base_netloc:
            internal_links += 1
            if any(x in p.path.lower() for x in ("/pricing", "/price", "/plans")):
                internal_pricing += 1
            if any(x in p.path.lower() for x in ("/tool", "/tools", "/free", "/app", "/editor")):
                internal_tools += 1
        else:
            external_links += 1
    return internal_links, external_links, internal_pricing, internal_tools


def compute_aeo_features(html: str, text: str) -> Dict[str, Any]:
    lower = html.lower()
    text_lower = text.lower()
    jsonld = extract_jsonld_blocks(html)
    types: List[str] = []
    for b in jsonld:
        types.extend(flatten_jsonld_types(b))
    types_norm = [t.lower() for t in types]

    def heading_present(needle: str) -> bool:
        return bool(re.search(rf">\\s*{re.escape(needle)}\\s*<", lower))

    has_key_takeaways = ("key takeaways" in text_lower) or heading_present("key takeaways")
    has_tldr = ("tl;dr" in text_lower) or ("tldr" in text_lower)
    has_faq = ("faq" in text_lower) or ("frequently asked questions" in text_lower) or ("faqpage" in types_norm)

    schema_article = any(t in types_norm for t in ["article", "blogposting", "newsarticle"])
    schema_faq = "faqpage" in types_norm
    schema_howto = "howto" in types_norm

    h1_count = len(re.findall(r"<h1\\b", lower))
    h2_count = len(re.findall(r"<h2\\b", lower))
    toc_present = ("table of contents" in text_lower) or ("toc" in lower and "contents" in lower)

    word_count = len(re.findall(r"[A-Za-z0-9_]+", text))
    list_count = len(re.findall(r"<(ul|ol)\\b", lower))
    table_count = len(re.findall(r"<table\\b", lower))

    # Answer-first proxy: does the first 220 words contain a direct answer pattern?
    words = re.findall(r"[A-Za-z0-9_']+", text)
    first_220 = " ".join(words[:220]).lower()
    answer_markers = [
        "here are",
        "in this guide",
        "in this article",
        "the best",
        "you can",
        "we'll",
        "this post",
        "this guide will",
    ]
    answer_first_hits = sum(1 for m in answer_markers if m in first_220)
    answer_first_score = min(100, 35 + answer_first_hits * 10 + (10 if has_key_takeaways else 0))

    # CTA proxy: count common CTA strings
    cta_phrases = ["get started", "start for free", "try for free", "sign up", "free trial", "pricing", "create video"]
    cta_count = sum(text_lower.count(p) for p in cta_phrases)
    cta_count = min(cta_count, 50)

    aeo_score = 50
    aeo_score += 10 if has_key_takeaways else 0
    aeo_score += 7 if has_faq else 0
    aeo_score += 5 if schema_faq else 0
    aeo_score += 5 if schema_article else 0
    aeo_score += 3 if schema_howto else 0
    aeo_score += 5 if toc_present else 0
    aeo_score += 5 if (table_count + list_count) >= 3 else 0
    aeo_score += 5 if answer_first_score >= 60 else 0
    aeo_score = int(max(0, min(100, aeo_score)))

    return {
        "has_key_takeaways": has_key_takeaways,
        "has_tldr": has_tldr,
        "has_faq": has_faq,
        "schema_types": "|".join(types),
        "schema_article": schema_article,
        "schema_faqpage": schema_faq,
        "schema_howto": schema_howto,
        "h1_count": h1_count,
        "h2_count": h2_count,
        "toc_present": toc_present,
        "word_count": word_count,
        "list_count": list_count,
        "table_count": table_count,
        "answer_first_score": answer_first_score,
        "cta_count_proxy": cta_count,
        "aeo_score": aeo_score,
    }


def scrape_pricing_and_affiliate(base: str, out_dir: Path, rate_limit_s: float, refresh: bool) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Best-effort: fetch pricing + affiliate related pages and extract price points.
    """
    sources: List[Dict[str, Any]] = []
    candidates = [
        urllib.parse.urljoin(base, "/pricing"),
        urllib.parse.urljoin(base, "/price"),
        urllib.parse.urljoin(base, "/plans"),
        urllib.parse.urljoin(base, "/affiliate"),
        urllib.parse.urljoin(base, "/affiliates"),
        urllib.parse.urljoin(base, "/partners"),
        urllib.parse.urljoin(base, "/terms"),
        urllib.parse.urljoin(base, "/privacy"),
    ]

    extracted: Dict[str, Any] = {"pages": [], "prices_usd": [], "monthly_prices_usd": [], "plan_prices_usd": [], "affiliate_mentions": []}
    seen: Set[str] = set()
    for u in candidates:
        if u in seen:
            continue
        seen.add(u)
        slug = slug_from_url(u)
        cache_path = out_dir / "data" / "raw" / "site_pages" / f"{slug}.html"
        if cache_path.exists() and not refresh:
            html = cache_path.read_text(encoding="utf-8", errors="replace")
            status = 200
            fetched_at = ""
            sources.append(
                {
                    "kind": "site_page",
                    "url": u,
                    "retrieved_at": "",
                    "status": status,
                    "local_path": str(cache_path),
                    "note": "pricing/affiliate/terms pages for revenue model evidence (cached)",
                }
            )
        else:
            fr = fetch_url(u)
            status = fr.status
            fetched_at = fr.fetched_at
            html = fr.body.decode("utf-8", errors="replace") if fr.body else ""
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(html, encoding="utf-8")
            sources.append(
                {
                    "kind": "site_page",
                    "url": u,
                    "retrieved_at": fetched_at,
                    "status": status,
                    "local_path": str(cache_path),
                    "note": "pricing/affiliate/terms pages for revenue model evidence",
                }
            )
            sleep_polite(rate_limit_s)

        if status < 200 or status >= 400 or not html:
            extracted["pages"].append({"url": u, "status": status})
            continue

        extracted["pages"].append({"url": u, "status": status})

        # Pricing page pattern: strike-through original -> current monthly price -> "/month"
        # Example: ... line-through">$49</span> ... tracking-tighter">$19</span> ... <span>/</span>month
        if "/pricing" in u or "/plans" in u or u.rstrip("/").endswith("/price"):
            for m in re.finditer(
                r'line-through">\$(\d{1,4}(?:\.\d{2})?)</span>.*?tracking-tighter">\$(\d{1,4}(?:\.\d{2})?)</span>.*?month',
                html,
                flags=re.I | re.S,
            ):
                try:
                    extracted["plan_prices_usd"].append(float(m.group(2)))
                except Exception:
                    continue

        # Extract prices like $19, $19.99
        for m in re.finditer(r"\$(\d{1,4}(?:\.\d{2})?)", html):
            val = m.group(1)
            try:
                price = float(val)
                extracted["prices_usd"].append(price)
                # Heuristic: monthly recurring prices appear close to "/month" and are not the struck-through original price.
                ctx_before = html[max(0, m.start() - 80) : m.start()].lower()
                ctx_after = html[m.end() : m.end() + 80].lower()
                if "month" in ctx_after and "k/" not in ctx_after[:10] and "line-through" not in ctx_before:
                    extracted["monthly_prices_usd"].append(price)
            except Exception:
                continue
        # Affiliate mentions
        if "affiliate" in html.lower() or "commission" in html.lower() or "recurring" in html.lower():
            snippet = re.sub(r"\\s+", " ", html.lower())
            # keep small snippets
            m = re.search(r"(\d{1,2}%\s*(?:recurring\s*)?(?:commissions?|commission)(?:\s*for\s*life)?)", snippet)
            if m:
                extracted["affiliate_mentions"].append({"url": u, "match": m.group(1)})

    # Dedup prices (rounded)
    prices = sorted({round(p, 2) for p in extracted["prices_usd"] if p > 0})
    extracted["prices_usd"] = prices
    extracted["monthly_prices_usd"] = sorted({round(p, 2) for p in extracted["monthly_prices_usd"] if p > 0})
    extracted["plan_prices_usd"] = sorted({round(p, 2) for p in extracted["plan_prices_usd"] if p > 0})
    return extracted, sources


def collect_free_tools_urls(base: str, out_dir: Path, rate_limit_s: float, refresh: bool) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Best-effort inventory: crawl homepage + /tools-like pages, plus navigation links.
    """
    sources: List[Dict[str, Any]] = []
    base_netloc = urllib.parse.urlparse(base).netloc
    seeds = [
        base,
        urllib.parse.urljoin(base, "/tools"),
        urllib.parse.urljoin(base, "/free"),
        urllib.parse.urljoin(base, "/free-tools"),
        urllib.parse.urljoin(base, "/ai-tools"),
        urllib.parse.urljoin(base, "/products"),
        urllib.parse.urljoin(base, "/features"),
    ]
    seen_pages: Set[str] = set()
    queue: List[Tuple[str, int]] = [(u, 0) for u in seeds]
    urls: Set[str] = set()

    while queue:
        u, depth = queue.pop(0)
        if u in seen_pages or depth > 2:
            continue
        seen_pages.add(u)
        slug = slug_from_url(u)
        cache_path = out_dir / "data" / "raw" / "site_pages" / f"seed_{slug}.html"
        if cache_path.exists() and not refresh:
            html = cache_path.read_text(encoding="utf-8", errors="replace")
            status = 200
            fetched_at = ""
            sources.append(
                {
                    "kind": "site_seed_page",
                    "url": u,
                    "retrieved_at": "",
                    "status": status,
                    "local_path": str(cache_path),
                    "note": "seed pages used to discover free tools URLs (cached)",
                }
            )
        else:
            fr = fetch_url(u)
            status = fr.status
            fetched_at = fr.fetched_at
            html = fr.body.decode("utf-8", errors="replace") if fr.body else ""
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(html, encoding="utf-8")
            sources.append(
                {
                    "kind": "site_seed_page",
                    "url": u,
                    "retrieved_at": fetched_at,
                    "status": status,
                    "local_path": str(cache_path),
                    "note": "seed pages used to discover free tools URLs",
                }
            )
            sleep_polite(rate_limit_s)

        if status < 200 or status >= 400 or not html:
            continue

        links = extract_links(html, u)
        for link in links:
            if not is_same_site(link, base_netloc):
                continue
            p = urllib.parse.urlparse(link)
            path = p.path.lower()
            if any(seg in path for seg in ("/tool", "/tools", "/free", "/editor", "/app")) and not path.startswith("/blog"):
                urls.add(link)
            # add to crawl queue shallowly
            if depth < 2 and link not in seen_pages:
                if any(seg in path for seg in ("/tool", "/tools", "/free", "/features", "/products")):
                    queue.append((link, depth + 1))

    rows = [{"url": u, "discovered_via": "site_crawl", "discovered_at": utc_now_iso()} for u in sorted(urls)]
    return rows, sources


def collect_free_tools_from_sitemaps(cache_dir: Path, base: str) -> List[str]:
    """
    Parse cached sitemap XML files and return tool-like URLs.
    This captures Virvid's programmatic tool pages that may not be reachable via shallow nav crawling.
    """
    base_netloc = urllib.parse.urlparse(base).netloc
    sitemap_dir = cache_dir / "sitemaps"
    if not sitemap_dir.exists():
        return []

    deny_paths = {
        "/pricing",
        "/affiliate",
        "/contact",
        "/faq",
        "/terms",
        "/terms-of-service",
        "/privacy",
        "/privacy-policy",
    }
    out: Set[str] = set()

    for xml_path in sitemap_dir.glob("*.xml"):
        try:
            xml_bytes = xml_path.read_bytes()
        except Exception:
            continue
        locs = parse_sitemap_xml(xml_bytes)
        for loc in locs:
            if not is_same_site(loc, base_netloc):
                continue
            p = urllib.parse.urlparse(loc)
            path = p.path.lower().rstrip("/")
            if not path or path == "/":
                continue
            if path.startswith("/blog"):
                continue
            if any(path == d or path.startswith(d + "/") for d in deny_paths):
                continue
            if any(k in path for k in ("generator", "hook", "script", "tools", "tool", "template", "prompt")):
                out.add(loc)

    return sorted(out)


def dataforseo_call_with_cache(
    client: DataForSEOClient,
    endpoint: str,
    payload: List[Dict[str, Any]],
    cache_path: Path,
    refresh: bool,
) -> Dict[str, Any]:
    def cache_is_usable(obj: Dict[str, Any]) -> bool:
        if obj.get("status_code") != 20000:
            return False
        tasks = obj.get("tasks") or []
        if not tasks:
            return True
        for t in tasks:
            sc = t.get("status_code")
            if sc == 20000:
                continue
            msg = str(t.get("status_message") or "")
            # Don't retry access/plan issues; keep the cached response to avoid repeated charges.
            if "access denied" in msg.lower() or "activate your subscription" in msg.lower():
                return True
            return False
        return True

    if cache_path.exists() and not refresh:
        cached = read_json(cache_path)
        if cache_is_usable(cached):
            return cached
    resp = client.post(endpoint, payload)
    write_json(cache_path, resp)
    return resp


def dataforseo_extract_historical_traffic(resp: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Normalize DataForSEO historical_bulk_traffic_estimation response into:
      [{month: YYYY-MM, organic_etv: int, ...}]
    Tries multiple possible shapes.
    """
    out: List[Dict[str, Any]] = []
    if resp.get("status_code") != 20000:
        return out
    tasks = resp.get("tasks") or []
    for task in tasks:
        results = task.get("result") or []
        for r in results:
            # Common Labs shape:
            # r["items"] = [{"target":"virvid.ai","metrics":{"organic":[{year,month,etv,count}, ...]}}]
            items = r.get("items") or []
            if isinstance(items, dict):
                items = [items]
            if isinstance(items, list) and items and isinstance(items[0], dict) and isinstance((items[0].get("metrics") or {}).get("organic"), list):
                for site_item in items:
                    metrics = site_item.get("metrics") or {}
                    organic_hist = metrics.get("organic") or []
                    for it in organic_hist:
                        if not isinstance(it, dict):
                            continue
                        if "year" in it and "month" in it:
                            ym = f"{safe_int(it.get('year')):04d}-{safe_int(it.get('month')):02d}"
                            out.append({"month": ym, "organic_etv": safe_float(it.get("etv"))})
                continue

            # Fallback: flat list items with year/month/date fields
            alt_items = r.get("items") or r.get("history") or r.get("data") or []
            if isinstance(alt_items, dict):
                alt_items = [alt_items]
            if not isinstance(alt_items, list):
                continue
            for it in alt_items:
                if not isinstance(it, dict):
                    continue
                ym = None
                if "date" in it and isinstance(it["date"], str):
                    d = parse_date_any(it["date"])
                    if d:
                        ym = month_bucket(d)
                if not ym and "year" in it and "month" in it:
                    ym = f"{safe_int(it.get('year')):04d}-{safe_int(it.get('month')):02d}"
                if not ym:
                    continue
                organic = it.get("organic_etv") or it.get("etv") or it.get("organic_traffic") or it.get("traffic")
                out.append({"month": ym, "organic_etv": safe_float(organic)})
    # merge duplicates by month (max)
    by_m: Dict[str, float] = {}
    for row in out:
        m = row["month"]
        by_m[m] = max(by_m.get(m, 0.0), safe_float(row.get("organic_etv"), 0.0))
    merged = [{"month": m, "organic_etv": round(by_m[m], 2)} for m in sorted(by_m.keys())]
    return merged


def dataforseo_extract_relevant_pages(resp: Dict[str, Any]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    if resp.get("status_code") != 20000:
        return out
    for task in resp.get("tasks") or []:
        for r in task.get("result") or []:
            for item in (r.get("items") or []):
                if not isinstance(item, dict):
                    continue
                metrics = item.get("metrics") or {}
                organic = (metrics.get("organic") or {}) if isinstance(metrics, dict) else {}
                out.append(
                    {
                        "url": item.get("url") or item.get("page") or item.get("page_address") or item.get("target") or "",
                        "etv": round(safe_float(item.get("etv") or item.get("organic_etv") or organic.get("etv") or 0.0), 2),
                        "keywords": safe_int(item.get("keywords") or item.get("ranked_keywords") or organic.get("count") or 0),
                        "backlinks": safe_int(item.get("backlinks") or 0),
                        "ref_domains": safe_int(item.get("ref_domains") or item.get("referring_domains") or 0),
                    }
                )
    # drop blanks
    out = [r for r in out if r.get("url")]
    # unique by url (max etv)
    by_u: Dict[str, Dict[str, Any]] = {}
    for r in out:
        u = str(r["url"])
        if u not in by_u or safe_int(r.get("etv")) > safe_int(by_u[u].get("etv")):
            by_u[u] = r
    return sorted(by_u.values(), key=lambda x: safe_int(x.get("etv")), reverse=True)


def dataforseo_extract_bulk_traffic(resp: Dict[str, Any]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    if resp.get("status_code") != 20000:
        return out
    for task in resp.get("tasks") or []:
        for r in task.get("result") or []:
            for item in (r.get("items") or []):
                if not isinstance(item, dict):
                    continue
                url = item.get("url") or item.get("target") or ""
                if not url:
                    continue
                metrics = item.get("metrics") or {}
                organic = (metrics.get("organic") or {}) if isinstance(metrics, dict) else {}
                out.append(
                    {
                        "url": url,
                        "etv": round(safe_float(item.get("etv") or item.get("organic_etv") or organic.get("etv") or 0.0), 2),
                        "keywords": safe_int(item.get("keywords") or item.get("ranked_keywords") or organic.get("count") or 0),
                    }
                )
    # unique by url
    by_u: Dict[str, Dict[str, Any]] = {}
    for r in out:
        u = str(r["url"])
        if u not in by_u or safe_int(r.get("etv")) > safe_int(by_u[u].get("etv")):
            by_u[u] = r
    return sorted(by_u.values(), key=lambda x: safe_float(x.get("etv")), reverse=True)


def chunk_list(xs: List[str], size: int) -> List[List[str]]:
    return [xs[i : i + size] for i in range(0, len(xs), size)]


def dataforseo_extract_ranked_keywords(resp: Dict[str, Any]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    if resp.get("status_code") != 20000:
        return out
    for task in resp.get("tasks") or []:
        target = task.get("data", {}).get("target") or task.get("data", {}).get("url") or ""
        for r in task.get("result") or []:
            for item in (r.get("items") or []):
                if not isinstance(item, dict):
                    continue
                # Labs schema: {keyword_data:{keyword,keyword_info:{...}}, ranked_serp_element:{serp_item:{rank_absolute,url}}}
                kw_data = item.get("keyword_data") or {}
                kw_info = (kw_data.get("keyword_info") or {}) if isinstance(kw_data, dict) else {}
                ranked = item.get("ranked_serp_element") or {}
                serp_item = (ranked.get("serp_item") or {}) if isinstance(ranked, dict) else {}
                keyword = ""
                if isinstance(kw_data, dict):
                    keyword = kw_data.get("keyword") or ""
                out.append(
                    {
                        "target": target,
                        "keyword": keyword,
                        "position": safe_int(serp_item.get("rank_absolute") or serp_item.get("rank_group") or 0),
                        "search_volume": safe_int(kw_info.get("search_volume") or 0),
                        "cpc": safe_float(kw_info.get("cpc") or 0.0),
                        "url": serp_item.get("url") or "",
                    }
                )
    out = [r for r in out if r.get("keyword")]
    return out


def dataforseo_extract_llm_mentions_top_pages(resp: Dict[str, Any]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    if resp.get("status_code") != 20000:
        return out
    for task in resp.get("tasks") or []:
        for r in task.get("result") or []:
            for item in (r.get("items") or []):
                if not isinstance(item, dict):
                    continue
                out.append(
                    {
                        "url": item.get("url") or "",
                        "mentions": safe_int(item.get("mentions") or item.get("mention_count") or 0),
                        "model": item.get("model") or "",
                        "score": safe_float(item.get("score") or 0),
                    }
                )
    out = [r for r in out if r.get("url")]
    # unique by url
    by_u: Dict[str, Dict[str, Any]] = {}
    for r in out:
        u = str(r["url"])
        if u not in by_u or safe_int(r.get("mentions")) > safe_int(by_u[u].get("mentions")):
            by_u[u] = r
    return sorted(by_u.values(), key=lambda x: safe_int(x.get("mentions")), reverse=True)


def build_sources_index(sources: List[Dict[str, Any]], out_path: Path) -> List[Dict[str, Any]]:
    """
    Assign [S#] ids and write 99-sources.md.
    Returns sources with id.
    """
    enriched: List[Dict[str, Any]] = []
    for i, s in enumerate(sources, start=1):
        enriched.append({**s, "id": f"S{i}"})

    lines = ["# Sources\n", f"> Generated: {utc_now_iso()}\n", "\n"]
    for s in enriched:
        url = s.get("url", "")
        kind = s.get("kind", "")
        retrieved_at = s.get("retrieved_at", "")
        status = s.get("status", "")
        local_path = s.get("local_path", "")
        note = s.get("note", "")
        lines.append(f"- [{s['id']}] **{kind}** — {url}\n")
        lines.append(f"  - retrieved_at: `{retrieved_at}`; status: `{status}`\n")
        if local_path:
            lines.append(f"  - local_path: `{local_path}`\n")
        if note:
            lines.append(f"  - note: {note}\n")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("".join(lines), encoding="utf-8")
    return enriched


def sources_lookup(sources_with_id: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Map from URL to [S#] reference.
    """
    m: Dict[str, str] = {}
    for s in sources_with_id:
        url = str(s.get("url", ""))
        if url and url not in m:
            m[url] = f"[{s['id']}]"
    return m


def generate_reports(
    out_root: Path,
    report_name: str,
    domain_target: str,
    location_code: Optional[int],
    language_code: str,
    blog_prefix: str,
    sources_with_id: List[Dict[str, Any]],
    blog_inventory: List[Dict[str, Any]],
    aeo_rows: List[Dict[str, Any]],
    domain_traffic: List[Dict[str, Any]],
    relevant_pages: List[Dict[str, Any]],
    blog_traffic: List[Dict[str, Any]],
    tools_traffic: List[Dict[str, Any]],
    ranked_keywords: List[Dict[str, Any]],
    llm_mentions: List[Dict[str, Any]],
    pricing_affiliate: Dict[str, Any],
    window_since: dt.date,
    window_until: dt.date,
) -> None:
    src_by_url = sources_lookup(sources_with_id)

    domain_traffic = filter_month_rows(domain_traffic, window_since, window_until)
    domain_traffic = sorted(domain_traffic, key=lambda r: str(r.get("month") or ""))

    geo_short = geo_display(location_code, language_code)
    geo_long = geo_note(location_code, language_code)

    # Helpers
    title_by_url = {r.get("url", ""): r.get("title", "") for r in blog_inventory}

    # 00 executive summary
    curve_lines = []
    for r in domain_traffic:
        curve_lines.append(f"| {r['month']} | {safe_float(r.get('organic_etv')):,.2f} |")
    curve_table = "\n".join([f"| Month | Organic ETV ({geo_short}) |", "|---|---:|"] + curve_lines) if curve_lines else "_No DataForSEO historical traffic returned._"

    top_blog = sorted(blog_traffic, key=lambda x: safe_float(x.get("etv")), reverse=True)[:10]
    top_blog_lines = []
    for r in top_blog:
        top_blog_lines.append(f"| {r.get('url','')} | {safe_float(r.get('etv')):,.2f} | {safe_int(r.get('keywords')):,} |")
    top_blog_table = "\n".join(["| Blog URL | ETV | Keywords |", "|---|---:|---:|"] + top_blog_lines) if top_blog_lines else "_No blog URL traffic estimation available._"

    top_tools = sorted(tools_traffic, key=lambda x: safe_float(x.get("etv")), reverse=True)[:10]
    top_tools_lines = []
    for r in top_tools:
        top_tools_lines.append(f"| {r.get('url','')} | {safe_float(r.get('etv')):,.2f} | {safe_int(r.get('keywords')):,} |")
    top_tools_table = "\n".join(["| Tool URL | ETV | Keywords |", "|---|---:|---:|"] + top_tools_lines) if top_tools_lines else "_No tool URL traffic estimation available._"

    # Milestones: top MoM deltas
    milestones: List[Dict[str, Any]] = []
    if len(domain_traffic) >= 2:
        diffs = []
        for i in range(1, len(domain_traffic)):
            prev = safe_float(domain_traffic[i - 1].get("organic_etv"))
            cur = safe_float(domain_traffic[i].get("organic_etv"))
            diffs.append((abs(cur - prev), domain_traffic[i - 1]["month"], domain_traffic[i]["month"], cur - prev))
        diffs_sorted = sorted(diffs, reverse=True)[:2]
        for _, m0, m1, delta in diffs_sorted:
            milestones.append(
                {
                    "date": f"{m1}-01",
                    "type": "seo_inflection",
                    "source_url": "DataForSEO historical_bulk_traffic_estimation",
                    "evidence_note": f"Organic ETV change from {m0}→{m1}: {delta:+.2f}",
                }
            )
    # Content milestone: top blog post ETV
    if top_blog:
        milestones.append(
            {
                "date": window_until.isoformat(),
                "type": "top_blog_asset",
                "source_url": top_blog[0].get("url", ""),
                "evidence_note": f"Top blog page by estimated organic ETV: {safe_float(top_blog[0].get('etv')):,.2f}",
            }
        )
    # Product milestone: pricing/affiliate page fetched
    for p in pricing_affiliate.get("pages", []):
        u = p.get("url", "")
        if u and p.get("status") and ("/pricing" in u or "/affiliate" in u):
            milestones.append(
                {
                    "date": window_until.isoformat(),
                    "type": "pricing_affiliate_reference",
                    "source_url": u,
                    "evidence_note": "Pricing/Affiliate page snapshot collected (see sources).",
                }
            )
            break

    # Content cadence milestone (peak publish month inside window)
    publish_counts: Dict[str, int] = {}
    for r in blog_inventory:
        d = parse_date_any(str(r.get("published_date") or ""))
        if not d or not within_window(d, window_since, window_until):
            continue
        m = month_bucket(d)
        publish_counts[m] = publish_counts.get(m, 0) + 1
    if publish_counts:
        peak_month = max(publish_counts.items(), key=lambda x: x[1])[0]
        milestones.append(
            {
                "date": f"{peak_month}-01",
                "type": "content_cadence_peak",
                "source_url": "url_inventory_blog.csv",
                "evidence_note": f"Peak blog publishing month in window: {peak_month} ({publish_counts[peak_month]} posts).",
            }
        )

    # Write milestones csv
    ms_path = out_root / "data" / "milestones_timeline.csv"
    write_csv(ms_path, milestones, fieldnames=["date", "type", "source_url", "evidence_note"])

    # Core sources references
    s_dataforseo_hist = None
    for s in sources_with_id:
        if s.get("kind") == "dataforseo" and "historical_bulk_traffic" in str(s.get("note", "")):
            s_dataforseo_hist = f"[{s['id']}]"
            break
    if not s_dataforseo_hist:
        s_dataforseo_hist = "[S?]"

    s_dataforseo_relevant = None
    for s in sources_with_id:
        if s.get("kind") == "dataforseo" and "relevant_pages" in str(s.get("note", "")):
            s_dataforseo_relevant = f"[{s['id']}]"
            break
    if not s_dataforseo_relevant:
        s_dataforseo_relevant = "[S?]"

    # 00-executive-summary.md
    exec_md = f"""# {report_name} 竞品研究（流量 + SEO/AEO）— 执行摘要

> 覆盖时间窗（自然月汇总）: **{window_since.isoformat()} ~ {window_until.isoformat()}**
> 口径: **{geo_long}**；访问量/收入为第三方估算区间（不等同 GA/GSC）。

## Key Takeaways
- 域名 SEO 流量（Organic ETV）近 6 个月曲线已落盘，可复跑更新 {s_dataforseo_hist}
- Blog 侧可按 URL 维度估算“当前 organic 贡献”，并按 AEO 特征（Key Takeaways/FAQ/schema/Answer-first）做结构化评分（见 `data/aeo_features_blog.csv`）。
- 收入与用户规模未公开披露：本报告用“SEO ETV → 总访问量区间 → 漏斗假设 → MRR 区间”模型，所有假设均显式写入 `data/revenue_model_inputs.json`（可调整）。
- 里程碑（SEO 拐点/Top 内容资产/商业页面变更）已输出到 `data/milestones_timeline.csv`，便于你做季度复盘与竞品对比。

## TL;DR Answer
{report_name} 的公开数据不足以直接得到“真实访问量/收入”，但我们可以用 DataForSEO Labs 的域名/页面级 organic 估算把 **SEO 增长曲线、博客内容资产的贡献分布、AEO 结构成熟度** 定量化；再用透明的漏斗假设把“访问量/付费/收入”变成可调整的区间模型，支持你在 30 分钟内复跑并更新近 6 个月的关键指标。

## 近 6 个月 SEO 曲线（Organic ETV）
{curve_table}

## Blog Top 内容资产（按 URL 的 organic ETV 估算）
{top_blog_table}

## Tools Top 资产（按 URL 的 organic ETV 估算）
{top_tools_table}

## 里程碑（近 6 个月）
详见 `data/milestones_timeline.csv`（SEO 拐点 + 内容资产 + 商业页面参考）。

## FAQ
### 1) 为什么这里的“访问量/收入”不是精确值？
因为 {report_name} 未公开 GA/GSC/财务披露；本报告采用第三方工具的 SEO 可见度估算 + 明示的漏斗假设，输出区间而非伪精确。

### 2) AEO 表现怎么评估？
以“答案前置 + 结构化块（Key Takeaways/TL;DR/FAQ）+ schema + 可引用结构（表格/列表）+ 内链/CTA”做特征抽取与评分，落到 `data/aeo_features_blog.csv`。

"""
    (out_root / "00-executive-summary.md").write_text(exec_md, encoding="utf-8")

    # 01-traffic-and-users.md (estimation)
    # Compute total visits range using organic shares
    shares = [0.30, 0.45, 0.60]
    sessions_per_user = list(DEFAULT_SESSIONS_PER_USER)
    rows_est = []
    for r in domain_traffic:
        organic = safe_float(r.get("organic_etv"))
        totals = [int(organic / s) if s > 0 else 0 for s in shares]
        totals_min = min(totals) if totals else 0
        totals_max = max(totals) if totals else 0
        spu_min = min(sessions_per_user) if sessions_per_user else 1.0
        spu_max = max(sessions_per_user) if sessions_per_user else 1.0
        users_min = int(totals_min / spu_max) if spu_max > 0 else 0
        users_max = int(totals_max / spu_min) if spu_min > 0 else 0
        rows_est.append(
            {
                "month": r["month"],
                "organic_etv": organic,
                "total_visits_min": totals_min,
                "total_visits_max": totals_max,
                "total_users_min": users_min,
                "total_users_max": users_max,
            }
        )
    lines = []
    for r in rows_est:
        lines.append(
            f"| {r['month']} | {r['organic_etv']:,.2f} | {r['total_visits_min']:,} | {r['total_visits_max']:,} | {r['total_users_min']:,} | {r['total_users_max']:,} |"
        )
    table = (
        "\n".join(
            ["| Month | Organic ETV | Total Visits (min) | Total Visits (max) | Total Users (min) | Total Users (max) |", "|---|---:|---:|---:|---:|---:|"]
            + lines
        )
        if lines
        else "_No domain traffic data._"
    )

    s_sources = s_dataforseo_hist
    traffic_md = f"""# 访问量与用户规模（估算）

> 口径：以 DataForSEO 的 **Organic ETV（月）** 为底座，推导“总访问量区间”。
> 假设：Organic 占总访问比例分别取 **30% / 45% / 60%** 三档（区间输出不宣称为真实值）。
> 用户估算：以 `users = visits / sessions_per_user` 推导，sessions/user 取 **{"/".join([str(x) for x in sessions_per_user])}** 三档（同样为假设）。

## Key Takeaways
- 该部分输出的是**可解释的区间估算**：只要你后续拿到 GA/GSC，就可以把这里的假设替换为真实数据。
- 若 {report_name} 的 Direct/Referral 占比很高（例如强品牌/强分销），则总访问量可能显著高于此区间；该不确定性在此明确保留为“证据缺口”。

## 近 6 个月总访问量区间（由 Organic ETV 推导）
{table}

## 置信度与证据缺口
- 置信度：中（SEO 可见度估算相对稳定，但“Organic 占比”不可验证）
- 证据缺口：{report_name} 未公开 GA/GSC；若你能提供 GA4/GSC 导出，可把该部分升级为真实口径。

## Sources
- DataForSEO historical bulk traffic estimation {s_sources}
"""
    (out_root / "01-traffic-and-users.md").write_text(traffic_md, encoding="utf-8")

    # 02-revenue-model.md + inputs json
    # Use pricing extraction (best-effort). If missing, use defaults and flag.
    default_plans = [
        {"name": "Starter", "monthly_price_usd": 19.0},
        {"name": "Creator", "monthly_price_usd": 39.0},
        {"name": "Business", "monthly_price_usd": 99.0},
    ]

    def plausible_monthly_prices(prices: Sequence[Any]) -> List[float]:
        out: List[float] = []
        for x in prices:
            try:
                p = float(x)
            except Exception:
                continue
            # Heuristic bounds to avoid pulling in "save $900" / enterprise banners / non-price numerals.
            if 3.0 <= p <= 300.0:
                out.append(p)
        return sorted({round(p, 2) for p in out})

    raw_plan = pricing_affiliate.get("plan_prices_usd") or []
    raw_monthly = pricing_affiliate.get("monthly_prices_usd") or []
    raw_all = pricing_affiliate.get("prices_usd") or []

    extracted_prices = plausible_monthly_prices(list(raw_plan) + list(raw_monthly))
    if not extracted_prices:
        extracted_prices = plausible_monthly_prices(raw_all)

    plans = default_plans
    note_pricing = ""
    if extracted_prices:
        prices_sorted = sorted(float(x) for x in extracted_prices)
        if len(prices_sorted) >= 3:
            reps = [prices_sorted[0], prices_sorted[len(prices_sorted) // 2], prices_sorted[-1]]
        elif len(prices_sorted) == 2:
            reps = [prices_sorted[0], prices_sorted[1], prices_sorted[1]]
        else:
            reps = [prices_sorted[0], prices_sorted[0], prices_sorted[0]]

        if reps:
            plans = [
                {"name": "Starter", "monthly_price_usd": reps[0]},
                {"name": "Creator", "monthly_price_usd": reps[1]},
                {"name": "Business", "monthly_price_usd": reps[2]},
            ]
            note_pricing = (
                "Pricing 从站内页面抓取到 `$` 数值（可能包含年付/折扣/文案数字），并做了“月付价格合理区间”过滤（3~300 USD）。"
                "因此此处仅作近似参考；建议用人工核对 pricing 页面后修正。"
            )
    else:
        note_pricing = "未能从公开页面稳定抽取到定价数字（可能为 JS 渲染/非 `$` 文案）。此处使用默认 SaaS 套餐价格占位，并明确为假设。"

    revenue_inputs = {
        "generated_at": utc_now_iso(),
        "window": {"since": window_since.isoformat(), "until": window_until.isoformat()},
        "traffic_to_total_assumptions": {
            "organic_share_scenarios": shares,
            "sessions_per_user_scenarios": sessions_per_user,
            "note": "Used to convert Organic ETV → total visits/users ranges; replace with GA/GSC when available.",
        },
        "plans": plans,
        "affiliate_commission_assumption": {"rate_recurring": 0.30, "note": "Only if affiliate program exists; verify on affiliate/partners page."},
        "traffic_to_paid_scenarios": [
            {"name": "A_conservative", "visit_to_paid_rate": 0.0005, "paid_mix": {"Starter": 0.60, "Creator": 0.35, "Business": 0.05}},
            {"name": "B_base", "visit_to_paid_rate": 0.0012, "paid_mix": {"Starter": 0.45, "Creator": 0.45, "Business": 0.10}},
            {"name": "C_optimistic", "visit_to_paid_rate": 0.0025, "paid_mix": {"Starter": 0.35, "Creator": 0.50, "Business": 0.15}},
        ],
        "notes": {
            "pricing_extraction": note_pricing,
            "warning": "This is an estimation model; not a financial disclosure.",
        },
    }
    write_json(out_root / "data" / "revenue_model_inputs.json", revenue_inputs)

    def arpu_from_mix(mix: Dict[str, float]) -> float:
        price_map = {p["name"]: float(p["monthly_price_usd"]) for p in plans}
        return sum(price_map.get(k, 0.0) * float(v) for k, v in mix.items())

    # use the last month total visits max as base; if missing, use 0
    last_month = rows_est[-1] if rows_est else {"total_visits_min": 0, "total_visits_max": 0, "month": ""}
    visits_mid = int((safe_int(last_month["total_visits_min"]) + safe_int(last_month["total_visits_max"])) / 2) if rows_est else 0

    scenarios_out = []
    for sc in revenue_inputs["traffic_to_paid_scenarios"]:
        arpu = arpu_from_mix(sc["paid_mix"])
        paid = int(visits_mid * float(sc["visit_to_paid_rate"]))
        mrr = paid * arpu
        scenarios_out.append(
            {"scenario": sc["name"], "visits_mid": visits_mid, "visit_to_paid_rate": sc["visit_to_paid_rate"], "est_paid_users": paid, "arpu": arpu, "est_mrr": mrr}
        )

    lines = []
    for r in scenarios_out:
        lines.append(f"| {r['scenario']} | {r['visits_mid']:,} | {r['visit_to_paid_rate']:.4%} | {r['est_paid_users']:,} | ${r['arpu']:.2f} | ${r['est_mrr']:,.0f} |")
    scenario_table = "\n".join(["| Scenario | Visits (mid) | Visit→Paid | Paid Users | ARPU | Est. MRR |", "|---|---:|---:|---:|---:|---:|"] + lines)

    pricing_page_lines = "\n".join(
        [f"- {p.get('url','')} (status {p.get('status','')})" for p in pricing_affiliate.get("pages", [])]
    ).strip()
    if not pricing_page_lines:
        pricing_page_lines = "_No pricing/affiliate pages captured._"

    revenue_md = f"""# 收入情况（区间模型）

> 该部分为“可解释的区间模型”，不是财务披露。所有假设与参数均写入 `data/revenue_model_inputs.json`。

## Key Takeaways
- 只要你后续拿到真实的“访问量、注册、付费转化、ARPU”，就可以替换该模型的假设，快速得到更可靠的 MRR/ARR。
- 定价提取为 best-effort：{note_pricing}

## 定价与商业页面证据（公开页面）
{pricing_page_lines}

## MRR 估算（基于访问量中位数与 Visit→Paid 假设）
{scenario_table}

## 置信度与证据缺口
- 置信度：低~中（取决于定价页是否可稳定解析、以及真实转化率与渠道结构）
- 证据缺口：真实付费用户数、套餐结构、年付折扣、渠道占比、churn。

"""
    (out_root / "02-revenue-model.md").write_text(revenue_md, encoding="utf-8")

    # 03-seo-search-traffic.md
    top_pages = relevant_pages[:30]
    lines = []
    for r in top_pages:
        lines.append(f"| {r.get('url','')} | {safe_float(r.get('etv')):,.2f} | {safe_int(r.get('keywords')):,} | {safe_int(r.get('backlinks')):,} |")
    top_pages_table = "\n".join(["| URL | ETV | Keywords | Backlinks |", "|---|---:|---:|---:|"] + lines) if lines else "_No relevant_pages data._"

    # Relevant pages breakdown: blog vs tools
    blog_rp = [r for r in relevant_pages if url_path_startswith(str(r.get("url", "")), blog_prefix)]
    tool_rp = [r for r in relevant_pages if r.get("url") and not url_path_startswith(str(r.get("url", "")), blog_prefix)]
    etv_total = sum(safe_float(r.get("etv")) for r in relevant_pages) if relevant_pages else 0.0
    etv_blog = sum(safe_float(r.get("etv")) for r in blog_rp) if blog_rp else 0.0
    etv_tools = sum(safe_float(r.get("etv")) for r in tool_rp) if tool_rp else 0.0
    rp_breakdown = f"- Relevant pages: {len(relevant_pages)} total; blog={len(blog_rp)}, tools/landing={len(tool_rp)}\n"
    rp_breakdown += f"- ETV split (sum): blog={etv_blog:,.2f}, tools/landing={etv_tools:,.2f}, total={etv_total:,.2f}\n"

    # Tools URL-level bulk estimation table (separate from relevant_pages)
    top_tools_rows = sorted(tools_traffic, key=lambda x: safe_float(x.get("etv")), reverse=True)[:15]
    tlines = []
    for r in top_tools_rows:
        tlines.append(f"| {r.get('url','')} | {safe_float(r.get('etv')):,.2f} | {safe_int(r.get('keywords')):,} |")
    tools_table = "\n".join(["| Tool URL | ETV | Keywords |", "|---|---:|---:|"] + tlines) if tlines else "_No tools URL traffic estimation available._"

    llm_top = llm_mentions[:20]
    llm_lines = []
    for r in llm_top:
        llm_lines.append(f"| {r.get('url','')} | {safe_int(r.get('mentions')):,} | {r.get('model','')} | {safe_float(r.get('score')):.2f} |")
    llm_table = "\n".join(["| URL | Mentions | Model | Score |", "|---|---:|---|---:|"] + llm_lines) if llm_lines else "_LLM mentions data not available (API may be disabled/unsupported)._"

    # Trend note from domain traffic curve (data-driven, avoid hard-coded month claims)
    trend_note = "域名级别的 organic ETV 数据缺失，无法做趋势解读。"
    if domain_traffic:
        start_m = str(domain_traffic[0].get("month") or "")
        end_m = str(domain_traffic[-1].get("month") or "")
        start_etv = safe_float(domain_traffic[0].get("organic_etv"))
        end_etv = safe_float(domain_traffic[-1].get("organic_etv"))
        nonzero_months = [r for r in domain_traffic if safe_float(r.get("organic_etv")) > 0.0]
        if start_etv <= 0.0 and nonzero_months:
            first_nz = nonzero_months[0]
            trend_note = f"该域名在 {geo_short} 的 SEO 可见度在本时间窗内从 **{first_nz.get('month')}** 开始出现非零 organic ETV，并在 **{end_m}** 达到 **{end_etv:,.2f}**（ETV 为第三方估算）。{s_dataforseo_hist}"
        else:
            delta = end_etv - start_etv
            pct = (delta / start_etv * 100.0) if start_etv > 0 else 0.0
            trend_note = f"近 6 个月在 {geo_short} 的 organic ETV 从 **{start_m} 的 {start_etv:,.2f}** 变化到 **{end_m} 的 {end_etv:,.2f}**（Δ {delta:+,.2f}, {pct:+.1f}%；ETV 为第三方估算）。{s_dataforseo_hist}"

    seo_md = f"""# SEO 搜索引擎流量与相关数据（{geo_short}）

## Key Takeaways
- 域名级别的 organic ETV 曲线（近 6 个月）见 `data/dataforseo_domain_traffic_6m.csv` {s_dataforseo_hist}
- Relevant pages 能快速定位“对自然搜索最关键的页面资产”（不等同全量站点 URL），见 `data/dataforseo_pages_relevant.csv`。
- Blog URL 级别可做 bulk traffic estimation（现状贡献），见 `data/dataforseo_blog_url_traffic.csv`。

## 近 6 个月趋势解读（结论）
- {trend_note}
- 当前 SEO 贡献更偏向“程序化工具页（script/hook/generator）+ 少量 blog 文章”的组合；这类结构通常用于覆盖大量长尾意图（快速起量、但需要持续内容质量与内链把权重导向核心转化页）。{s_dataforseo_relevant}

## Relevant Pages 结构拆分（blog vs tools）
{rp_breakdown}

## Relevant Pages（Top 30）
{top_pages_table}

## Tools URL 级别估算（Top 15）
{tools_table}

## LLM Mentions Top Pages（可选）
{llm_table}

## Notes
- 这里的 ETV 为第三方估算指标，用于趋势与相对排序（不要当作 GA 的精确 visits）。
"""
    (out_root / "03-seo-search-traffic.md").write_text(seo_md, encoding="utf-8")

    # 04-blog-performance-aeo.md
    # Join AEO rows with traffic
    traffic_by_url = {r["url"]: r for r in blog_traffic}
    llm_by_url = {r["url"]: r for r in llm_mentions}
    combined = []
    for r in aeo_rows:
        u = r["url"]
        t = traffic_by_url.get(u, {})
        lm = llm_by_url.get(u, {})
        combined.append({**r, "etv": safe_float(t.get("etv")), "keywords": safe_int(t.get("keywords")), "llm_mentions": safe_int(lm.get("mentions")), "llm_score": safe_float(lm.get("score"))})
    combined_sorted = sorted(combined, key=lambda x: (safe_float(x.get("etv")), safe_int(x.get("aeo_score"))), reverse=True)
    top = combined_sorted[:20]
    lines = []
    for r in top:
        lines.append(
            f"| {r.get('url','')} | {safe_float(r.get('etv')):,.2f} | {safe_int(r.get('aeo_score'))} | {safe_int(r.get('word_count')):,} | {('Y' if r.get('has_key_takeaways') else 'N')} | {('Y' if r.get('has_faq') else 'N')} |"
        )
    top_table = "\n".join(
        ["| URL | ETV | AEO | Words | Key Takeaways | FAQ |", "|---|---:|---:|---:|:--:|:--:|"] + lines
    ) if lines else "_No AEO feature extraction output._"

    # Aggregate AEO stats
    n = len(aeo_rows)
    if n:
        pct = lambda k: (sum(1 for r in aeo_rows if str(r.get(k)) == "True" or r.get(k) is True) / n) * 100.0
        avg_words = sum(safe_int(r.get("word_count")) for r in aeo_rows) / n
        avg_aeo = sum(safe_int(r.get("aeo_score")) for r in aeo_rows) / n
        takeaways_pct = pct("has_key_takeaways")
        faq_pct = pct("has_faq")
        toc_pct = pct("toc_present")
        schema_any = sum(1 for r in aeo_rows if (str(r.get("schema_types") or "").strip() != "")) / n * 100.0
        agg_lines = [
            f"- Blog pages analyzed: **{n}** (snapshotted).",
            f"- Avg word count: **{avg_words:,.0f}**; Avg AEO score: **{avg_aeo:.1f}/100**.",
            f"- Key Takeaways coverage: **{takeaways_pct:.1f}%**; FAQ coverage: **{faq_pct:.1f}%**; TOC presence: **{toc_pct:.1f}%**.",
            f"- JSON-LD schema detected (any type): **{schema_any:.1f}%** (if low, may be missing schema or rendered client-side).",
        ]
        agg_block = "\n".join(agg_lines)
    else:
        agg_block = "_No AEO stats available._"

    # Title pattern scan (very lightweight)
    patterns = {
        "how_to": re.compile(r"\bhow to\b", re.I),
        "vs": re.compile(r"\bvs\b|\bversus\b", re.I),
        "free": re.compile(r"\bfree\b", re.I),
        "templates": re.compile(r"\btemplates?\b", re.I),
        "ideas": re.compile(r"\bideas\b", re.I),
        "monetize": re.compile(r"\bmonetiz", re.I),
    }
    pattern_counts: Dict[str, int] = {k: 0 for k in patterns}
    for u in title_by_url:
        t = title_by_url.get(u) or ""
        for k, rx in patterns.items():
            if rx.search(t):
                pattern_counts[k] += 1
    pattern_summary = "\n".join([f"- {k}: {v}" for k, v in sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)])

    # Top by AEO (not traffic)
    by_aeo = sorted(combined, key=lambda x: safe_int(x.get("aeo_score")), reverse=True)[:10]
    aeo_lines = []
    for r in by_aeo:
        aeo_lines.append(f"| {r.get('url','')} | {safe_int(r.get('aeo_score'))} | {safe_int(r.get('word_count')):,} | {title_by_url.get(r.get('url',''), '')} |")
    aeo_table = "\n".join(["| URL | AEO | Words | Title |", "|---|---:|---:|---|"] + aeo_lines) if aeo_lines else "_No AEO ranking available._"

    blog_md = f"""# Blog 流量表现与 AEO 结构评估

## Key Takeaways
- Blog 页面按 URL 的 organic 贡献（ETV）可用于识别“真正带来搜索流量的文章资产”（而不是只看发布频率）。
- AEO 结构成熟度可以通过 Key Takeaways/FAQ/schema/Answer-first 等特征抽取做量化对比，形成可复制的写作模板与改造清单。

## Blog AEO 概况（量化）
{agg_block}

## 标题与选题模式（粗粒度统计）
{pattern_summary}

## Top Blog Posts（ETV × AEO 综合排序，Top 20）
{top_table}

## Top Posts by AEO Score（不看流量，只看结构）
{aeo_table}

## 输出文件索引
- Blog URL 清单：`data/url_inventory_blog.csv`
- Blog URL → traffic estimation：`data/dataforseo_blog_url_traffic.csv`
- Blog AEO 特征与评分：`data/aeo_features_blog.csv`

"""
    (out_root / "04-blog-performance-aeo.md").write_text(blog_md, encoding="utf-8")

    # 05-milestones-last-6-months.md
    ms_lines = []
    for m in milestones:
        ms_lines.append(f"- **{m.get('date','')}** `{m.get('type','')}` — {m.get('evidence_note','')} ({m.get('source_url','')})")
    milestones_md = f"""# 近 6 个月里程碑（可验证）

> 输出 CSV：`data/milestones_timeline.csv`

## Milestones
{os.linesep.join(ms_lines) if ms_lines else '_No milestones produced (missing upstream data)._'}

## 说明
- SEO 拐点来自域名级 monthly organic ETV 的环比变化（取绝对值 Top 2）。
- 内容资产里程碑以 blog URL 的 current ETV 估算 Top 1/Top N 作为线索。
- 商业页面里程碑目前仅做“采集到公开页面快照”的引用点；如需更精确（例如价格变更日期），需要历史快照或 Wayback/公开公告。
"""
    (out_root / "05-milestones-last-6-months.md").write_text(milestones_md, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default=DEFAULT_NAME, help="Display name used in report headings")
    ap.add_argument("--base", default=DEFAULT_BASE)
    ap.add_argument("--blog", default=DEFAULT_BLOG)
    ap.add_argument("--domain-target", default="", help="Domain target for DataForSEO (default: derived from --base, without www.)")
    ap.add_argument("--out-dir", default=str(Path("research 竞品分析/virvid-ai")))
    ap.add_argument("--since", default=TIME_WINDOW_SINCE.isoformat())
    ap.add_argument("--until", default=TIME_WINDOW_UNTIL.isoformat())
    ap.add_argument("--geo", default="", help="Shortcut: global-en or us-en. If set, overrides --location-code/--language-code.")
    ap.add_argument("--language-code", default=EN_LANGUAGE_CODE)
    ap.add_argument("--location-code", type=parse_optional_int, default=US_LOCATION_CODE, help="DataForSEO location_code. Use 'none' to omit (Global).")
    ap.add_argument("--rate-limit-seconds", type=float, default=0.9)
    ap.add_argument("--workers", type=int, default=1, help="Crawler worker threads for blog snapshots (default: 1)")
    ap.add_argument("--max-list-pages", type=int, default=20)
    ap.add_argument("--max-posts", type=int, default=0, help="0 means no limit")
    ap.add_argument("--dry-run", action="store_true", help="Fetch only a few pages and skip expensive steps")
    ap.add_argument("--refresh", action="store_true", help="Re-fetch site pages even if cached")
    ap.add_argument("--refresh-dataforseo", action="store_true", help="Re-call DataForSEO even if cached")
    ap.add_argument("--skip-dataforseo", action="store_true")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    out_root = Path(args.out_dir)
    out_root.mkdir(parents=True, exist_ok=True)
    (out_root / "data" / "raw" / "dataforseo").mkdir(parents=True, exist_ok=True)
    (out_root / "data" / "raw" / "site_pages").mkdir(parents=True, exist_ok=True)
    (out_root / "snapshots" / "html").mkdir(parents=True, exist_ok=True)
    (out_root / "snapshots" / "text").mkdir(parents=True, exist_ok=True)
    (out_root / "snapshots" / "meta").mkdir(parents=True, exist_ok=True)

    since = dt.date.fromisoformat(args.since)
    until = dt.date.fromisoformat(args.until)

    # Determine DataForSEO target + geo
    report_name = str(args.name or "").strip() or derive_domain_target(args.base)
    domain_target = str(args.domain_target or "").strip() or derive_domain_target(args.base)
    language_code = str(args.language_code or "").strip() or EN_LANGUAGE_CODE
    location_code: Optional[int] = args.location_code if args.location_code is not None else None

    argv = sys.argv[1:]
    if args.geo:
        g = str(args.geo).strip().lower()
        if g in {"global-en", "global"}:
            location_code = None
            language_code = "en"
        elif g in {"us-en", "us"}:
            location_code = US_LOCATION_CODE
            language_code = "en"
        else:
            raise SystemExit(f"Unsupported --geo: {args.geo} (expected global-en or us-en)")
    else:
        # If caller explicitly sets language but doesn't set location, interpret as Global/en by default.
        # This preserves existing behavior for legacy runs that never passed --language-code.
        if "--language-code" in argv and "--location-code" not in argv:
            location_code = None

    cache_dir = out_root / "data" / "raw" / "crawl_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)

    _blog_root, blog_prefix = blog_root_and_prefix(args.blog)

    sources: List[Dict[str, Any]] = []

    # Load prior manifest mapping (for re-runs without --refresh)
    manifest_path = out_root / "data" / "snapshots_manifest.jsonl"
    prior_manifest: Dict[str, Dict[str, Any]] = {}
    if manifest_path.exists() and not args.refresh:
        for row in read_jsonl(manifest_path):
            u = str(row.get("url", ""))
            if u:
                prior_manifest[u] = row

    # URL discovery
    blog_rows, discovery_sources = discover_blog_urls(
        base=args.base,
        blog_index=args.blog,
        rate_limit_s=args.rate_limit_seconds,
        max_list_pages=(3 if args.dry_run else args.max_list_pages),
        refresh=args.refresh,
        cache_dir=cache_dir,
    )
    sources.extend(discovery_sources)

    # Free tools inventory (best-effort)
    tools_rows, tools_sources = collect_free_tools_urls(
        base=args.base,
        out_dir=out_root,
        rate_limit_s=args.rate_limit_seconds,
        refresh=args.refresh,
    )
    sources.extend(tools_sources)

    # Enrich with programmatic tool pages from sitemap cache
    tool_sitemap_urls = collect_free_tools_from_sitemaps(cache_dir=cache_dir, base=args.base)
    for u in tool_sitemap_urls:
        tools_rows.append({"url": u, "discovered_via": "sitemap", "discovered_at": utc_now_iso()})
    # de-dup
    seen_tools: Set[str] = set()
    uniq_tools: List[Dict[str, Any]] = []
    for r in tools_rows:
        u = str(r.get("url") or "")
        if not u or u in seen_tools:
            continue
        seen_tools.add(u)
        uniq_tools.append(r)
    tools_rows = uniq_tools

    write_csv(out_root / "data" / "url_inventory_free_tools.csv", tools_rows, fieldnames=["url", "discovered_via", "discovered_at"])

    # Pricing/affiliate pages
    pricing_affiliate, pa_sources = scrape_pricing_and_affiliate(
        base=args.base,
        out_dir=out_root,
        rate_limit_s=args.rate_limit_seconds,
        refresh=args.refresh,
    )
    sources.extend(pa_sources)
    write_json(out_root / "data" / "raw" / "pricing_affiliate_extract.json", pricing_affiliate)

    # Fetch blog posts and snapshot
    base_netloc = urllib.parse.urlparse(args.base).netloc
    blog_inventory: List[Dict[str, Any]] = []
    manifest_rows: List[Dict[str, Any]] = []
    aeo_rows: List[Dict[str, Any]] = []

    urls = [r["url"] for r in blog_rows]
    if args.dry_run:
        urls = urls[:3]
    elif args.max_posts and args.max_posts > 0:
        urls = urls[: args.max_posts]

    limiter = RateLimiter(args.rate_limit_seconds)
    workers = max(1, int(args.workers or 1))

    def process_one(idx_url: Tuple[int, str]) -> Tuple[int, Dict[str, Any], Dict[str, Any], Optional[Dict[str, Any]]]:
        idx, url = idx_url
        cached = prior_manifest.get(url) if not args.refresh else None
        cached_html_path = Path(str(cached["html_path"])) if (cached and cached.get("html_path")) else None
        cached_status = safe_int(cached.get("status"), 0) if cached else 0
        cached_text_path = Path(str(cached.get("text_path", ""))) if (cached and cached.get("text_path")) else None
        cached_meta_path = Path(str(cached.get("meta_path", ""))) if (cached and cached.get("meta_path")) else None

        did_fetch = False
        if cached_html_path and cached_html_path.exists() and cached_html_path.stat().st_size > 0 and 200 <= cached_status < 400:
            body = cached_html_path.read_bytes()
            status = cached_status
            fetched_at = str(cached.get("fetched_at") or "")
            fr = FetchResult(
                url=url,
                status=status,
                final_url=url,
                fetched_at=fetched_at,
                content_type="",
                body=body,
                error=str(cached.get("error") or ""),
            )
            content_hash = str(cached.get("sha256") or sha256_bytes(body))
            html_path = cached_html_path
        else:
            did_fetch = True
            fr = fetch_url_with_retries(url, limiter=limiter, timeout_s=45, max_retries=3)
            content_hash = sha256_bytes(fr.body) if fr.body else ""
            html = fr.body.decode("utf-8", errors="replace") if fr.body else ""

            jsonld = extract_jsonld_blocks(html) if html else []
            meta = extract_meta(html) if html else {}
            published = extract_published_date(html, meta, jsonld) if html else None
            mb = month_bucket(published)
            slug = slug_from_url(url)

            html_path = out_root / "snapshots" / "html" / mb / f"{slug}.html"
            html_path.parent.mkdir(parents=True, exist_ok=True)
            if fr.body:
                html_path.write_bytes(fr.body)
            else:
                html_path.write_text("", encoding="utf-8")

        body = fr.body
        html = body.decode("utf-8", errors="replace") if body else ""

        jsonld = extract_jsonld_blocks(html) if html else []
        meta = extract_meta(html) if html else {}
        published = extract_published_date(html, meta, jsonld) if html else None
        mb = month_bucket(published)
        slug = slug_from_url(url)

        # Prefer cached text/meta paths if present; else use deterministic month bucket paths.
        text_path = cached_text_path or (out_root / "snapshots" / "text" / mb / f"{slug}.txt")
        meta_path = cached_meta_path or (out_root / "snapshots" / "meta" / mb / f"{slug}.json")

        text = ""
        if html:
            te = TextExtractor()
            te.feed(html)
            text = te.text()
        text_path.parent.mkdir(parents=True, exist_ok=True)
        text_path.write_text(text, encoding="utf-8")

        internal_links, external_links, internal_pricing, internal_tools = extract_internal_external_link_counts(html, url, base_netloc) if html else (0, 0, 0, 0)

        row = {
            "url": url,
            "title": meta.get("og:title") or meta.get("title_tag") or meta.get("twitter:title") or "",
            "published_date": published.isoformat() if published else "",
            "month": mb,
            "slug": slug,
            "fetched_at": fr.fetched_at,
            "status": fr.status,
        }

        meta_obj = {
            "url": url,
            "final_url": fr.final_url,
            "status": fr.status,
            "content_type": fr.content_type,
            "fetched_at": fr.fetched_at,
            "sha256": content_hash,
            "title": row["title"],
            "published_date": row["published_date"],
            "canonical": meta.get("canonical", ""),
            "meta": meta,
            "internal_links": internal_links,
            "external_links": external_links,
            "internal_links_pricing": internal_pricing,
            "internal_links_tools": internal_tools,
        }
        write_json(meta_path, meta_obj)

        manifest_row = {
            "url": url,
            "status": fr.status,
            "fetched_at": fr.fetched_at,
            "sha256": content_hash,
            "html_path": str(html_path),
            "text_path": str(text_path),
            "meta_path": str(meta_path),
            "error": fr.error,
        }

        aeo_row: Optional[Dict[str, Any]] = None
        if html:
            feats = compute_aeo_features(html, text)
            if within_window(published, since, until):
                aeo_row = {"url": url, **feats}
            else:
                aeo_row = {"url": url, **feats, "out_of_window": True}

        return idx, row, manifest_row, aeo_row

    indexed_urls = list(enumerate(urls, start=1))
    results: List[Tuple[int, Dict[str, Any], Dict[str, Any], Optional[Dict[str, Any]]]] = []
    if workers <= 1:
        for item in indexed_urls:
            results.append(process_one(item))
            if item[0] % 5 == 0:
                print(f"[crawl] {item[0]}/{len(indexed_urls)} processed", file=sys.stderr)
    else:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = [ex.submit(process_one, item) for item in indexed_urls]
            done = 0
            for fut in as_completed(futs):
                results.append(fut.result())
                done += 1
                if done % 10 == 0 or done == len(futs):
                    print(f"[crawl] {done}/{len(futs)} processed (workers={workers})", file=sys.stderr)

    results_sorted = sorted(results, key=lambda x: x[0])
    for _, row, manifest_row, aeo_row in results_sorted:
        blog_inventory.append(row)
        manifest_rows.append(manifest_row)
        if aeo_row:
            aeo_rows.append(aeo_row)

    # Write inventories
    write_csv(
        out_root / "data" / "url_inventory_blog.csv",
        blog_inventory,
        fieldnames=["url", "title", "published_date", "month", "slug", "fetched_at", "status"],
    )
    write_jsonl(out_root / "data" / "snapshots_manifest.jsonl", manifest_rows)
    # AEO features
    aeo_fieldnames = [
        "url",
        "aeo_score",
        "answer_first_score",
        "has_key_takeaways",
        "has_tldr",
        "has_faq",
        "schema_article",
        "schema_faqpage",
        "schema_howto",
        "schema_types",
        "h1_count",
        "h2_count",
        "toc_present",
        "word_count",
        "list_count",
        "table_count",
        "cta_count_proxy",
        "out_of_window",
    ]
    # ensure keys
    for r in aeo_rows:
        r.setdefault("out_of_window", False)
    write_csv(out_root / "data" / "aeo_features_blog.csv", aeo_rows, fieldnames=aeo_fieldnames)

    # DataForSEO (optional)
    domain_traffic_rows: List[Dict[str, Any]] = []
    relevant_pages_rows: List[Dict[str, Any]] = []
    blog_traffic_rows: List[Dict[str, Any]] = []
    tools_traffic_rows: List[Dict[str, Any]] = []
    ranked_keywords_rows: List[Dict[str, Any]] = []
    llm_mentions_rows: List[Dict[str, Any]] = []

    # If --skip-dataforseo is set, we still try to rebuild outputs from cached raw responses.
    if args.skip_dataforseo or args.dry_run:
        raw_dir = out_root / "data" / "raw" / "dataforseo"
        hist_cache = raw_dir / "historical_bulk_traffic_estimation.json"
        if hist_cache.exists():
            sources.append(
                {
                    "kind": "dataforseo",
                    "url": "https://api.dataforseo.com/v3/dataforseo_labs/google/historical_bulk_traffic_estimation/live",
                    "retrieved_at": utc_now_iso(),
                    "status": read_json(hist_cache).get("status_code"),
                    "local_path": str(hist_cache),
                    "note": "DataForSEO historical_bulk_traffic_estimation (raw response, cached)",
                }
            )
            domain_traffic_rows = filter_month_rows(dataforseo_extract_historical_traffic(read_json(hist_cache)), since, until)
            write_csv(out_root / "data" / "dataforseo_domain_traffic_6m.csv", domain_traffic_rows, fieldnames=["month", "organic_etv"])

        rp_cache = raw_dir / "relevant_pages.json"
        if rp_cache.exists():
            sources.append(
                {
                    "kind": "dataforseo",
                    "url": "https://api.dataforseo.com/v3/dataforseo_labs/google/relevant_pages/live",
                    "retrieved_at": utc_now_iso(),
                    "status": read_json(rp_cache).get("status_code"),
                    "local_path": str(rp_cache),
                    "note": "DataForSEO relevant_pages (raw response, cached)",
                }
            )
            relevant_pages_rows = dataforseo_extract_relevant_pages(read_json(rp_cache))
            write_csv(
                out_root / "data" / "dataforseo_pages_relevant.csv",
                relevant_pages_rows,
                fieldnames=["url", "etv", "keywords", "backlinks", "ref_domains"],
            )

        bulk_files = sorted(raw_dir.glob("bulk_traffic_blog_*.json"))
        bulk_all: List[Dict[str, Any]] = []
        for p in bulk_files:
            try:
                if p.name.endswith("_01.json"):
                    sources.append(
                        {
                            "kind": "dataforseo",
                            "url": "https://api.dataforseo.com/v3/dataforseo_labs/google/bulk_traffic_estimation/live",
                            "retrieved_at": utc_now_iso(),
                            "status": read_json(p).get("status_code"),
                            "local_path": str(p),
                            "note": "DataForSEO bulk_traffic_estimation for blog URLs (raw response, cached; first chunk)",
                        }
                    )
                bulk_all.extend(dataforseo_extract_bulk_traffic(read_json(p)))
            except Exception:
                continue
        if bulk_all:
            # de-dup by url (max etv)
            by_u: Dict[str, Dict[str, Any]] = {}
            for r in bulk_all:
                u = str(r.get("url") or "")
                if not u:
                    continue
                if u not in by_u or safe_float(r.get("etv")) > safe_float(by_u[u].get("etv")):
                    by_u[u] = r
            blog_traffic_rows = sorted(by_u.values(), key=lambda x: safe_float(x.get("etv")), reverse=True)
            write_csv(out_root / "data" / "dataforseo_blog_url_traffic.csv", blog_traffic_rows, fieldnames=["url", "etv", "keywords"])

        bulk_tool_files = sorted(raw_dir.glob("bulk_traffic_tools_*.json"))
        tool_all: List[Dict[str, Any]] = []
        for p in bulk_tool_files:
            try:
                if p.name.endswith("_01.json"):
                    sources.append(
                        {
                            "kind": "dataforseo",
                            "url": "https://api.dataforseo.com/v3/dataforseo_labs/google/bulk_traffic_estimation/live",
                            "retrieved_at": utc_now_iso(),
                            "status": read_json(p).get("status_code"),
                            "local_path": str(p),
                            "note": "DataForSEO bulk_traffic_estimation for tools URLs (raw response, cached; first chunk)",
                        }
                    )
                tool_all.extend(dataforseo_extract_bulk_traffic(read_json(p)))
            except Exception:
                continue
        if tool_all:
            by_u: Dict[str, Dict[str, Any]] = {}
            for r in tool_all:
                u = str(r.get("url") or "")
                if not u:
                    continue
                if u not in by_u or safe_float(r.get("etv")) > safe_float(by_u[u].get("etv")):
                    by_u[u] = r
            tools_traffic_rows = sorted(by_u.values(), key=lambda x: safe_float(x.get("etv")), reverse=True)
            write_csv(out_root / "data" / "dataforseo_tools_url_traffic.csv", tools_traffic_rows, fieldnames=["url", "etv", "keywords"])

        rk_files = sorted(raw_dir.glob("ranked_keywords_*.json"))
        rk_all: List[Dict[str, Any]] = []
        for p in rk_files:
            try:
                if p.name == "ranked_keywords_001.json":
                    sources.append(
                        {
                            "kind": "dataforseo",
                            "url": "https://api.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live",
                            "retrieved_at": utc_now_iso(),
                            "status": read_json(p).get("status_code"),
                            "local_path": str(p),
                            "note": "DataForSEO ranked_keywords (raw response, cached; sample page)",
                        }
                    )
                rk_all.extend(dataforseo_extract_ranked_keywords(read_json(p)))
            except Exception:
                continue
        ranked_keywords_rows = rk_all
        if ranked_keywords_rows:
            write_csv(
                out_root / "data" / "dataforseo_blog_top_keywords.csv",
                ranked_keywords_rows,
                fieldnames=["target", "keyword", "position", "search_volume", "cpc", "url"],
            )

        llm_cache = raw_dir / "llm_mentions_top_pages.json"
        if llm_cache.exists():
            try:
                sources.append(
                    {
                        "kind": "dataforseo",
                        "url": "https://api.dataforseo.com/v3/ai_optimization/llm_mentions/top_pages/live",
                        "retrieved_at": utc_now_iso(),
                        "status": read_json(llm_cache).get("status_code"),
                        "local_path": str(llm_cache),
                        "note": "DataForSEO ai_optimization llm_mentions/top_pages (raw response, cached)",
                    }
                )
                llm_mentions_rows = dataforseo_extract_llm_mentions_top_pages(read_json(llm_cache))
                if llm_mentions_rows:
                    write_csv(
                        out_root / "data" / "dataforseo_llm_mentions_top_pages.csv",
                        llm_mentions_rows,
                        fieldnames=["url", "mentions", "model", "score"],
                    )
            except Exception:
                pass

    if not args.skip_dataforseo and not args.dry_run:
        username, password = load_dataforseo_creds(repo_root)
        client = DataForSEOClient(username, password)

        # 1) historical bulk traffic
        hist_item: Dict[str, Any] = {"targets": [domain_target], "language_code": language_code}
        if location_code is not None:
            hist_item["location_code"] = int(location_code)
        hist_payload = [
            hist_item
        ]
        hist_cache = out_root / "data" / "raw" / "dataforseo" / "historical_bulk_traffic_estimation.json"
        try:
            hist_resp = dataforseo_call_with_cache(
                client,
                "dataforseo_labs/google/historical_bulk_traffic_estimation/live",
                hist_payload,
                hist_cache,
                refresh=args.refresh_dataforseo,
            )
            sources.append(
                {
                    "kind": "dataforseo",
                    "url": "https://api.dataforseo.com/v3/dataforseo_labs/google/historical_bulk_traffic_estimation/live",
                    "retrieved_at": utc_now_iso(),
                    "status": hist_resp.get("status_code"),
                    "local_path": str(hist_cache),
                    "note": "DataForSEO historical_bulk_traffic_estimation (raw response)",
                }
            )
            domain_traffic_rows = filter_month_rows(dataforseo_extract_historical_traffic(hist_resp), since, until)
            write_csv(out_root / "data" / "dataforseo_domain_traffic_6m.csv", domain_traffic_rows, fieldnames=["month", "organic_etv"])
        except Exception as e:
            write_json(out_root / "data" / "raw" / "dataforseo" / "historical_bulk_traffic_estimation.error.json", {"error": str(e), "payload": hist_payload})

        # 2) relevant pages
        rp_item: Dict[str, Any] = {"target": domain_target, "language_code": language_code, "limit": 1000}
        if location_code is not None:
            rp_item["location_code"] = int(location_code)
        rp_payload = [
            rp_item
        ]
        rp_cache = out_root / "data" / "raw" / "dataforseo" / "relevant_pages.json"
        try:
            rp_resp = dataforseo_call_with_cache(
                client,
                "dataforseo_labs/google/relevant_pages/live",
                rp_payload,
                rp_cache,
                refresh=args.refresh_dataforseo,
            )
            sources.append(
                {
                    "kind": "dataforseo",
                    "url": "https://api.dataforseo.com/v3/dataforseo_labs/google/relevant_pages/live",
                    "retrieved_at": utc_now_iso(),
                    "status": rp_resp.get("status_code"),
                    "local_path": str(rp_cache),
                    "note": "DataForSEO relevant_pages (raw response)",
                }
            )
            relevant_pages_rows = dataforseo_extract_relevant_pages(rp_resp)
            write_csv(
                out_root / "data" / "dataforseo_pages_relevant.csv",
                relevant_pages_rows,
                fieldnames=["url", "etv", "keywords", "backlinks", "ref_domains"],
            )
        except Exception as e:
            write_json(out_root / "data" / "raw" / "dataforseo" / "relevant_pages.error.json", {"error": str(e), "payload": rp_payload})

        # 3) bulk traffic estimation for blog URLs (batch)
        # DataForSEO often limits targets count per call; chunk to 200.
        blog_targets = [r["url"] for r in blog_inventory if r.get("status") and int(r["status"]) < 400]
        chunks: List[List[str]] = []
        chunk_size = 200
        for i in range(0, len(blog_targets), chunk_size):
            chunks.append(blog_targets[i : i + chunk_size])

        collected_bulk: List[Dict[str, Any]] = []
        for ci, chunk in enumerate(chunks, start=1):
            bt_payload = [
                {
                    "targets": chunk,
                    **({"location_code": int(location_code)} if location_code is not None else {}),
                    "language_code": language_code,
                }
            ]
            cache_path = out_root / "data" / "raw" / "dataforseo" / f"bulk_traffic_blog_{ci:02d}.json"
            try:
                bt_resp = dataforseo_call_with_cache(
                    client,
                    "dataforseo_labs/google/bulk_traffic_estimation/live",
                    bt_payload,
                    cache_path,
                    refresh=args.refresh_dataforseo,
                )
                sources.append(
                    {
                        "kind": "dataforseo",
                        "url": "https://api.dataforseo.com/v3/dataforseo_labs/google/bulk_traffic_estimation/live",
                        "retrieved_at": utc_now_iso(),
                        "status": bt_resp.get("status_code"),
                        "local_path": str(cache_path),
                        "note": f"DataForSEO bulk_traffic_estimation for blog URLs (chunk {ci})",
                    }
                )
                collected_bulk.extend(dataforseo_extract_bulk_traffic(bt_resp))
            except Exception as e:
                write_json(cache_path.with_suffix(".error.json"), {"error": str(e), "payload": bt_payload})
        blog_traffic_rows = sorted(collected_bulk, key=lambda x: safe_float(x.get("etv")), reverse=True)
        write_csv(out_root / "data" / "dataforseo_blog_url_traffic.csv", blog_traffic_rows, fieldnames=["url", "etv", "keywords"])

        # 3.5) bulk traffic estimation for tools URLs (batch, small)
        tool_targets = [r.get("url", "") for r in tools_rows]
        tool_targets = [u for u in tool_targets if u and not url_path_startswith(u, blog_prefix)]
        # Exclude the /tools listing page itself from estimation (optional)
        tool_targets = [u for u in tool_targets if not u.rstrip("/").endswith("/tools")]
        tool_chunks = chunk_list(tool_targets, 200)
        collected_tools: List[Dict[str, Any]] = []
        for ci, chunk in enumerate(tool_chunks, start=1):
            tt_payload = [
                {
                    "targets": chunk,
                    **({"location_code": int(location_code)} if location_code is not None else {}),
                    "language_code": language_code,
                }
            ]
            cache_path = out_root / "data" / "raw" / "dataforseo" / f"bulk_traffic_tools_{ci:02d}.json"
            try:
                tt_resp = dataforseo_call_with_cache(
                    client,
                    "dataforseo_labs/google/bulk_traffic_estimation/live",
                    tt_payload,
                    cache_path,
                    refresh=args.refresh_dataforseo,
                )
                if ci == 1:
                    sources.append(
                        {
                            "kind": "dataforseo",
                            "url": "https://api.dataforseo.com/v3/dataforseo_labs/google/bulk_traffic_estimation/live",
                            "retrieved_at": utc_now_iso(),
                            "status": tt_resp.get("status_code"),
                            "local_path": str(cache_path),
                            "note": "DataForSEO bulk_traffic_estimation for tools URLs (raw response; first chunk)",
                        }
                    )
                collected_tools.extend(dataforseo_extract_bulk_traffic(tt_resp))
            except Exception as e:
                write_json(cache_path.with_suffix(".error.json"), {"error": str(e), "payload": tt_payload})
        # de-dup
        by_u: Dict[str, Dict[str, Any]] = {}
        for r in collected_tools:
            u = str(r.get("url") or "")
            if not u:
                continue
            if u not in by_u or safe_float(r.get("etv")) > safe_float(by_u[u].get("etv")):
                by_u[u] = r
        tools_traffic_rows = sorted(by_u.values(), key=lambda x: safe_float(x.get("etv")), reverse=True)
        write_csv(out_root / "data" / "dataforseo_tools_url_traffic.csv", tools_traffic_rows, fieldnames=["url", "etv", "keywords"])

        # 4) ranked keywords for top 30 blog pages (cost control)
        top_for_kw = blog_traffic_rows[:30]
        rk_all: List[Dict[str, Any]] = []
        for i, r in enumerate(top_for_kw, start=1):
            target_url = r["url"]
            rk_payload = [
                {
                    "target": target_url,
                    "target_type": "page",
                    **({"location_code": int(location_code)} if location_code is not None else {}),
                    "language_code": language_code,
                    "limit": 200,
                }
            ]
            cache_path = out_root / "data" / "raw" / "dataforseo" / f"ranked_keywords_{i:03d}.json"
            try:
                rk_resp = dataforseo_call_with_cache(
                    client,
                    "dataforseo_labs/google/ranked_keywords/live",
                    rk_payload,
                    cache_path,
                    refresh=args.refresh_dataforseo,
                )
                if i == 1:
                    sources.append(
                        {
                            "kind": "dataforseo",
                            "url": "https://api.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live",
                            "retrieved_at": utc_now_iso(),
                            "status": rk_resp.get("status_code"),
                            "local_path": str(cache_path),
                            "note": "DataForSEO ranked_keywords (raw response, repeated per top blog page)",
                        }
                    )
                rk_all.extend(dataforseo_extract_ranked_keywords(rk_resp))
            except Exception as e:
                write_json(cache_path.with_suffix(".error.json"), {"error": str(e), "payload": rk_payload})
        ranked_keywords_rows = rk_all
        write_csv(
            out_root / "data" / "dataforseo_blog_top_keywords.csv",
            ranked_keywords_rows,
            fieldnames=["target", "keyword", "position", "search_volume", "cpc", "url"],
        )

        # 5) llm mentions top pages (optional)
        llm_payload = [{"target": domain_target, "limit": 200}]
        llm_cache = out_root / "data" / "raw" / "dataforseo" / "llm_mentions_top_pages.json"
        try:
            llm_resp = dataforseo_call_with_cache(
                client,
                "ai_optimization/llm_mentions/top_pages/live",
                llm_payload,
                llm_cache,
                refresh=args.refresh_dataforseo,
            )
            sources.append(
                {
                    "kind": "dataforseo",
                    "url": "https://api.dataforseo.com/v3/ai_optimization/llm_mentions/top_pages/live",
                    "retrieved_at": utc_now_iso(),
                    "status": llm_resp.get("status_code"),
                    "local_path": str(llm_cache),
                    "note": "DataForSEO AI Optimization llm_mentions/top_pages (raw response)",
                }
            )
            llm_mentions_rows = dataforseo_extract_llm_mentions_top_pages(llm_resp)
            write_csv(
                out_root / "data" / "dataforseo_llm_mentions_top_pages.csv",
                llm_mentions_rows,
                fieldnames=["url", "mentions", "model", "score"],
            )
        except Exception as e:
            write_json(out_root / "data" / "raw" / "dataforseo" / "llm_mentions_top_pages.error.json", {"error": str(e), "payload": llm_payload})

    # Build sources + reports
    sources_with_id = build_sources_index(sources, out_root / "99-sources.md")
    generate_reports(
        out_root=out_root,
        report_name=report_name,
        domain_target=domain_target,
        location_code=location_code,
        language_code=language_code,
        blog_prefix=blog_prefix,
        sources_with_id=sources_with_id,
        blog_inventory=blog_inventory,
        aeo_rows=aeo_rows,
        domain_traffic=domain_traffic_rows,
        relevant_pages=relevant_pages_rows,
        blog_traffic=blog_traffic_rows,
        tools_traffic=tools_traffic_rows,
        ranked_keywords=ranked_keywords_rows,
        llm_mentions=llm_mentions_rows,
        pricing_affiliate=pricing_affiliate,
        window_since=since,
        window_until=until,
    )

    print(f"Done. Outputs in: {out_root}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
