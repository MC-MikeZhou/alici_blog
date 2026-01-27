# AEO 评分报告

**文章**: How to Create Viral AI Videos: Sora 2, Kling & Runway Complete Guide
**评分日期**: 2025-01-15
**评分版本**: Draft v1

---

## 总分: 73/100 (Fair)

```
┌─────────────────────────────────────────────────────────────────┐
│                        AEO SCORE: 73                            │
├─────────────────────────────────────────────────────────────────┤
│  ████████████████████████████████████████████████░░░░░░░░░░░░░  │
│  |_______________|_______________|_______________|               │
│  0              40              75             100               │
│              Critical         Good          Excellent            │
│                                 ↑                                │
│                            目标门槛                              │
└─────────────────────────────────────────────────────────────────┘

当前状态: Fair (60-74) — 接近 Good 门槛，需小幅改进
```

---

## 分模块得分

| 模块 | 得分 | 满分 | 占比 | 状态 |
|------|------|------|------|------|
| **M1: 内容结构** | 29 | 30 | 97% | ✅ 优秀 |
| **M2: 技术可索引** | 15 | 25 | 60% | ⚠️ 需改进 |
| **M3: 引用与 E-E-A-T** | 10 | 25 | 40% | ❌ 薄弱 |
| **M4: 可见性设计** | 19 | 20 | 95% | ✅ 优秀 |

---

## Module 1: 内容结构 (29/30) ✅

| 评估项 | 得分 | 满分 | 说明 |
|--------|------|------|------|
| 标题/H1/描述对齐 | 4 | 4 | ✅ 完全对齐，关键词一致 |
| 标题层级结构 | 4 | 4 | ✅ H2/H3 层级清晰 |
| 开篇直答 | 4 | 4 | ✅ 前50词直接回答核心问题 |
| Q&A 格式 | 3 | 4 | ⚠️ 有 FAQ 但正文无散布式问答 |
| 列表/表格使用 | 4 | 4 | ✅ 多个表格和列表，使用恰当 |
| 段落长度 | 3 | 3 | ✅ 段落简短，可扫描性高 |
| 关键信息可见性 | 4 | 4 | ✅ 无折叠内容 |
| 文本化事实 | 3 | 3 | ✅ 所有数据为文本格式 |

**亮点**:
- 开篇直答执行出色，第一段即给出"三要素"答案
- 表格使用恰当（工具对比、提示词对比）
- 段落控制良好，无大段文字

**改进建议**:
- 在正文中增加 1-2 个问答式小标题（如 "What makes a prompt go viral?"）

---

## Module 2: 技术可索引 (15/25) ⚠️

| 评估项 | 得分 | 满分 | 说明 |
|--------|------|------|------|
| 页面可索引性 | 4 | 4 | ✅ 假设正常发布 |
| 片段资格 | 4 | 4 | ✅ 假设无 nosnippet |
| JS 渲染依赖 | 4 | 5 | ⚠️ Framer 有部分 JS 依赖 |
| Schema Markup | 0 | 4 | ❌ **缺失** - 需添加 |
| Schema 一致性 | 0 | 4 | ❌ 无 Schema 无法评估 |
| 语义 HTML | 3 | 4 | ⚠️ 需确认 Framer 输出 |

**主要问题**:
> ❌ **缺少 Schema Markup** (-8 分)
>
> Schema 占 Perplexity 排名算法约 10%。建议添加:
> - `Article` Schema (文章基本信息)
> - `FAQPage` Schema (FAQ 章节)
> - `HowTo` Schema (步骤内容)

**改进建议**:
```json
// 发布时需添加的 Schema 类型
{
  "@type": "Article",
  "headline": "How to Create Viral AI Videos...",
  "author": { "@type": "Person", "name": "..." },
  "datePublished": "2025-01-15",
  "dateModified": "2025-01-15"
}

{
  "@type": "FAQPage",
  "mainEntity": [
    { "@type": "Question", "name": "How long should AI videos be for TikTok?" }
    // ... 5 个 FAQ
  ]
}
```

---

## Module 3: 引用与 E-E-A-T (10/25) ❌

| 评估项 | 得分 | 满分 | 说明 |
|--------|------|------|------|
| 独立可引用块 | 4 | 4 | ✅ 多个独立可引用的结论句 |
| 具体数据统计 | 3 | 4 | ⚠️ 有数据但可更多 |
| 来源归属 | 1 | 4 | ❌ **缺失** - 无外部来源 |
| 作者信息 | 0 | 4 | ❌ **缺失** - 无作者 |
| 作者凭证 | 0 | 3 | ❌ **缺失** - 无凭证 |
| 发布/更新日期 | 2 | 3 | ⚠️ 有发布日期，无更新日期 |
| 外部权威信号 | 0 | 3 | ⚠️ 新文章，暂无外链 |

**主要问题**:

> ❌ **缺少作者信息** (-7 分)
>
> E-E-A-T 是 AI 引用的重要信号。建议添加:
> - 作者姓名
> - 作者职位/背景 (如 "AI Content Strategist")
> - 作者头像

> ❌ **缺少来源引用** (-3 分)
>
> AI 更倾向引用"自己有来源"的内容。建议为以下数据添加来源:
> - "85% of social video is watched without sound" → 来源?
> - "7-15 seconds optimal for TikTok" → TikTok 官方数据?
> - Sora/Kling/Runway 功能描述 → 官方文档链接

**改进建议**:
1. 添加作者信息块
2. 为关键数据添加来源链接
3. 添加 "Last updated: YYYY-MM-DD" 时间戳

---

## Module 4: 可见性设计 (19/20) ✅

| 评估项 | 得分 | 满分 | 说明 |
|--------|------|------|------|
| 语义化 URL | 4 | 4 | ✅ `/how-to-create-viral-ai-videos` |
| Meta 描述含直答 | 3 | 4 | ⚠️ 描述性但未直接回答 |
| 品牌/实体一致性 | 4 | 4 | ✅ 命名一致 |
| 查询变体覆盖 | 4 | 4 | ✅ 覆盖多种问法 |
| 主题相关 FAQ | 4 | 4 | ✅ 5 个高度相关问题 |

**改进建议**:
- Meta description 可改为直接回答式:
  > "To create viral AI videos, use Sora 2, Kling 2.0, or Runway Gen-4 with the formula: familiar format + unexpected twist. This guide covers tool selection, prompt writing, and platform optimization."

---

## 优先改进清单

| 优先级 | 改进项 | 预期提分 | 工作量 |
|--------|--------|----------|--------|
| 🔴 P0 | 添加作者信息和凭证 | +7 分 | 5 分钟 |
| 🔴 P0 | 添加来源引用 (3-5 个) | +3 分 | 15 分钟 |
| 🟡 P1 | 确保发布时有 Schema | +8 分 | 发布配置 |
| 🟢 P2 | 优化 Meta description | +1 分 | 2 分钟 |
| 🟢 P2 | 正文增加问答式小标题 | +1 分 | 5 分钟 |

**改进后预期得分**: 73 + 10 = **83 分** (Good)

---

## 可引用块识别

以下内容最可能被 AI 答案引擎引用:

### 1. 核心公式 (高引用潜力)
> "Creating viral AI videos requires three core elements: the right tool, a compelling prompt, and platform-optimized formatting."

### 2. 提示词结构 (高引用潜力)
> "[Familiar Format] + [Unexpected Subject/Twist] + [Specific Details] + [Tone/Style]"

### 3. 工具推荐 (中引用潜力)
> "Kling 2.0 is the most beginner-friendly AI video generator. It offers open access without waitlists, generates quickly, and produces consistent results with simple prompts."

### 4. 平台数据 (中引用潜力)
> "The optimal length for TikTok AI videos is 7-15 seconds."

---

## 结论

**当前状态**: 文章内容结构优秀 (97%)，但 E-E-A-T 信号薄弱 (40%)。

**最小改进方案**: 添加作者信息 + 3-5 个来源链接，即可达到 75+ 分门槛。

**建议行动**: 执行 auto-improver 进行自动改进，或手动修改后重新评分。
