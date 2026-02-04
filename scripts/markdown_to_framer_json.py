#!/usr/bin/env python3
"""
Markdown → Framer CMS JSON (v1.3-compatible minimal converter)
 - Reads Markdown with YAML frontmatter
 - Integrates 06-cover-metadata.json for cover.url
 - Converts body to Framer-compatible HTML (no <figure> for <img>, alt before src)
 - Replaces selected image placeholders with generated CDN URLs
 - Outputs array JSON to 06-article-final.json
"""

import os
import re
import sys
import argparse
import json
import math
from pathlib import Path
from datetime import datetime

import yaml
import markdown


def read_markdown(path: Path):
    text = path.read_text(encoding='utf-8')
    fm = {}
    body = text
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            fm = yaml.safe_load(parts[1]) or {}
            body = parts[2].strip()
    return fm, body


def sanitize_slug(s: str) -> str:
    s = s.lower()
    s = re.sub(r'[^a-z0-9\-]+', '-', s)
    s = re.sub(r'-{2,}', '-', s).strip('-')
    return s


def derive_slug_from_dir(article_dir: Path) -> str:
    # directory name like: 2026-01-28-youtube-thumbnail-0-to-1_副本
    name = article_dir.name
    # remove date prefix
    m = re.match(r'\d{4}-\d{2}-\d{2}-(.+)', name)
    base = m.group(1) if m else name
    # remove non-ascii suffix (like _副本)
    base = re.sub(r'[^a-zA-Z0-9\-]+', '-', base)
    return sanitize_slug(base)


def md_to_framer_html(md_text: str) -> str:
    # Remove top-level H1 lines
    md_text = re.sub(r'^# .*$', '', md_text, flags=re.MULTILINE)

    # Remove the first markdown image only when it is explicitly marked as a hero image.
    # Framer uses `cover.url` as the hero; we should not drop the first inline image by accident.
    first_img = re.search(r'^\s*!\[(?P<alt>[^\]]*)\]\((?P<src>[^)]+)\)\s*$', md_text, flags=re.MULTILINE)
    if first_img and re.search(r'\bhero\b', first_img.group('alt') or '', flags=re.IGNORECASE):
        md_text = re.sub(r'^\s*!\[[^\]]*\]\([^)]+\)\s*\n?', '', md_text, count=1, flags=re.MULTILINE)

    html = markdown.markdown(
        md_text,
        extensions=['tables', 'fenced_code', 'nl2br']
    )

    # Links: add target="_blank"
    html = re.sub(r'<a\s+href="([^"]+)"', r'<a href="\1" target="_blank"', html)

    # Headings:
    # - H3-H6 → <p><strong>...</strong></p>
    # - H2 → <h6><strong>...</strong></h6>
    #
    # Order matters: convert H3-H6 first so our H2->H6 output isn't re-processed.
    for level in range(3, 7):
        html = re.sub(
            fr'<h{level}[^>]*>(.*?)</h{level}>',
            r'<p><strong>\1</strong></p>',
            html,
            flags=re.DOTALL
        )
    html = re.sub(
        r'<h2[^>]*>(.*?)</h2>',
        r'<h6><strong>\1</strong></h6>',
        html,
        flags=re.DOTALL
    )

    # Lists: <li> → add data-preset-tag and wrap in <p>
    html = re.sub(r'<li>(.*?)</li>', r'<li data-preset-tag="p"><p>\1</p></li>', html, flags=re.DOTALL)

    # Ensure <img> format: no <figure>, and alt before src
    # Remove any wrapping <figure> that markdown might produce (it doesn't by default)
    html = html.replace('<figure>', '').replace('</figure>', '')

    # Reorder attributes in <img ...>
    def reorder_img(m):
        attrs = m.group(1)
        # capture src and alt
        src_m = re.search(r'src=\"(.*?)\"', attrs)
        alt_m = re.search(r'alt=\"(.*?)\"', attrs)
        src = src_m.group(1) if src_m else ''
        alt = alt_m.group(1) if alt_m else ''
        # other attrs
        others = re.sub(r'(src=\".*?\"|alt=\".*?\")', '', attrs).strip()
        parts = [f'alt="{alt}"', f'src="{src}"']
        if others:
            parts.append(others)
        return '<img ' + ' '.join(parts) + '>'

    html = re.sub(r'<img\s+([^>]+)>', reorder_img, html)

    # Replace em dash
    html = html.replace('—', ' - ')

    return html


def extract_tlnr(md_body: str) -> str:
    """
    TLNR (Too Long; Not Reading):
    Prefer extracting from the explicit DIRECT_ANSWER block if present; otherwise
    take the first real paragraph (skip hero image, headings, lists).
    """
    body = re.sub(r'^# .*$', '', md_body, flags=re.MULTILINE).strip()

    # 1) Prefer explicit DIRECT_ANSWER block
    m = re.search(r'<!--\s*DIRECT_ANSWER\s*-->(.*?)<!--\s*/DIRECT_ANSWER\s*-->', body, flags=re.DOTALL)
    if m:
        t = m.group(1)
        # Strip markdown links/images and collapse whitespace
        t = re.sub(r'!\[.*?\]\(.*?\)', '', t)
        t = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', t)
        t = re.sub(r'`([^`]+)`', r'\1', t)
        t = re.sub(r'\s+', ' ', t).strip()
        return t[:300]

    # 2) Fallback: first paragraph that isn't an image/list/heading
    paras = [p.strip() for p in body.split('\n\n') if p.strip()]
    for p in paras:
        if p.startswith('!['):
            continue
        if p.startswith(('#', '-', '*', '1)', '1.')):
            continue
        t = re.sub(r'\s+', ' ', p).strip()
        if len(t) >= 50:
            return t[:300]
    return ''


def compute_read_time(md_body: str) -> str:
    # Rough estimate: 800 Chinese chars/min or 200 words/min
    # use characters
    chars = len(re.sub(r'\s+', '', md_body))
    minutes = max(4, math.ceil(chars / 800))
    return f"{minutes} min"


def replace_placeholders_with_images(md_body: str, mapping: dict) -> str:
    # mapping: {index0_based: url}
    lines = md_body.splitlines()
    count = 0
    for i, line in enumerate(lines):
        if re.search(r'!\[.*?\]\(placeholder\)', line):
            if count in mapping:
                url = mapping[count]
                # keep original alt text
                alt = re.sub(r'^.*!\[(.*?)\]\(placeholder\).*$', r'\1', line)
                lines[i] = re.sub(r'!\[.*?\]\(placeholder\)', f'![{alt}]({url})', line)
            count += 1
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description="Markdown → Framer CMS JSON")
    parser.add_argument("markdown_file", help="Path to the Markdown file")
    parser.add_argument(
        "--out",
        dest="out_path",
        default=None,
        help="Output JSON path (default: <article_dir>/06-article-final.json)",
    )
    args = parser.parse_args()

    md_path = Path(args.markdown_file)
    article_dir = md_path.parent

    fm, md_body = read_markdown(md_path)

    # Optional placeholder replacement mapping (by occurrence order).
    # If your project uses `!(...)(placeholder)` images, pass explicit image URLs
    # in markdown instead of relying on this mapping.
    md_body_replaced = md_body

    # Cover URL from 06-cover-metadata.json
    cover_meta_path = article_dir / '06-cover-metadata.json'
    cover_url = ''
    if cover_meta_path.exists():
        try:
            cover_url = json.loads(cover_meta_path.read_text(encoding='utf-8')).get('cdn_url', '')
        except Exception:
            cover_url = ''
    if not cover_url:
        cover_url = (fm.get('featured_image') or {}).get('url', '')
    if not cover_url:
        print('❌ Missing cover image URL (06-cover-metadata.json or frontmatter.featured_image.url)')
        sys.exit(2)

    # Slug
    slug = fm.get('slug') or derive_slug_from_dir(article_dir)

    # Main category mapping
    cat = (fm.get('category') or 'tutorial').lower()
    if cat in ['how-to', 'guide']:
        main_category = 'tutorial'
    elif cat in ['list', 'comparison', 'best', 'top']:
        main_category = 'list'
    elif cat in ['news', 'announcement', 'update']:
        main_category = 'news'
    else:
        main_category = 'tutorial'

    # Title/meta
    title = fm.get('title', 'Untitled')
    meta_title = title[:60]
    tlnr = extract_tlnr(md_body_replaced)
    meta_description = (tlnr[:157] + '...') if len(tlnr) > 160 else tlnr
    # Sub title: 优先 frontmatter，回退中文默认
    sub_title = fm.get('sub_title') or '从添加到表达：小屏可读的一页工作流'

    # Body HTML
    article_html = md_to_framer_html(md_body_replaced)

    # Date & read_time
    # Prefer frontmatter date when present, else fallback to today.
    fm_date = (fm.get('date') or '').strip()
    if re.match(r'^\d{4}-\d{2}-\d{2}$', fm_date):
        iso_date = f"{fm_date}T00:00:00.000Z"
    elif re.match(r'^\d{4}-\d{2}-\d{2}T', fm_date):
        iso_date = fm_date
    else:
        iso_date = datetime.utcnow().strftime('%Y-%m-%dT00:00:00.000Z')
    # Prefer frontmatter read_time when present and already formatted like "12 min".
    fm_read_time = (fm.get('read_time') or '').strip()
    if re.match(r'^\d+\s+min$', fm_read_time):
        read_time = fm_read_time
    else:
        read_time = compute_read_time(md_body_replaced)

    # CTA: 优先读取 frontmatter，其次使用统一产品链接
    cta_link = (fm.get('CTA_alici_link') or '').strip()
    cta_button = (fm.get('CTA button') or '').strip()
    if not cta_link:
        # Keyword-based fallback (image vs video). Keep conservative defaults.
        title_lower = (fm.get('title') or '').lower()
        tags_lower = [str(t).lower() for t in (fm.get('tags') or [])]
        haystack = ' '.join([title_lower] + tags_lower)
        if any(k in haystack for k in ['image', 'ai image', 'text-in-image', 'portrait', 'nano banana']):
            cta_link = 'https://app.alici.ai/pages/imageGen'
            cta_button = cta_button or 'Generate AI Images Free'
        else:
            cta_link = 'https://app.alici.ai/'
            cta_button = cta_button or 'Try alici.ai Free'
    if not cta_button:
        cta_button = 'Try alici.ai Free'

    obj = {
        "Slug": slug,
        "title": title,
        "sub_title": sub_title,
        "TLNR": tlnr,
        "cover": {"url": cover_url},
        "Date": iso_date,
        "read_time": read_time,
        "main_category": main_category,
        "recommend_category": "",
        "article_body_content": article_html,
        "CTA_alici_link": cta_link,
        "CTA button": cta_button,
        "meta_title": meta_title,
        "meta_description": meta_description,
        "tag_for_SEO": ', '.join((fm.get('tags') or []) or [])
    }

    out_path = Path(args.out_path) if args.out_path else (article_dir / '06-article-final.json')
    out_path.write_text(json.dumps([obj], ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"✅ Framer JSON written: {out_path}")


if __name__ == '__main__':
    main()
