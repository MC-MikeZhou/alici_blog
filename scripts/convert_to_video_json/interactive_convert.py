#!/usr/bin/env python3
"""
Interactive converter to generate a video-split JSON (no HTML injection).

Steps:
 1) Load existing Framer JSON (array with one article object)
 2) Collect cloud video URLs:
    - Parse ./video_resources/video_links.txt using separators: newline/space/comma
    - Optionally upload local videos in ./video_resources to CDN (rsync)
 3) Map each video to an insertion position (before body, or before a heading)
 4) Produce *-video.json with ONLY:
    - article_body_content (first segment of original HTML)
    - article_body_content_2..N (subsequent segments)
    - video_link_1..N (ordered by insertion request; video_link_1 is BEFORE BODY if chosen)

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


def load_schema_example() -> Dict[str, Any]:
    """Load blog_scheme_example.json (with // comments) and return the first object.
    Falls back to empty dict if not found or parse error.
    """
    try:
        repo_root = Path(__file__).resolve().parents[2]
        schema_path = repo_root / "skills" / "utilities" / "convert-to-video-framer-json" / "blog_scheme_example.json"
        raw = schema_path.read_text(encoding="utf-8")
        # Strip // comments outside strings
        out = []
        in_str = False
        esc = False
        i = 0
        while i < len(raw):
            ch = raw[i]
            if in_str:
                out.append(ch)
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    in_str = False
                i += 1
                continue
            # not in string
            if ch == '"':
                in_str = True
                out.append(ch)
                i += 1
                continue
            if ch == '/' and i + 1 < len(raw) and raw[i + 1] == '/':
                # skip until newline
                while i < len(raw) and raw[i] not in ('\n', '\r'):
                    i += 1
                continue
            out.append(ch)
            i += 1

        cleaned = ''.join(out)
        obj = json.loads(cleaned)
        if isinstance(obj, list) and obj:
            return obj[0]
        if isinstance(obj, dict):
            return obj
    except Exception:
        pass
    return {}


def unify_key(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


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



def list_headings(html: str) -> List[Tuple[int, str]]:
    headings = []
    for i, m in enumerate(HEADING_RE.finditer(html), start=1):
        text = re.sub(r"\s+", " ", m.group(1)).strip()
        headings.append((i, text))
    return headings


# (No HTML injection helpers by design)


def build_parts_with_embeds(html: str, plan: List[Dict[str, Any]]) -> Tuple[str, List[Any]]:
    # Generate combined HTML and a parts array reflecting inserted positions
    # Plan items: {url, start, position: {type: 'before_body'|'before_heading', index: int}}
    # We build by walking through the html and slicing at insertion points.

    # Compute absolute insertion indices for headings
    headings = list(HEADING_RE.finditer(html))
    insert_points: List[Tuple[int, str]] = []  # (char_index, embed_html)
    embeds_meta: List[Dict[str, Any]] = []

    for item in plan:
        pos = item.get("position", {}) or {}
        if pos.get("type") == "before_body":
            # Do NOT split content at 0 for before_body; only record a video link later
            continue
        elif pos.get("type") == "before_heading":
            idx = pos.get("index", 1)
            if 1 <= idx <= len(headings):
                char_index = headings[idx - 1].start()
            else:
                char_index = len(html)
            insert_points.append((char_index, ""))
        else:
            # default to append at end
            insert_points.append((len(html), ""))

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
        # we are not injecting any video HTML; splitting only
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
parser = argparse.ArgumentParser(description="Generate blog-scheme video JSON interactively (non-destructive)")
    parser.add_argument("--input", required=True, help="Path to existing Framer JSON (array)")
    parser.add_argument("--resources-dir", default="./video_resources", help="Directory with video_links.txt and local videos")
    parser.add_argument("--output", help="Output JSON path (default: alongside input with -video suffix)")
    # Schema is no longer required; we follow fixed field naming:
    # article_body_content, article_body_content_2..N and video_link_1..N
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

    # 5) Offer uploading local videos (construct CDN URLs for files under resources dir)
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
              "You may add start hints like 'start=1:23' on the same line.\n"
              "If you prefer, just press Enter and I will construct URLs from file names using CDN_VIDEO_URL_PREFIX.")
        while True:
            u = input().strip()
            if not u:
                break
            up_more = parse_links_with_meta(u)
            if up_more:
                uploaded_items.extend(up_more)

        # Construct CDN URLs automatically if none were pasted
        if not uploaded_items:
            url_prefix = os.environ.get("CDN_VIDEO_URL_PREFIX", "https://ct2.alici.ai/static/video/other/gen_videos/")
            for v in local_videos:
                uploaded_items.append({"url": url_prefix + v.name, "start": 0})

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

    # 8) Build content parts WITHOUT injecting any iframe/video markup.
    # Compute insertion character indices
    matches = list(HEADING_RE.finditer(body_html))
    split_positions: List[int] = []
    for item in plan:
        pos = item.get("position", {}) or {}
        if pos.get("type") == "before_heading":
            idx = pos.get("index", 1)
            if 1 <= idx <= len(matches):
                split_positions.append(matches[idx - 1].start())
            else:
                split_positions.append(len(body_html))
        # Skip before_body for split; it does not create a new part before content
    split_positions = sorted([i for i in split_positions if 0 <= i <= len(body_html)])

    # Split into parts around indices (m internal videos → m+1 parts)
    parts_html: List[str] = []
    last = 0
    for posi in split_positions:
        parts_html.append(body_html[last:posi])
        last = posi
    parts_html.append(body_html[last:])

    # 9) Build output JSON (retain all source fields; ensure example fields present with source values only)
    schema_item = load_schema_example()  # only used for field names
    out_article: Dict[str, Any] = dict(article)

    # Build case-insensitive map of source keys
    src_lc = {unify_key(k): k for k in article.keys()}

    # Ensure example fields exist; values MUST come from source JSON only.
    missing: List[str] = []
    if isinstance(schema_item, dict) and schema_item:
        for k in schema_item.keys():
            uk = unify_key(k)
            if uk in src_lc:
                # If the canonical example key casing differs, ensure that key also exists in output
                if k not in out_article:
                    out_article[k] = article[src_lc[uk]]
            else:
                missing.append(k)

    if missing:
        print("❌ Aborted: required fields (from blog_scheme_example.json) missing in source JSON.")
        print("   Missing (by canonical names):")
        for m in missing:
            print("   -", m)
        print("\n请先在源 JSON 中补齐这些字段的值（或通过编辑环节补齐），再重新运行本命令。")
        return 1
    # Set primary content and numbered parts
    # Determine source content key
    source_body = article.get("article_body_content") or article.get("content") or body_html

    if parts_html:
        out_article["article_body_content"] = parts_html[0] if parts_html[0] else source_body
        for i in range(1, len(parts_html)):
            out_article[f"article_body_content_{i+1}"] = parts_html[i]
    else:
        out_article["article_body_content"] = source_body
    # Video links (ordered by plan): first could be BEFORE BODY
    for i, it in enumerate(all_items, start=1):
        out_article[f"video_link_{i}"] = it["url"]

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

    # Output as array (consistent with Framer export style)
    write_json(out_path, [out_article])

    print("\n" + "=" * 70)
    print("✅ Video Framer JSON generated")
    print("=" * 70)
    print(f"Output: {out_path}")
    print("Summary:")
    print(f" - Parts: {len(parts_html)} (content segments)")
    print(f" - Videos: {len(plan)}")
    print("Next:")
    print(" - Validate article_body_content splits and video_link_1..N fields")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
