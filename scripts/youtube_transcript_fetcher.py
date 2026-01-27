#!/usr/bin/env python3
"""
YouTube Transcript Fetcher
Fetches transcript from YouTube video and saves to structured markdown file.
"""

import sys
import json
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi
import re

def extract_video_id(url):
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'^([0-9A-Za-z_-]{11})$'
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def format_timestamp(seconds):
    """Convert seconds to MM:SS format."""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def fetch_transcript(video_url, language=None):
    """Fetch transcript from YouTube video."""
    video_id = extract_video_id(video_url)

    if not video_id:
        raise ValueError(f"Invalid YouTube URL or video ID: {video_url}")

    print(f"Video ID: {video_id}")
    print(f"Fetching transcript...")

    # Fetch transcript
    api = YouTubeTranscriptApi()
    if language:
        transcript = api.fetch(video_id, languages=[language])
    else:
        transcript = api.fetch(video_id)

    # Get snippets (the actual transcript entries)
    transcript_list = list(transcript)

    return video_id, transcript_list

def save_transcript(video_id, transcript_list, output_path):
    """Save transcript to markdown file with YAML frontmatter."""
    # Generate metadata
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Format transcripts
    timestamped_text = []
    plain_text = []

    for entry in transcript_list:
        timestamp = format_timestamp(entry.start)
        text = entry.text.strip()

        timestamped_text.append(f"[{timestamp}] {text}")
        plain_text.append(text)

    timestamped_content = "\n".join(timestamped_text)
    plain_content = " ".join(plain_text)

    # Create markdown content
    markdown_content = f"""---
video_id: {video_id}
video_url: https://www.youtube.com/watch?v={video_id}
fetched_date: {current_date}
transcript_language: auto
total_entries: {len(transcript_list)}
---

# YouTube Transcript: {video_id}

## Timestamped Version

{timestamped_content}

## Plain Text Version

{plain_content}
"""

    # Save to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"\n✅ Transcript saved to: {output_path}")
    print(f"📊 Total entries: {len(transcript_list)}")
    print(f"📝 Word count: {len(plain_content.split())}")

    return markdown_content

def main():
    if len(sys.argv) < 2:
        print("Usage: python youtube_transcript_fetcher.py <YouTube-URL> [language]")
        sys.exit(1)

    video_url = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        # Fetch transcript
        video_id, transcript_list = fetch_transcript(video_url, language)

        # Generate output path
        current_date = datetime.now().strftime("%Y-%m-%d")
        output_path = f"/Users/H/Documents/AliciBlog/reports 待发文章/{current_date}-ai-video-prompts/transcript.md"

        # Save transcript
        content = save_transcript(video_id, transcript_list, output_path)

        # Display preview (first 500 chars)
        print("\n📄 Preview (first 500 chars):")
        print("-" * 60)
        print(content[:500] + "...")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
