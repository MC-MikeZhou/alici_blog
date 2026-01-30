#!/usr/bin/env python3
"""
Thumbnail Mode - Step 1 Initializer

Creates a project directory under `reports 待发文章/YYYY-MM-DD-{topic-or-batch}`
and archives provided sources for offline viewing:
 - Web pages → Markdown via r.jina.ai + local assets
 - YouTube → transcript.json (Supadata) + metadata.json + thumbnails/

Usage:
  python3 scripts/thumbnail_init.py --name 2026-01-29-vidiq-youtube-thumbnail-design-tips \
    --urls "https://vidiq.com/blog/post/youtube-thumbnail-design-tips/" \
           "https://www.youtube.com/watch?v=dB6DXcZo6hE"

Notes:
 - SUPADATA_API_KEY is read from environment or .env file at repo root.
 - YOUTUBE_API_KEY optional; falls back to oEmbed if missing.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen, Request

REPO_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = REPO_ROOT / "reports 待发文章"

# Some sources (and r.jina.ai) can block Python's default HTTP stack.
# We keep urllib as the default, but fall back to curl when needed.
# Note: r.jina.ai can be surprisingly picky about User-Agent strings.
# "Mozilla/5.0" is a safe, low-friction default here.
BROWSER_UA = "Mozilla/5.0"


def read_env(key: str) -> Optional[str]:
    # Prefer environment variable
    val = os.environ.get(key)
    if val:
        return val
    # Fallback to .env file in repo root
    env_path = REPO_ROOT / ".env"
    if env_path.exists():
        try:
            for line in env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    if k.strip() == key:
                        return v.strip().strip('"')
        except Exception:
            pass
    return None


def http_get(url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 30) -> bytes:
    # Prefer urllib, fallback to curl on common blocks (403/503).
    base_headers = {
        "User-Agent": os.environ.get("THUMBNAIL_INIT_USER_AGENT", BROWSER_UA),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    }
    if headers:
        base_headers.update(headers)
    try:
        req = Request(url, headers=base_headers)
        with urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except Exception as e:
        # curl fallback: -L follow redirects; -f fail on 4xx/5xx
        try:
            return subprocess.check_output(
                [
                    "curl",
                    "-sS",
                    "-L",
                    "-f",
                    "-A",
                    base_headers["User-Agent"],
                    url,
                ],
                stderr=subprocess.STDOUT,
                timeout=timeout,
            )
        except Exception:
            raise e


def is_youtube_url(url: str) -> bool:
    return any(h in url for h in ["youtube.com", "youtu.be"])


def extract_video_id(url: str) -> Optional[str]:
    # Supports watch/shorts/embed/youtu.be
    u = urlparse(url)
    if u.netloc.endswith("youtu.be"):
        vid = u.path.strip("/")
        return vid if vid else None
    if "/shorts/" in u.path:
        return u.path.rsplit("/", 1)[-1]
    if "/embed/" in u.path:
        return u.path.rsplit("/", 1)[-1]
    qs = parse_qs(u.query)
    if "v" in qs and qs["v"]:
        return qs["v"][0]
    # Fallback regex
    m = re.search(r"([0-9A-Za-z_-]{11})", url)
    return m.group(1) if m else None


def jina_markdown(url: str) -> str:
    # Use https://r.jina.ai/<url>
    # Normalize to https scheme
    if url.startswith("http://"):
        url_https = "https://" + url[len("http://"):]
    else:
        url_https = url
    jina_url = f"https://r.jina.ai/{url_https}"
    # Retry a few times; r.jina.ai sometimes rate-limits.
    last_err: Optional[Exception] = None
    for i in range(4):
        try:
            data = http_get(jina_url, timeout=45)
            txt = data.decode("utf-8", errors="replace")
            # When blocked, r.jina.ai sometimes returns an HTML "403 Forbidden" page.
            if "403 Forbidden" in txt and "<title>403</title>" in txt:
                raise RuntimeError("r.jina.ai returned 403 HTML page")
            if "Service Unavailable" in txt and "<title>" in txt:
                raise RuntimeError("r.jina.ai returned Service Unavailable HTML page")
            return txt
        except Exception as e:
            last_err = e
            time.sleep(1.5 * (i + 1))
    raise RuntimeError(f"Failed to fetch markdown via r.jina.ai: {url}: {last_err}")


def sanitize_filename(name: str) -> str:
    # Keep alnum, dash, underscore, dot; replace others with '-'
    name = re.sub(r"[^A-Za-z0-9._-]", "-", name)
    name = re.sub(r"-+", "-", name).strip("-")
    return name or "file"


def extract_image_urls_from_md(md: str) -> List[str]:
    urls: List[str] = []
    # Markdown image: ![alt](url)
    for m in re.finditer(r"!\[[^\]]*\]\((https?://[^)\s]+)\)", md):
        urls.append(m.group(1))
    # Also handle <img src="...">
    for m in re.finditer(r"<img[^>]+src=\"(https?://[^\">\s]+)\"", md, re.IGNORECASE):
        urls.append(m.group(1))
    # Deduplicate preserving order
    seen = set()
    out = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def download_to(path: Path, url: str) -> bool:
    try:
        data = http_get(url, timeout=45)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return True
    except Exception:
        return False


def rewrite_md_images(md: str, mapping: Dict[str, str]) -> str:
    # Replace only exact URL occurrences from mapping keys
    for src, rel in mapping.items():
        md = md.replace(src, rel)
    return md


def handle_web(url: str, base_dir: Path) -> Dict[str, str]:
    """Fetch web page as Markdown and local assets.
    Returns dict with keys: type, url, dir, content_md, assets
    """
    print(f"[web] Fetching Markdown via r.jina.ai: {url}")
    md = jina_markdown(url)
    content_md_path = base_dir / "content.md"
    content_md_path.write_text(md, encoding="utf-8")

    # Extract and download images
    imgs = extract_image_urls_from_md(md)
    mapping: Dict[str, str] = {}
    assets_dir = base_dir / "assets"
    downloaded = []
    for i, img_url in enumerate(imgs, 1):
        # derive filename
        parsed = urlparse(img_url)
        fname = sanitize_filename(Path(parsed.path).name or f"image-{i}.png")
        # If filename is too generic or missing ext, prefix index
        if not re.search(r"\.[A-Za-z0-9]{2,5}$", fname):
            fname = f"{i:02d}-" + fname + ".png"
        target = assets_dir / fname
        ok = download_to(target, img_url)
        if ok:
            rel = f"assets/{fname}"
            mapping[img_url] = rel
            downloaded.append(rel)
    # Rewrite content.md if any assets downloaded
    if mapping:
        new_md = rewrite_md_images(md, mapping)
        content_md_path.write_text(new_md, encoding="utf-8")

    return {
        "type": "web",
        "url": url,
        "dir": str(base_dir),
        "content_md": str(content_md_path),
        "assets": json.dumps(downloaded, ensure_ascii=False),
    }


def supadata_transcript(video_id: str, api_key: Optional[str]) -> Optional[dict]:
    if not api_key:
        return None
    url = f"https://api.supadata.ai/v1/youtube/transcript?videoId={video_id}"
    try:
        data = http_get(url, headers={"x-api-key": api_key})
        return json.loads(data.decode("utf-8", errors="replace"))
    except Exception:
        return None


def youtube_metadata_v3(video_id: str, api_key: Optional[str]) -> Optional[dict]:
    if not api_key:
        return None
    url = (
        "https://www.googleapis.com/youtube/v3/videos"
        f"?part=snippet,contentDetails,statistics&id={video_id}&key={api_key}"
    )
    try:
        data = http_get(url)
        meta = json.loads(data.decode("utf-8", errors="replace"))
        return meta
    except Exception:
        return None


def youtube_oembed(video_id: str) -> Optional[dict]:
    # Fallback without API key
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    try:
        data = http_get(url)
        return json.loads(data.decode("utf-8", errors="replace"))
    except Exception:
        return None


def download_thumbnails(video_id: str, thumbs_dir: Path) -> List[str]:
    thumbs_dir.mkdir(parents=True, exist_ok=True)
    variants = [
        "maxresdefault.jpg",
        "sddefault.jpg",
        "hqdefault.jpg",
        "mqdefault.jpg",
        "default.jpg",
    ]
    saved: List[str] = []
    for v in variants:
        url = f"https://i.ytimg.com/vi/{video_id}/{v}"
        target = thumbs_dir / v
        if download_to(target, url):
            saved.append(str(target))
    return saved


def handle_youtube(url: str, base_dir: Path, supa_key: Optional[str], yt_key: Optional[str]) -> Dict[str, str]:
    vid = extract_video_id(url)
    if not vid:
        raise RuntimeError(f"Cannot extract videoId from {url}")
    print(f"[yt] videoId={vid}")

    # transcript
    tr_json = supadata_transcript(vid, supa_key)
    transcript_path = base_dir / "transcript.json"
    if tr_json is not None:
        transcript_path.write_text(json.dumps(tr_json, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        transcript_path.write_text(json.dumps({"error": "transcript_unavailable"}), encoding="utf-8")

    # metadata
    meta = youtube_metadata_v3(vid, yt_key)
    used = "youtube_v3"
    if meta is None:
        meta = youtube_oembed(vid) or {"error": "metadata_unavailable"}
        used = "oembed"
    metadata_path = base_dir / "metadata.json"
    metadata_path.write_text(json.dumps({"source": used, "data": meta}, ensure_ascii=False, indent=2), encoding="utf-8")

    # thumbnails
    saved_thumbs = download_thumbnails(vid, base_dir / "thumbnails")

    return {
        "type": "youtube",
        "url": url,
        "dir": str(base_dir),
        "video_id": vid,
        "transcript": str(transcript_path),
        "metadata": str(metadata_path),
        "thumbnails": json.dumps(saved_thumbs, ensure_ascii=False),
    }


def make_source_dir(parent: Path, url: str) -> Path:
    if is_youtube_url(url):
        vid = extract_video_id(url) or "unknown"
        return parent / f"yt-{vid}"
    # web
    u = urlparse(url)
    domain = (u.hostname or "web").split(":")[0]
    domain_base = domain.split(".")[-2] if "." in domain else domain
    slug = Path(u.path).name or "index"
    slug = re.sub(r"[^a-zA-Z0-9-]", "-", slug.lower())[:40] or "page"
    return parent / f"web-{domain_base}-{slug}"


def append_implementation_log(proj_dir: Path, name: str, urls: List[str], sources: List[Dict[str, str]]):
    path = proj_dir / "00-implementation.md"
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    operator = os.environ.get("USER") or os.environ.get("USERNAME") or "unknown"
    lines = [
        f"# Thumbnail Mode Init Log\n",
        f"Time: {ts}\n",
        f"Operator: {operator}\n",
        f"Project: {name}\n",
        f"Sources:\n",
    ]
    for s in sources:
        lines.append(f"- {s.get('type')}: {s.get('url')} → {s.get('dir')}\n")
    lines.append("\n")
    if path.exists():
        with path.open("a", encoding="utf-8") as f:
            f.write("\n".join(lines))
    else:
        with path.open("w", encoding="utf-8") as f:
            f.write("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(description="Thumbnail Mode Step 1 Initializer")
    parser.add_argument("--name", required=True, help="Project directory name under 'reports 待发文章/'")
    parser.add_argument("--urls", nargs="+", required=True, help="One or more source URLs")
    args = parser.parse_args()

    proj_name = args.name.strip()
    urls = args.urls

    # Prepare directories
    proj_dir = REPORTS_DIR / proj_name
    sources_dir = proj_dir / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)

    # Load keys
    supa_key = read_env("SUPADATA_API_KEY")
    yt_key = read_env("YOUTUBE_API_KEY")

    results: List[Dict[str, str]] = []

    for url in urls:
        sdir = make_source_dir(sources_dir, url)
        sdir.mkdir(parents=True, exist_ok=True)
        try:
            if is_youtube_url(url):
                res = handle_youtube(url, sdir, supa_key, yt_key)
            else:
                res = handle_web(url, sdir)
            results.append(res)
            print(f"[ok] {url} archived → {sdir}")
        except Exception as e:
            print(f"[error] {url}: {e}")

    append_implementation_log(proj_dir, proj_name, urls, results)
    print(f"\n✅ Init complete: {proj_dir}")


if __name__ == "__main__":
    main()
