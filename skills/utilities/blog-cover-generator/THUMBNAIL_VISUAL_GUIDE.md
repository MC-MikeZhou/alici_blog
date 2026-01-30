# Thumbnail Style Cover 视觉规范

> **版本**: v1.0
> **更新日期**: 2026-01-30
> **适用范围**: Thumbnail 相关博客文章的封面图生成

---

## 1. 概述

### 1.1 定位差异

| 维度 | Professional Cover (Category A) | Thumbnail Style Cover (Category B) |
|------|--------------------------------|-----------------------------------|
| **整体调性** | 极简主义 (Minimalism) | 视觉冲击力 (Visual Impact) |
| **空间处理** | 40%+ 留白 | 高密度填充，10-20% 留白 |
| **构图原则** | 单一焦点 | 人脸为锚点 + 多元素装饰 |
| **表现手法** | 抽象隐喻 | 直观表达 + 情绪放大 |
| **色彩饱和度** | 低饱和、绿色系 | 高饱和 (Vibrant)、多彩 |
| **适用场景** | 技术文档、产品发布 | YouTube 相关、教程、变现话题 |

### 1.2 适用场景

- Thumbnail 工具使用教程
- YouTube 创作者相关内容
- 视频变现、收益话题
- AI 生成作品展示
- 工具对比评测

### 1.3 检测触发条件

当文章满足以下任一条件时，自动使用 Thumbnail Style：
- 文章路径包含 `thumbnail`
- 标题包含: `thumbnail`, `缩略图`, `封面设计`, `youtube`, `视频封面`, `点击率`
- 标签包含上述关键词

---

## 2. 色彩规范 (Thumbnail Palette)

### 2.1 主色系 (4 选 1 作为背景主导)

| 名称 | 色值 | 情绪 | 适用场景 | Prompt 关键词 |
|------|------|------|---------|--------------|
| **Electric Purple** | `#7C3AED` | 神秘、高价值 | 收益、变现、高级功能 | `electric purple`, `vibrant violet` |
| **Vibrant Red** | `#EF4444` | 紧迫、刺激 | 热门话题、对比评测 | `vibrant red`, `energetic coral` |
| **Bright Blue** | `#3B82F6` | 信任、科技 | 教程、指南 | `bright blue`, `electric blue` |
| **Lime Green** | `#84CC16` | 成功、增长 | 成果展示、最佳实践 | `lime green`, `fresh green` |

### 2.2 强调色 (用于装饰元素)

| 名称 | 色值 | 用途 | Prompt 关键词 |
|------|------|------|--------------|
| **Golden Yellow** | `#FBBF24` | 金钱、奖励、高亮 | `golden yellow`, `bright gold` |
| **Hot Pink** | `#EC4899` | 活力、女性向 | `hot pink`, `magenta accent` |
| **Orange Pop** | `#F97316` | 紧迫感、CTA | `vibrant orange`, `energetic orange` |

### 2.3 背景处理

| 类型 | 描述 | Prompt 关键词 |
|------|------|--------------|
| **波浪渐变** | 水平波浪纹理 + 双色渐变 | `wavy gradient background`, `fluid wave pattern` |
| **涂鸦散落** | 随机图形散落纹理 | `confetti pattern`, `scattered doodle texture` |
| **几何弹跳** | 活泼几何图形 | `bouncy geometric shapes`, `playful polygons` |

---

## 3. 人物规范

### 3.1 三种人物来源

| 来源 | 说明 | 使用方式 | 推荐度 |
|------|------|---------|--------|
| **A. Alici 模特** | 预设品牌模特，风格统一 | 直接使用 URL + image-to-image | ⭐⭐⭐ 推荐 |
| **B. AI 生成** | Prompt 描述人物特征 | 纯文本生成 | ⭐⭐ 备选 |
| **C. 用户自定义** | 用户提供照片 | 上传 → 获取 URL → image-to-image | ⭐⭐⭐ 定制化 |

### 3.2 Alici 模特库

| 模特 | 名称 | URL | 适用场景 |
|------|------|-----|---------|
| 👩 | **AliciLucy** | `https://ct2.alici.ai/static/image/other/design/aliciLucy.png` | 女性向、创作者展示、教程 |
| 👨 | **AliciAndy** | `https://ct2.alici.ai/static/image/other/design/aliciAndy.png` | 男性向、技术教程、评测 |

### 3.3 用户自定义照片流程

```
用户: "用我的照片" + [本地文件]
       ↓
Step 1: 上传照片到 CDN
  rsync -avz [本地路径] root@45.76.70.215:/var/www/static/static/image/other/gen_images/
  密码: 5A_p@cjpX74H(LJM
       ↓
Step 2: 获取照片 URL
  https://ct2.alici.ai/static/image/other/gen_images/[filename]
       ↓
Step 3: 使用 image-to-image 模式生成
```

### 3.4 人物姿态库

| 姿态 ID | 名称 | 描述 | Prompt 关键词 | 适用子类型 |
|---------|------|------|--------------|-----------|
| **P1** | Showcase | 单手展示/指向 | `pointing gesture`, `presenting pose`, `showing something` | T1 |
| **P2** | Double Hold | 双手举物 | `holding items in both hands`, `displaying objects` | T2 |
| **P3** | Thumbs Up | 竖拇指/自信 | `thumbs up`, `confident pose`, `approval gesture` | T3 |
| **P4** | Surprise | 惊讶/张嘴 | `surprised expression`, `open mouth excitement`, `amazed face` | T4 |
| **P5** | Thinking | 思考/手托下巴 | `thinking pose`, `hand on chin`, `contemplative` | 通用 |

### 3.5 人物位置规则

```
┌────────────────────────────────────────┐
│                                        │
│   ┌──────┐              ┌──────┐       │
│   │装饰区│              │装饰区│       │  ← 上方 20%：装饰元素
│   └──────┘              └──────┘       │
│                                        │
│         ┌──────────────────┐           │
│         │                  │           │
│         │    人物区域       │           │  ← 中部 60%：人物主体
│         │  (脸在上 1/3)    │           │
│         │                  │           │
│         └──────────────────┘           │
│                                        │
│   ┌──────────────────────────────┐     │
│   │        文字区域               │     │  ← 下方 20%：文字
│   └──────────────────────────────┘     │
│                                        │
└────────────────────────────────────────┘

规则:
- 人物占画面 40-60%
- 人脸位于画面上 1/3（视觉焦点黄金区）
- 人物可居中或偏左/右（为装饰元素留空间）
- 装饰元素围绕人物但不遮挡脸部
```

---

## 4. 装饰元素库

### 4.1 3D 图标元素

| 元素 ID | 名称 | 用途 | Prompt 关键词 |
|---------|------|------|--------------|
| **D1** | 金币/美元 | 收益、变现 | `3D golden coins`, `floating dollar signs`, `money icons` |
| **D2** | 播放按钮 | 视频相关 | `3D play button`, `video player icon` |
| **D3** | 勾选清单 | 教程、步骤 | `3D checklist`, `checkmark icons`, `task list` |
| **D4** | 设备框 | 作品展示 | `phone mockup`, `floating device frames` |
| **D5** | 箭头/增长 | 增长、趋势 | `3D arrows pointing up`, `growth indicators` |
| **D6** | 星星/闪光 | 强调、新功能 | `sparkle effects`, `star decorations` |
| **D7** | VS 符号 | 对比 | `VS text`, `versus badge` |

### 4.2 元素组合规则

| 场景 | 推荐元素组合 | 数量限制 |
|------|-------------|---------|
| 收益/变现 | D1 + D5 + D6 | 3-5 个 |
| 视频教程 | D2 + D3 + D4 | 2-4 个 |
| 作品展示 | D4 + D6 | 2-3 个 |
| 对比评测 | D7 + D4 | 2 个 |

### 4.3 元素放置原则

- 元素围绕人物分布，形成视觉框架
- 不遮挡人物脸部
- 大小有层次变化（近大远小）
- 使用柔和阴影增加立体感

---

## 5. 文字规范

### 5.1 文字层级

| 层级 | 内容 | 样式 | 位置 | Prompt 关键词 |
|------|------|------|------|--------------|
| **H1** | 核心关键词 (≤3 词) | 特大号、粗体、白色 | 画面下方或中央 | `large bold white text`, `prominent title` |
| **H2** | 补充说明 (可选) | 中号、白色 | H1 下方 | `medium subtitle`, `supporting text` |
| **Tag** | 品牌标识 "Alici.AI" | 小号、40% 透明度 | 角落 | `small brand tag`, `subtle watermark` |

### 5.2 文字提取规则

从文章标题智能提取封面文字：

| 原标题 | H1 | H2 |
|--------|----|----|
| "How to Create Click-Worthy YouTube Thumbnails with AI" | "AI THUMBNAILS" | "Click-Worthy Design" |
| "Best AI Thumbnail Generators 2026" | "AI THUMBNAILS" | "Best Generators 2026" |
| "Alici vs Canva Thumbnail Maker Comparison" | "ALICI vs CANVA" | "Thumbnail Showdown" |

**规则**:
- H1: 提取核心关键词，全大写，≤3 词
- H2: 提取补充信息，首字母大写

### 5.3 文字位置策略

| 子类型 | 文字位置 | 原因 |
|--------|---------|------|
| T1 Creator Showcase | 底部居中 | 人物和作品在中上方 |
| T2 Money/Success | 底部居中或左下 | 人物居中，装饰元素分布两侧 |
| T3 Tutorial Hero | 右侧或底部 | 人物偏左，留右侧给文字 |
| T4 Reaction Shot | 底部居中 | 人物表情为主焦点 |

### 5.4 文字 Prompt 模板

```
Typography:
- Main title: "[H1_TEXT]" in extra-bold white sans-serif,
  very large and prominent, positioned at [POSITION]
- Subtitle: "[H2_TEXT]" in bold white,
  50% size of main title, below the main title
- Brand tag: "Alici.AI" in small white at 40% opacity,
  positioned in bottom-right corner

Text style:
- Clean sans-serif font (similar to Inter or Montserrat)
- Strong contrast against background
- Slight drop shadow for readability
- No decorative fonts or scripts
```

---

## 6. 四种子类型

### 6.1 子类型总览

| 子类型 | 代码 | 适用场景 | 背景色 | 人物姿态 | 装饰元素 |
|--------|------|---------|--------|---------|---------|
| **T1: Creator Showcase** | `creator-showcase` | AI 生成作品展示 | Red/Pink | P1 Showcase | D4 + D6 |
| **T2: Money/Success** | `money-success` | 收益、变现、成功 | Purple/Gold | P2 Double Hold | D1 + D5 |
| **T3: Tutorial Hero** | `tutorial-hero` | 教程、How-to | Blue/Green | P3 Thumbs Up | D3 + D2 |
| **T4: Reaction Shot** | `reaction-shot` | 评测、惊喜发现 | Red/Orange | P4 Surprise | D7 + D4 |

### 6.2 T1: Creator Showcase

**适用场景**: AI 生成作品展示、创作者工具介绍

**视觉特征**:
- 背景: 红色/粉色波浪渐变
- 人物: 展示手势，指向作品
- 装饰: 浮动设备框展示作品 + 闪光效果
- 文字: 底部居中

### 6.3 T2: Money/Success

**适用场景**: 收益、变现、成功案例

**视觉特征**:
- 背景: 紫色渐变，高级感
- 人物: 双手举物（金钱符号），兴奋表情
- 装饰: 金币 + 美元符号 + 增长箭头
- 文字: 底部居中

### 6.4 T3: Tutorial Hero

**适用场景**: 教程、How-to、指南类内容

**视觉特征**:
- 背景: 蓝色/绿色，干净专业
- 人物: 竖拇指，自信友好
- 装饰: 清单图标 + 播放按钮
- 文字: 右侧或底部

### 6.5 T4: Reaction Shot

**适用场景**: 评测、惊喜发现、对比内容

**视觉特征**:
- 背景: 红色/橙色渐变，高能量
- 人物: 惊讶表情，夸张手势
- 装饰: VS 符号 + 产品截图
- 文字: 底部居中

---

## 7. 完整 Prompt 模板

### 7.1 基础结构 (ICSB-T 框架)

```
[Image type]
Thumbnail-style blog cover image, YouTube creator aesthetic

[Character]
[PERSON_DESCRIPTION], [POSE_DESCRIPTION], [EXPRESSION]
Positioned [POSITION], occupying [PERCENTAGE] of frame

[Background]
[BACKGROUND_TYPE] background in [PRIMARY_COLOR]
[PATTERN_DESCRIPTION]
Dynamic, energetic feel

[Decorative Elements]
[ELEMENT_1_DESCRIPTION] floating near [POSITION_1]
[ELEMENT_2_DESCRIPTION] placed at [POSITION_2]
All elements in [STYLE] style with soft shadows

[Typography]
- Main title: "[H1_TEXT]" in extra-bold white sans-serif, positioned at [POSITION]
- Subtitle: "[H2_TEXT]" in bold white, 50% size
- Brand tag: "Alici.AI" in small white at 40% opacity

[Composition]
Face positioned in upper third of frame
High visual density, minimal negative space

[Style]
Vibrant, high-saturation colors
Soft 3D elements with gentle shadows
Professional YouTube thumbnail aesthetic
Clean but energetic composition

Aspect ratio: 16:9
Resolution: 1920x1080
```

### 7.2 T1: Creator Showcase 完整模板

```
Create a vibrant YouTube-style blog cover image.

Character:
[PERSON_DESC: friendly young content creator / OR use reference image URL]
with presenting gesture, one hand showing/pointing at floating elements,
warm smile, engaging eye contact.
Positioned center-right, occupying 50% of frame.

Background:
Wavy gradient background flowing from vibrant red (#EF4444) to coral pink.
Subtle wave pattern texture, dynamic and energetic feel.

Decorative Elements:
- Floating device frames (phone/tablet mockups) showing AI-generated images,
  positioned to the left of the person, tilted at playful angles
- Small sparkle effects scattered around the frames
- All elements in soft 3D style with gentle drop shadows

Typography:
- Main title: "[H1_TEXT]" in extra-bold white sans-serif,
  very large and prominent, positioned at bottom center
- Subtitle: "[H2_TEXT]" in bold white, 50% size, below main title
- Brand tag: "Alici.AI" in small white at 40% opacity, bottom-right corner

Style:
High-saturation colors, YouTube thumbnail aesthetic.
Soft 3D decorative elements.
Professional but approachable feel.

Aspect ratio: 16:9
Resolution: 1920x1080
```

### 7.3 T2: Money/Success 完整模板

```
Create a vibrant YouTube-style blog cover image.

Character:
[PERSON_DESC: excited young entrepreneur / OR use reference image URL]
with holding gesture (items in both hands), displaying objects,
big excited smile, eyes wide with joy.
Positioned center, occupying 55% of frame.

Background:
Wavy gradient background in electric purple (#7C3AED) with subtle
confetti-like pattern texture. Rich, premium feel.

Decorative Elements:
- 3D golden coins floating on both sides of the person, various sizes
- Dollar sign icons ($) in golden yellow scattered around upper corners
- Upward arrows suggesting growth, in lighter purple
- All elements with soft 3D rendering and gentle glow

Typography:
- Main title: "[H1_TEXT]" in extra-bold white sans-serif,
  very large and prominent, positioned at bottom center
- Subtitle: "[H2_TEXT]" in bold white, 50% size, below main title
- Brand tag: "Alici.AI" in small white at 40% opacity, bottom-right corner

Style:
High-saturation purple and gold color scheme.
Soft 3D elements with subtle shadows.
YouTube "money-making" video thumbnail aesthetic.

Aspect ratio: 16:9
Resolution: 1920x1080
```

### 7.4 T3: Tutorial Hero 完整模板

```
Create a vibrant YouTube-style blog cover image.

Character:
[PERSON_DESC: helpful instructor / OR use reference image URL]
with thumbs up gesture, confident stance,
confident smile, approachable expression.
Positioned center-left, occupying 45% of frame.

Background:
Solid bright blue (#3B82F6) with subtle geometric pattern.
Clean, trustworthy, educational feel.

Decorative Elements:
- 3D checklist/clipboard icon with green checkmarks, floating to the right
- Play button icon suggesting video tutorial
- Small arrow icons pointing to checklist
- All in clean 3D style with soft shadows

Typography:
- Main title: "[H1_TEXT]" in extra-bold white sans-serif,
  very large and prominent, positioned at right side or bottom
- Subtitle: "[H2_TEXT]" in bold white, 50% size
- Brand tag: "Alici.AI" in small white at 40% opacity, bottom-right corner

Style:
Bright, clean colors (blue + green accents).
Soft 3D elements.
Educational YouTube thumbnail aesthetic.
Trustworthy, professional feel.

Aspect ratio: 16:9
Resolution: 1920x1080
```

### 7.5 T4: Reaction Shot 完整模板

```
Create a vibrant YouTube-style blog cover image.

Character:
[PERSON_DESC: expressive reviewer / OR use reference image URL]
with surprised gesture, hands up or near face,
shocked/amazed expression, open mouth, wide eyes.
Positioned center, occupying 50% of frame.

Background:
Bold gradient from vibrant red (#EF4444) to orange (#F97316).
Dynamic wave or burst pattern radiating from center.

Decorative Elements:
- Product/tool screenshots in floating frames on sides
- "VS" badge if comparison content
- Exclamation marks or burst effects for emphasis
- All with energetic 3D styling

Typography:
- Main title: "[H1_TEXT]" in extra-bold white sans-serif,
  very large and prominent, positioned at bottom center
- Subtitle: "[H2_TEXT]" in bold white, 50% size
- Brand tag: "Alici.AI" in small white at 40% opacity, bottom-right corner

Style:
High-energy, high-saturation colors.
Dramatic 3D elements.
Reaction/review YouTube thumbnail aesthetic.
Exciting, must-click energy.

Aspect ratio: 16:9
Resolution: 1920x1080
```

### 7.6 Image-to-Image 模式模板 (使用照片时)

```
Create a vibrant YouTube-style blog cover image.

[IMAGE REFERENCE]
Use the provided reference image as the main person.
Preserve the person's face, expression, and general appearance.
Reference URL: [PERSON_IMAGE_URL]

[BACKGROUND]
Replace/extend the background with:
[BACKGROUND_DESCRIPTION - wavy gradient, color, pattern from T1-T4]

[DECORATIVE ELEMENTS]
Add the following 3D elements around the person:
[ELEMENTS_DESCRIPTION - coins, icons, etc. from T1-T4]

[TYPOGRAPHY]
- Main title: "[H1_TEXT]" in extra-bold white sans-serif, positioned at [POSITION]
- Subtitle: "[H2_TEXT]" in bold white, 50% size
- Brand tag: "Alici.AI" in small white at 40% opacity

[STYLE]
Blend the person naturally into the new environment.
Match lighting between person and background.
High-saturation, YouTube thumbnail aesthetic.

Aspect ratio: 16:9
Resolution: 1920x1080
```

---

## 8. 内容类型映射

### 8.1 自动检测规则

| 文章类型 | 关键词检测 | 推荐子类型 | 备选 |
|---------|-----------|-----------|------|
| Thumbnail 工具教程 | `thumbnail`, `how to`, `tutorial`, `guide` | T3 Tutorial Hero | T1 Creator |
| 变现/收益话题 | `money`, `earn`, `$`, `monetize`, `income` | T2 Money/Success | T4 Reaction |
| AI 生成作品展示 | `generated`, `created`, `showcase`, `examples` | T1 Creator Showcase | T3 Tutorial |
| 工具对比评测 | `vs`, `comparison`, `best`, `review` | T4 Reaction Shot | T1 Creator |
| 惊喜发现/新功能 | `new`, `amazing`, `shocking`, `update` | T4 Reaction Shot | T2 Money |

### 8.2 人物选择逻辑

```python
def select_person_source(user_input, preferences):
    # 1. 用户明确指定照片
    if user_input.has_photo:
        photo_url = upload_to_cdn(user_input.photo)
        return {"source": "custom", "url": photo_url}

    # 2. 用户指定使用模特
    if "lucy" in user_input.lower():
        return {"source": "alici", "url": ALICI_LUCY_URL, "name": "Lucy"}
    if "andy" in user_input.lower():
        return {"source": "alici", "url": ALICI_ANDY_URL, "name": "Andy"}

    # 3. 根据内容自动选择模特
    if preferences.get("gender") == "female":
        return {"source": "alici", "url": ALICI_LUCY_URL, "name": "Lucy"}
    elif preferences.get("gender") == "male":
        return {"source": "alici", "url": ALICI_ANDY_URL, "name": "Andy"}

    # 4. 默认使用 AI 生成通用人物
    return {"source": "ai_generated", "description": "friendly content creator"}

ALICI_LUCY_URL = "https://ct2.alici.ai/static/image/other/design/aliciLucy.png"
ALICI_ANDY_URL = "https://ct2.alici.ai/static/image/other/design/aliciAndy.png"
```

---

## 9. 执行流程

### 9.1 与 SKILL.md 的集成

```
blog-cover-generator v2.0 执行流程:

Phase 1: 读取文章
       ↓
Phase 1.5: 判断封面类型 (NEW)
  └── 检测 thumbnail 关键词 → Category B
  └── 其他 → Category A (Professional)
       ↓
Phase 2: 选择子类型
  └── Category B: T1-T4 (本文档)
  └── Category A: 原有 6 种类型
       ↓
Phase 3: 选择人物来源
  └── Alici 模特 / AI 生成 / 用户照片
       ↓
Phase 4: 构建 Prompt
  └── 从本文档 Section 7 选择模板
  └── 填充变量 (人物、背景、装饰、文字)
       ↓
Phase 5: FAL.ai 生成
  └── 模型: nano-banana
  └── 比例: 16:9
  └── 分辨率: 1920x1080
       ↓
Phase 6: CDN 上传
       ↓
Phase 7: 输出元数据
```

### 9.2 输出文件

```
/reports/YYYY-MM-DD-{topic-slug}/
├── assets/
│   └── cover.png                   # 封面图片 (1920x1080)
├── 06-cover-metadata.json          # 封面元数据
└── 07-article-final.json           # Framer JSON (含 cover_image_url)
```

### 9.3 元数据格式

```json
{
  "category": "thumbnail",
  "subtype": "T2-money-success",
  "person_source": {
    "type": "alici",
    "name": "Lucy",
    "url": "https://ct2.alici.ai/static/image/other/design/aliciLucy.png"
  },
  "background_color": "#7C3AED",
  "h1_text": "AI MONEY",
  "h2_text": "How Creators Earn",
  "prompt_used": "[full prompt text]",
  "cdn_url": "https://ct2.alici.ai/static/image/other/gen_images/{slug}-cover.png",
  "generated_at": "2026-01-30T14:30:00Z",
  "model": "fal-ai/nano-banana"
}
```

---

## 10. 质量检查清单

### 生成后检查项

- [ ] **人物**: 脸部清晰，表情符合子类型要求？
- [ ] **背景**: 颜色符合子类型规范，饱和度足够？
- [ ] **装饰元素**: 数量适中，不遮挡人脸？
- [ ] **文字**: H1 清晰可读，位置正确？
- [ ] **构图**: 人脸在上 1/3，整体平衡？
- [ ] **比例**: 16:9？
- [ ] **分辨率**: 1920x1080？

### 常见问题修正

| 问题 | 原因 | 修正方法 |
|------|------|---------|
| 人脸模糊 | 人物描述不够详细 | 增加面部特征描述 |
| 文字乱码 | AI 文字生成不稳定 | 减少文字长度，使用简单词汇 |
| 装饰元素遮挡人脸 | 位置描述不明确 | 明确 "elements around but not covering face" |
| 饱和度不够 | 颜色描述太温和 | 使用 "vibrant", "electric", "bold" 等词 |

---

## Changelog

**v1.0** (2026-01-30):
- 初始版本
- 4 种子类型: T1 Creator Showcase, T2 Money/Success, T3 Tutorial Hero, T4 Reaction Shot
- 色彩规范: 4 主色 + 3 强调色
- 人物系统: Alici 模特库 (Lucy/Andy) + AI 生成 + 用户自定义
- 装饰元素库: D1-D7
- 文字规范: H1/H2/Tag 三层级
- ICSB-T Prompt 框架
- Image-to-image 模式支持

---

**文档维护者**: Claude Opus 4.5
**最后更新**: 2026-01-30
**状态**: ✅ 正式启用
