# fetch-transcript

Fetch YouTube video transcript/subtitles and save to structured file.

## Usage

```
/fetch-transcript <YouTube-URL> [language]
```

## Arguments

- `<YouTube-URL>` (required): Full YouTube URL or video ID
  - Examples:
    - `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
    - `https://youtu.be/dQw4w9WgXcQ`
    - `dQw4w9WgXcQ`

- `[language]` (optional): Language code for specific subtitle language
  - Examples: `en`, `zh`, `es`, `ja`, `zh-TW`
  - If not specified, uses default language

## Examples

```bash
# Fetch transcript in default language
/fetch-transcript https://www.youtube.com/watch?v=dQw4w9WgXcQ

# Fetch transcript in specific language
/fetch-transcript https://www.youtube.com/watch?v=dQw4w9WgXcQ zh

# Using just video ID
/fetch-transcript dQw4w9WgXcQ
```

## What it Does

1. Fetches transcript from YouTube via Supadata API
2. Displays formatted transcript with timestamps in chat
3. Saves to `/reports/transcripts/YYYY-MM-DD-{video-id}.md`
4. File includes both timestamped and plain text versions

## Output Format

The saved file includes:
- YAML frontmatter with video metadata
- Timestamped version: `[MM:SS] Transcript text...`
- Plain text version: Continuous text without timestamps

## Integration

Saved transcripts can be used as reference sources for:
- Blog writing (`blog-tutorial-writer`)
- Content analysis
- Research materials

## Related

- Skill: `youtube-transcript-fetcher`
- Output directory: `/reports/transcripts/`
