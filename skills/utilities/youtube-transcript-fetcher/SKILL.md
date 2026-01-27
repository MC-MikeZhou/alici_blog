---
name: youtube-transcript-fetcher
type: skill
provides: youtube-transcript
dependencies: []
description: 抓取 YouTube 视频字幕/脚本
metadata:
  version: 1.1
  author: H
  updated: 2026-01-21
---

# YouTube Transcript Fetcher Skill

## Purpose
Fetch YouTube video transcripts/subtitles using the Supadata API and save them in a structured format for future reference or as input for other skills (e.g., blog-tutorial-writer).

## Platform Compatibility

| Platform | Support Status | Notes |
|----------|---------------|-------|
| **Claude Code CLI** | Full Support | Has Bash/WebFetch tools for API calls |
| **Claude Desktop + MCP** | Full Support | With proper MCP server configuration |
| **Claude.ai Web (Projects)** | Manual Mode | No tool execution - see Manual Usage below |
| **Claude.ai (Chat)** | Manual Mode | No tool execution - see Manual Usage below |

### Automatic Mode (Claude Code CLI / Desktop + MCP)
In these environments, Claude can automatically:
1. Execute curl commands via Bash tool
2. Call the Supadata API directly
3. Process and format the response
4. Save files to disk

### Manual Mode (Claude.ai Web Version)
**Claude.ai web version cannot execute tools or make API calls.** When using this Skill in Claude.ai:

1. Claude will generate the curl command for you
2. **You** must copy and run it in your terminal
3. Copy the API response back to Claude
4. Claude will format and display the transcript
5. You'll need to manually save the output

## Trigger Words
- "抓取字幕"
- "获取脚本"
- "YouTube transcript"
- "视频字幕"
- "/fetch-transcript"

## Allowed Tools
- WebFetch
- Write
- Read
- Bash

## Input Requirements

When this skill is invoked, you need one of the following:
1. **YouTube URL**: Full URL (e.g., `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
2. **Video ID**: Just the ID portion (e.g., `dQw4w9WgXcQ`)

Optional parameters:
- **Language**: Specific language code (e.g., "en", "zh", "es") - if not specified, default language will be used
- **Text only**: Boolean to request plain text format without timestamps

## API Information

### Endpoint
```
GET https://api.supadata.ai/v1/youtube/transcript
```

### Authentication
```
Header: x-api-key: sd_fe238b5804c459d03740695389a2eb25
```

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes* | Full YouTube URL |
| `videoId` | string | Yes* | Video ID (use either url or videoId) |
| `text` | boolean | No | true=returns plain text, default false |
| `lang` | string | No | Language code (e.g., "en", "zh") |
| `chunkSize` | number | No | Chunk size (50-10000) |

*Either `url` or `videoId` is required

### Response Format

```json
{
  "content": [
    {
      "text": "Hello and welcome...",
      "offset": 8150,
      "duration": 1200,
      "lang": "en"
    }
  ],
  "lang": "en",
  "availableLangs": ["en", "es", "zh-TW"]
}
```

## Execution Steps

### Step 1: Parse Input
Extract the YouTube URL or video ID from the user's request.

If given a full URL, extract the video ID:
- From `watch?v=VIDEO_ID` format
- From `youtu.be/VIDEO_ID` format
- From `youtube.com/embed/VIDEO_ID` format

### Step 2: Fetch Transcript

**If tools are available** (Claude Code CLI / Desktop + MCP):
Use the Bash tool to call the Supadata API:

```bash
curl -X GET "https://api.supadata.ai/v1/youtube/transcript?url=YOUTUBE_URL" \
  -H "x-api-key: sd_fe238b5804c459d03740695389a2eb25"
```

Or with video ID:

```bash
curl -X GET "https://api.supadata.ai/v1/youtube/transcript?videoId=VIDEO_ID" \
  -H "x-api-key: sd_fe238b5804c459d03740695389a2eb25"
```

**If tools are NOT available** (Claude.ai web version):
Output the curl command and ask the user to execute it in their terminal.

Optional: Add `&lang=LANG_CODE` for specific language or `&text=true` for plain text.

### Step 3: Process Response

**Automatic mode:** Claude receives the API response directly from the Bash tool.

**Manual mode:** Wait for the user to paste the API response, then proceed.

Parse the JSON response to extract:
- Transcript content (array of segments with text, offset, duration)
- Primary language
- Available languages

### Step 4: Format Output

Create two versions:

**A. Timestamped Version**
Format each segment with timestamp:
```
[MM:SS] Transcript text...
```

Convert offset (milliseconds) to MM:SS format.

**B. Plain Text Version**
Concatenate all text segments without timestamps.

### Step 5: Display in Chat

Show the user:
```markdown
## YouTube Transcript 获取成功

**视频**: [VIDEO_URL]
**语言**: [PRIMARY_LANG]
**可用语言**: [AVAILABLE_LANGS]

### 脚本内容

[00:08] Hello and welcome...
[00:12] Today we're going to...
...

---
已保存至: /reports/transcripts/YYYY-MM-DD-video-id.md
```

### Step 6: Save to File

**Automatic mode only** (requires Write tool):

Create directory if needed:
```bash
mkdir -p /Users/H/Documents/AliciBlog/reports/transcripts
```

Save to: `/Users/H/Documents/AliciBlog/reports/transcripts/YYYY-MM-DD-{video-id}.md`

**Manual mode:** Claude will display the formatted transcript, and you'll need to manually copy-paste it to a file on your computer.

File format:
```markdown
---
video_url: https://youtube.com/watch?v=xxx
video_id: xxx
fetched_at: YYYY-MM-DD
language: en
available_languages: [en, es, zh-TW]
---

# YouTube Transcript

## 带时间戳版本

[00:08] Hello and welcome...
[00:12] Today we're going to...

## 纯文本版本

Hello and welcome... Today we're going to...
```

## Error Handling

Handle these common errors:

1. **Invalid URL/Video ID**: Inform user and ask for correct input
2. **No transcript available**: Check if video has captions enabled
3. **API error**: Display error message and suggest retry
4. **Language not available**: Show available languages and ask user to choose

## Integration with Other Skills

The saved transcript files can be used as reference materials for:
- `blog-tutorial-writer`: Use as source material for blog posts
- Any content creation skill that benefits from video transcript context

Reference in Topic Brief:
```json
{
  "reference_sources": {
    "youtube_transcripts": [
      "/Users/H/Documents/AliciBlog/reports/transcripts/2026-01-19-video-id.md"
    ]
  }
}
```

## Example Usage

**User**: `/fetch-transcript https://www.youtube.com/watch?v=dQw4w9WgXcQ`

**Expected Flow**:
1. Extract video ID: `dQw4w9WgXcQ`
2. Call API with video ID
3. Process and format transcript
4. Display in chat with timestamps
5. Save to `/Users/H/Documents/AliciBlog/reports/transcripts/2026-01-21-dQw4w9WgXcQ.md`
6. Confirm save location to user

## Notes

- Always ensure the `/Users/H/Documents/AliciBlog/reports/transcripts/` directory exists before saving
- Use today's date (YYYY-MM-DD format) as file prefix for easy chronological sorting
- If transcript is very long, consider showing first ~20 lines in chat and mentioning "... (truncated, see full transcript in saved file)"
- Keep the API key secure and never display it in user-facing output
