#!/usr/bin/env python3
"""
Framer Preview Generator
Converts Markdown articles to Framer CMS-compatible preview HTML
"""

import sys
import os
import re
import json
from pathlib import Path
from datetime import datetime
import markdown
import yaml

def strip_duplicate_cover(body_html: str, cover_url: str) -> str:
    """Remove the first cover image if it also appears in the body."""
    if not cover_url:
        return body_html
    cover_re = re.escape(cover_url)
    patterns = [
        re.compile(r'<p>\s*<img[^>]*src="' + cover_re + r'"[^>]*>\s*</p>', re.IGNORECASE),
        re.compile(r'<figure>\s*<img[^>]*src="' + cover_re + r'"[^>]*>\s*</figure>', re.IGNORECASE),
        re.compile(r'<img[^>]*src="' + cover_re + r'"[^>]*>', re.IGNORECASE),
    ]
    for pat in patterns:
        if pat.search(body_html):
            return pat.sub('', body_html, count=1)
    return body_html

def parse_markdown_file(file_path):
    """Parse markdown file with frontmatter"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split frontmatter and body
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1])
            body = parts[2].strip()
            return frontmatter, body

    return {}, content

def parse_json_file(file_path):
    """Parse Framer CMS JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if isinstance(data, list) and len(data) > 0:
        article = data[0]
        return {
            'title': article.get('title', ''),
            'sub_title': article.get('sub_title', ''),
            'featured_image': {'url': article.get('cover', {}).get('url', '')},
            'read_time': article.get('read_time', ''),
            'date': article.get('Date', ''),
            'CTA_alici_link': article.get('CTA_alici_link', ''),
            'CTA button': article.get('CTA button', '')
        }, article.get('article_body_content', '')

    return {}, ''

def markdown_to_framer_html(md_text):
    """Convert Markdown to Framer-compatible HTML"""

    # Remove H1 titles (they're in frontmatter)
    md_text = re.sub(r'^# .*$', '', md_text, flags=re.MULTILINE)

    # Remove markdown images that are duplicates of hero image
    md_text = re.sub(r'!\[.*?\]\(.*?\)\n?', '', md_text, count=1)

    # Convert to basic HTML using markdown library
    html = markdown.markdown(
        md_text,
        extensions=['tables', 'fenced_code', 'nl2br']
    )

    # Apply Framer-specific transformations

    # H2 → <h6><strong>
    html = re.sub(
        r'<h2>(.*?)</h2>',
        r'<h6><strong>\1</strong></h6>',
        html
    )

    # H3 → <p><strong>
    html = re.sub(
        r'<h3>(.*?)</h3>',
        r'<p><strong>\1</strong></p>',
        html
    )

    # H4, H5, H6 → <p><strong>
    for level in range(4, 7):
        html = re.sub(
            f'<h{level}>(.*?)</h{level}>',
            r'<p><strong>\1</strong></p>',
            html
        )

    # List items → add data-preset-tag and wrap in <p>
    html = re.sub(
        r'<li>(.*?)</li>',
        r'<li data-preset-tag="p"><p>\1</p></li>',
        html,
        flags=re.DOTALL
    )

    # Tables → wrap in <figure>
    html = re.sub(
        r'<table>',
        r'<figure><table><tbody>',
        html
    )
    html = re.sub(
        r'</table>',
        r'</tbody></table></figure>',
        html
    )

    # Table headers → <th><p>
    html = re.sub(
        r'<th>(.*?)</th>',
        r'<th><p>\1</p></th>',
        html,
        flags=re.DOTALL
    )

    # Table cells → <td><p>
    html = re.sub(
        r'<td>(.*?)</td>',
        r'<td><p>\1</p></td>',
        html,
        flags=re.DOTALL
    )

    # Images → wrap in <figure>
    html = re.sub(
        r'<img\s+([^>]+)>',
        r'<figure><img \1></figure>',
        html
    )

    # Links → add target="_blank"
    html = re.sub(
        r'<a\s+href="([^"]+)"',
        r'<a href="\1" target="_blank"',
        html
    )

    # Blockquotes → wrap <p> if not already
    html = re.sub(
        r'<blockquote>(?!<p>)(.*?)</blockquote>',
        r'<blockquote><p>\1</p></blockquote>',
        html,
        flags=re.DOTALL
    )

    return html

def count_content_stats(html):
    """Count content statistics from HTML"""
    h6_count = len(re.findall(r'<h6>', html))
    img_count = len(re.findall(r'<figure><img', html))
    table_count = len(re.findall(r'<figure><table', html))
    ul_count = len(re.findall(r'<ul>', html))
    ol_count = len(re.findall(r'<ol>', html))

    return {
        'h2_count': h6_count,
        'image_count': img_count,
        'table_count': table_count,
        'list_count': ul_count + ol_count
    }

def generate_preview_html(input_file):
    """Generate Framer preview HTML from input file"""

    input_path = Path(input_file)
    if not input_path.exists():
        print(f"❌ Error: File not found: {input_file}")
        return None

    # Determine input type and parse
    if input_path.suffix == '.json':
        frontmatter, body_html = parse_json_file(input_file)
        is_json_input = True
    else:
        frontmatter, body_md = parse_markdown_file(input_file)
        body_html = markdown_to_framer_html(body_md)
        is_json_input = False

    # Extract metadata
    title = frontmatter.get('title', 'Untitled')
    sub_title = frontmatter.get('sub_title', '')
    cover_url = frontmatter.get('featured_image', {}).get('url', '')
    read_time = frontmatter.get('read_time', '5 min')
    date_str = frontmatter.get('date', datetime.now().strftime('%Y-%m-%d'))

    # If body already includes the cover image, remove the duplicate
    body_html = strip_duplicate_cover(body_html, cover_url)

    # Format date
    if 'T' in date_str:
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        date_formatted = date_obj.strftime('%B %d, %Y')
    else:
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            date_formatted = date_obj.strftime('%B %d, %Y')
        except:
            date_formatted = date_str

    # CTA
    cta_link = frontmatter.get('CTA_alici_link', 'https://app.alici.ai/')
    cta_button = frontmatter.get('CTA button', 'Try alici.ai Free')

    # Load template
    template_path = Path(__file__).parent.parent / '.claude/skills/_shared/framer-previewer/TEMPLATE.html'
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # Prepare subtitle block
    if sub_title:
        sub_title_block = f'<p class="article-subtitle">{sub_title}</p>'
    else:
        sub_title_block = ''

    # Replace template variables
    html = template.replace('{{TITLE}}', title)
    html = html.replace('{{SUB_TITLE_BLOCK}}', sub_title_block)
    html = html.replace('{{COVER_URL}}', cover_url)
    html = html.replace(
        '{{COVER_URL|IMG}}',
        f'<img alt="cover" src="{cover_url}" />' if cover_url else ''
    )
    html = html.replace('{{READ_TIME}}', read_time)
    html = html.replace('{{DATE}}', date_formatted)
    html = html.replace('{{ARTICLE_BODY}}', body_html)
    html = html.replace('{{CTA_LINK}}', cta_link)
    html = html.replace('{{CTA_BUTTON}}', cta_button)

    # Determine output file
    input_stem = input_path.stem
    output_dir = input_path.parent

    # Preserve version suffix if present
    if '-v' in input_stem:
        version_match = re.search(r'(-v\d+\.\d+)', input_stem)
        version_suffix = version_match.group(1) if version_match else ''
        output_file = output_dir / f"07-preview{version_suffix}.html"
    else:
        output_file = output_dir / "07-preview.html"

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    # Generate stats
    stats = count_content_stats(body_html)

    # Print summary
    print("\n" + "=" * 60)
    print("🎨 Framer 预览已生成")
    print("=" * 60)
    print(f"\n预览文件: {output_file}")
    print(f"\n📊 内容摘要:")
    print(f"- 标题: {title}")
    print(f"- 封面: {'✅ ' + cover_url[:50] + '...' if cover_url else '❌ 未找到'}")
    print(f"- 正文图片: {stats['image_count']} 张")
    print(f"- 章节: {stats['h2_count']} 个 H2")
    print(f"- 表格: {stats['table_count']} 个")
    print(f"- 列表: {stats['list_count']} 个")
    print(f"- CTA: \"{cta_button}\" → {cta_link}")
    print(f"\n📝 请在浏览器中打开以查看完整效果")
    print(f"\nmacOS: open {output_file}")
    print(f"Linux: xdg-open {output_file}")
    print("=" * 60 + "\n")

    return str(output_file)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 generate_framer_preview.py <input_file>")
        print("Input can be: .md (Markdown) or .json (Framer JSON)")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = generate_preview_html(input_file)

    if output_file:
        print(f"✅ Preview generated successfully: {output_file}")
    else:
        print("❌ Preview generation failed")
        sys.exit(1)
