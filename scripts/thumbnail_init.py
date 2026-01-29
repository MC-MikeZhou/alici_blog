#!/usr/bin/env python3
"""
Thumbnail Mode – Step 1 initializer (v0.1)

Creates a project directory under `reports 待发文章/` with a suggested name,
sets up source subfolders for each input URL, and writes a 00-implementation.md
log plus a minimal 01-article-draft.md placeholder (structure-only).

Notes
- Network fetching is NOT performed here (repo CI often restricts network).
  The script writes fetch.log files with recommended commands you can run
  manually (wget/curl for web; transcript tool for YouTube) and records
  what remains to be done.

Usage examples
- Interactive (user must choose a name; agent only suggests):
    python3 scripts/thumbnail_init.py https://www.youtube.com/watch?v=dQw4w9WgXcQ

- Non-interactive (user-decided name is required):
    python3 scripts/thumbnail_init.py --name 2026-01-29-youtube-thumbnail-0-to-1 \
        https://www.youtube.com/watch?v=dQw4w9WgXcQ https://alici.ai/blog/thumbnail

"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple


REPORTS_ROOT = Path("reports 待发文章")


def now_iso() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def today_str() -> str:
    return dt.date.today().isoformat()


def slugify(text: str, max_len: int = 30) -> str:
    text = text.lower()
    # Replace non-alphanumeric with dashes
    text = re.sub(r"[^a-z0-9]+", "-", text)
    # Collapse multiple dashes
    text = re.sub(r"-+", "-", text).strip("-")
    # Trim length
    if len(text) > max_len:
        text = text[:max_len].rstrip("-")
    # Enforce minimal length
    if len(text) < 3:
        text = (text + "-xxx")[:3]
    return text


def parse_domain(url: str) -> str:
    m = re.match(r"^https?://([^/]+)/?", url)
    if not m:
        return "unknown"
    domain = m.group(1).lower()
    # Keep registrable part (rough heuristic)
    parts = domain.split(":")[0].split(".")
    if len(parts) >= 2:
        return ".".join(parts[-2:])
    return parts[0]


def parse_path_slug(url: str, max_len: int = 20) -> str:
    # Prefer last non-empty path segment
    m = re.match(r"^https?://[^/]+/(.*)$", url)
    if not m:
        return "page"
    path = m.group(1).split("?")[0].strip("/")
    if not path:
        return "home"
    segs = [s for s in path.split("/") if s]
    if not segs:
        return "home"
    return slugify(segs[-1], max_len=max_len)


def is_youtube(url: str) -> bool:
    return bool(re.search(r"(youtube\.com|youtu\.be)", url, re.I))


def parse_youtube_id(url: str) -> str | None:
    # Support watch, share, embed
    # watch?v=ID
    m = re.search(r"[?&]v=([\w-]{6,})", url)
    if m:
        return m.group(1)
    # youtu.be/ID
    m = re.search(r"youtu\.be/([\w-]{6,})", url)
    if m:
        return m.group(1)
    # embed/ID
    m = re.search(r"/embed/([\w-]{6,})", url)
    if m:
        return m.group(1)
    return None


def suggest_names(urls: List[str]) -> Tuple[str, str, str]:
    d = today_str()
    # Derive short topic from first URL path or youtube id
    first = urls[0]
    short_topic = "thumbnail"
    if is_youtube(first):
        vid = parse_youtube_id(first) or "video"
        short_topic = f"youtube-{vid[:6]}"
    else:
        # try using last path segment as topic
        seg = parse_path_slug(first, max_len=30)
        short_topic = seg or "thumbnail"

    # Normalize to a nicer topic slug: keep 2-4 keywords if possible
    short_topic = slugify(short_topic, max_len=30)
    if not short_topic.startswith("thumbnail"):
        short_topic = f"{short_topic}"

    # Choice 1: YYYY-MM-DD-thumbnail-{short-topic}
    c1 = f"{d}-thumbnail-{short_topic}"

    # Choice 2: YYYY-MM-DD-{source}-{short-topic}
    if is_youtube(first):
        source = "youtube"
    else:
        source = parse_domain(first).split(":")[0]
    c2 = f"{d}-{source}-{short_topic}"

    # Choice 3: batch if multiple URLs
    if len(urls) >= 2:
        c3 = f"{d}-batch-{len(urls)}"
    else:
        c3 = f"{d}-{short_topic}"
    return c1, c2, c3


def ensure_unique_name(base: str) -> str:
    """Ensure the final directory name under REPORTS_ROOT is unique.
    Tries -2, -3, ... then falls back to adding -HHmm if needed.
    """
    parent = REPORTS_ROOT
    name = base
    idx = 2
    while (parent / name).exists():
        trial = f"{base}-{idx}"
        if not (parent / trial).exists():
            name = trial
            break
        idx += 1
        # Hard stop: after 9 attempts, add HHmm
        if idx > 9:
            hhmm = dt.datetime.now().strftime("%H%M")
            name = f"{base}-{hhmm}"
            break
    return name


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def make_web_source(root: Path, url: str) -> None:
    domain = parse_domain(url)
    slug = parse_path_slug(url, max_len=20)
    d = root / f"web-{domain}-{slug}"
    d.mkdir(parents=True, exist_ok=True)

    # Placeholders
    write_file(d / "raw.html", "<!-- To be fetched via curl -L ... -->\n")
    (d / "page_complete").mkdir(exist_ok=True)

    metadata = {
        "title": None,
        "description": None,
        "lang": None,
        "canonical": None,
        "og": {},
        "author": None,
        "published": None,
        "modified": None,
        "images": [],
        "source_url": url,
        "fetched_at": None,
    }
    write_file(d / "metadata.json", json.dumps(metadata, ensure_ascii=False, indent=2))

    fetch_log = f"""
[{now_iso()}] INIT ONLY (no network fetch performed)
URL: {url}
Recommended manual fetch commands:
  # Full page with assets (local mirror)
  wget --convert-links --page-requisites --adjust-extension --span-hosts \
       --no-parent -e robots=off -U "Mozilla/5.0" -P page_complete \
       "{url}"

  # Raw HTML snapshot
  curl -L -sS -H 'User-Agent: Mozilla/5.0' "{url}" > raw.html

After fetching, update metadata.json (title/og/author etc.) and set fetched_at.
""".strip() + "\n"
    write_file(d / "fetch.log", fetch_log)


def make_yt_source(root: Path, url: str) -> None:
    vid = parse_youtube_id(url) or "video"
    d = root / f"yt-{vid}"
    d.mkdir(parents=True, exist_ok=True)
    (d / "thumbnails").mkdir(exist_ok=True)

    transcript = {
        "video_id": vid,
        "source_url": url,
        "segments": [],
        "fetched_at": None,
        "notes": "Populate via youtube_transcript_fetcher or Supadata."
    }
    write_file(d / "transcript.json", json.dumps(transcript, ensure_ascii=False, indent=2))

    metadata = {
        "video_id": vid,
        "title": None,
        "channel": None,
        "published_at": None,
        "description": None,
        "duration": None,
        "source_url": url,
        "fetched_at": None,
    }
    write_file(d / "metadata.json", json.dumps(metadata, ensure_ascii=False, indent=2))

    fetch_log = f"""
[{now_iso()}] INIT ONLY (no network fetch performed)
URL: {url}
Recommended next steps:
  # 1) Fetch transcript (choose one):
  - python3 scripts/youtube_transcript_fetcher.py --video "{vid}" --output "transcript.json"
    (You may need to modify the script to support custom output path.)

  # 2) Save video thumbnails (max res) to ./thumbnails/
  - Manually download from: https://img.youtube.com/vi/{vid}/maxresdefault.jpg
  - Or fetch variants: default.jpg, hqdefault.jpg, mqdefault.jpg, sddefault.jpg

  # 3) Fill metadata.json with title/channel/publish date once available.
""".strip() + "\n"
    write_file(d / "fetch.log", fetch_log)


def draft_placeholder() -> str:
    return (
        "# TITLE — Thumbnail Patterns (2026)\n\n"
        "## Key Takeaways\n"
        "- [Placeholder] 3–5 rules (e.g., main copy ≤ 4 words; subject covers 40–60% of frame)\n"
        "- [Placeholder] Strong contrast, low information density, maximize legibility\n\n"
        "## Source Attribution / About This Guide\n"
        "Based on [Source: link]. Disclosure: alici.ai did not independently verify all results; performance varies by material and audience.\n\n"
        "## Thumbnail Pattern Catalog\n"
        "### Pattern A — [Name]\n"
        "Why it works: ...\n\n"
        "When to use: ...\n\n"
        "Text limit: ...\n\n"
        "Pitfalls: ...\n\n"
        "### Pattern B — [Name]\n\n"
        "## Case Grid (optional)\n\n"
        "## How to Try\n"
        "1) Pick a pattern → 2–4 word copy → subject-background contrast → 10–15% scale check\n\n"
        "## Mini FAQ\n\n"
        "## Final Advice\n"
        "Start with 1–2 patterns and A/B test; aim for integrator posture (L4).\n"
    )


def write_implementation_md(project_dir: Path, urls: List[str], final_name: str, name_candidates: Tuple[str, str, str], name_source: str) -> None:
    content = [
        f"# 00-implementation.md — Thumbnail Mode Init\n",
        f"CreatedAt: {now_iso()}\n",
        f"ProjectDir: {project_dir}\n",
        f"Operator: thumbnail_init.py\n",
        f"NameSource: {name_source}\n",
        "\n",
        "## Inputs (URLs)\n",
        *(f"- {u}\n" for u in urls),
        "\n",
        "## Name Candidates (for traceability)\n",
        f"- 1) {name_candidates[0]}\n",
        f"- 2) {name_candidates[1]}\n",
        f"- 3) {name_candidates[2]}\n",
        "\n",
        "## Next Steps\n",
        "- Fetch web pages (wget/curl) or transcripts/metadata for YouTube.\n",
        "- Fill source metadata.json files (title/og/author or video title/channel).\n",
        "- Proceed to Step 2 questionnaire and Step 3 extraction.\n",
    ]
    write_file(project_dir / "00-implementation.md", "".join(content))


def build_confirmed_brief_json(urls: List[str]) -> dict:
    # Minimal baseline aligned with thumbnail.md (rewrite_mode mapping)
    return {
        "mode": "thumbnail_rewrite_baseline",
        "rewrite_mode": {
            "enabled": True,
            "reference_ratio": 0.8,
            "word_count_ratio": [0.8, 1.2],
            "brand_swap": "Alici AI",
            "lock_pattern_catalog": True,
            "lock_design_rules": True,
            "no_fabricated_metrics": True,
        },
        "validation": {
            "check_pattern_set_match": True,
            "check_word_count_range": True,
            "check_claim_accuracy": True,
            "strict": True,
        },
        "inputs": urls,
        "created_at": now_iso(),
    }


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="Initialize Thumbnail Mode project directory and sources")
    parser.add_argument("urls", nargs="+", help="One or more source URLs (web or YouTube)")
    parser.add_argument("--name", dest="name", default=None, help="Project directory name under 'reports 待发文章/' (user-decided; required for non-interactive usage)")
    args = parser.parse_args(argv)

    urls = args.urls
    # Ensure reports root exists
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)

    # Determine project name
    final_name: str
    c1, c2, c3 = suggest_names(urls)
    if args.name:
        base = slugify(args.name, max_len=60)
        final_name = ensure_unique_name(base)
        name_source = "user-provided --name"
    else:
        # Interactive: user must explicitly choose; agent only suggests
        print("Detected material. Suggested directory names (you decide):")
        print(f"  1) {c1}")
        print(f"  2) {c2}")
        print(f"  3) {c3}")
        base = None
        for _ in range(3):
            choice = input("Choose 1/2/3 or enter custom (slug), leave empty to retry: ").strip()
            if choice == "1":
                base = c1
                break
            elif choice == "2":
                base = c2
                break
            elif choice == "3":
                base = c3
                break
            elif choice:
                base = slugify(choice, max_len=60)
                break
            else:
                print("A project name is required. Please choose or type a custom slug.")
        if not base:
            print("No project name chosen. Aborting without creating files.")
            return 1
        final_name = ensure_unique_name(base)
        name_source = "user-chosen (interactive)"

    project_dir = REPORTS_ROOT / final_name
    sources_dir = project_dir / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)

    # For each URL, create a scoped source folder
    for url in urls:
        if is_youtube(url):
            make_yt_source(sources_dir, url)
        else:
            make_web_source(sources_dir, url)

    # Write logs and placeholders
    write_implementation_md(project_dir, urls, final_name, (c1, c2, c3), name_source)
    write_file(project_dir / "01-article-draft.md", draft_placeholder())
    brief = build_confirmed_brief_json(urls)
    write_file(project_dir / "00-confirmed-brief.json", json.dumps(brief, ensure_ascii=False, indent=2))

    print(f"Initialized: {project_dir}")
    print("Sources:")
    for child in sorted(sources_dir.iterdir()):
        if child.is_dir():
            print(f"  - {child.relative_to(project_dir)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
