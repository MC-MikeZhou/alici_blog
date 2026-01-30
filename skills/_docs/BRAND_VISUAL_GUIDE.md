# alici.ai 品牌视觉规范

> **版本**: v1.1
> **更新日期**: 2026-01-30
> **适用范围**: 所有 alici.ai 博客文章配图、营销素材、社交媒体图片

---

## 0. 视觉规范体系 (v1.1 新增)

本文档定义 **Professional Cover** 的视觉规范（极简、绿色系、抽象隐喻）。

对于 **Thumbnail 相关内容**（YouTube、视频封面、创作者工具），请参考：

> 📄 **[THUMBNAIL_VISUAL_GUIDE.md](/skills/utilities/blog-cover-generator/THUMBNAIL_VISUAL_GUIDE.md)**
> - 高饱和色彩（Purple/Red/Blue/Green）
> - 人脸为核心构图
> - 动感背景 + 3D 装饰元素
> - 4 种子类型: T1 Creator Showcase, T2 Money/Success, T3 Tutorial Hero, T4 Reaction Shot

---

## 1. 核心美学理念

alici.ai 的视觉语言追求**极简主义 + 留白感 + 象征主义**，传达专业、值得信赖、现代科技的品牌形象。

| 维度 | 定义 | 应用原则 |
|------|------|----------|
| **整体调性** | 极简主义 (Minimalism) | 去除一切不必要的装饰，聚焦核心信息 |
| **空间处理** | 大量留白 (Negative Space) | 画面至少 40% 留白，呼吸感优先于信息密度 |
| **构图原则** | 单一焦点 (Single Focal Point) | 一张图传达一个核心概念,避免多主体 |
| **表现手法** | 抽象隐喻 (Symbolic Abstraction) | 用抽象符号代替具象描绘，提升层次感 |

### 视觉参考

**学习对象**: [Stripe](https://stripe.com)
**学习内容**: 样式、留白方式、渐变处理、3D元素、微妙光影
**不学习**: Stripe 的蓝紫色调（alici.ai 是绿色中心）

---

## 2. 色彩规范

### 2.1 主色调 - 绿色渐变系统

alici.ai 以**绿色为中心**构建品牌色彩体系，传达"生长、创新、可信赖"的品牌特质。

| 色彩层级 | 色值示例 | 用途 | Prompt 关键词 |
|---------|---------|------|--------------|
| **深绿** (Dark Green) | `#059669` | 渐变起点，深色背景 | `deep emerald`, `forest green`, `dark teal` |
| **中绿** (Primary Green) | `#10B981` | 主色调，品牌识别色 | `fresh green`, `mint green`, `vibrant green` |
| **浅绿** (Light Green) | `#A7F3D0` | 渐变终点，高光区域 | `soft mint`, `light green`, `pale aqua` |
| **辅助色** (Accent) | 待定 | 强调、CTA、对比元素 | `subtle warm accent` (暖色系点缀) |

### 2.2 中性色系统

| 用途 | 色值 | 应用场景 |
|------|------|----------|
| **背景白** | `#FFFFFF` / `#F9FAFB` | 主背景，留白区域 |
| **浅灰** | `#F3F4F6` / `#E5E7EB` | 次级背景，卡片、分隔 |
| **中灰** | `#9CA3AF` / `#6B7280` | 辅助文字，图标 |
| **深灰** | `#374151` / `#1F2937` | 主文字，标题 |

### 2.3 渐变规则

**推荐渐变方向**:
- 从左上到右下 (45°)
- 从上到下 (垂直)
- 径向渐变 (Radial，从中心向外)

**渐变示例**:
```
linear-gradient(135deg, #059669 0%, #10B981 50%, #A7F3D0 100%)
```

**Prompt 表达**:
```
Soft gradient background flowing from deep emerald to fresh mint to pale aqua,
Stripe-style smooth transitions, subtle and sophisticated
```

---

## 3. Prompt 框架 - ICSB 结构

### 3.1 ICSB 框架定义

**ICS (v2.1 及之前)**:
```
Image type + Content + Style
```

**ICSB (v2.2 及之后)**:
```
Image type + Content + Style + Brand Layer
```

### 3.2 Brand Layer 模板

**所有 alici.ai 配图 Prompt 必须添加此 Brand Layer**:

```
Brand aesthetic: alici.ai (Stripe-inspired, green-centered)

Color palette:
- GREEN-CENTERED gradient: deep emerald → fresh mint → light green
- Soft, sophisticated transitions (similar gradient feel to Stripe, but in green tones)
- Muted saturation, avoid overly vibrant colors

Style elements (from Stripe):
- Generous negative space (40%+ of canvas)
- Soft 3D elements with subtle shadows and highlights
- Single clear focal point
- Clean, breathable composition with implied motion
- Modern, professional, trustworthy visual language

Avoid:
- Blue/purple tones (Stripe's brand colors)
- Saturated, loud colors
- Cluttered layouts with multiple focal points
- Literal, photographic representations (prefer abstract/symbolic)
```

### 3.3 完整 Prompt 示例

```
[Image type]
Editorial illustration in minimalist magazine cover style

[Content]
- Central element: Single abstract shape representing AI decision-making
- Symbolic representation: Flowing paths converging to a focal point
- Minimal text overlay: "Choose Your AI Tool" in clean sans-serif
- Depth: Soft 3D layering with foreground and background elements

[Style]
- Composition: 60% negative space, focal point in golden ratio position
- Lighting: Soft ambient lighting with subtle gradient glow
- Texture: Smooth, polished surfaces with gentle shadows
- Format: 16:9 widescreen, horizontal orientation

[Brand Layer]
Brand aesthetic: alici.ai (Stripe-inspired, green-centered)

Color palette:
- GREEN-CENTERED gradient: deep emerald → fresh mint → light green
- Soft transitions, muted saturation

Style elements:
- Generous negative space (40%+)
- Soft 3D with subtle shadows
- Single focal point
- Clean, breathable composition
- Professional, trustworthy feel

Avoid: Blue/purple, saturated colors, clutter, literal photos
```

---

## 4. 设计原则详解

### 4.1 留白原则 (40%+ Rule)

**定义**: 画面至少 40% 区域为空白或极简背景

**实施方法**:
1. 主体元素占据画面中心 30-40%
2. 四周预留宽敞边距
3. 元素之间保持充足间距

**Prompt 表达**:
```
Generous white space surrounding the central element,
breathable composition with wide margins,
clean uncluttered background
```

### 4.2 单一焦点原则

**定义**: 每张图传达一个核心概念,视觉焦点唯一

**实施方法**:
1. 主体元素明显大于其他元素
2. 使用对比、颜色、光影引导视线
3. 避免多个同等视觉权重的元素

**Prompt 表达**:
```
Single dominant focal point in the center,
all other elements subtle and supporting,
clear visual hierarchy
```

### 4.3 抽象隐喻原则

**定义**: 用抽象符号代替具象描绘

| 概念 | ❌ 具象表达 | ✅ 抽象表达 |
|------|-----------|-----------|
| AI 工具对比 | 10 个工具界面截图 | 10 个浮动卡片 + 连线 |
| 决策流程 | 详细流程图 | 3-4 个简单路径 + 箭头 |
| 数据对比 | 完整表格 | 抽象柱状图符号 |

**Prompt 表达**:
```
Abstract symbolic representation rather than literal depiction,
conceptual shapes and forms,
avoid photographic realism
```

### 4.4 Stripe 风格元素

**从 Stripe 学习的设计手法**:

1. **3D 元素处理**:
   - 柔和的 3D 形状（非夸张的立体效果）
   - 微妙的阴影和高光
   - 轻微的景深效果

2. **渐变处理**:
   - 柔和过渡，无明显色阶断层
   - 多色渐变（3-4 种颜色）
   - 渐变方向有动态感

3. **运动暗示**:
   - 元素排列有方向性
   - 暗示流动或移动
   - 但整体平衡稳定

**Prompt 表达**:
```
Stripe-style design: soft 3D elements with gentle shadows,
smooth multi-color gradients with no harsh transitions,
composition with implied motion but balanced stability
```

---

## 5. 图片类型规范

### 5.1 Hero Image (封面图)

**用途**: 文章开头 + featured_image
**比例**: 16:9, 2K 分辨率
**设计要点**:
- 最强视觉冲击力
- 传达文章核心主题
- 可包含简洁标题文字
- 品牌识别度最高

**Brand Layer 要求**:
- 绿色渐变占主导
- 40%+ 留白
- 单一主视觉元素

### 5.2 Concept Image (概念图)

**用途**: 说明抽象概念、决策流程
**比例**: 16:9, 1K 分辨率
**设计要点**:
- 抽象隐喻优先
- 简化为 3-5 个核心元素
- 辅助理解，非机械信息堆砌

**Brand Layer 要求**:
- 极简构图
- 象征性符号
- 清晰视觉逻辑

### 5.3 Comparison Image (对比图)

**用途**: 数据对比、产品对比
**比例**: 16:9, 1K 分辨率
**设计要点**:
- 信息层级清晰
- 颜色编码辅助对比
- 可读性优先，但保持美学

**Brand Layer 要求**:
- 留白原则依然适用
- 简化表格为抽象符号
- 避免密集信息堆叠

---

## 6. 质量检查清单

### 图片生成后检查项

- [ ] **色彩**: 是否使用绿色中心渐变？无蓝紫色调？
- [ ] **留白**: 画面是否有至少 40% 留白？
- [ ] **焦点**: 视觉焦点是否唯一且清晰？
- [ ] **抽象度**: 是否避免了过于具象的表达？
- [ ] **比例**: 是否为 16:9？
- [ ] **分辨率**: Hero 为 2K，其他为 1K？
- [ ] **Brand Layer**: Prompt 中是否包含完整 Brand Layer？
- [ ] **Stripe 风格**: 是否体现柔和 3D、渐变、留白？

---

## 7. 迭代机制

### 7.1 用户反馈收集

**方式 1: 参考图片**
```
用户: "我喜欢这个风格 [URL]，可以参考一下吗？"
→ Claude 分析图片，提取设计元素，更新本规范
```

**方式 2: 文字描述**
```
用户: "我觉得绿色太深了，能浅一点吗？"
→ Claude 更新色彩规范，调整 Prompt 模板
```

**方式 3: 竞品参考**
```
用户: "参考 [竞品] 的配图风格"
→ Claude 分析竞品，提取可学习元素（注明不学习的部分）
```

### 7.2 规范更新流程

1. **用户提供反馈** → Claude 理解需求
2. **Claude 更新本文档** → 修改对应章节
3. **更新 Editor SKILL.md** → 引用最新规范
4. **重新生成测试图片** → 验证效果
5. **用户确认** → 规范正式生效

### 7.3 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| v1.1 | 2026-01-30 | 新增 Section 0 视觉规范体系，引用 THUMBNAIL_VISUAL_GUIDE.md |
| v1.0 | 2026-01-15 | 初始版本，定义绿色中心色彩体系、ICSB 框架、Stripe 风格参考 |

---

## 8. 附录: 常见错误与修正

### 错误示例 1: 信息过载

**问题**: 画面塞满元素，无留白
**修正**: 保留核心元素 3-5 个，其余删除，增加边距

### 错误示例 2: 颜色饱和度过高

**问题**: 使用鲜艳的纯绿色 (#00FF00)
**修正**: 使用低饱和度绿色 (#10B981) + 渐变

### 错误示例 3: 多焦点混乱

**问题**: 同时有 5 个同等大小的主体
**修正**: 放大一个主体为焦点，其他作为辅助

### 错误示例 4: 过于具象

**问题**: 使用真实产品截图堆砌
**修正**: 用抽象卡片、符号代替截图

### 错误示例 5: 蓝紫色调渗入

**问题**: Prompt 写了 "tech blue" 或 "purple accent"
**修正**: 明确写 "NO blue or purple, green-centered only"

---

**文档维护者**: Claude Sonnet 4.5 + Editor Skill v2.2
**最后更新**: 2026-01-15
**状态**: ✅ 正式启用

---

## Sources

- [Google Nano Banana 2 API: AI Image Generation + Editing | fal.ai](https://fal.ai/models/fal-ai/nano-banana/api)
- [How to Specify Aspect Ratio in Nano Banana Pro: Complete 2025 Developer Guide](https://www.aifreeapi.com/en/posts/nano-banana-aspect-ratio-guide)
