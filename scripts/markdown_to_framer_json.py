#!/usr/bin/env python3
"""
Convert AliciBlog Markdown (with YAML frontmatter) into Framer CMS JSON.

Outputs an array JSON file: 06-article-final.json
Compatible with existing preview generator: scripts/generate_framer_preview.py

Usage:
  python3 scripts/markdown_to_framer_json.py /path/to/01-article-edited.md
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple

import markdown
import yaml


def parse_markdown_file(file_path: Path) -> Tuple[Dict[str, Any], str]:
    content = file_path.read_text(encoding="utf-8")
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1]) or {}
            body = parts[2].strip()
            return frontmatter, body
    return {}, content


def markdown_to_framer_html(md_text: str) -> str:
    # Remove H1 (title lives in frontmatter)
    md_text = re.sub(r"^# .*?$", "", md_text, flags=re.MULTILINE)

    html = markdown.markdown(md_text, extensions=["tables", "fenced_code", "nl2br"])

    # H2 → <h6><strong>
    html = re.sub(r"<h2>(.*?)</h2>", r"<h6><strong>\1</strong></h6>", html)
    # H3+ → <p><strong>
    html = re.sub(r"<h3>(.*?)</h3>", r"<p><strong>\1</strong></p>", html)
    for level in range(4, 6):
        html = re.sub(fr"<h{level}>(.*?)</h{level}>", r"<p><strong>\1</strong></p>", html)

    # List items → Framer preset
    html = re.sub(r"<li>(.*?)</li>", r"<li data-preset-tag=\"p\"><p>\1</p></li>", html, flags=re.DOTALL)

    # Tables → wrap in <figure>
    html = re.sub(r"<table>", r"<figure><table><tbody>", html)
    html = re.sub(r"</table>", r"</tbody></table></figure>", html)
    html = re.sub(r"<th>(.*?)</th>", r"<th><p>\1</p></th>", html, flags=re.DOTALL)
    html = re.sub(r"<td>(.*?)</td>", r"<td><p>\1</p></td>", html, flags=re.DOTALL)

    # Images → wrap in <figure>
    html = re.sub(r"<img\s+([^>]+)>", r"<figure><img \1></figure>", html)

    # Links → new tab
    html = re.sub(r"<a\s+href=\"([^\"]+)\"", r"<a href=\"\1\" target=\"_blank\"", html)

    # Blockquotes → ensure <p>
    html = re.sub(r"<blockquote>(?!<p>)(.*?)</blockquote>", r"<blockquote><p>\1</p></blockquote>", html, flags=re.DOTALL)

    return html


def iso_date(date_str: str) -> str:
    date_str = (date_str or "").strip()
    if not date_str:
        return datetime.utcnow().strftime("%Y-%m-%dT00:00:00.000Z")
    if "T" in date_str:
        # normalize Z
        if date_str.endswith("Z"):
            return date_str.replace("Z", ".000Z") if "." not in date_str else date_str
        return date_str
    try:
        dt_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return dt_obj.strftime("%Y-%m-%dT00:00:00.000Z")
    except Exception:
        return date_str


def truncate(s: str, max_len: int) -> str:
    s = s.strip()
    if len(s) <= max_len:
        return s
    return s[: max_len - 3].rstrip() + "..."


def guess_tlnr(md_body: str) -> str:
    # prefer Quick Answer paragraph
    m = re.search(r"## Quick Answer.*?\n(.+?)(\n\n|$)", md_body, flags=re.DOTALL)
    if m:
        para = re.sub(r"\s+", " ", m.group(1)).strip()
        return truncate(para, 260)
    # fallback: first non-empty paragraph
    for chunk in md_body.split("\n\n"):
        c = re.sub(r"\s+", " ", chunk).strip()
        if not c:
            continue
        if c.startswith(("!", "#")):
            continue
        # Skip heading-only chunks (e.g., "## Title")
        if re.fullmatch(r"#+\s+.+", c):
            continue
        if c:
            return truncate(c, 260)
    return ""


def load_cover_url(article_dir: Path, frontmatter: Dict[str, Any]) -> str:
    cover_meta = article_dir / "06-cover-metadata.json"
    if cover_meta.exists():
        try:
            data = json.loads(cover_meta.read_text(encoding="utf-8"))
            cdn_url = (data.get("cdn_url") or "").strip()
            if cdn_url:
                return cdn_url
        except Exception:
            pass
    featured = frontmatter.get("featured_image") or {}
    return str((featured.get("url") or "")).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("md_file", help="Markdown file path (usually 01-article-edited.md)")
    args = parser.parse_args()

    md_path = Path(args.md_file).expanduser().resolve()
    if not md_path.exists():
        raise SystemExit(f"File not found: {md_path}")

    fm, body_md = parse_markdown_file(md_path)
    article_dir = md_path.parent

    title = str(fm.get("title") or "Untitled").strip()
    slug = str(fm.get("slug") or "").strip()
    category = str(fm.get("category") or "tutorial").strip()
    tags = fm.get("tags") or []
    if isinstance(tags, list):
        tag_str = ", ".join(str(t) for t in tags)
    else:
        tag_str = str(tags)

    cover_url = load_cover_url(article_dir, fm)
    if not cover_url:
        cover_url = "placeholder"

    html = markdown_to_framer_html(body_md)
    word_count = len(re.findall(r"\b\w+\b", body_md))
    read_time = f"{max(1, int(math.ceil(word_count / 200)))} min"

    meta_title = truncate(str(fm.get("meta_title") or title), 60)
    meta_description = truncate(str(fm.get("meta_description") or ""), 160)
    tlnr = guess_tlnr(body_md)

    sub_title = str(fm.get("sub_title") or "").strip()

    # CTA mapping (default): keep a stable alici.ai landing page unless overridden.
    cta_link = str(fm.get("CTA_alici_link") or "https://alici.ai/video-super-agent").strip()
    cta_button = str(fm.get("CTA button") or "Try Video Super Agent").strip()

    out = [
        {
            "Slug": slug or re.sub(r"-{2,}", "-", re.sub(r"[^a-z0-9]+", "-", title.lower())).strip("-"),
            "title": title,
            "sub_title": sub_title,
            "TLNR": tlnr,
            "cover": {"url": cover_url},
            "Date": iso_date(str(fm.get("date") or "")),
            "read_time": read_time,
            "main_category": category,
            "recommend_category": "",
            "article_body_content": html,
            "CTA_alici_link": cta_link,
            "CTA button": cta_button,
            "meta_title": meta_title,
            "meta_description": meta_description,
            "tag_for_SEO": tag_str,
        }
    ]

    out_path = article_dir / "06-article-final.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(str(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
