#!/usr/bin/env python3
"""
YouTube Transcript Fetcher (Supadata)

Fetches transcripts/subtitles via Supadata API and saves to structured Markdown.

Why Supadata:
- No HTML scraping
- Stable JSON response format
- Aligns with AliciBlog docs: `.claude/commands/fetch-transcript.md`
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from typing import Any


SUPADATA_ENDPOINT = "https://api.supadata.ai/v1/youtube/transcript"


def extract_video_id(value: str) -> str | None:
    patterns = [
        r"(?:v=)([0-9A-Za-z_-]{11})",
        r"(?:youtu\.be/)([0-9A-Za-z_-]{11})",
        r"(?:embed/)([0-9A-Za-z_-]{11})",
        r"^([0-9A-Za-z_-]{11})$",
    ]

    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            return match.group(1)
    return None


def load_dotenv_if_present(dotenv_path: str = ".env") -> None:
    if not os.path.exists(dotenv_path):
        return

    try:
        with open(dotenv_path, "r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = val
    except OSError:
        return


def format_timestamp_ms(ms: int) -> str:
    sec = ms // 1000
    h = sec // 3600
    m = (sec % 3600) // 60
    s = sec % 60
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


@dataclass(frozen=True)
class TranscriptSegment:
    text: str
    offset_ms: int
    duration_ms: int | None = None
    lang: str | None = None


@dataclass(frozen=True)
class TranscriptResponse:
    video_id: str
    video_url: str
    lang: str | None
    available_langs: list[str]
    segments: list[TranscriptSegment]
    raw: dict[str, Any]


def fetch_supadata_transcript(
    *,
    video_id: str,
    lang: str | None = None,
    text_only: bool = False,
    chunk_size: int | None = None,
    api_key: str,
) -> TranscriptResponse:
    params: dict[str, Any] = {"videoId": video_id}
    if lang:
        params["lang"] = lang
    if text_only:
        params["text"] = "true"
    if chunk_size is not None:
        params["chunkSize"] = str(int(chunk_size))

    url = f"{SUPADATA_ENDPOINT}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"x-api-key": api_key})

    with urllib.request.urlopen(req, timeout=60) as resp:
        payload = resp.read().decode("utf-8", errors="replace")

    data = json.loads(payload)
    content = data.get("content", [])

    segments: list[TranscriptSegment] = []
    if isinstance(content, list):
        for seg in content:
            if not isinstance(seg, dict):
                continue
            text = (seg.get("text") or "").strip()
            if not text:
                continue
            segments.append(
                TranscriptSegment(
                    text=text,
                    offset_ms=int(seg.get("offset") or 0),
                    duration_ms=int(seg.get("duration")) if seg.get("duration") is not None else None,
                    lang=seg.get("lang"),
                )
            )
    elif isinstance(content, str):
        text = content.strip()
        if text:
            segments.append(TranscriptSegment(text=text, offset_ms=0))

    return TranscriptResponse(
        video_id=video_id,
        video_url=f"https://www.youtube.com/watch?v={video_id}",
        lang=data.get("lang"),
        available_langs=list(data.get("availableLangs") or []),
        segments=segments,
        raw=data,
    )


def render_markdown(response: TranscriptResponse) -> str:
    fetched_date = datetime.now().strftime("%Y-%m-%d")

    timestamped_lines: list[str] = []
    plain_parts: list[str] = []

    for seg in response.segments:
        ts = format_timestamp_ms(seg.offset_ms)
        timestamped_lines.append(f"[{ts}] {seg.text}")
        plain_parts.append(seg.text)

    timestamped_content = "\n".join(timestamped_lines)
    plain_content = " ".join(plain_parts)

    return (
        "---\n"
        f"video_id: {response.video_id}\n"
        f"video_url: {response.video_url}\n"
        f"fetched_date: {fetched_date}\n"
        f"transcript_language: {response.lang or 'unknown'}\n"
        f"available_languages: {json.dumps(response.available_langs, ensure_ascii=False)}\n"
        "source: supadata\n"
        f"total_entries: {len(timestamped_lines)}\n"
        "---\n\n"
        f"# YouTube Transcript: {response.video_id}\n\n"
        "## Timestamped Version\n\n"
        f"{timestamped_content}\n\n"
        "## Plain Text Version\n\n"
        f"{plain_content}\n"
    )


def build_default_output_path(video_id: str) -> str:
    current_date = datetime.now().strftime("%Y-%m-%d")
    return os.path.join("reports", "transcripts", f"{current_date}-{video_id}.md")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Fetch YouTube transcripts via Supadata API.")
    parser.add_argument("youtube", help="YouTube URL or 11-char video ID")
    parser.add_argument("language", nargs="?", default=None, help="Optional language code (e.g., en, zh)")
    parser.add_argument("--out", dest="out_path", default=None, help="Output markdown path")
    parser.add_argument("--text-only", action="store_true", help="Request plain text mode from API (best-effort)")
    parser.add_argument("--chunk-size", type=int, default=None, help="Supadata chunkSize (50-10000)")
    parser.add_argument("--save-raw-json", action="store_true", help="Also save raw JSON next to the markdown")
    args = parser.parse_args(argv)

    load_dotenv_if_present(".env")
    api_key = os.environ.get("SUPADATA_API_KEY", "").strip()
    if not api_key:
        print("❌ Missing SUPADATA_API_KEY. Set it in environment or .env.", file=sys.stderr)
        return 1

    video_id = extract_video_id(args.youtube)
    if not video_id:
        print(f"❌ Invalid YouTube URL or video ID: {args.youtube}", file=sys.stderr)
        return 1

    out_path = args.out_path or build_default_output_path(video_id)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    print(f"Video ID: {video_id}")
    print("Fetching transcript via Supadata…")

    try:
        response = fetch_supadata_transcript(
            video_id=video_id,
            lang=args.language,
            text_only=args.text_only,
            chunk_size=args.chunk_size,
            api_key=api_key,
        )
    except Exception as e:
        print(f"❌ Error fetching transcript: {e}", file=sys.stderr)
        return 1

    markdown = render_markdown(response)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    if args.save_raw_json:
        raw_path = os.path.splitext(out_path)[0] + ".supadata.json"
        with open(raw_path, "w", encoding="utf-8") as f:
            json.dump(response.raw, f, ensure_ascii=False)

    print(f"\n✅ Transcript saved to: {out_path}")
    print(f"📊 Total entries: {len(response.segments)}")
    print(f"📝 Word count: {len(' '.join(s.text for s in response.segments).split())}")
    print("\n📄 Preview (first 500 chars):")
    print("-" * 60)
    print((markdown[:500] + "...") if len(markdown) > 500 else markdown)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
