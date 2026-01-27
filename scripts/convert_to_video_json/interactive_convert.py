#!/usr/bin/env python3
"""
Interactive converter to generate a video-enhanced Framer JSON.

Steps:
 1) Load existing Framer JSON (array with one article object)
 2) Collect cloud video URLs:
    - Parse ./video_resources/video_links.txt using separators: newline/space/comma
    - Optionally upload local videos in ./video_resources to CDN (rsync)
 3) Map each video to an insertion position (before body, or before a heading)
 4) Produce 06-article-final-video.json with:
    - article_body_content (combined HTML with embedded videos)
    - article_body_content_parts (array of html/video blocks)
    - video_embeds (metadata)

Note: video_links.txt parsing is delimiter-based (newline/space/comma). Non-HTTP(S)
      tokens are ignored. You may still add extra URLs interactively.
"""

import argparse
import json
import os
import re
import subprocess
import urllib.parse
from pathlib import Path
from typing import Dict, List, Tuple, Any


HEADING_RE = re.compile(r"<h6><strong>(.*?)</strong></h6>", re.IGNORECASE | re.DOTALL)


def read_json(path: Path) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list) or not data:
        raise ValueError("Input JSON must be a non-empty array")
    return data


def write_json(path: Path, data: List[Dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


TRAILING_PUNCT = ",.;:!?)\]\}\uFF0C\u3002\uFF1B\u3001\uFF09\u300D\u300F\u2019\u201D'\"]"


def parse_time_token(token: str) -> int:
    """Parse a time token like '75', '75s', '1:15', '01:02:03', '1m15s'. Return seconds or 0."""
    t = token.strip().lower()
    # h:mm:ss or mm:ss
    if re.match(r"^\d{1,2}:\d{2}(:\d{2})?$", t):
        parts = [int(x) for x in t.split(":")]
        if len(parts) == 2:
            m, s = parts
            return m * 60 + s
        if len(parts) == 3:
            h, m, s = parts
            return h * 3600 + m * 60 + s
    # XmYs pattern
    m = re.match(r"^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$", t)
    if m and any(m.groups()):
        h = int(m.group(1) or 0)
        m_ = int(m.group(2) or 0)
        s = int(m.group(3) or 0)
        return h * 3600 + m_ * 60 + s
    # seconds or seconds with s
    m = re.match(r"^(\d+)(s)?$", t)
    if m:
        return int(m.group(1))
    return 0


def parse_start_from_url(url: str) -> int:
    """Extract start seconds from URL query or fragment (t/start params)."""
    try:
        p = urllib.parse.urlparse(url)
        q = urllib.parse.parse_qs(p.query)
        # t can be 75, 75s, 1m15s
        if "t" in q and q["t"]:
            sec = parse_time_token(q["t"][0])
            if sec:
                return sec
        if "start" in q and q["start"]:
            try:
                return int(q["start"][0])
            except ValueError:
                pass
        # fragment t=... support
        if p.fragment:
            m = re.search(r"t=([^&]+)", p.fragment)
            if m:
                sec = parse_time_token(m.group(1))
                if sec:
                    return sec
    except Exception:
        pass
    return 0


def parse_links_with_meta(text: str) -> List[Dict[str, Any]]:
    """Find http(s) URLs in text robustly, trimming trailing punctuation.
    For each URL, also try to infer start seconds from the URL or same-line tokens.
    Returns a list of {url, start} in first-seen order (dedup by url).
    """
    items: List[Dict[str, Any]] = []
    seen = set()
    lines = text.splitlines() if text else []
    url_pattern = re.compile(r"https?://[^\s<>()\[\]{}\"']+")
    for line in lines:
        for m in url_pattern.finditer(line):
            raw = m.group(0)
            # Trim trailing punctuation
            url = raw.rstrip(TRAILING_PUNCT)
            if url in seen:
                continue
            start = parse_start_from_url(url)
            # Also scan the rest of the line for time hints like 'start: 1:23', 'at 75s'
            tail = line[m.end():]
            time_hits = re.findall(r"(?:start\s*[:=]?\s*|at\s+|#t=|\bt=)([0-9hms:]+)", tail, flags=re.IGNORECASE)
            for th in time_hits:
                sec = parse_time_token(th)
                if sec:
                    start = start or sec
                    break
            items.append({"url": url, "start": start})
            seen.add(url)
    # Fallback split if no matches but text present
    if not items and text:
        tokens = re.split(r"[\s,\u3001\uFF0C]+", text)
        for tok in tokens:
            t = tok.strip().rstrip(TRAILING_PUNCT)
            if t.startswith("http://") or t.startswith("https://"):
                if t not in seen:
                    items.append({"url": t, "start": parse_start_from_url(t)})
                    seen.add(t)
    return items


def is_youtube(url: str) -> bool:
    return any(host in url for host in ("youtube.com", "youtu.be"))


def extract_youtube_id(url: str) -> str:
    # Supports typical patterns: watch?v=ID, youtu.be/ID, embed/ID
    m = re.search(r"[?&]v=([0-9A-Za-z_-]{11})", url)
    if m:
        return m.group(1)
    m = re.search(r"youtu\.be/([0-9A-Za-z_-]{11})", url)
    if m:
        return m.group(1)
    m = re.search(r"/embed/([0-9A-Za-z_-]{11})", url)
    if m:
        return m.group(1)
    return ""


def build_embed_block(url: str, start_seconds: int = 0) -> Tuple[str, Dict[str, Any]]:
    if is_youtube(url):
        vid = extract_youtube_id(url)
        start_q = f"?start={start_seconds}" if start_seconds > 0 else ""
        html = (
            f'<div class="video-embed">\n'
            f'  <iframe src="https://www.youtube-nocookie.com/embed/{vid}{start_q}"'
            f'          title="Video Walkthrough" frameborder="0"'
            f'          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"'
            f'          allowfullscreen></iframe>\n'
            f'</div>'
        )
        meta = {"type": "youtube", "url": url, "video_id": vid, "start": start_seconds}
        return html, meta
    else:
        html = (
            f'<div class="video-embed">\n'
            f'  <video controls src="{url}" playsinline></video>\n'
            f'</div>'
        )
        meta = {"type": "file", "url": url, "start": start_seconds}
        return html, meta


def list_headings(html: str) -> List[Tuple[int, str]]:
    headings = []
    for i, m in enumerate(HEADING_RE.finditer(html), start=1):
        text = re.sub(r"\s+", " ", m.group(1)).strip()
        headings.append((i, text))
    return headings


def insert_before_heading(html: str, embed_html: str, heading_index: int) -> str:
    # Find the Nth heading and insert before it
    matches = list(HEADING_RE.finditer(html))
    if 1 <= heading_index <= len(matches):
        m = matches[heading_index - 1]
        start = m.start()
        return html[:start] + embed_html + "\n" + html[start:]
    return html + "\n" + embed_html  # fallback to end


def build_parts_with_embeds(html: str, plan: List[Dict[str, Any]]) -> Tuple[str, List[Any]]:
    # Generate combined HTML and a parts array reflecting inserted positions
    # Plan items: {url, start, position: {type: 'before_body'|'before_heading', index: int}}
    # We build by walking through the html and slicing at insertion points.

    # Compute absolute insertion indices for headings
    headings = list(HEADING_RE.finditer(html))
    insert_points: List[Tuple[int, str]] = []  # (char_index, embed_html)
    embeds_meta: List[Dict[str, Any]] = []

    for item in plan:
        embed_html, meta = build_embed_block(item["url"], item.get("start", 0))
        pos = item.get("position", {}) or {}
        if pos.get("type") == "before_body":
            insert_points.append((0, embed_html))
            meta.update({"position": {"type": "before_body"}})
        elif pos.get("type") == "before_heading":
            idx = pos.get("index", 1)
            if 1 <= idx <= len(headings):
                char_index = headings[idx - 1].start()
            else:
                char_index = len(html)
            insert_points.append((char_index, embed_html))
            meta.update({"position": {"type": "before_heading", "index": idx}})
        else:
            # default to append at end
            insert_points.append((len(html), embed_html))
            meta.update({"position": {"type": "append_end"}})
        embeds_meta.append(meta)

    # Sort by index so that earlier insertions don't disturb later index
    insert_points.sort(key=lambda x: x[0])

    parts: List[Any] = []
    cursor = 0
    combined = ""
    for i, (char_index, embed_html) in enumerate(insert_points):
        if char_index > cursor:
            chunk = html[cursor:char_index]
            parts.append({"type": "html", "content": chunk})
            combined += chunk
        parts.append({"type": "video", "content": embed_html})
        combined += embed_html
        cursor = char_index
    # tail
    if cursor < len(html):
        tail = html[cursor:]
        parts.append({"type": "html", "content": tail})
        combined += tail

    return combined, parts


def prompt_yes_no(msg: str, default_no: bool = True) -> bool:
    dv = "n" if default_no else "y"
    s = input(f"{msg} [y/N]: ").strip().lower()
    if s == "":
        return not default_no
    return s.startswith("y")


def main():
    parser = argparse.ArgumentParser(description="Generate framer video JSON interactively")
    parser.add_argument("--input", required=True, help="Path to existing Framer JSON (array)")
    parser.add_argument("--resources-dir", default="./video_resources", help="Directory with video_links.txt and local videos")
    parser.add_argument("--output", help="Output JSON path (default: alongside input with -video suffix)")
    parser.add_argument("--max-inline", type=int, default=4, help="Max videos inside body (excludes before-body)")

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ Input not found: {input_path}")
        return 1

    resources_dir = Path(args.resources_dir)
    links_file = resources_dir / "video_links.txt"

    # 1) Load JSON
    data = read_json(input_path)
    article = data[0]
    body_html = article.get("article_body_content", "")
    if not body_html:
        print("❌ article_body_content missing in input JSON")
        return 1

    title = article.get("title", "(untitled)")
    print("=" * 70)
    print("🎬 Convert-to-Video Framer JSON (interactive)")
    print("=" * 70)
    print(f"Article: {title}")
    print(f"Input JSON: {input_path}")
    print(f"Resources:  {resources_dir}")

    # 2) Confirm need
    if not prompt_yes_no("Do you want to embed videos into the article?", default_no=True):
        print("➡️  Skipped. Nothing changed.")
        return 0

    # 3) Collect cloud links from video_links.txt (auto-parse), allow manual additions
    cloud_items: List[Dict[str, Any]] = []
    if links_file.exists():
        raw = read_text_file(links_file)
        parsed_items = parse_links_with_meta(raw)
        if parsed_items:
            print("\n🔗 Video links parsed from video_links.txt:")
            for i, it in enumerate(parsed_items, 1):
                s = f" (start={it['start']}s)" if it.get("start") else ""
                print(f"  {i}. {it['url']}{s}")
            cloud_items.extend(parsed_items)
        else:
            print("\nℹ️  video_links.txt present but no valid HTTP(S) URLs found.")
    else:
        print("\nℹ️  No video_links.txt found.")

    print("\nAdd more cloud video URLs? Enter one per line (empty line to finish).\n"
          "You may include start time like '?t=75s', 'start=1:23', or 'at 1:23'.")
    while True:
        u = input().strip()
        if not u:
            break
        more = parse_links_with_meta(u)
        if more:
            cloud_items.extend(more)

    # 5) Offer uploading local videos
    local_videos = []
    if resources_dir.exists():
        for p in resources_dir.iterdir():
            if p.is_file() and p.suffix.lower() in (".mp4", ".webm", ".mov", ".mkv"):
                local_videos.append(p)

    upload_chosen = False
    if local_videos:
        print("\n📹 Local videos found:")
        for v in local_videos:
            print("  -", v.name)
        upload_chosen = prompt_yes_no("Upload these to CDN now?", default_no=False)

    uploaded_items: List[Dict[str, Any]] = []
    if upload_chosen:
        upl = Path(__file__).parent / "upload_videos.py"
        cmd = ["python", str(upl), "--dir", str(resources_dir)]
        print("\nRunning:", " ".join(cmd))
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            print("❌ Upload failed — you can retry later.")
        print("\nIf upload printed CDN URLs above, paste them here (one per line, empty line to end).\n"
              "You may add start hints like 'start=1:23' on the same line.")
        while True:
            u = input().strip()
            if not u:
                break
            up_more = parse_links_with_meta(u)
            if up_more:
                uploaded_items.extend(up_more)

    # Merge URLs (cloud + uploaded)
    all_items: List[Dict[str, Any]] = []
    by_url = set()
    for it in cloud_items + uploaded_items:
        url = it.get("url")
        if not url or url in by_url:
            continue
        by_url.add(url)
        all_items.append({"url": url, "start": int(it.get("start") or 0)})

    if not all_items:
        print("⚠️  No video URLs provided — aborting.")
        return 1

    # 6) Choose positions
    headings = list_headings(body_html)
    print("\n🔖 Headings detected (H2 -> <h6><strong>):")
    for idx, text in headings:
        print(f"  {idx}. {text}")
    print("  0. (Before body — default top embed)")

    plan: List[Dict[str, Any]] = []
    # First: allow optional pre-body default
    # Default per requirement: one video is placed before body by default
    use_pre_body = prompt_yes_no("Insert a video BEFORE BODY (top)?", default_no=False)
    if use_pre_body:
        first = all_items[0]
        url = first["url"]
        start = int(first.get("start") or 0)
        if is_youtube(url) and start == 0:
            s = input("Optional start time in seconds (Enter to skip): ").strip()
            if s.isdigit():
                start = int(s)
        plan.append({"url": url, "start": start, "position": {"type": "before_body"}})

    # For remaining videos, allow up to max-inline
    remaining_items = all_items[1:] if use_pre_body else all_items
    count_allowed = min(args.max_inline, len(remaining_items))
    for i in range(count_allowed):
        print(f"\nSelect insertion for video #{i+1} (of {count_allowed})")
        print("Enter heading index (1..N) or blank to skip:")
        raw = input().strip()
        if not raw:
            continue
        try:
            idx = int(raw)
        except ValueError:
            print("  Invalid number, skipping this video.")
            continue
        it = remaining_items[i]
        url = it["url"]
        start = int(it.get("start") or 0)
        if is_youtube(url) and start == 0:
            s = input("Optional start time in seconds (Enter to skip): ").strip()
            if s.isdigit():
                start = int(s)
        plan.append({"url": url, "start": start, "position": {"type": "before_heading", "index": idx}})

    # 7) Confirm plan
    print("\n📋 Insertion plan:")
    for item in plan:
        pos = item.get("position", {})
        if pos.get("type") == "before_body":
            where = "before BODY"
        elif pos.get("type") == "before_heading":
            where = f"before H2 #{pos.get('index')}"
        else:
            where = "append end"
        print(f" - {item['url']} @ {where} (start={item.get('start',0)})")

    if not prompt_yes_no("Proceed to generate video JSON?", default_no=False):
        print("➡️  Cancelled.")
        return 0

    # 8) Build combined HTML and parts
    combined_html, parts = build_parts_with_embeds(body_html, plan)

    # Build output article object —
    out_article = dict(article)  # shallow copy
    out_article["article_body_content"] = combined_html
    out_article["article_body_content_parts"] = parts
    out_article["video_embeds"] = plan

    # 9) Decide output path
    if args.output:
        out_path = Path(args.output)
    else:
        # Default naming rule: append "-video" before extension
        if input_path.name.endswith(".json"):
            stem = input_path.stem
            # Avoid duplicate suffix
            if stem.endswith("-video"):
                output_name = f"{stem}.json"
            else:
                output_name = f"{stem}-video.json"
            out_path = input_path.parent / output_name
        else:
            out_path = input_path.with_name(input_path.name + "-video")

    # Non-destructive safety: never overwrite the input JSON
    try:
        if out_path.resolve() == input_path.resolve():
            print("❌ Refusing to overwrite input JSON. Specify a different --output or rely on default '-video' suffix.")
            return 1
    except Exception:
        pass

    write_json(out_path, [out_article])

    print("\n" + "=" * 70)
    print("✅ Video Framer JSON generated")
    print("=" * 70)
    print(f"Output: {out_path}")
    print("Summary:")
    print(f" - Parts: {len(parts)} (html/video blocks)")
    print(f" - Videos: {len(plan)}")
    print("Next:")
    print(" - Preview using your usual preview method")
    print(" - Validate rendering of <div class=\"video-embed\"> blocks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
