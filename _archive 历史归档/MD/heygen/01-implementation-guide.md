# HeyGen + Remotion Integration - Implementation Guide

## Overview

This integration combines **HeyGen digital avatars** with **Remotion animations** to create engaging video content. The system generates a 15-20 second video featuring a digital presenter introducing the "5 Best AI Video Generators" article while animated rating charts appear in the background.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    HeyGen API                           │
│  - Digital avatar video generation                      │
│  - Transparent background (WebM)                        │
│  - Voice synthesis                                      │
└───────────────────┬─────────────────────────────────────┘
                    │
                    │ Download video
                    ↓
┌─────────────────────────────────────────────────────────┐
│              Remotion Project                           │
│  /public/avatar-intro.webm                              │
└───────────────────┬─────────────────────────────────────┘
                    │
                    │ Composite layers
                    ↓
┌─────────────────────────────────────────────────────────┐
│          AvatarIntro Composition                        │
│  ┌───────────────────────────────────────────────────┐  │
│  │ Layer 2 (Foreground): HeyGen avatar               │  │
│  │   - Transparent background                        │  │
│  │   - 60% width, bottom aligned                     │  │
│  │   - Drop shadow for depth                         │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │ Layer 1 (Background): Animated bar chart          │  │
│  │   - Starts at frame 60 (2s delay)                 │  │
│  │   - Shows tool ratings (9.5, 9.4, 9.3...)         │  │
│  │   - Green gradient brand styling                  │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                    │
                    │ Render
                    ↓
┌─────────────────────────────────────────────────────────┐
│           Final MP4 Video                               │
│  - 1080x1920 (9:16 vertical)                            │
│  - 600 frames @ 30fps (20 seconds)                      │
│  - Ready for social media                               │
└─────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Implementation

### Step 1: Generate HeyGen Video

```bash
# Navigate to Remotion project
cd /Users/H/Documents/AliciBlog/vibe-skills/remotion-videos

# Run the generation script
./scripts/heygen-generate.sh
```

**What this does:**
1. Sends API request to HeyGen with:
   - **Script**: "Today we're looking at the 5 best AI video generators in 2026..."
   - **Avatar**: Angela in black skirt
   - **Voice**: Female voice (ID: 1bd001e7e50f421d891986aad5158bc8)
   - **Dimensions**: 1080x1920 (9:16 vertical)
   - **Background**: Transparent
2. Polls every 10 seconds for completion (max 10 minutes)
3. Downloads video to `public/avatar-intro.webm`
4. Saves metadata to `/Users/H/Documents/AliciBlog/MD/heygen/avatar-intro-metadata.json`

**Expected output:**
```
=== HeyGen Video Generation ===

Step 1: Requesting video generation...
✓ Video generation started
  Video ID: abc123xyz...

Step 2: Waiting for video generation...
  [1/60] Status: processing... (waiting 10s)
  [2/60] Status: processing... (waiting 10s)
  ...
✓ Video completed!

Step 3: Downloading video...
✓ Video downloaded to: /Users/H/Documents/AliciBlog/vibe-skills/remotion-videos/public/avatar-intro.webm

Step 4: Metadata saved
✓ Metadata saved to: /Users/H/Documents/AliciBlog/MD/heygen/avatar-intro-metadata.json

=== Success! ===
File: /Users/H/Documents/AliciBlog/vibe-skills/remotion-videos/public/avatar-intro.webm
Size: 2.3M
Video ID: abc123xyz...
```

---

### Step 2: Preview in Remotion Studio

```bash
# Start Remotion development server
cd /Users/H/Documents/AliciBlog/vibe-skills/remotion-videos
npm run dev
```

**In the browser:**
1. Navigate to http://localhost:3000
2. Select **"AvatarIntro"** from the composition dropdown
3. Preview the video:
   - 0:00-0:02 - Avatar introduces (solo)
   - 0:02-0:20 - Rating chart animates in background
   - Avatar positioned at bottom center (60% width)
   - Green gradient brand styling

---

### Step 3: Render Final Video

```bash
# Render to MP4
cd /Users/H/Documents/AliciBlog/vibe-skills/remotion-videos
npx remotion render src/index.ts AvatarIntro output/avatar-intro.mp4

# Or use npm script (if configured)
npm run build -- src/index.ts AvatarIntro output/avatar-intro.mp4
```

**Render options:**
```bash
# HD quality (default)
npx remotion render src/index.ts AvatarIntro output/avatar-intro.mp4

# Higher quality (slower)
npx remotion render src/index.ts AvatarIntro output/avatar-intro.mp4 \
  --codec h264 \
  --quality 95

# Custom frame range (e.g., first 10 seconds)
npx remotion render src/index.ts AvatarIntro output/avatar-intro.mp4 \
  --frames=0-300
```

**Output location:**
```
/Users/H/Documents/AliciBlog/vibe-skills/remotion-videos/output/avatar-intro.mp4
```

---

## File Structure

```
/Users/H/Documents/AliciBlog/
├── vibe-skills/remotion-videos/
│   ├── scripts/
│   │   └── heygen-generate.sh          # HeyGen API script
│   ├── public/
│   │   └── avatar-intro.webm           # Downloaded HeyGen video
│   ├── src/
│   │   ├── compositions/ai-video-generators/
│   │   │   └── AvatarIntro.tsx         # Main composition
│   │   ├── components/
│   │   │   ├── AnimatedBarChart.tsx    # Rating chart component
│   │   │   └── BrandFrame.tsx          # Brand styling wrapper
│   │   ├── data/
│   │   │   └── ai-video-generators.json # Tool data
│   │   └── Root.tsx                    # Composition registry
│   └── output/
│       └── avatar-intro.mp4            # Final rendered video
└── MD/heygen/
    ├── 00-heygen-api-setup-guide.md    # API setup instructions
    ├── 01-implementation-guide.md      # This file
    └── avatar-intro-metadata.json      # HeyGen generation metadata
```

---

## Customization Guide

### Change Avatar Script

Edit `scripts/heygen-generate.sh`:

```bash
# Line 18-19
SCRIPT_TEXT="Your new script here. Keep it under 30 seconds for best results."
```

### Change Avatar Character

Edit `scripts/heygen-generate.sh`:

```bash
# Line 41-42 - Available avatars:
# - Angela-inblackskirt-20220820 (current)
# - Josh-inbluesweater-20220720
# - Monica-ingraysuit-20220820
# ... (run ./scripts/list-avatars.sh to see all)

"avatar_id": "Josh-inbluesweater-20220720",
```

### Change Voice

Edit `scripts/heygen-generate.sh`:

```bash
# Line 49 - Available voices:
# - 1bd001e7e50f421d891986aad5158bc8 (current - female)
# - 2e5e7e8e9f0g531d992097bbe6269cd9 (male professional)
# ... (check HeyGen docs for full list)

"voice_id": "2e5e7e8e9f0g531d992097bbe6269cd9"
```

### Adjust Avatar Size/Position

Edit `src/compositions/ai-video-generators/AvatarIntro.tsx`:

```tsx
// Line 56-63
<OffthreadVideo
  src={staticFile('avatar-intro.webm')}
  transparent
  style={{
    width: '70%',              // Change from 60% to 70%
    height: 'auto',
    paddingBottom: '150px',    // Adjust vertical position
    filter: 'drop-shadow(0 20px 40px rgba(0, 0, 0, 0.5))',
  }}
/>
```

### Change Chart Delay

Edit `src/compositions/ai-video-generators/AvatarIntro.tsx`:

```tsx
// Line 31 - Change delay from 60 frames (2 seconds) to 90 frames (3 seconds)
<Sequence from={90}>
```

### Change Video Duration

Edit `src/Root.tsx`:

```tsx
// Line 42 - Change from 600 frames (20s) to 450 frames (15s)
<Composition
  id="AvatarIntro"
  component={AvatarIntro}
  durationInFrames={450}  // 450 frames @ 30fps = 15 seconds
  fps={VIDEO.fps}
  width={VIDEO.width}
  height={VIDEO.height}
/>
```

---

## Troubleshooting

### Issue: "Video file not found" in Remotion

**Cause**: HeyGen video hasn't been generated yet

**Solution**:
```bash
# 1. Check if file exists
ls -lh /Users/H/Documents/AliciBlog/vibe-skills/remotion-videos/public/avatar-intro.webm

# 2. If not, generate it
cd /Users/H/Documents/AliciBlog/vibe-skills/remotion-videos
./scripts/heygen-generate.sh
```

---

### Issue: "Transparent background not working"

**Cause**: Video format or codec issue

**Solution**:
1. Verify the HeyGen video has alpha channel:
   ```bash
   ffprobe public/avatar-intro.webm 2>&1 | grep -i alpha
   # Should show: yuva420p (with alpha channel)
   ```

2. If not, regenerate with HeyGen ensuring transparent background is enabled

---

### Issue: "Avatar appears too small/large"

**Solution**: Adjust width in `AvatarIntro.tsx`:
```tsx
style={{
  width: '60%',  // Try values between 40%-80%
  ...
}}
```

---

### Issue: "Chart appears too early/late"

**Solution**: Adjust delay in `AvatarIntro.tsx`:
```tsx
<Sequence from={60}>  // Change this value (frames @ 30fps)
  // 30 frames = 1 second
  // 60 frames = 2 seconds
  // 90 frames = 3 seconds
```

---

### Issue: "HeyGen API timeout"

**Cause**: Video generation takes longer than expected

**Solution**: Script already handles this with 60 polling attempts (10 minutes). If it still times out:
1. Check HeyGen dashboard for generation status
2. Check credit balance
3. Try shorter script

---

## Performance Tips

### Faster Previews

```bash
# Preview at lower quality
npm run dev
# Then in browser, set playback quality to "Low"
```

### Faster Renders

```bash
# Use concurrency (4 threads)
npx remotion render src/index.ts AvatarIntro output/avatar-intro.mp4 \
  --concurrency=4

# Lower quality (faster)
npx remotion render src/index.ts AvatarIntro output/avatar-intro.mp4 \
  --quality=80
```

### Reduce File Size

```bash
# H.264 with compression
npx remotion render src/index.ts AvatarIntro output/avatar-intro.mp4 \
  --codec=h264 \
  --quality=75 \
  --crf=28
```

---

## Next Steps

1. **✅ Complete**: HeyGen API setup
2. **✅ Complete**: Script generation
3. **✅ Complete**: Remotion composition
4. **⏳ To Do**: Generate HeyGen video
5. **⏳ To Do**: Preview in Remotion Studio
6. **⏳ To Do**: Render final video
7. **Future**: Add more compositions (price comparison, feature matrix)

---

## Resources

- **HeyGen API Docs**: https://docs.heygen.com/reference/api-overview
- **Remotion Docs**: https://www.remotion.dev/docs/
- **Project Files**: `/Users/H/Documents/AliciBlog/vibe-skills/remotion-videos/`
- **Support**: Check `/Users/H/Documents/AliciBlog/MD/heygen/` for guides

---

## Quick Commands Reference

```bash
# Generate HeyGen video
cd /Users/H/Documents/AliciBlog/vibe-skills/remotion-videos
./scripts/heygen-generate.sh

# Preview in Remotion Studio
npm run dev

# Render final video
npx remotion render src/index.ts AvatarIntro output/avatar-intro.mp4

# Check HeyGen API status
echo $HEYGEN_API_KEY | head -c 20
curl -s -o /dev/null -w "HTTP %{http_code}\n" \
  -X GET "https://api.heygen.com/v2/avatars" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```
