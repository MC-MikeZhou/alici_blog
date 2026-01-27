# InVideo 方法论优化存档

> 本文档记录了基于 InVideo 竞品洞察对 Kling Motion Control 文章进行优化的完整过程，供 Editor Skill 升级参考。

---

## 1. 洞察来源

### 1.1 竞品研究文件

| 文件 | 路径 | 核心内容 |
|------|------|----------|
| 内容框架 | `/competitive-research/invideo-blog/01-content-framework.md` | 8 种内容类型 + 37 种标题公式 |
| AEO 开篇 | `/competitive-research/invideo-blog/03-aeo-opening-patterns.md` | 24 种开篇模式 + 选择矩阵 |
| 标题公式 | `/.claude/skills/_shared/smart-launcher/TITLE_FORMULAS.md` | 37 种公式索引 |
| 开篇模式 | `/.claude/skills/_shared/smart-launcher/OPENING_PATTERNS.md` | 24 种模式索引 |

### 1.2 Editor v2.9 新增配置

| 配置文件 | 路径 | 用途 |
|----------|------|------|
| `title-formulas.yaml` | `/.claude/skills/_shared/editor/prompts/` | 标题公式验证 |
| `opening-patterns.yaml` | `/.claude/skills/_shared/editor/prompts/` | 开篇模式检测 |
| `integration-levels.yaml` | `/.claude/skills/_shared/editor/prompts/` | L1-L20 产品植入层级 |
| `citation-pyramid.yaml` | `/.claude/skills/_shared/editor/prompts/` | 5 层引用权威金字塔 |

---

## 2. 优化决策过程

### 2.1 原始文章分析

**AEO 评分预估**: ~82 分

**优点识别**:
- ✅ AIDA 开篇框架（直接断言模式）
- ✅ 5 步清晰 Workflow
- ✅ 4 种创意模式分类
- ✅ 7 要素 Prompt 框架
- ✅ 限制主动披露（透明度）
- ✅ 表格展示能力参数

**待优化点识别**:
- ⚠️ 标题缺少年份标签
- ⚠️ 缺少 Key Takeaways 前置
- ⚠️ FAQ 数量不足（5 个 vs 推荐 7-10 个）
- ⚠️ 无外部引用来源
- ⚠️ 缺少真实案例研究
- ⚠️ 无产品 CTA 植入
- ⚠️ 开篇模式可优化

### 2.2 InVideo 方法论映射

| InVideo 规则 | 适用性 | 优化动作 |
|--------------|--------|----------|
| **标题必须包含年份** | 高 | 添加 (2026) 后缀 |
| **Key Takeaways 前置** | 高 | 新增 6 点 Key Takeaways 章节 |
| **Data Hook 开篇** | 高 | 91% 统计 + $50K 成本对比 |
| **FAQ 7-10 个** | 高 | 从 5 个扩展到 10 个 |
| **L2 上下文 CTA** | 高 | Step 3 后植入 alici.ai 卡片 |
| **L5 Bonus 章节** | 高 | 新增 Quick Alternative 章节 |
| **外部引用 ≥3** | 中 | 新增 Wyzowl + Kling 官方链接 |

### 2.3 用户确认结果

通过 AskUserQuestion 工具确认的选项：

1. **产品植入**: ✅ 添加 CTA + Bonus 章节（InVideo L5-L7 策略）
2. **开篇模式**: ✅ 改用 Data Hook（数据钩子）
3. **标题年份**: 使用 "2026"
4. **Key Takeaways**: 前置到标题后
5. **FAQ 扩展**: 增加到 8-10 个问题

---

## 3. 具体优化内容

### 3.1 标题优化

**InVideo 公式应用**:
```
How to [Action] with AI in under [Time] — Complete Guide for [Year]
```

**执行结果**:
- 旧：`How to Turn Yourself Into Any Character Using Kling Motion Control`
- 新：`How to Turn Yourself Into Any Character Using Kling Motion Control (2026)`

### 3.2 Key Takeaways 章节

**位置**: Hero 图片后，正文前

**内容**:
```markdown
## Key Takeaways

- **Recording**: Use stable camera, good lighting, and solid-color clothes for best results
- **Frame 1**: Extract in CapCut at 4K resolution — this determines your final quality
- **Character Swap**: Use Nano Banana Pro with the 7-element prompt structure for accurate transformations
- **Kling Settings**: Select "Partial" mode when framing doesn't match perfectly
- **4 Creative Modes**: Face swap → Full character → Semi-VFX → Full scene modification
- **Duration Limit**: Maximum 30 seconds per generation at 1080p (Pro mode)
```

**AEO 作用**: AI 搜索引擎可直接抓取要点作为摘要回答

### 3.3 Data Hook 开篇

**InVideo 模式**: Data Hook + Problem-Solution

**执行结果**:
```markdown
**[91% of businesses now use video for marketing](https://www.wyzowl.com/video-marketing-statistics/).**
But creating character transformation videos traditionally requires $50,000+ motion capture equipment
and professional studios. Most creators assumed this type of content was out of reach.

[Kling 2.6 Motion Control](https://klingai.com) changed this entirely. With just a smartphone,
CapCut, and 30 minutes, you can transfer your real movements onto any character — celebrities,
anime figures, historical personas.
```

**数据来源**: Wyzowl Video Marketing Statistics 2024

### 3.4 FAQ 扩展

**原始 FAQ (5 个)**:
1. What equipment do I need to get started?
2. Can I record with my phone or do I need a professional camera?
3. How much does it cost to generate one video?
4. Can I use these videos for commercial purposes?
5. What if the generated character doesn't match my movements exactly?

**新增 FAQ (5 个)**:
6. What's the difference between Exact and Partial mode?
7. How do I fix character drift or clothing morph issues?
8. What's the best aspect ratio for Motion Control videos?
9. Can I create videos longer than 30 seconds?
10. What's the best tool for generating the transformed character image?

**InVideo 规则**: FAQ 章节应有 7-10 个问题，覆盖常见搜索查询

### 3.5 产品植入 (alici.ai)

**InVideo L2: 上下文 CTA 卡片**

位置：Step 3 (Nano Banana Pro) 后

```markdown
> **Quick Alternative**: If you don't have Nano Banana Pro, you can use
> [alici.ai Image Generator](https://app.alici.ai/pages/imageGen) to create
> the transformed character image. It supports the same 7-element prompt
> structure and exports at 4K resolution with free credits for new users.
```

**InVideo L3: FAQ 明确推荐**

```markdown
**What's the best tool for generating the transformed character image?**

[Nano Banana Pro](https://nanobananapp.com) is popular for its quality and prompt flexibility.
[alici.ai](https://app.alici.ai/pages/imageGen) offers a beginner-friendly alternative with
free credits, supporting the same 7-element prompt structure and exporting at 4K resolution.
```

**InVideo L5-L7: Bonus 章节**

```markdown
## BONUS: Quick Alternative Workflow with alici.ai

Don't have time for the full 5-step workflow? Here's a faster alternative that handles
character transformation in one tool:

1. Go to [alici.ai Video Generator](https://app.alici.ai/pages/videoGen)
2. Upload your reference video (the recording of yourself)
3. Describe your target character in one prompt using the 7-element structure
4. Generate and download in under 3 minutes
```

### 3.6 外部引用

| 引用 | 权威层级 | 位置 |
|------|----------|------|
| Wyzowl 视频营销统计 | Level 2 (Industry Report) | 开篇 Data Hook |
| Kling AI 官方 | Level 1 (Official Source) | 开篇 + What is 章节 |
| Nano Banana Pro | Level 3 (Tool Reference) | FAQ |

---

## 4. Editor Skill 升级建议

### 4.1 自动检测项

基于本次优化，Editor v2.9+ 应自动检测：

| 检测项 | 规则 | 动作 |
|--------|------|------|
| 标题年份 | 标题是否包含当前年份 | 自动添加 |
| Key Takeaways | 正文前是否有 Key Takeaways 章节 | 建议添加 |
| FAQ 数量 | FAQ 数量是否 ≥ 7 | 建议扩展 |
| 外部引用数量 | 引用数量是否 ≥ 3 | 建议添加 |
| 植入层级 | 是否达到 L3+ | 建议添加 CTA |
| 开篇模式 | 是否匹配 24 种 AEO 模式 | 建议优化 |

### 4.2 自动修复项

| 问题 | 自动修复 | 仅建议 |
|------|----------|--------|
| 标题缺年份 | ✅ 自动添加 | - |
| 开篇非 AEO 模式 | ✅ 自动重写 | - |
| FAQ 不足 | - | ⚠️ 建议扩展 |
| 引用不足 | - | ⚠️ 建议添加 |
| 植入层级低 | ✅ 自动添加 CTA | - |

### 4.3 报告模板建议

`04-editor-report.md` 应包含：

```markdown
## Competitive Review Results (InVideo Methodology)

### Title Analysis
- Formula Match: [公式名称] / No Match
- Year Tag: ✅ / ❌
- Action: [修改描述]

### Opening Analysis
- Pattern Match: [模式名称] / No Match
- Data Hook: ✅ / ❌
- Action: [修改描述]

### Integration Level
- Current: L[X]
- Target: L3+
- CTA Count: [数量]
- Action: [修改描述]

### Citation Authority
- Level 1-3 Ratio: [百分比]
- Total Citations: [数量]
- Action: [建议]

### FAQ Coverage
- Count: [数量] / Target: 7-10
- Action: [建议]
```

---

## 5. 预期效果

| 指标 | v1.0 | v2.0 | 变化 |
|------|------|------|------|
| AEO 预估分 | ~82 | 90+ | +8 |
| FAQ 数量 | 5 | 10 | +5 |
| 外部引用 | 0 | 4 | +4 |
| CTA 入口 | 0 | 3 | +3 |
| Key Takeaways | 无 | 6 点 | 新增 |
| 开篇模式 | 直接断言 | Data Hook | 升级 |
| 标题公式 | 无年份 | 含 2026 | 升级 |

---

## 6. 参考文档

- InVideo 竞品研究: `/competitive-research/invideo-blog/`
- Editor v2.9 配置: `/.claude/skills/_shared/editor/prompts/`
- SmartLauncher 公式库: `/.claude/skills/_shared/smart-launcher/`
- AEO 评分框架: `/.claude/skills/_shared/aeo-analyzer/EVALUATION_FRAMEWORK.md`
