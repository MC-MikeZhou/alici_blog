# Prompt 结构模板 - Higgsfield 竞品洞察

> 来源: Higgsfield "Sora 2 Prompt Guide" 分析
> 适用 Skills: blog-tutorial-writer (教程章节结构)

---

## 核心发现

Higgsfield 的 Prompt Guide 提出了 **7 要素 Prompt 结构**，这是他们教程类内容的核心框架。

---

## Prompt 哲学 (引用原文)

> "Prompt length is a strategic choice: short prompts invite creative partnership; long prompts give you precise directorial control."

> "Sora 2 operates on a powerful reasoning model that doesn't just follow instructions; it creatively interprets them - anything you don't specify the AI will invent for you."

**核心观点**:
- **短 Prompt** → 邀请 AI 创意合作
- **长 Prompt** → 精准导演控制

---

## 两种 Prompt 策略

### 策略 1: Descriptive Prompt (描绘画面)

**定义**: Painting a Picture - 描述你看到的画面

**示例**:
```
"A barista carefully pouring steamed milk into espresso,
creating intricate latte art. The warm cafe lighting
creates a cozy morning atmosphere."
```

**适用场景**:
- 需要氛围感
- 艺术性优先
- 给 AI 发挥空间

---

### 策略 2: Directive Prompt (下达指令)

**定义**: Giving a Command - 像导演一样下指令

**示例**:
```
"Close-up shot. Barista's hands. f/2.8 shallow DOF.
Frame: latte art in center. Lighting: warm key light
from left at 45°. Duration: 5s pour action."
```

**适用场景**:
- 技术规格明确
- 商业项目
- 需要精准控制

---

## 七要素 Prompt 结构

Higgsfield 教程中的标准化 Prompt 组成部分:

### 1. Format & Style (格式风格)

**定义**: 视频的整体风格和格式

**示例要素**:
- Cinematic / Documentary / UGC / Commercial
- 16:9 / 9:16 / 1:1
- Realistic / Stylized / Animated

**Prompt 示例**:
```
"Cinematic commercial shot, 16:9 format,
hyper-realistic style with slight color grading"
```

---

### 2. Camera and Lens (镜头设置)

**定义**: 摄影机角度、镜头焦距、景别

**示例要素**:
- Shot type: Close-up / Medium / Wide / Extreme close-up
- Lens: 24mm / 50mm / 85mm / 200mm
- Camera movement: Static / Pan / Tilt / Dolly / Crane

**Prompt 示例**:
```
"Medium shot, 50mm lens, camera slowly dollies forward,
shallow depth of field (f/2.8)"
```

---

### 3. Location & Framing (场景构图)

**定义**: 拍摄地点、环境、构图

**示例要素**:
- Location: Studio / Outdoor / Cafe / Office
- Framing: Rule of thirds / Center composition / Leading lines
- Environment details

**Prompt 示例**:
```
"Modern minimalist cafe interior, subject positioned
using rule of thirds, background features blurred
espresso machines and pendant lights"
```

---

### 4. Lighting and Color Palette (光照配色)

**定义**: 光照设置和色彩方案

**示例要素**:
- Lighting: Natural / Studio / Golden hour / Blue hour
- Key light position and intensity
- Color palette: Warm / Cool / Monochrome
- Mood: Bright / Moody / Dramatic

**Prompt 示例**:
```
"Warm cafe lighting, soft key light from frame left
at 45 degrees, warm orange and brown color palette,
morning atmosphere, gentle shadows"
```

---

### 5. Motion and Action Beats (动作节拍)

**定义**: 主体的动作和时间节奏

**示例要素**:
- Action description: Pouring / Walking / Speaking
- Timing: 2s / 5s / Slow motion
- Motion quality: Smooth / Fast / Jerky

**Prompt 示例**:
```
"Barista slowly pours steamed milk over 5 seconds,
creating latte art. Smooth, controlled hand movement.
Pour completes at end of clip."
```

---

### 6. Dialogue Blocks (对白段落)

**定义**: 角色说话的内容和方式 (如适用)

**示例要素**:
- Character speech
- Tone and emotion
- Lip-sync requirements

**Prompt 示例**:
```
"Barista looks at camera and says warmly:
'Welcome to our cafe. Let me make you
something special today.'"
```

---

### 7. Audio Cues (音效提示)

**定义**: 背景音效和环境声音 (如适用)

**示例要素**:
- Foley sounds: Coffee machine / Footsteps / Door
- Ambient sound: Cafe chatter / Traffic / Birds
- Music mood (if any)

**Prompt 示例**:
```
"Audio: gentle cafe ambiance, espresso machine
steaming in background, soft jazz playing,
warm morning atmosphere sounds"
```

---

## 完整 Prompt 示例

### 示例 1: 短 Prompt (Descriptive 策略)

```
A barista making latte art in a cozy morning cafe,
warm lighting, professional but intimate atmosphere.
```

**优点**: 简洁、给 AI 发挥空间
**缺点**: 细节不可控

---

### 示例 2: 长 Prompt (Directive 策略)

```
**Format & Style**: Cinematic commercial, 16:9, realistic

**Camera & Lens**: Medium close-up shot, 50mm lens,
camera static then slow dolly forward, f/2.8 shallow DOF

**Location & Framing**: Modern minimalist cafe interior,
subject center-frame using rule of thirds, blurred
background with espresso machines

**Lighting & Color**: Warm cafe lighting, soft key light
from frame left at 45°, warm orange-brown palette,
morning golden hour atmosphere

**Motion & Action**: Barista's hands pour steamed milk
into espresso cup over 5 seconds, creating rosetta latte
art pattern, smooth controlled movement

**Audio**: Gentle espresso machine steam in background,
soft cafe ambiance, warm morning atmosphere
```

**优点**: 精准控制
**缺点**: 复杂、需要专业知识

---

## 应用到 blog-tutorial-writer

### 升级建议: 新增 "Prompt 结构章节"

**当前问题**: 教程文章中 Prompt 示例缺乏结构化

**升级方案**: 在教程类文章中加入标准化 Prompt 模板

```markdown
## How to Structure Your Sora 2 Prompts

Professional prompts should include these 7 elements:

### 1. Format & Style
Specify your video format and overall aesthetic.
Example: "Cinematic commercial, 16:9, realistic style"

### 2. Camera & Lens
Define shot type, lens choice, and camera movement.
Example: "Medium shot, 50mm lens, slow dolly forward"

[... 其他要素 ...]

## Complete Prompt Example

Here's a professional prompt using all 7 elements:

[完整示例]
```

---

## Prompt 检查清单 (Checklist)

用于教程文章中指导用户:

```
创建 Prompt 前，检查以下要素:

☐ Format & Style - 风格明确了吗?
☐ Camera & Lens - 镜头设置清楚了吗?
☐ Location & Framing - 场景构图描述了吗?
☐ Lighting & Color - 光照和配色指定了吗?
☐ Motion & Action - 动作节拍明确了吗?
☐ Dialogue - 需要对白吗? (可选)
☐ Audio - 需要音效提示吗? (可选)
```

---

## 对比表: 短 vs 长 Prompt

| 维度 | 短 Prompt | 长 Prompt |
|------|-----------|-----------|
| **长度** | 1-2 句 (20-50 词) | 5-10 句 (100-300 词) |
| **控制度** | 低 (AI 自由发挥) | 高 (精准控制) |
| **适用场景** | 艺术创作、灵感探索 | 商业项目、产品演示 |
| **学习曲线** | 简单 | 需要专业知识 |
| **示例** | "A barista making coffee" | [见上方 7 要素完整示例] |

---

## 应用清单

### blog-tutorial-writer v2.0 升级

**新增章节模板**:

```yaml
tutorial_sections:
  - title: "Understanding Prompt Structure"
    subsections:
      - "Two Prompt Strategies: Descriptive vs Directive"
      - "7 Essential Elements of Professional Prompts"
      - "Format & Style"
      - "Camera & Lens"
      - "Location & Framing"
      - "Lighting & Color"
      - "Motion & Action"
      - "Dialogue (Optional)"
      - "Audio (Optional)"

  - title: "Complete Prompt Examples"
    subsections:
      - "Short Prompt Example (Beginner)"
      - "Long Prompt Example (Professional)"
      - "Prompt Checklist"
```

---

### 与 BLOG_WRITING_PRINCIPLES 的关系

**建议**: 将 Prompt 结构模板作为「技术教程标准化章节」加入原则

```markdown
## Tutorial Content Structure Principles

### For AI Generation Tutorials:

1. **Always include Prompt Structure section**
   - Explain short vs long prompts
   - Provide 7-element checklist
   - Give complete examples

2. **Show progression**
   - Prompt v1 (simple) → Result → Issues
   - Prompt v2 (detailed) → Result → Improvements

3. **Make it actionable**
   - Checklist format
   - Copy-pasteable templates
```

---

## 参考来源

Sources:
- [Sora 2 Prompt Guide: Professional Tips and Examples](https://higgsfield.ai/sora-2-prompt-guide)
- [SORA 2 Prompt Guide: How to Create Viral Videos Like a Pro](https://higgsfield.ai/blog/SORA-2-Prompt-Guide-How-to-Create-Viral-Videos-Like-a-Pro)
- [Sora 2 Prompting Guide - OpenAI Cookbook](https://cookbook.openai.com/examples/sora/sora2_prompting_guide)

---

## 版本历史

- v1.0 (2026-01-18): 初始版本，基于 Higgsfield Sora 2 Prompt Guide
