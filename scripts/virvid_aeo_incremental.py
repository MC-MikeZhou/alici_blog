#!/usr/bin/env python3
"""
Virvid Blog Incrementality (AEO) runner.

Goal
----
Quantify (with public signals + transparent modeling) how much Virvid's Blog/Tools
can contribute via:
- Exposure: SERP/AI Overview citations (zero-click possible)
- Click: modeled clicks from rank + search volume (CTR curve assumption)
- Assist: share-of-voice proxy on high-intent queries

Outputs land in:
  research 竞品分析/virvid-ai/aeo-incremental/

Design constraints
------------------
- stdlib-only (no bs4/pandas/yaml deps)
- safe: no hard-coded credentials; reads DataForSEO creds from .mcp.json
- reproducible: cache raw API responses, then derive CSV/MD
"""

from __future__ import annotations

import argparse
import base64
import csv
import datetime as dt
import hashlib
import json
import os
import random
import re
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


DEFAULT_VIRVID_ROOT = Path("research 竞品分析/virvid-ai")
DEFAULT_OUT_DIR = DEFAULT_VIRVID_ROOT / "aeo-incremental"
DEFAULT_CONFIG = DEFAULT_OUT_DIR / "config.yaml"

USER_AGENT = "Mozilla/5.0 (compatible; AliciBlogResearchBot/1.0; +https://alici.ai)"
DATAFORSEO_BASE = "https://api.dataforseo.com/v3"


def utc_now_iso() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(read_text(path))


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
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


def safe_int(val: Any, default: int = 0) -> int:
    try:
        if val is None:
            return default
        return int(val)
    except Exception:
        return default


def safe_float(val: Any, default: float = 0.0) -> float:
    try:
        if val is None:
            return default
        return float(val)
    except Exception:
        return default


def slugify(s: str, max_len: int = 120) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    if not s:
        s = "x"
    return s[:max_len]


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()


class YamlLite:
    """
    YAML-lite parser supporting:
    - key: value (scalars)
    - key:
        - item
        - item
    - key:
        subkey: value
    - key:
        1: 0.28
        2: 0.15
    No quotes/escapes/anchors.
    """

    @staticmethod
    def load(path: Path) -> Dict[str, Any]:
        root: Dict[str, Any] = {}
        stack: List[Dict[str, Any]] = [{"indent": 0, "container": root, "parent": None, "parent_key": None}]

        for raw in read_text(path).splitlines():
            line = raw.rstrip()
            if not line or line.lstrip().startswith("#"):
                continue
            indent = len(line) - len(line.lstrip(" "))
            line = line.lstrip(" ")

            while stack and indent < stack[-1]["indent"]:
                stack.pop()
            container = stack[-1]["container"]

            if line.startswith("- "):
                item = line[2:].strip()
                if isinstance(container, dict):
                    # If we created a placeholder dict for a key: block, convert it to list on first '-'.
                    top = stack[-1]
                    parent = top.get("parent")
                    parent_key = top.get("parent_key")
                    if parent is not None and parent_key and len(container) == 0:
                        new_list: List[Any] = []
                        parent[parent_key] = new_list
                        top["container"] = new_list
                        container = new_list
                    else:
                        raise ValueError(f"Invalid list item context: {raw}")
                if isinstance(container, list):
                    container.append(YamlLite._parse_scalar(item))
                continue

            if ":" not in line:
                continue

            key, rest = line.split(":", 1)
            key = key.strip()
            rest = rest.strip()

            if rest == "":
                # start a nested dict or list; decide later by peeking at next items
                # For simplicity: if next non-empty line at deeper indent starts with '-', treat as list.
                # We can't peek easily here; default to dict and convert to list on first '-'.
                new_container: Any = {}
                if isinstance(container, dict):
                    container[key] = new_container
                else:
                    raise ValueError(f"Invalid mapping context: {raw}")
                stack.append(
                    {
                        "indent": indent + 2,
                        "container": new_container,
                        "parent": container,
                        "parent_key": key,
                    }
                )
            else:
                val = YamlLite._parse_scalar(rest)
                if isinstance(container, dict):
                    container[key] = val
                else:
                    raise ValueError(f"Invalid mapping context: {raw}")

        # post-process: convert dicts that only have numeric keys to dict[int,float] kept as str->float
        return YamlLite._normalize(root)

    @staticmethod
    def _parse_scalar(s: str) -> Any:
        if s.lower() in {"true", "false"}:
            return s.lower() == "true"
        if re.fullmatch(r"-?\d+", s):
            return int(s)
        if re.fullmatch(r"-?\d+\.\d+", s):
            return float(s)
        return s

    @staticmethod
    def _normalize(obj: Any) -> Any:
        if isinstance(obj, dict):
            # Detect a "placeholder dict" that should be a list: it has no keys (already a dict)
            # We handle list conversion dynamically at use sites; keep dict.
            return {k: YamlLite._normalize(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [YamlLite._normalize(x) for x in obj]
        return obj


class AnchorParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: List[str] = []
        self._in_a = False
        self._a_text = ""
        self.anchors: List[Tuple[str, str]] = []  # (href, text)

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        if tag.lower() == "a":
            href = ""
            for k, v in attrs:
                if k.lower() == "href" and v:
                    href = v
                    break
            self._in_a = True
            self._a_text = ""
            self.hrefs.append(href)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._in_a:
            href = self.hrefs[-1] if self.hrefs else ""
            text = re.sub(r"\s+", " ", self._a_text).strip()
            self.anchors.append((href, text))
            self._in_a = False
            self._a_text = ""

    def handle_data(self, data: str) -> None:
        if self._in_a:
            self._a_text += data


class HeadingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.h1: List[str] = []
        self.h2: List[str] = []
        self._capture: Optional[str] = None
        self._buf = ""

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        t = tag.lower()
        if t in {"h1", "h2"}:
            self._capture = t
            self._buf = ""

    def handle_endtag(self, tag: str) -> None:
        t = tag.lower()
        if self._capture == t:
            text = re.sub(r"\s+", " ", self._buf).strip()
            if text:
                if t == "h1":
                    self.h1.append(text)
                elif t == "h2":
                    self.h2.append(text)
            self._capture = None
            self._buf = ""

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._buf += data


def read_dataforseo_creds(mcp_path: Path) -> Tuple[str, str]:
    mcp = read_json(mcp_path)
    env = (((mcp or {}).get("mcpServers") or {}).get("dataforseo") or {}).get("env") or {}
    username = str(env.get("DATAFORSEO_USERNAME", "")).strip()
    password = str(env.get("DATAFORSEO_PASSWORD", "")).strip()
    if not username or not password:
        raise RuntimeError("Missing DataForSEO credentials in .mcp.json (mcpServers.dataforseo.env).")
    return username, password


@dataclass
class SerpConfig:
    location_code: int
    language_code: str
    device: str
    os: str


class DataForSEOClient:
    def __init__(self, username: str, password: str, user_agent: str = USER_AGENT) -> None:
        credentials = f"{username}:{password}".encode("utf-8")
        self._auth_header = base64.b64encode(credentials).decode("ascii")
        self._user_agent = user_agent

    def post(self, endpoint: str, payload: List[Dict[str, Any]], timeout_s: int = 60) -> Dict[str, Any]:
        """
        Prefer urllib (pure stdlib). If DNS/network issues prevent it (seen intermittently in this environment),
        fall back to `curl` which tends to be more reliable here.
        """
        try:
            return self._post_urllib(endpoint, payload, timeout_s=timeout_s)
        except Exception:
            return self._post_curl(endpoint, payload, timeout_s=timeout_s)

    def _post_urllib(self, endpoint: str, payload: List[Dict[str, Any]], timeout_s: int) -> Dict[str, Any]:
        url = f"{DATAFORSEO_BASE}/{endpoint}"
        headers = {
            "Authorization": f"Basic {self._auth_header}",
            "Content-Type": "application/json",
            "User-Agent": self._user_agent,
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def _post_curl(self, endpoint: str, payload: List[Dict[str, Any]], timeout_s: int) -> Dict[str, Any]:
        url = f"{DATAFORSEO_BASE}/{endpoint}"
        body = json.dumps(payload)
        cmd = [
            "curl",
            "-sS",
            "--retry",
            "3",
            "--retry-all-errors",
            "--connect-timeout",
            "20",
            "--max-time",
            str(max(30, int(timeout_s))),
            "-X",
            "POST",
            url,
            "-H",
            "Content-Type: application/json",
            "-H",
            f"Authorization: Basic {self._auth_header}",
            "-H",
            f"User-Agent: {self._user_agent}",
            "--data-binary",
            body,
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError((proc.stderr or proc.stdout or "").strip() or f"curl_failed rc={proc.returncode}")
        try:
            return json.loads(proc.stdout)
        except Exception as e:
            snippet = (proc.stdout or "")[:400]
            raise RuntimeError(f"curl_json_parse_error: {e}; stdout_snippet={snippet!r}")


def with_retries(fn, *, retries: int = 3, base_sleep_s: float = 1.2) -> Any:
    last_err: Optional[BaseException] = None
    for attempt in range(retries):
        try:
            return fn()
        except Exception as e:
            last_err = e
            sleep_s = base_sleep_s * (2 ** attempt) + random.random() * 0.3
            time.sleep(sleep_s)
    if last_err:
        raise last_err
    raise RuntimeError("unknown retry error")


def read_csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_csv_rows(path: Path, rows: List[Dict[str, Any]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def normalize_query(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\s+", " ", s)
    s = s.replace("’", "'")
    return s


def normalize_title_for_query(title: str) -> str:
    t = title.strip()
    t = re.sub(r"\([^)]*\)", " ", t)  # remove parentheticals
    t = re.sub(r"\b(20\d{2})\b", " ", t)
    t = re.sub(r"[^A-Za-z0-9]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = t.lower()
    # Clean common HTML-entity artifacts (e.g., "&amp;" -> "amp" in some inventories)
    t = re.sub(r"\bamp\b", "and", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def classify_query(q: str) -> Tuple[str, str, str, int]:
    s = q.lower()
    intent = "informational"
    funnel = "awareness"
    topic = "generators_tools"
    priority = 3

    if "virvid" in s or "revid" in s or "arcads" in s:
        intent = "navigational"
        funnel = "decision"
        priority = 1

    if " vs " in f" {s} " or "alternatives" in s or "best" in s:
        intent = "commercial"
        funnel = "consideration"
        topic = "comparisons"
        priority = 1

    if "generator" in s or "tool" in s or "free" in s:
        intent = "transactional" if "generator" in s else "commercial"
        funnel = "decision"
        topic = "generators_tools"
        priority = min(priority, 1)

    if s.startswith("how to ") or "what is " in s:
        intent = "informational"
        funnel = "interest"
        priority = min(priority, 2)

    if "hook" in s:
        topic = "hooks"
    elif "shorts" in s:
        topic = "youtube_shorts" if "youtube" in s else "ai_shorts"
    elif "tiktok" in s:
        topic = "tiktok"
    elif "reels" in s or "instagram" in s:
        topic = "instagram_reels"
    elif "script" in s or "template" in s or "templates" in s:
        topic = "scripts_templates"
    elif "ad" in s or "ads" in s:
        topic = "ai_video_ads"
    elif "disclosure" in s or "requirements" in s or "policy" in s:
        topic = "disclosure_policy"
    elif "monetize" in s or "monetization" in s:
        topic = "monetization"

    return intent, funnel, topic, priority


def dedupe_preserve(items: Sequence[str]) -> List[str]:
    seen: set[str] = set()
    out: List[str] = []
    for it in items:
        k = it.strip().lower()
        if not k or k in seen:
            continue
        seen.add(k)
        out.append(it)
    return out


def parse_tools_slug_to_query(url: str) -> Optional[str]:
    try:
        p = urllib.parse.urlparse(url)
    except Exception:
        return None
    slug = p.path.strip("/")
    if not slug or slug.startswith("blog/"):
        return None
    q = slug.replace("-", " ").strip()
    q = re.sub(r"\s+", " ", q)
    if not q:
        return None
    return q.lower()


def load_snapshot_map(virvid_root: Path) -> Dict[str, Path]:
    manifest = virvid_root / "data" / "snapshots_manifest.jsonl"
    url_to_html: Dict[str, Path] = {}
    for row in read_jsonl(manifest):
        url = str(row.get("url", "")).strip()
        html_path = str(row.get("html_path", "")).strip()
        if not url or not html_path:
            continue
        p = (virvid_root / html_path) if not Path(html_path).is_absolute() else Path(html_path)
        if p.exists():
            url_to_html[url] = p
    return url_to_html


def load_snapshot_meta_map(virvid_root: Path) -> Dict[str, Path]:
    manifest = virvid_root / "data" / "snapshots_manifest.jsonl"
    url_to_meta: Dict[str, Path] = {}
    for row in read_jsonl(manifest):
        url = str(row.get("url", "")).strip()
        meta_path = str(row.get("meta_path", "")).strip()
        if not url or not meta_path:
            continue
        p = (virvid_root / meta_path) if not Path(meta_path).is_absolute() else Path(meta_path)
        if p.exists():
            url_to_meta[url] = p
    return url_to_meta


def extract_link_signals(html: str) -> Dict[str, Any]:
    ap = AnchorParser()
    try:
        ap.feed(html)
    except Exception:
        pass
    hrefs = [h for h in ap.hrefs if h]
    anchors = ap.anchors

    def any_href_contains(substr: str) -> bool:
        return any(substr in (h or "").lower() for h in hrefs)

    def count_anchor_text(pattern: str) -> int:
        rx = re.compile(pattern, re.I)
        n = 0
        for _, text in anchors:
            if text and rx.search(text):
                n += 1
        return n

    has_pricing = any_href_contains("/pricing")
    has_signup = any_href_contains("/signup") or any_href_contains("sign-up") or any_href_contains("auth")
    has_app = any_href_contains("/app") or any_href_contains("/editor") or any_href_contains("/generate")
    cta_like = count_anchor_text(r"\b(try|get started|sign up|start free|start now)\b")

    return {
        "has_pricing_link": has_pricing,
        "has_signup_link": has_signup,
        "has_app_link": has_app,
        "cta_like_count": cta_like,
        "anchor_count": len(anchors),
    }


def build_virvid_assets_index(virvid_root: Path, out_dir: Path) -> Path:
    blog_inv = read_csv_rows(virvid_root / "data" / "url_inventory_blog.csv")
    tool_inv = read_csv_rows(virvid_root / "data" / "url_inventory_free_tools.csv")
    aeo_rows = read_csv_rows(virvid_root / "data" / "aeo_features_blog.csv")
    blog_traffic = read_csv_rows(virvid_root / "data" / "dataforseo_blog_url_traffic.csv")
    tool_traffic = read_csv_rows(virvid_root / "data" / "dataforseo_tools_url_traffic.csv")

    aeo_by_url: Dict[str, Dict[str, str]] = {r.get("url", ""): r for r in aeo_rows if r.get("url")}
    blog_inv_by_url: Dict[str, Dict[str, str]] = {r.get("url", ""): r for r in blog_inv if r.get("url")}
    tool_inv_by_url: Dict[str, Dict[str, str]] = {r.get("url", ""): r for r in tool_inv if r.get("url")}

    traffic_by_url: Dict[str, Dict[str, str]] = {}
    for r in blog_traffic + tool_traffic:
        u = r.get("url") or r.get("target") or ""
        if u:
            traffic_by_url[u] = r

    url_to_html = load_snapshot_map(virvid_root)

    assets: List[Dict[str, Any]] = []
    url_to_meta = load_snapshot_meta_map(virvid_root)

    for url, inv in blog_inv_by_url.items():
        aeo = aeo_by_url.get(url, {})
        tr = traffic_by_url.get(url, {})
        html_path = url_to_html.get(url)
        signals = {}
        if html_path and html_path.exists():
            signals = extract_link_signals(read_text(html_path))
        # resolve title/date from meta if inventory is missing
        title = inv.get("title", "") or ""
        date = inv.get("published_date", inv.get("date", "")) or ""
        meta_path = url_to_meta.get(url)
        if meta_path and meta_path.exists():
            try:
                meta = read_json(meta_path)
                title = title or str(meta.get("title") or "")
                date = date or str(meta.get("published_date") or meta.get("date") or "")
            except Exception:
                pass
        assets.append(
            {
                "url": url,
                "asset_type": "blog",
                "title": title,
                "date": date,
                "aeo_score": aeo.get("aeo_score", ""),
                "word_count": aeo.get("word_count", ""),
                "etv": tr.get("etv", tr.get("traffic_etv", "")),
                "keywords": tr.get("keywords", ""),
                "has_pricing_link": signals.get("has_pricing_link", ""),
                "has_signup_link": signals.get("has_signup_link", ""),
                "has_app_link": signals.get("has_app_link", ""),
                "cta_like_count": signals.get("cta_like_count", ""),
            }
        )

    for url, inv in tool_inv_by_url.items():
        tr = traffic_by_url.get(url, {})
        html_path = url_to_html.get(url)
        signals = {}
        if html_path and html_path.exists():
            signals = extract_link_signals(read_text(html_path))
        assets.append(
            {
                "url": url,
                "asset_type": "tool",
                "title": inv.get("title", inv.get("slug", "")),
                "date": inv.get("date", ""),
                "aeo_score": "",
                "word_count": "",
                "etv": tr.get("etv", tr.get("traffic_etv", "")),
                "keywords": tr.get("keywords", ""),
                "has_pricing_link": signals.get("has_pricing_link", ""),
                "has_signup_link": signals.get("has_signup_link", ""),
                "has_app_link": signals.get("has_app_link", ""),
                "cta_like_count": signals.get("cta_like_count", ""),
            }
        )

    out_path = out_dir / "data" / "virvid_assets_index.csv"
    fieldnames = [
        "url",
        "asset_type",
        "title",
        "date",
        "aeo_score",
        "word_count",
        "etv",
        "keywords",
        "has_pricing_link",
        "has_signup_link",
        "has_app_link",
        "cta_like_count",
    ]
    write_csv_rows(out_path, assets, fieldnames)
    return out_path


def build_query_universe(
    virvid_root: Path,
    out_dir: Path,
    config: Dict[str, Any],
    *,
    max_queries: Optional[int] = None,
) -> Path:
    blog_inv = read_csv_rows(virvid_root / "data" / "url_inventory_blog.csv")
    tool_inv = read_csv_rows(virvid_root / "data" / "url_inventory_free_tools.csv")

    url_to_html = load_snapshot_map(virvid_root)
    url_to_meta = load_snapshot_meta_map(virvid_root)

    candidates: List[Tuple[str, str, str]] = []  # (query, source, related_url)

    def slug_from_url(url: str) -> str:
        try:
            p = urllib.parse.urlparse(url)
            slug = p.path.strip("/").split("/")[-1]
            return slug
        except Exception:
            return ""

    for row in blog_inv:
        url = (row.get("url") or "").strip()
        title = (row.get("title") or "").strip()
        if not url:
            continue
        # If inventory title is missing, try snapshot meta; else fall back to slug.
        if not title:
            mp = url_to_meta.get(url)
            if mp and mp.exists():
                try:
                    meta = read_json(mp)
                    title = str(meta.get("title") or "").strip()
                except Exception:
                    title = ""
        if not title:
            title = slug_from_url(url).replace("-", " ").strip()
        if not title:
            continue
        q = normalize_title_for_query(title)
        if q:
            candidates.append((q, "blog_title", url))
        # add extra patterns for VS/comparisons
        if " vs " in f" {q} " or q.startswith("virvid vs"):
            candidates.append((q.replace("virvid", "").strip(), "blog_title_variant", url))
            candidates.append((q.replace(" vs ", " alternatives ").strip(), "blog_title_variant", url))
        # use headings for long-tail
        html_path = url_to_html.get(url)
        if html_path and html_path.exists():
            hp = HeadingParser()
            try:
                hp.feed(read_text(html_path))
            except Exception:
                hp = None
            if hp:
                for h in (hp.h1[:1] + hp.h2[:2]):
                    hq = normalize_title_for_query(h)
                    if hq and len(hq.split()) >= 3:
                        candidates.append((hq.lower(), "blog_heading", url))

    for row in tool_inv:
        url = (row.get("url") or "").strip()
        if not url:
            continue
        q = parse_tools_slug_to_query(url)
        if q:
            candidates.append((q, "tool_slug", url))
            if "generator" not in q:
                candidates.append((q + " generator", "tool_slug_variant", url))

    for seed in (config.get("generic_query_seeds") or []):
        if isinstance(seed, str) and seed.strip():
            candidates.append((seed.strip().lower(), "generic_seed", ""))

    # Programmatic expansions (deterministic, capped by final query_count)
    def add_variant(q: str, src: str, rel: str) -> None:
        q = normalize_query(q).strip().lower()
        if not q:
            return
        candidates.append((q, src, rel))

    def expand_base_query(q: str, src: str, rel: str) -> None:
        s = q.strip().lower()
        toks = s.split()
        if len(toks) < 3:
            return

        # year variants for freshness
        if "2026" not in s:
            add_variant(s + " 2026", src + "_v", rel)

        if "free" not in toks and ("generator" in toks or "templates" in toks or "template" in toks):
            add_variant("free " + s, src + "_v", rel)

        if "best" not in toks and ("generator" in toks or "tools" in toks or "tool" in toks):
            add_variant("best " + s, src + "_v", rel)

        if s.startswith("how to "):
            add_variant(s.replace("how to ", "", 1), src + "_v", rel)
        elif s.startswith("what are "):
            add_variant(s.replace("what are ", "", 1), src + "_v", rel)
        elif s.startswith("what is "):
            add_variant(s.replace("what is ", "", 1), src + "_v", rel)

        if "templates" in toks or "template" in toks:
            add_variant(s + " examples", src + "_v", rel)
        if "hook" in toks:
            add_variant(s + " examples", src + "_v", rel)
            add_variant(s + " formulas", src + "_v", rel)

    # Expand from existing candidates (use a snapshot to avoid infinite growth)
    base_candidates = list(candidates)
    for q, src, rel in base_candidates:
        if src in {"blog_title", "tool_slug", "tool_slug_variant", "generic_seed"}:
            expand_base_query(q, src, rel)

    # normalize/dedupe
    raw_queries = [normalize_query(q) for q, _, _ in candidates if q]
    raw_queries = dedupe_preserve(raw_queries)

    def is_too_generic(q: str) -> bool:
        s = q.strip().lower()
        if s in {"tools", "tool", "generator", "generators", "templates", "template", "ideas"}:
            return True
        toks = [t for t in s.split() if t]
        # Discard 1-token queries unless navigational/brand
        if len(toks) < 2 and "virvid" not in s:
            return True
        # Discard obviously broken short tails
        if len(s) < 6 and "virvid" not in s:
            return True
        return False

    raw_queries = [q for q in raw_queries if not is_too_generic(q)]

    # Build a map from query -> best source/related_url
    meta_by_query: Dict[str, Tuple[str, str]] = {}
    for q, src, rel in candidates:
        nq = normalize_query(q).strip().lower()
        if not nq:
            continue
        if nq not in meta_by_query:
            meta_by_query[nq] = (src, rel)

    limit = safe_int(max_queries or config.get("query_count") or 300, 300)

    rows: List[Dict[str, Any]] = []
    for q in raw_queries[:limit]:
        intent, funnel, topic, priority = classify_query(q)
        src, rel = meta_by_query.get(q.strip().lower(), ("", ""))
        rows.append(
            {
                "query": q,
                "intent": intent,
                "funnel_stage": funnel,
                "topic_cluster": topic,
                "priority": priority,
                "source": src,
                "related_url": rel,
            }
        )

    out_path = out_dir / "data" / "query_universe.csv"
    fieldnames = ["query", "intent", "funnel_stage", "topic_cluster", "priority", "source", "related_url"]
    write_csv_rows(out_path, rows, fieldnames)
    return out_path


def serp_cache_path(out_dir: Path, cfg: SerpConfig, query: str) -> Path:
    key = json.dumps(
        {
            "query": query,
            "location_code": cfg.location_code,
            "language_code": cfg.language_code,
            "device": cfg.device,
            "os": cfg.os,
        },
        sort_keys=True,
    )
    name = f"{slugify(query, 80)}__{sha1(key)[:10]}.json"
    return out_dir / "data" / "raw" / "dataforseo_serp" / name


def volumes_cache_path(out_dir: Path, cfg: SerpConfig, queries: List[str]) -> Path:
    key = json.dumps(
        {
            "queries_sha1": sha1("\n".join(sorted([q.strip().lower() for q in queries]))),
            "location_code": cfg.location_code,
            "language_code": cfg.language_code,
        },
        sort_keys=True,
    )
    name = f"keyword_volumes__{sha1(key)[:12]}.json"
    return out_dir / "data" / "raw" / "dataforseo_keywords_data" / name


def call_serp_advanced(
    client: DataForSEOClient,
    cfg: SerpConfig,
    query: str,
    *,
    depth: int = 100,
) -> Dict[str, Any]:
    payload = [
        {
            "keyword": query,
            "location_code": cfg.location_code,
            "language_code": cfg.language_code,
            "device": cfg.device,
            "os": cfg.os,
            "depth": depth,
        }
    ]
    return client.post("serp/google/organic/live/advanced", payload, timeout_s=90)


def call_serp_advanced_batch(
    client: DataForSEOClient,
    cfg: SerpConfig,
    queries: List[str],
    *,
    depth: int = 100,
) -> Dict[str, Any]:
    payload = [
        {
            "keyword": q,
            "location_code": cfg.location_code,
            "language_code": cfg.language_code,
            "device": cfg.device,
            "os": cfg.os,
            "depth": depth,
        }
        for q in queries
    ]
    return client.post("serp/google/organic/live/advanced", payload, timeout_s=120)


def call_keyword_volumes(
    client: DataForSEOClient,
    cfg: SerpConfig,
    queries: List[str],
) -> Dict[str, Any]:
    payload = [
        {
            "keywords": queries,
            "location_code": cfg.location_code,
            "language_code": cfg.language_code,
            "search_partners": False,
        }
    ]
    return client.post("keywords_data/google_ads/search_volume/live", payload, timeout_s=90)


def extract_serp_features_from_response(resp: Dict[str, Any], query: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "query": query,
        "ai_overview_present": False,
        "featured_snippet_present": False,
        "people_also_ask_present": False,
        "paa_question_count": 0,
        "virvid_rank": "",
        "virvid_best_url": "",
        "virvid_best_asset_type": "",
        "top10_domains": "",
        "top10_urls": "",
        "aio_cites_virvid": False,
        "aio_citation_domains": "",
        "aio_citation_urls": "",
    }

    if resp.get("status_code") != 20000:
        out["error"] = f"api_status={resp.get('status_code')} {resp.get('status_message', '')}".strip()
        return out

    tasks = resp.get("tasks") or []
    if not tasks:
        out["error"] = "no_tasks"
        return out

    # For live endpoints, a single payload yields a single task/result.
    task = tasks[0] if isinstance(tasks, list) else tasks
    if (task or {}).get("status_code") != 20000:
        out["error"] = f"task_status={task.get('status_code')} {task.get('status_message', '')}".strip()
        return out

    result = (task or {}).get("result") or []
    if not result:
        out["error"] = "no_result"
        return out

    items = (result[0] or {}).get("items") or []
    top_org: List[Tuple[int, str, str]] = []  # (rank, domain, url)
    virvid_best_rank: Optional[int] = None
    virvid_best_url = ""

    aio_refs_domains: List[str] = []
    aio_refs_urls: List[str] = []

    def collect_urls_domains(obj: Any) -> None:
        if isinstance(obj, dict):
            url = obj.get("url") or obj.get("source_url") or obj.get("link")
            dom = obj.get("domain") or obj.get("source_domain")
            if isinstance(url, str) and url.startswith("http"):
                aio_refs_urls.append(url)
            if isinstance(dom, str) and "." in dom:
                aio_refs_domains.append(dom)
            for v in obj.values():
                collect_urls_domains(v)
        elif isinstance(obj, list):
            for v in obj:
                collect_urls_domains(v)

    for it in items:
        it_type = (it or {}).get("type")
        if it_type == "ai_overview":
            out["ai_overview_present"] = True
            collect_urls_domains(it)
        elif it_type == "featured_snippet":
            out["featured_snippet_present"] = True
        elif it_type == "people_also_ask":
            out["people_also_ask_present"] = True
            paa_items = (it or {}).get("items") or []
            out["paa_question_count"] = len(paa_items) if isinstance(paa_items, list) else 0
        elif it_type == "organic":
            rank = safe_int(it.get("rank_group"), 0)
            domain = str(it.get("domain") or "")
            url = str(it.get("url") or "")
            if rank and domain and url:
                if rank <= 10:
                    top_org.append((rank, domain, url))
                if domain.endswith("virvid.ai") or domain == "virvid.ai":
                    if virvid_best_rank is None or rank < virvid_best_rank:
                        virvid_best_rank = rank
                        virvid_best_url = url

    if virvid_best_rank is not None:
        out["virvid_rank"] = virvid_best_rank
        out["virvid_best_url"] = virvid_best_url
        out["virvid_best_asset_type"] = "blog" if "/blog/" in virvid_best_url else "tool_or_landing"

    top_org_sorted = [x for x in sorted(top_org, key=lambda t: t[0])]
    out["top10_domains"] = "|".join([d for _, d, _ in top_org_sorted])
    out["top10_urls"] = "|".join([u for _, _, u in top_org_sorted])

    # citations
    aio_refs_urls = [u for u in aio_refs_urls if isinstance(u, str)]
    aio_refs_domains = [d for d in aio_refs_domains if isinstance(d, str)]
    aio_refs_urls = dedupe_preserve(aio_refs_urls)
    aio_refs_domains = dedupe_preserve(aio_refs_domains)

    cites = any("virvid.ai" in u for u in aio_refs_urls) or any(d.endswith("virvid.ai") for d in aio_refs_domains)
    out["aio_cites_virvid"] = cites
    out["aio_citation_domains"] = "|".join(aio_refs_domains[:50])
    out["aio_citation_urls"] = "|".join(aio_refs_urls[:50])
    return out


def run_serp_collection(
    client: DataForSEOClient,
    out_dir: Path,
    cfg: SerpConfig,
    queries: List[str],
    *,
    refresh: bool,
) -> Tuple[Path, Path, Path]:
    raw_dir = out_dir / "data" / "raw" / "dataforseo_serp"
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_batches_dir = out_dir / "data" / "raw" / "dataforseo_serp_batches"
    raw_batches_dir.mkdir(parents=True, exist_ok=True)

    snapshots_path = out_dir / "data" / "serp_snapshots.jsonl"
    features_path = out_dir / "data" / "serp_features.csv"
    aio_path = out_dir / "data" / "aio_citations.csv"

    snapshot_rows: List[Dict[str, Any]] = []
    feature_rows: List[Dict[str, Any]] = []
    aio_rows: List[Dict[str, Any]] = []

    # First: load cached queries
    to_fetch: List[str] = []
    for q in queries:
        cache_path = serp_cache_path(out_dir, cfg, q)
        if cache_path.exists() and not refresh:
            fetched_at = utc_now_iso()
            try:
                resp = read_json(cache_path)
                feature = extract_serp_features_from_response(resp, q)
                feature.setdefault("error", "")
                feature["fetched_at"] = fetched_at
                feature["cache_path"] = str(cache_path.relative_to(out_dir))
                feature["cache_hit"] = True
                snapshot_rows.append(
                    {
                        "query": q,
                        "fetched_at": fetched_at,
                        "cache_path": str(cache_path.relative_to(out_dir)),
                        "cache_hit": True,
                        "ok": True,
                        "error": "",
                    }
                )
                feature_rows.append(feature)
                aio_rows.append(
                    {
                        "query": q,
                        "fetched_at": fetched_at,
                        "ai_overview_present": feature.get("ai_overview_present", False),
                        "aio_cites_virvid": feature.get("aio_cites_virvid", False),
                        "aio_citation_domains": feature.get("aio_citation_domains", ""),
                        "aio_citation_urls": feature.get("aio_citation_urls", ""),
                    }
                )
            except Exception as e:
                to_fetch.append(q)
                snapshot_rows.append(
                    {
                        "query": q,
                        "fetched_at": fetched_at,
                        "cache_path": str(cache_path.relative_to(out_dir)),
                        "cache_hit": True,
                        "ok": False,
                        "error": f"cache_read_error: {type(e).__name__}: {e}",
                    }
                )
        else:
            to_fetch.append(q)

    # Then: fetch remaining in batches
    batch_size = 20
    for i in range(0, len(to_fetch), batch_size):
        batch = to_fetch[i : i + batch_size]
        fetched_at = utc_now_iso()
        batch_key = sha1(json.dumps({"batch": batch, "cfg": cfg.__dict__}, sort_keys=True))
        batch_cache_path = raw_batches_dir / f"serp_batch__{batch_key[:12]}.json"

        def fetch_batch() -> Dict[str, Any]:
            return call_serp_advanced_batch(client, cfg, batch, depth=100)

        try:
            resp = with_retries(fetch_batch, retries=3)
            write_json(batch_cache_path, resp)
            tasks = resp.get("tasks") or []
            # Map keyword -> task
            task_by_kw: Dict[str, Any] = {}
            if isinstance(tasks, list):
                for t in tasks:
                    data = (t or {}).get("data") or {}
                    kw = str(data.get("keyword") or "").strip()
                    if kw:
                        task_by_kw[kw] = t

            for q in batch:
                cache_path = serp_cache_path(out_dir, cfg, q)
                task = task_by_kw.get(q)
                per_resp: Dict[str, Any]
                if task is None:
                    per_resp = {"status_code": resp.get("status_code", 0), "tasks": []}
                else:
                    per_resp = {"status_code": resp.get("status_code", 0), "tasks": [task]}
                write_json(cache_path, per_resp)

                feature = extract_serp_features_from_response(per_resp, q)
                feature.setdefault("error", "")
                feature["fetched_at"] = fetched_at
                feature["cache_path"] = str(cache_path.relative_to(out_dir))
                feature["cache_hit"] = False

                snapshot_rows.append(
                    {
                        "query": q,
                        "fetched_at": fetched_at,
                        "cache_path": str(cache_path.relative_to(out_dir)),
                        "cache_hit": False,
                        "ok": True,
                        "error": "",
                        "batch_cache_path": str(batch_cache_path.relative_to(out_dir)),
                    }
                )
                feature_rows.append(feature)
                aio_rows.append(
                    {
                        "query": q,
                        "fetched_at": fetched_at,
                        "ai_overview_present": feature.get("ai_overview_present", False),
                        "aio_cites_virvid": feature.get("aio_cites_virvid", False),
                        "aio_citation_domains": feature.get("aio_citation_domains", ""),
                        "aio_citation_urls": feature.get("aio_citation_urls", ""),
                    }
                )
        except Exception as e:
            for q in batch:
                cache_path = serp_cache_path(out_dir, cfg, q)
                snapshot_rows.append(
                    {
                        "query": q,
                        "fetched_at": fetched_at,
                        "cache_path": str(cache_path.relative_to(out_dir)),
                        "cache_hit": False,
                        "ok": False,
                        "error": f"batch_error: {type(e).__name__}: {e}",
                    }
                )
        time.sleep(0.8 + random.random() * 0.4)

    write_jsonl(snapshots_path, snapshot_rows)
    write_csv_rows(
        features_path,
        feature_rows,
        fieldnames=[
            "query",
            "fetched_at",
            "cache_path",
            "cache_hit",
            "ai_overview_present",
            "featured_snippet_present",
            "people_also_ask_present",
            "paa_question_count",
            "virvid_rank",
            "virvid_best_url",
            "virvid_best_asset_type",
            "top10_domains",
            "top10_urls",
            "aio_cites_virvid",
            "aio_citation_domains",
            "aio_citation_urls",
            "error",
        ],
    )
    write_csv_rows(
        aio_path,
        aio_rows,
        fieldnames=[
            "query",
            "fetched_at",
            "ai_overview_present",
            "aio_cites_virvid",
            "aio_citation_domains",
            "aio_citation_urls",
        ],
    )
    return snapshots_path, features_path, aio_path


def build_serp_from_raw_batches(out_dir: Path, cfg: SerpConfig, queries: List[str]) -> Tuple[Path, Path, Path]:
    """
    Build serp_features.csv + aio_citations.csv from raw batch JSON responses.

    This is the "offline build" path meant to work even when Python networking is unreliable,
    by letting a separate fetch step (shell curl) populate `data/raw/dataforseo_serp_batches/`.
    """
    raw_batches_dir = out_dir / "data" / "raw" / "dataforseo_serp_batches"
    raw_batches_dir.mkdir(parents=True, exist_ok=True)

    snapshots_path = out_dir / "data" / "serp_snapshots.jsonl"
    features_path = out_dir / "data" / "serp_features.csv"
    aio_path = out_dir / "data" / "aio_citations.csv"

    # Load all batch files and map keyword -> task object (fallback only).
    task_by_kw: Dict[str, Any] = {}
    for p in sorted(raw_batches_dir.glob("*.json")):
        try:
            resp = read_json(p)
        except Exception:
            continue
        tasks = resp.get("tasks") or []
        if not isinstance(tasks, list):
            continue
        for t in tasks:
            data = (t or {}).get("data") or {}
            kw = str(data.get("keyword") or "").strip()
            if kw and kw not in task_by_kw:
                task_by_kw[kw] = t

    snapshot_rows: List[Dict[str, Any]] = []
    feature_rows: List[Dict[str, Any]] = []
    aio_rows: List[Dict[str, Any]] = []
    fetched_at = utc_now_iso()

    for q in queries:
        cache_path = serp_cache_path(out_dir, cfg, q)
        # Prefer per-query raw cache if present (fetch script can populate these directly).
        cache_exists = cache_path.exists()
        if cache_exists:
            try:
                per_resp = read_json(cache_path)
            except Exception:
                per_resp = None
        else:
            per_resp = None

        if per_resp is None:
            task = task_by_kw.get(q)
            if task is None:
                snapshot_rows.append(
                    {
                        "query": q,
                        "fetched_at": fetched_at,
                        "cache_path": str(cache_path.relative_to(out_dir)),
                        "cache_hit": False,
                        "ok": False,
                        "error": "missing_serp_raw_task",
                    }
                )
                continue
            per_resp = {"status_code": 20000, "tasks": [task]}
            write_json(cache_path, per_resp)
            cache_exists = False

        feature = extract_serp_features_from_response(per_resp, q)
        feature.setdefault("error", "")
        feature["fetched_at"] = fetched_at
        feature["cache_path"] = str(cache_path.relative_to(out_dir))
        feature["cache_hit"] = cache_exists
        feature_rows.append(feature)
        aio_rows.append(
            {
                "query": q,
                "fetched_at": fetched_at,
                "ai_overview_present": feature.get("ai_overview_present", False),
                "aio_cites_virvid": feature.get("aio_cites_virvid", False),
                "aio_citation_domains": feature.get("aio_citation_domains", ""),
                "aio_citation_urls": feature.get("aio_citation_urls", ""),
            }
        )
        snapshot_rows.append(
            {
                "query": q,
                "fetched_at": fetched_at,
                "cache_path": str(cache_path.relative_to(out_dir)),
                "cache_hit": False,
                "ok": True,
                "error": "",
            }
        )

    write_jsonl(snapshots_path, snapshot_rows)
    write_csv_rows(
        features_path,
        feature_rows,
        fieldnames=[
            "query",
            "fetched_at",
            "cache_path",
            "cache_hit",
            "ai_overview_present",
            "featured_snippet_present",
            "people_also_ask_present",
            "paa_question_count",
            "virvid_rank",
            "virvid_best_url",
            "virvid_best_asset_type",
            "top10_domains",
            "top10_urls",
            "aio_cites_virvid",
            "aio_citation_domains",
            "aio_citation_urls",
            "error",
        ],
    )
    write_csv_rows(
        aio_path,
        aio_rows,
        fieldnames=[
            "query",
            "fetched_at",
            "ai_overview_present",
            "aio_cites_virvid",
            "aio_citation_domains",
            "aio_citation_urls",
        ],
    )
    return snapshots_path, features_path, aio_path


def extract_volumes_from_response(resp: Dict[str, Any]) -> Dict[str, int]:
    out: Dict[str, int] = {}
    if resp.get("status_code") != 20000:
        return out
    tasks = resp.get("tasks") or []
    for task in tasks if isinstance(tasks, list) else [tasks]:
        if (task or {}).get("status_code") != 20000:
            continue
        result = (task or {}).get("result") or []
        for item in result:
            kw = str(item.get("keyword") or "").strip()
            sv = safe_int(item.get("search_volume"), 0)
            if kw:
                out[kw] = sv
    return out


def run_keyword_volumes(
    client: DataForSEOClient,
    out_dir: Path,
    cfg: SerpConfig,
    queries: List[str],
    *,
    refresh: bool,
) -> Path:
    raw_dir = out_dir / "data" / "raw" / "dataforseo_keywords_data"
    raw_dir.mkdir(parents=True, exist_ok=True)

    rows: List[Dict[str, Any]] = []
    # chunk to avoid payload limits
    for i in range(0, len(queries), 100):
        chunk = queries[i : i + 100]
        cache_path = volumes_cache_path(out_dir, cfg, chunk)
        fetched_at = utc_now_iso()

        def fetch() -> Dict[str, Any]:
            return call_keyword_volumes(client, cfg, chunk)

        resp: Optional[Dict[str, Any]] = None
        cache_hit = False
        err = ""
        ok = True
        try:
            if cache_path.exists() and not refresh:
                resp = read_json(cache_path)
                cache_hit = True
            else:
                resp = with_retries(fetch, retries=3)
                write_json(cache_path, resp)
                cache_hit = False
        except Exception as e:
            ok = False
            err = f"{type(e).__name__}: {e}"

        vols = extract_volumes_from_response(resp or {})
        for q in chunk:
            rows.append(
                {
                    "query": q,
                    "search_volume": vols.get(q, 0),
                    "fetched_at": fetched_at,
                    "cache_path": str(cache_path.relative_to(out_dir)),
                    "cache_hit": cache_hit,
                    "ok": ok,
                    "error": err,
                }
            )
        time.sleep(0.4 + random.random() * 0.2)

    out_path = out_dir / "data" / "query_volumes.csv"
    write_csv_rows(
        out_path,
        rows,
        fieldnames=["query", "search_volume", "fetched_at", "cache_path", "cache_hit", "ok", "error"],
    )
    return out_path


def build_volumes_from_raw_batches(out_dir: Path, queries: List[str]) -> Path:
    """
    Build query_volumes.csv from raw keyword volume batch JSON responses.
    Fetch step should populate `data/raw/dataforseo_keywords_data/`.
    """
    raw_dir = out_dir / "data" / "raw" / "dataforseo_keywords_data"
    raw_dir.mkdir(parents=True, exist_ok=True)

    vol_by_kw: Dict[str, int] = {}
    for p in sorted(raw_dir.glob("*.json")):
        try:
            resp = read_json(p)
        except Exception:
            continue
        vol_by_kw.update(extract_volumes_from_response(resp))

    fetched_at = utc_now_iso()
    rows: List[Dict[str, Any]] = []
    for q in queries:
        rows.append(
            {
                "query": q,
                "search_volume": vol_by_kw.get(q, 0),
                "fetched_at": fetched_at,
                "cache_path": "",
                "cache_hit": True,
                "ok": True,
                "error": "",
            }
        )

    out_path = out_dir / "data" / "query_volumes.csv"
    write_csv_rows(
        out_path,
        rows,
        fieldnames=["query", "search_volume", "fetched_at", "cache_path", "cache_hit", "ok", "error"],
    )
    return out_path


def read_config_or_default(config_path: Path) -> Dict[str, Any]:
    if not config_path.exists():
        raise RuntimeError(f"Missing config: {config_path}")
    cfg = YamlLite.load(config_path)
    # YAML-lite cannot distinguish dict-vs-list placeholders for nested blocks;
    # ensure known list keys are lists.
    for k in ["generic_query_seeds", "topic_clusters"]:
        v = cfg.get(k)
        if isinstance(v, dict):
            cfg[k] = []
        if v is None:
            cfg[k] = []
    return cfg


def load_ctr_curve(cfg: Dict[str, Any]) -> Dict[int, float]:
    curve_raw = cfg.get("ctr_curve") or {}
    curve: Dict[int, float] = {}
    if isinstance(curve_raw, dict):
        for k, v in curve_raw.items():
            try:
                rk = int(k)
            except Exception:
                rk = safe_int(k, 0)
            if rk <= 0:
                continue
            curve[rk] = safe_float(v, 0.0)
    return curve


def build_answer_engine_tests(out_dir: Path, query_rows: List[Dict[str, Any]], n: int) -> Path:
    # stratified sample: prioritize commercial/transactional + ensure topic diversity
    buckets: Dict[str, List[Dict[str, Any]]] = {}
    for r in query_rows:
        topic = r.get("topic_cluster", "misc")
        buckets.setdefault(topic, []).append(r)

    picked: List[Dict[str, Any]] = []
    topics = sorted(buckets.keys())
    rnd = random.Random(42)
    for t in topics:
        rnd.shuffle(buckets[t])

    # round-robin pick
    while len(picked) < n and any(buckets.values()):
        for t in topics:
            if len(picked) >= n:
                break
            if not buckets.get(t):
                continue
            picked.append(buckets[t].pop(0))

    rows = []
    now = utc_now_iso()
    for r in picked:
        q = r.get("query", "")
        rows.append(
            {
                "query": q,
                "topic_cluster": r.get("topic_cluster", ""),
                "intent": r.get("intent", ""),
                "funnel_stage": r.get("funnel_stage", ""),
                "created_at": now,
                "google": {"cites_virvid": None, "citations": [], "evidence_path": ""},
                "perplexity": {"cites_virvid": None, "citations": [], "evidence_path": ""},
                "chatgpt": {"cites_virvid": None, "citations": [], "evidence_path": ""},
                "notes": "",
            }
        )

    out_path = out_dir / "data" / "answer_engine_tests.jsonl"
    write_jsonl(out_path, rows)
    return out_path


def token_set(s: str) -> set[str]:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    toks = [t for t in s.split() if len(t) >= 3]
    stop = {"what", "your", "best", "with", "from", "that", "this", "free", "2026", "2025"}
    return {t for t in toks if t not in stop}


def build_alici_index() -> List[Dict[str, Any]]:
    # heuristic: use `reports/**/01-article*.md` as content artifacts
    base = Path("reports")
    if not base.exists():
        return []
    paths = sorted(base.glob("**/01-article*.md"))
    out: List[Dict[str, Any]] = []
    for p in paths:
        try:
            txt = read_text(p)
        except Exception:
            continue
        m = re.search(r"^#\s+(.+)$", txt, flags=re.M)
        title = m.group(1).strip() if m else p.stem
        out.append(
            {
                "path": str(p),
                "title": title,
                "tokens": token_set(title),
            }
        )
    return out


def build_alici_gap_map(
    out_dir: Path,
    query_rows: List[Dict[str, Any]],
    serp_by_query: Dict[str, Dict[str, Any]],
    vol_by_query: Dict[str, int],
) -> Path:
    alici = build_alici_index()
    if not alici:
        # still output an empty map for determinism
        out_path = out_dir / "data" / "alici_gap_map.csv"
        write_csv_rows(
            out_path,
            [],
            fieldnames=[
                "topic_cluster",
                "query_example",
                "intent",
                "funnel_stage",
                "search_volume",
                "virvid_rank",
                "ai_overview_present",
                "aio_cites_virvid",
                "closest_alici_title",
                "closest_alici_path",
                "coverage_score",
                "recommended_action",
                "recommended_opening_pattern",
                "recommended_product_integration",
            ],
        )
        return out_path

    def best_match(q: str) -> Tuple[float, str, str]:
        qt = token_set(q)
        best = (0.0, "", "")
        for a in alici:
            at = a["tokens"]
            if not qt or not at:
                continue
            inter = len(qt & at)
            union = len(qt | at)
            score = inter / union if union else 0.0
            if score > best[0]:
                best = (score, a["title"], a["path"])
        return best

    gap_rows: List[Dict[str, Any]] = []

    # focus on higher-volume/high-intent queries
    sorted_q = sorted(
        query_rows,
        key=lambda r: (-safe_int(vol_by_query.get(r["query"], 0)), r.get("priority", 3)),
    )
    for r in sorted_q[:120]:
        q = r["query"]
        sv = safe_int(vol_by_query.get(q, 0), 0)
        if sv <= 0:
            continue
        serp = serp_by_query.get(q, {})
        match_score, match_title, match_path = best_match(q)
        # gap if match score is low and query is high intent or has AIO citations
        intent = r.get("intent", "")
        is_high_intent = intent in {"transactional", "commercial", "navigational"}
        aio_cites = bool(serp.get("aio_cites_virvid", False))
        if match_score < 0.18 and (is_high_intent or aio_cites):
            topic = r.get("topic_cluster", "")
            opening_pattern = "Key Takeaways + Answer-first"
            if topic in {"comparisons"}:
                opening_pattern = "Reframe / Verdict-first (invideo showdown)"
            elif topic in {"ai_video_ads", "disclosure_policy"}:
                opening_pattern = "Data Hook (with citations)"
            product_integration = "L2 (context CTA) → L3 (FAQ recommendation)"
            if topic in {"comparisons"}:
                product_integration = "L4 (position as workflow layer)"
            gap_rows.append(
                {
                    "topic_cluster": topic,
                    "query_example": q,
                    "intent": intent,
                    "funnel_stage": r.get("funnel_stage", ""),
                    "search_volume": sv,
                    "virvid_rank": serp.get("virvid_rank", ""),
                    "ai_overview_present": serp.get("ai_overview_present", False),
                    "aio_cites_virvid": serp.get("aio_cites_virvid", False),
                    "closest_alici_title": match_title,
                    "closest_alici_path": match_path,
                    "coverage_score": f"{match_score:.3f}",
                    "recommended_action": "Create or update Alici article + add tool landing CTA loop",
                    "recommended_opening_pattern": opening_pattern,
                    "recommended_product_integration": product_integration,
                }
            )

    out_path = out_dir / "data" / "alici_gap_map.csv"
    write_csv_rows(
        out_path,
        gap_rows,
        fieldnames=[
            "topic_cluster",
            "query_example",
            "intent",
            "funnel_stage",
            "search_volume",
            "virvid_rank",
            "ai_overview_present",
            "aio_cites_virvid",
            "closest_alici_title",
            "closest_alici_path",
            "coverage_score",
            "recommended_action",
            "recommended_opening_pattern",
            "recommended_product_integration",
        ],
    )
    return out_path


def build_incrementality_model(
    out_dir: Path,
    cfg: Dict[str, Any],
    query_rows: List[Dict[str, Any]],
    serp_by_query: Dict[str, Dict[str, Any]],
    vol_by_query: Dict[str, int],
) -> Path:
    ctr = load_ctr_curve(cfg)
    aeo_factor = safe_float(cfg.get("aeo_click_factor"), 0.2)

    scenarios = {
        "A": {"seo_ctr_mult": 0.7, "aeo_factor": min(aeo_factor, 0.1)},
        "B": {"seo_ctr_mult": 1.0, "aeo_factor": aeo_factor},
        "C": {"seo_ctr_mult": 1.2, "aeo_factor": max(aeo_factor, 0.3)},
    }

    def boolish(v: Any) -> bool:
        return str(v).lower() in {"true", "1", "yes"}

    # aggregate by topic+funnel+intent
    agg: Dict[Tuple[str, str, str], Dict[str, Any]] = {}

    for r in query_rows:
        q = r["query"]
        sv = safe_int(vol_by_query.get(q, 0), 0)
        serp = serp_by_query.get(q, {})
        rank = safe_int(serp.get("virvid_rank"), 0)
        aio_present = boolish(serp.get("ai_overview_present", False))
        aio_cites = boolish(serp.get("aio_cites_virvid", False))

        topic = r.get("topic_cluster", "")
        funnel = r.get("funnel_stage", "")
        intent = r.get("intent", "")
        key = (topic, funnel, intent)
        bucket = agg.setdefault(
            key,
            {
                "topic_cluster": topic,
                "funnel_stage": funnel,
                "intent": intent,
                "n_queries": 0,
                "n_queries_with_volume": 0,
                "sum_search_volume": 0,
                "n_virvid_top20": 0,
                "n_virvid_top50": 0,
                "n_virvid_top20_with_volume": 0,
                "n_virvid_top50_with_volume": 0,
                "n_ai_overview": 0,
                "n_aio_cites_virvid": 0,
                "n_ai_overview_with_volume": 0,
                "n_aio_cites_virvid_with_volume": 0,
                "est_seo_clicks_A": 0.0,
                "est_seo_clicks_B": 0.0,
                "est_seo_clicks_C": 0.0,
                "est_aeo_clicks_A": 0.0,
                "est_aeo_clicks_B": 0.0,
                "est_aeo_clicks_C": 0.0,
                "est_total_clicks_A": 0.0,
                "est_total_clicks_B": 0.0,
                "est_total_clicks_C": 0.0,
                "aeo_cited_impressions": 0,
            },
        )

        bucket["n_queries"] += 1
        if sv > 0:
            bucket["n_queries_with_volume"] += 1
            bucket["sum_search_volume"] += sv
        if rank and rank <= 20:
            bucket["n_virvid_top20"] += 1
        if rank and rank <= 50:
            bucket["n_virvid_top50"] += 1
        if sv > 0 and rank and rank <= 20:
            bucket["n_virvid_top20_with_volume"] += 1
        if sv > 0 and rank and rank <= 50:
            bucket["n_virvid_top50_with_volume"] += 1
        if aio_present:
            bucket["n_ai_overview"] += 1
        if aio_cites:
            bucket["n_aio_cites_virvid"] += 1
        if sv > 0 and aio_present:
            bucket["n_ai_overview_with_volume"] += 1
        if sv > 0 and aio_cites:
            bucket["n_aio_cites_virvid_with_volume"] += 1
            bucket["aeo_cited_impressions"] += sv

        # clicks modeling (monthly proxy using search_volume)
        base_ctr = ctr.get(rank, 0.0) if rank else 0.0
        for label, sc in scenarios.items():
            seo_clicks = sv * base_ctr * sc["seo_ctr_mult"]
            # if cited in AIO, allow clicks even if rank is low/unknown
            ref_rank = rank if rank else 10
            ref_ctr = ctr.get(min(ref_rank, 20), 0.018)  # fallback
            aeo_clicks = (sv * ref_ctr * sc["aeo_factor"]) if aio_cites else 0.0
            bucket[f"est_seo_clicks_{label}"] += seo_clicks
            bucket[f"est_aeo_clicks_{label}"] += aeo_clicks
            bucket[f"est_total_clicks_{label}"] += (seo_clicks + aeo_clicks)

    rows = list(agg.values())
    rows.sort(key=lambda r: (-safe_int(r.get("sum_search_volume"), 0), r.get("topic_cluster", "")))

    out_path = out_dir / "data" / "incrementality_model.csv"
    write_csv_rows(
        out_path,
        rows,
        fieldnames=[
            "topic_cluster",
            "funnel_stage",
            "intent",
            "n_queries",
            "n_queries_with_volume",
            "sum_search_volume",
            "n_virvid_top20",
            "n_virvid_top50",
            "n_virvid_top20_with_volume",
            "n_virvid_top50_with_volume",
            "n_ai_overview",
            "n_aio_cites_virvid",
            "n_ai_overview_with_volume",
            "n_aio_cites_virvid_with_volume",
            "aeo_cited_impressions",
            "est_seo_clicks_A",
            "est_aeo_clicks_A",
            "est_total_clicks_A",
            "est_seo_clicks_B",
            "est_aeo_clicks_B",
            "est_total_clicks_B",
            "est_seo_clicks_C",
            "est_aeo_clicks_C",
            "est_total_clicks_C",
        ],
    )
    return out_path


def build_brief_md(
    out_dir: Path,
    cfg: Dict[str, Any],
    query_rows: List[Dict[str, Any]],
    serp_rows: List[Dict[str, Any]],
    vol_by_query: Dict[str, int],
) -> Path:
    # derive top-line stats (and avoid misleading "self-generated query" inflation)
    n = len(query_rows)
    q_with_sv = [r for r in query_rows if safe_int(vol_by_query.get(r["query"], 0), 0) > 0]
    n_sv = len(q_with_sv)
    total_sv = sum(safe_int(vol_by_query.get(r["query"], 0), 0) for r in q_with_sv)

    serp_by_q = {r.get("query", ""): r for r in serp_rows if r.get("query")}

    def boolish(v: Any) -> bool:
        return str(v).lower() in {"true", "1", "yes"}

    def serp_stats(rows: List[Dict[str, Any]]) -> Dict[str, int]:
        top20 = top50 = aio = 0
        for rr in rows:
            q = rr["query"]
            s = serp_by_q.get(q, {})
            rank = safe_int(s.get("virvid_rank"), 0)
            if rank and rank <= 20:
                top20 += 1
            if rank and rank <= 50:
                top50 += 1
            if boolish(s.get("ai_overview_present", False)):
                aio += 1
        return {"top20": top20, "top50": top50, "aio_present": aio}

    all_stats = serp_stats(query_rows)
    sv_stats = serp_stats(q_with_sv)

    # AIO citations availability: current SERP payloads often include AIO blocks but references/citations are null.
    # So "aio_cites_virvid == 0" should not be interpreted as "never cited".
    aio_any = sum(1 for q in query_rows if boolish(serp_by_q.get(q["query"], {}).get("ai_overview_present", False)))
    aio_urls_nonempty = sum(
        1
        for q in query_rows
        if (serp_by_q.get(q["query"], {}).get("aio_citation_urls") or "").strip() != ""
    )

    # identify representative queries (by search volume)
    top_queries = sorted(
        q_with_sv,
        key=lambda r: (-safe_int(vol_by_query.get(r["query"], 0), 0), safe_int(r.get("priority", 3), 3)),
    )[:12]

    lines: List[str] = []
    lines.append("# Virvid Blog 增量贡献（AEO 视角）— Brief\n")
    lines.append(f"> 生成时间：{utc_now_iso()}\n")
    lines.append("> 说明：本报告不使用 Virvid 内部 GA/GSC；全部结论基于 **公开可验证信号** + **透明假设模型**。\n")

    lines.append("## Key Takeaways")
    lines.append(f"- 我们把“增量”拆成 **Exposure/Click/Assist** 三层指标，避免把 SEO 工具的 ETV 当成 AEO 真实流量。")
    lines.append(f"- 本次 query 宇宙规模：**{n}** 条（含大量来自 Virvid 自家内容/工具页的长尾 query 变体）。")
    lines.append(f"- 有搜索量（US/en Google Ads SV）可观测的 query：**{n_sv}** 条；总月搜索量（proxy）：**{total_sv:,}**。")
    lines.append(
        f"- **仅在“有搜索量的 query 子集”**里，Virvid 进入 Top20：**{sv_stats['top20']}**，Top50：**{sv_stats['top50']}**（更接近真实增量的 Click proxy）。"
    )
    lines.append(
        f"- SERP 出现 AI Overview：全量 query 里 **{all_stats['aio_present']}** 次；有搜索量子集里 **{sv_stats['aio_present']}** 次。"
    )
    if aio_any > 0 and aio_urls_nonempty == 0:
        lines.append(
            "- 注意：本次使用的 DataForSEO SERP 响应中，AI Overview 的 `references/citations` 字段多为 **空/None**，因此 `aio_citations.csv` 目前无法用来证明“是否引用 virvid.ai”（这是证据缺口，不是结论）。"
        )
    elif aio_any > 0 and aio_urls_nonempty > 0:
        lines.append(
            f"- AIO citations 可用性：在出现 AI Overview 的 **{aio_any}** 条 query 中，仅 **{aio_urls_nonempty}** 条返回了可解析的 citation URLs；其中 **virvid.ai = 0**（更像是“可见但不被引用”的阶段）。"
        )
    lines.append("- 关键差异点：即便 SEO 排名/点击很低，AEO 仍可能通过 **“被引用但零点击”** 或 **“被引用→品牌词助攻”** 产生增量；需要用后续证据包验证。")
    lines.append("- 对 Alici 的启发：把内容矩阵做成“漏斗覆盖 + 工具页闭环”，并用可被引用的结构（Key Takeaways/FAQ/表格）去争夺 AIO citations。")
    lines.append("")

    lines.append("## TL;DR Answer")
    lines.append(
        "Virvid 的 Blog/Tools 是否带来“增量”，不能只看 SEO ETV。更可靠的做法是：先用 SERP 数据量化 **AIO 是否出现、是否引用 virvid.ai、Virvid 排名分布**；再用搜索量×CTR 曲线做 Click 区间，并把“被引用但不点击”的 Exposure 单列；最后把这些发现映射成 Alici 的内容缺口与可复制模板。"
    )
    lines.append("")

    lines.append("## 本次落盘的数据（可复查）")
    lines.append(f"- Query 宇宙：`data/query_universe.csv`")
    lines.append(f"- SERP 原始快照：`data/serp_snapshots.jsonl` + `data/raw/dataforseo_serp/`")
    lines.append(f"- SERP 特征表：`data/serp_features.csv`")
    lines.append(f"- AIO 引用表：`data/aio_citations.csv`")
    lines.append(f"- 搜索量表：`data/query_volumes.csv` + `data/raw/dataforseo_keywords_data/`")
    lines.append(f"- 增量模型：`data/incrementality_model.csv`")
    lines.append(f"- Alici 缺口映射：`data/alici_gap_map.csv`")
    lines.append("")

    lines.append("## 代表性高价值 Query（用于人工验证 Answer Engines）")
    lines.append("| Query | SV | Virvid Rank | AIO | AIO cites virvid.ai |")
    lines.append("|---|---:|---:|:--:|:--:|")
    for r in top_queries:
        q = r["query"]
        sv = safe_int(vol_by_query.get(q, 0), 0)
        sf = serp_by_q.get(q, {})
        rank = sf.get("virvid_rank", "")
        aio = "Y" if sf.get("ai_overview_present") in (True, "True", "true", "1", 1) else ""
        cites = "Y" if sf.get("aio_cites_virvid") in (True, "True", "true", "1", 1) else ""
        lines.append(f"| {q} | {sv:,} | {rank or ''} | {aio} | {cites} |")
    lines.append("")

    lines.append("## 需要补的证据（Evidence Gaps）")
    lines.append("- **AEO 真实点击/会话**：需要 Virvid 自身 GA4/日志（不可能拿到）或 Alici 自身在未来实验中验证。")
    lines.append("- **ChatGPT/Perplexity 引用**：已生成 `data/answer_engine_tests.jsonl` 作为人工核验清单；证据存放见 `evidence/README.md`。")
    lines.append("- **Assist（品牌助攻）**：建议补充 Google Trends（品牌词）与“品牌词 SOV”监控（可在周更中加入）。")
    lines.append("")

    lines.append("## 对 Alici 的 10 个可执行动作（从竞品→落地）")
    lines.append("1) 建立 **Exposure/Click/Assist** 三层看板：AIO citations、AI referrer、排名分布。")
    lines.append("2) 把“工具页”当成增长资产：每篇 blog 必须指向一个对应 free tool / use case landing，形成闭环。")
    lines.append("3) 每篇文章默认结构：Key Takeaways → TL;DR → 正文 → FAQ → 可引用表格（AIO 更容易抽取）。")
    lines.append("4) 决策型内容优先：`X vs Y`、`Best tools for ...`、`Alternatives` 作为转化入口。")
    lines.append("5) 认知型内容做权威：数据 Hook + 引用金字塔（官方/研究/媒体/平台）。")
    lines.append("6) FAQ 写成“目标 query 句式”，并在 FAQ 里做软推荐（L3 植入）。")
    lines.append("7) 竞品对比的 Verdict 段，用 L4 植入：把 Alici 定位成“工作流层/整合层”。")
    lines.append("8) 对每个 topic_cluster 建一个“pillar page + 子文章 + 工具页”结构，避免散点爆文。")
    lines.append("9) 追踪 AIO 引用源：哪些权威站被引用最多→反推 Alici 的 citation strategy。")
    lines.append("10) 用本脚本周更：每周重跑 SERP + 抽样 Answer Engine，观察 citations 是否增加（里程碑）。")
    lines.append("")

    lines.append("## FAQ")
    lines.append("### 1) 为什么我感觉 ChatGPT 能找到 Virvid，但 SEO 工具显示很低？")
    lines.append("可能是“曝光无点击”：被引用/被总结不等于产生站内会话。也可能是 Virvid 只在小部分 query 被引用，而你刚好撞到那一部分。")
    lines.append("### 2) 这个模型输出的是“真实流量”吗？")
    lines.append("不是。它是用搜索量×CTR×排名×AIO 引用信号做的区间估算，用于比较与决策，不用于对外披露。")
    lines.append("### 3) 怎么把它变成 Alici 的真实增长？")
    lines.append("在 Alici 上做实验：同一 topic 做 2 个版本（有/无 tool 闭环 + 有/无可引用表格/FAQ），并在 GA4 看 AI referrer 与 landing page 分布。")
    lines.append("")

    out_path = out_dir / "00-brief.md"
    write_text(out_path, "\n".join(lines).rstrip() + "\n")
    return out_path


def cmd_run(args: argparse.Namespace) -> None:
    virvid_root = Path(args.virvid_root)
    out_dir = Path(args.out_dir)
    config_path = Path(args.config)

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "data").mkdir(parents=True, exist_ok=True)
    (out_dir / "data" / "raw").mkdir(parents=True, exist_ok=True)

    cfg = read_config_or_default(config_path)
    serp_cfg = SerpConfig(
        location_code=safe_int(cfg.get("location_code"), 2840),
        language_code=str(cfg.get("language_code") or "en"),
        device=str(cfg.get("device") or "desktop"),
        os=str(cfg.get("os") or "windows"),
    )

    # Agent A
    build_virvid_assets_index(virvid_root, out_dir)

    # Agent B
    build_query_universe(virvid_root, out_dir, cfg, max_queries=args.max_queries)
    query_rows = read_csv_rows(out_dir / "data" / "query_universe.csv")
    queries = [r["query"] for r in query_rows if r.get("query")]

    # DataForSEO client (online path)
    if not args.offline_build:
        username, password = read_dataforseo_creds(Path(".mcp.json"))
        client = DataForSEOClient(username, password)

        # Agent C: SERP + AIO citations
        if not args.skip_serp:
            run_serp_collection(client, out_dir, serp_cfg, queries, refresh=bool(args.refresh_serp))

        # Keyword volumes
        if not args.skip_volumes:
            run_keyword_volumes(client, out_dir, serp_cfg, queries, refresh=bool(args.refresh_volumes))
    else:
        # Offline build path: expects raw batch JSON already fetched via shell curl.
        if not args.skip_serp:
            build_serp_from_raw_batches(out_dir, serp_cfg, queries)
        if not args.skip_volumes:
            build_volumes_from_raw_batches(out_dir, queries)

    serp_rows = read_csv_rows(out_dir / "data" / "serp_features.csv")
    serp_by_query: Dict[str, Dict[str, Any]] = {r.get("query", ""): r for r in serp_rows if r.get("query")}

    vol_rows = read_csv_rows(out_dir / "data" / "query_volumes.csv")
    vol_by_query: Dict[str, int] = {
        r.get("query", ""): safe_int(r.get("search_volume"), 0) for r in vol_rows if r.get("query")
    }

    # Agent D: Answer engine test checklist (semi-manual)
    build_answer_engine_tests(out_dir, query_rows, safe_int(cfg.get("answer_engine_sample_count"), 30))

    # Agent E: Incrementality model
    build_incrementality_model(out_dir, cfg, query_rows, serp_by_query, vol_by_query)

    # Agent F: Alici gap map
    build_alici_gap_map(out_dir, query_rows, serp_by_query, vol_by_query)

    # Brief
    build_brief_md(out_dir, cfg, query_rows, serp_rows, vol_by_query)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="virvid_aeo_incremental.py")
    sub = p.add_subparsers(dest="cmd", required=True)

    runp = sub.add_parser("run", help="Run the AEO incrementality pipeline")
    runp.add_argument("--virvid-root", dest="virvid_root", default=str(DEFAULT_VIRVID_ROOT))
    runp.add_argument("--out-dir", dest="out_dir", default=str(DEFAULT_OUT_DIR))
    runp.add_argument("--config", default=str(DEFAULT_CONFIG))
    runp.add_argument("--max-queries", type=int, default=None, help="Override query_count for cheaper runs")
    runp.add_argument("--refresh-serp", action="store_true", help="Refresh SERP cache")
    runp.add_argument("--refresh-volumes", action="store_true", help="Refresh keyword volumes cache")
    runp.add_argument("--skip-serp", action="store_true", help="Skip SERP fetching (use existing cache if any)")
    runp.add_argument("--skip-volumes", action="store_true", help="Skip keyword volumes fetching (volumes=0)")
    runp.add_argument(
        "--offline-build",
        action="store_true",
        help="Do not call DataForSEO; build outputs from raw batch JSON under data/raw/",
    )
    runp.set_defaults(func=cmd_run)

    return p


def main(argv: Optional[Sequence[str]] = None) -> None:
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
