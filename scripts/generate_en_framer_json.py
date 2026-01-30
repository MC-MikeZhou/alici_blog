#!/usr/bin/env python3
"""
Generate an English variant of 06-article-final.json as 06-article-final-en.json
by translating key fields and replacing article_body_content with an English HTML
that mirrors the Chinese structure.
"""

import json
from pathlib import Path

def main(base_json_path: Path):
    with base_json_path.open('r', encoding='utf-8') as f:
        data = json.load(f)
    if not isinstance(data, list) or not data:
        raise SystemExit('Input JSON must be an array with one object')

    obj = data[0]

    # Build English fields
    title_en = 'How to Add/Change YouTube Thumbnails (2026): 12 High‑CTR Types'
    sub_title_en = 'Specs + 12 Types + Decision Matrix + Workflow + A/B Testing'
    tlnr_en = (
        'Key takeaways: Get the upload/change flow right first, then use a simple '
        'decision matrix to pick from 12 click‑worthy types. Confirm official specs '
        '(1280×720, 16:9, PNG/JPG, ≤2MB). Design fundamentals: single focal subject, '
        'strong contrast, 3–5‑word copy, and promise consistency. Ship with a brief‑to‑export '
        'workflow and improve via a 7‑day A/B plan (change one variable at a time).'
    )

    # English article body (HTML)
    body_en = r'''
<p><strong>Key Takeaways</strong></p>
<ul>
  <li data-preset-tag="p"><p>Get the “upload/change thumbnail” flow right first, then use the decision matrix to choose from 12 high‑CTR types.</p></li>
  <li data-preset-tag="p"><p>Confirm official specs before designing: 1280×720, 16:9, PNG/JPG/GIF/BMP, ≤2MB, account verified and policy‑compliant.</p></li>
  <li data-preset-tag="p"><p>Four design fundamentals: one clear subject, strong contrast, 3–5‑word copy, and promise consistency (no clickbait).</p></li>
  <li data-preset-tag="p"><p>Use a simple production workflow: Brief → Choose Type → Sketch → Visual (shoot/compose/generate) → Copy → Export → Upload.</p></li>
  <li data-preset-tag="p"><p>Run a 7‑day A/B plan: change exactly one variable per day (face/copy/background/colors) and observe CTR + first‑48h metrics.</p></li>
  </ul>
<p> -  - </p>
<p><strong>Reframe + Data Hook</strong><br />
Thumbnails are not decoration — they’re the first decision point that earns a click. For beginners, the safest path is: first fix the “how to add/replace” flow and meet official specs, then use a lightweight decision matrix to select one of 12 click‑worthy types and execute. In this guide you’ll get: a one‑page workflow, a decision matrix, a beginner‑friendly A/B checklist, and an official spec cheat‑sheet.</p>
<p><strong>Data Hook (from YouTube Help)</strong><br />
• Recommended resolution: 1280×720 (min width 640px)<br />
• Aspect ratio: 16:9<br />
• Formats: JPG, GIF, BMP, or PNG<br />
• Max size: ≤ 2MB<br />
Note: Following these specs helps ensure readability across devices (see Source Attribution).</p>

<h6><strong>Part 0 | Why Thumbnails Matter (without “CTR‑only thinking”)</strong></h6>
<ul>
  <li data-preset-tag="p"><p>Thumbnails directly influence CTR and downstream distribution.</p></li>
  <li data-preset-tag="p"><p>Pure CTR chasing risks “click, then disappointment”, hurting watch time and satisfaction.</p></li>
  <li data-preset-tag="p"><p>Safer approach: keep promise consistency, then maximize readability and appeal; optimize weekly, watch the first‑48h signals.</p></li>
  </ul>

<h6><strong>Part A | Basics: Add/Replace & Auto Candidates</strong></h6>
<p><strong>1) How YouTube generates thumbnails (auto)</strong></p>
<ul>
  <li data-preset-tag="p"><p>YouTube auto‑extracts candidate frames. You can pick one or upload a custom image.</p></li>
  <li data-preset-tag="p"><p>For live, replays, and regular videos, manage thumbnails in each edit page.</p></li>
  </ul>
<p><strong>2) How to add/replace (beginner path)</strong></p>
<p>1) Open YouTube Studio → Content/Videos.<br />
2) Select the target video → Edit/Details.<br />
3) In “Thumbnails”: choose an auto frame or click “Upload thumbnail”.<br />
4) Save after previewing.</p>
<p><strong>3) Requirements for custom thumbnails</strong></p>
<ul>
  <li data-preset-tag="p"><p>Check account status/compliance; feature must not be restricted.</p></li>
  <li data-preset-tag="p"><p>Verify your account if required to enable custom thumbnails.</p></li>
  <li data-preset-tag="p"><p>Follow content policies; avoid misleading imagery.</p></li>
  </ul>
<p><strong>3‑b) Official spec cheat‑sheet</strong></p>
<ul>
  <li data-preset-tag="p"><p>Resolution: 1280×720 (min width 640px)</p></li>
  <li data-preset-tag="p"><p>Aspect ratio: 16:9</p></li>
  <li data-preset-tag="p"><p>Formats: JPG/GIF/BMP/PNG</p></li>
  <li data-preset-tag="p"><p>Max size: ≤ 2MB</p></li>
  <li data-preset-tag="p"><p>Mobile first: single subject + high contrast + short copy.</p></li>
  </ul>
<blockquote>
<p>Pro Tip (AEO): In the first 3 paragraphs after Key Takeaways, surface the shortest possible “how‑to” answer (Studio → Content → Edit → Thumbnails → Upload/Choose → Save). Use structured elements (short lists, tables) for machine readability.</p>
  </blockquote>
<p><strong>4) Live: setting a thumbnail</strong></p>
<ul>
  <li data-preset-tag="p"><p>Before going live: upload a live‑specific thumbnail in the live settings.</p></li>
  <li data-preset-tag="p"><p>During/after: you can still replace thumbnails in the edit page for replays.</p></li>
  </ul>

<h6><strong>Part B | Design System: from “Readable” to “Worth a Click”</strong></h6>
<p><strong>5) Four fundamentals</strong></p>
<ul>
  <li data-preset-tag="p"><p>One clear subject; no clutter.</p></li>
  <li data-preset-tag="p"><p>Strong foreground/background contrast; phone‑first legibility.</p></li>
  <li data-preset-tag="p"><p>3–5‑word copy; don’t repeat the title.</p></li>
  <li data-preset-tag="p"><p>Promise consistency with the video (no over‑promise).</p></li>
  <li data-preset-tag="p"><p>Channel style continuity—helps recognition.</p></li>
  </ul>
<p><strong>6) Layout & hierarchy</strong></p>
<ul>
  <li data-preset-tag="p"><p>Rule of thirds; keep UI‑safe margins.</p></li>
  <li data-preset-tag="p"><p>Hierarchy: subject > copy > decoration.</p></li>
  <li data-preset-tag="p"><p>Phone preview: shrink to 25% and test 1‑second readability.</p></li>
  </ul>
<p><strong>7) Copy & typography</strong></p>
<ul>
  <li data-preset-tag="p"><p>Express one promise or emotion; avoid duplicating the title.</p></li>
  <li data-preset-tag="p"><p>Prefer clean, high‑contrast sans‑serif; prioritize legibility.</p></li>
  </ul>
<p><strong>8) Color & contrast</strong></p>
<ul>
  <li data-preset-tag="p"><p>Use complementary colors for punch; be careful with low‑saturation monochromes.</p></li>
  <li data-preset-tag="p"><p>Reduce background noise; subtle stroke or translucent bar for copy.</p></li>
  </ul>
<p><strong>9) Faces & emotion</strong></p>
<ul>
  <li data-preset-tag="p"><p>Close‑ups build emotion faster; avoid covering facial features.</p></li>
  <li data-preset-tag="p"><p>Keep skin tones natural; avoid over‑processing highlights/shadows.</p></li>
  </ul>

<p><strong>10) Pattern library: 12 types across 4 mindsets</strong></p>
<ul>
  <li data-preset-tag="p"><p>Promise: How‑to, Facts/Stats, Quote.</p></li>
  <li data-preset-tag="p"><p>Contrast: Before/After, VS.</p></li>
  <li data-preset-tag="p"><p>Emotion: Close‑up emotion, Emotional moments, Humor/Satire, High‑energy action.</p></li>
  <li data-preset-tag="p"><p>Proof: Product close‑up, Stunning landscape (scene as proof), Question hook.</p></li>
  </ul>

<p><strong>11) 12 click‑worthy types (quick picker)</strong></p>
<ol>
  <li data-preset-tag="p"><p>Question Hook — a short, direct question that begs an answer.</p></li>
  <li data-preset-tag="p"><p>Facts & Stats — a data point as a visual anchor.</p></li>
  <li data-preset-tag="p"><p>Before/After — visible changes; mirror composition and white balance.</p></li>
  <li data-preset-tag="p"><p>VS Comparison — neutral but strong; don’t reveal the winner on the cover.</p></li>
  <li data-preset-tag="p"><p>Quote/Sound Bite — one punchy sentence, not a paragraph.</p></li>
  <li data-preset-tag="p"><p>Close‑Up Emotion — real reaction, uncluttered background.</p></li>
  <li data-preset-tag="p"><p>High‑Energy Action — freeze a clean action moment.</p></li>
  <li data-preset-tag="p"><p>Product Close‑Up — let the product be the hero; honest textures.</p></li>
  <li data-preset-tag="p"><p>Humor/Satire — light, on‑topic; avoid misleading tropes.</p></li>
  <li data-preset-tag="p"><p>Stunning Landscape — composition and color carry the frame.</p></li>
  <li data-preset-tag="p"><p>Emotional Moments — big facial area for instant empathy.</p></li>
  <li data-preset-tag="p"><p>Tutorial/How‑to — highlight the outcome (what you’ll get), not process clutter.</p></li>
  </ol>

<h6><strong>Case Stories | 5 reusable ideas (images later)</strong></h6>
<p><strong>Case 1: Question Hook — make the question the hero.</strong><br />
Skip complex compositions. A clean background and a bold 3–4‑word question is enough. Try a no‑face minimal version first; if your channel has a strong persona, try a “half profile looking at the question” variant and compare on phone.</p>
<img src="https://ct2.alici.ai/static/image/other/gen_images/case-question-hook.png" alt="Question hook demo">

<p><strong>Case 2: Before/After — compare what’s visible.</strong><br />
Mirror composition and keep white balance consistent. Keep the divider subtle; bring the key difference close to the divider for easy alignment. If the change is too small, skip Before/After and show a result close‑up instead.</p>
<img src="https://ct2.alici.ai/static/image/other/gen_images/case-before-after.png" alt="Before/After demo">

<p><strong>Case 3: VS — don’t announce the winner on the cover.</strong><br />
Place contenders symmetrically with a restrained “VS” in the middle. Add 1–2 short labels below each. Let the video tell the conclusion; the cover’s job is to make people want to watch the process.</p>
<img src="https://ct2.alici.ai/static/image/other/gen_images/case-vs-comparison.png" alt="VS comparison demo">

<p><strong>Case 4: Close‑Up Emotion — let the expression do the talking.</strong><br />
Push the frame close, keep tones natural, keep the background calm. If you add copy, keep it tiny and away from the face. Make the eyes look “toward” an element to guide gaze, rather than staring at the camera.</p>
<img src="https://ct2.alici.ai/static/image/other/gen_images/case-closeup-emotion.png" alt="Close-up emotion demo">

<p><strong>Case 5: Tutorial/How‑to — “show the result”.</strong><br />
Avoid step‑dumping on the cover. Show an outcome (e.g., “crisper footage” close‑up) and a 3–4‑word benefit label. The cover sells the promise; the steps live in the video.</p>
<img src="https://ct2.alici.ai/static/image/other/gen_images/case-howto.png" alt="How-to cover demo">

<h6><strong>Part C | Decision Matrix (Type × Scene × Emotion)</strong></h6>
<figure><table><tbody>
  <tr><th><p>Goal/Scene</p></th><th><p>Primary Type</p></th><th><p>Backup</p></th><th><p>Copy Length</p></th><th><p>Face?</p></th><th><p>Common Mistakes</p></th></tr>
  <tr><td><p>Answer a clear question</p></td><td><p>Question hook</p></td><td><p>Quote</p></td><td><p>3–5 words</p></td><td><p>Optional</p></td><td><p>Copy too long; title duplication</p></td></tr>
  <tr><td><p>Show a visible change</p></td><td><p>Before/After</p></td><td><p>VS</p></td><td><p>0–3 words</p></td><td><p>Depends</p></td><td><p>Small difference; asymmetric comparison</p></td></tr>
  <tr><td><p>Tool/solution showdown</p></td><td><p>VS</p></td><td><p>Facts & Stats</p></td><td><p>0–3 words</p></td><td><p>No</p></td><td><p>Too many elements; clutter</p></td></tr>
  <tr><td><p>Strong emotional pull</p></td><td><p>Close‑up emotion</p></td><td><p>Emotional moments</p></td><td><p>0–2 words</p></td><td><p>Yes</p></td><td><p>Face covered; color cast</p></td></tr>
  <tr><td><p>Product/feature focus</p></td><td><p>Product close‑up</p></td><td><p>Facts & Stats</p></td><td><p>0–3 words</p></td><td><p>No</p></td><td><p>Complex angle; unclear texture</p></td></tr>
  <tr><td><p>Teaching/method</p></td><td><p>Tutorial</p></td><td><p>Question hook</p></td><td><p>3–5 words</p></td><td><p>Depends</p></td><td><p>Title‑like copy; too long</p></td></tr>
  <tr><td><p>Entertainment/light</p></td><td><p>Humor/Satire</p></td><td><p>High‑energy action</p></td><td><p>0–3 words</p></td><td><p>Depends</p></td><td><p>Deep insider joke; off‑topic</p></td></tr>
  <tr><td><p>Scenery as the hook</p></td><td><p>Stunning landscape</p></td><td><p>Emotional moments</p></td><td><p>0–2 words</p></td><td><p>No</p></td><td><p>Blur from DoF/exposure issues</p></td></tr>
  </tbody></table></figure>

<h6><strong>Part D | Production Workflow (0→1→N)</strong></h6>
<ol>
  <li data-preset-tag="p"><p>Brief (30–60s): promise, emotion goal, subject/props.</p></li>
  <li data-preset-tag="p"><p>Choose Type: pick one that best expresses the promise.</p></li>
  <li data-preset-tag="p"><p>Sketch: subject/copy positions, contrast, safe margins; phone test.</p></li>
  <li data-preset-tag="p"><p>Visual: shoot/compose/generate; control noise and materials; export 16:9.</p></li>
  <li data-preset-tag="p"><p>Copy: 3–5 words; avoid title duplication.</p></li>
  <li data-preset-tag="p"><p>Export & check specs: 1280×720, ≤2MB, PNG/JPG; quick phone preview.</p></li>
  <li data-preset-tag="p"><p>Upload & naming: Studio → Content → Edit → Thumbnails → Upload/Choose → Save.</p></li>
  </ol>

<h6><strong>Part E | 7‑Day A/B Plan</strong></h6>
<ul>
  <li data-preset-tag="p"><p>Day 1–2: Baseline CTR, impressions, avg watch time.</p></li>
  <li data-preset-tag="p"><p>Day 3: Face vs no face.</p></li>
  <li data-preset-tag="p"><p>Day 4: 3 vs 5 words; verb vs noun.</p></li>
  <li data-preset-tag="p"><p>Day 5: Background — solid vs scene.</p></li>
  <li data-preset-tag="p"><p>Day 6: Colors — complementary high‑contrast vs gentle mono.</p></li>
  <li data-preset-tag="p"><p>Day 7: Review; promote the winner as new baseline.</p></li>
  </ul>

<h6><strong>Part F | Design with Purpose</strong></h6>
<ul>
  <li data-preset-tag="p"><p>Decide what the viewer must read in 1 second; then decide whether to add text/faces/props.</p></li>
  <li data-preset-tag="p"><p>If the thumbnail already tells the core info, the title should complement, not repeat.</p></li>
  <li data-preset-tag="p"><p>Conversely, if the title is very explicit, the thumbnail can lean into emotion or scene.</p></li>
  </ul>

<p><strong>Visual Prompt Pack (quick starts)</strong></p>
<ul>
  <li data-preset-tag="p"><p>Hero Cover (16:9): “Clean YouTube thumbnail, one bold subject, high contrast teal accent, minimal 3-word overlay in English, cinematic lighting, plain background, 16:9, professional, readable on mobile”.</p></li>
  <li data-preset-tag="p"><p>VS Comparison (16:9): “Split-screen VS thumbnail, left vs right product silhouettes, big VS in center with low opacity, strong color contrast, minimal labels, clean background, 16:9, bold and balanced”.</p></li>
  </ul>

<h6><strong>Mini FAQ</strong></h6>
<p><strong>Q1: Why can’t I see the “Upload thumbnail” button?</strong><br />
Check requirements: account status & verification; enable custom thumbnails per platform policy.</p>
<p><strong>Q2: Can I replace a thumbnail after upload?</strong><br />
Yes. Go to YouTube Studio → video edit page → Thumbnails.</p>
<p><strong>Q3: How do I set thumbnails for live?</strong><br />
Upload in live settings before streaming; you can still replace it later for replays.</p>
<p><strong>Q4: Where do auto thumbnails come from?</strong><br />
YouTube auto‑extracts frames and lets you pick a candidate.</p>
<p><strong>Q5: Which type should beginners start with?</strong><br />
Start from your “promise”, then pick one type from the 12 that expresses it most directly. Keep a single subject, strong contrast, and short copy.</p>

<p><strong>CTA | What to do next</strong><br />
Add/replace your next video’s thumbnail following Part A. Use the decision matrix to pick one type, ensure single subject + high contrast + 3–5‑word copy, and run the 7‑day A/B plan.</p>

<p><strong>Source Attribution</strong><br />
• YouTube Help: Add video thumbnails on YouTube — https://support.google.com/youtube/answer/72431<br />
• YouTube Help: Verify your YouTube account — https://support.google.com/youtube/answer/171664<br />
• YouTube Help: Get started with live streaming — https://support.google.com/youtube/answer/2474026<br />
• YouTube Help: Spam, deceptive practices, & scams policies — https://support.google.com/youtube/answer/2801973<br />
• vidIQ: The 12 Best YouTube Thumbnails People Love to Click On — https://vidiq.com/blog/post/types-youtube-thumbnails/<br />
• InVideo: How to Add a Thumbnail to a YouTube Video and Grab Your Audience’s Attention — https://invideo.io/blog/how-to-add-thumbnail-to-youtube-video/</p>
'''

    # Assign English values
    obj_en = {
        "Slug": obj.get("Slug", ""),
        "title": title_en,
        "sub_title": sub_title_en,
        "TLNR": tlnr_en,
        "cover": obj.get("cover", {}),
        "Date": obj.get("Date", ""),
        "read_time": obj.get("read_time", "8 min"),
        "main_category": obj.get("main_category", "tutorial"),
        "recommend_category": obj.get("recommend_category", "tutorial"),
        "article_body_content": body_en,
        "CTA_alici_link": obj.get("CTA_alici_link", "https://alici.ai/youtube-thumbnail"),
        "CTA button": "Try Alici AI Free",
        "meta_title": title_en[:60],
        "meta_description": "Get the upload/change flow right, confirm specs, pick from 12 high‑CTR types with a decision matrix, and optimize via a 7‑day A/B plan.",
        "tag_for_SEO": "youtube, thumbnail, tutorial, 2026, CTR"
    }

    out_path = base_json_path.parent / '06-article-final-en.json'
    out_path.write_text(json.dumps([obj_en], ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'✅ English Framer JSON written: {out_path}')


if __name__ == '__main__':
    base = Path('reports 待发文章/2026-01-28-youtube-thumbnail-0-to-1/06-article-final.json')
    if not base.exists():
        raise SystemExit('Missing base JSON: 06-article-final.json')
    main(base)

