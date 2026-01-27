# E-E-A-T 强化指南

> **版本**: v1.0
> **基于**: Editor Skill v2.9 Module 6 + citation-pyramid.yaml
> **最后更新**: 2026-01-23
> **文档用途**: E-E-A-T 内容深度优化的完整参考

---

## 什么是 E-E-A-T？

E-E-A-T 是 Google 搜索质量评估指南的核心框架，用于评估内容的可信度和价值：

| 维度 | 英文 | 含义 |
|------|------|------|
| **E** | Experience | 经验 - 作者是否有真实的使用/测试经验 |
| **E** | Expertise | 专业性 - 作者在该领域是否具备专业知识 |
| **A** | Authoritativeness | 权威性 - 内容来源是否权威可信 |
| **T** | Trustworthiness | 可信度 - 信息是否准确、透明、可靠 |

---

## 四维度评估标准

### 1. Experience（经验）

**检查项**:
- [ ] 原创案例研究 ≥ 2（含完整 prompt/config + 具体结果）
- [ ] 第一人称叙述 ≥ 1（"我们测试发现...", "Based on our testing..."）
- [ ] 迭代示例 - 至少一个 before/after 或 v1 → v2 改进故事

**评分标准**:

| 等级 | 描述 |
|------|------|
| **A** | 2+ 详细案例研究 + 具体结果 + 第一人称测试方法论 |
| **B** | 1 详细案例研究 + 第一人称测试描述 |
| **C** | 仅通用示例 OR 声称测试但无具体细节 |
| **D** | 无原创示例，仅引用外部案例 |
| **⛔ BLOCKING** | 文章声称专业/测试但提供零证据 |

**正确示例**:
```markdown
## Real-World Test: Kling 2.6 vs Runway Gen-3

We generated 200 videos across both models (n=200) to compare quality and speed.

**Test Setup**:
- Prompt: "A dancer performing hip-hop moves in a neon-lit studio"
- Settings: 1080p, 5 seconds, high quality
- Date: January 2026

**Results**:
| Metric | Kling 2.6 | Runway Gen-3 |
|--------|-----------|--------------|
| Generation Time | 45s | 120s |
| Motion Coherence | 9/10 | 7/10 |
| Cost per video | $0.10 | $0.25 |
```

---

### 2. Expertise（专业性）

**检查项**:
- [ ] 作者命名（禁止 "Content Team", "Editorial Staff" 等匿名署名）
- [ ] Bio 具体 - 必须包含：具体职位 + 公司/项目 + 年限/成就
- [ ] 作者 URL 可验证 - 指向 LinkedIn/Twitter/个人网站等可验证页面
- [ ] 内容体现专业知识（不仅仅是 bio 声明）

**评分标准**:

| 等级 | 描述 |
|------|------|
| **A** | 命名作者 + 可验证背景 + 内容展示深度领域知识 |
| **B** | 命名作者 + Bio 中声明背景 |
| **C** | 命名作者但 Bio 通用 |
| **D** | 团队署名 |
| **⛔ BLOCKING** | 无任何作者信息 |

**正确示例 - 命名作者**:
```yaml
author:
  name: "Hans Chen"
  title: "CEO & AI Video Researcher"
  company: "alici.ai"
  bio: "Hans has tested 10,000+ AI video prompts across Kling, Runway, Sora, and Veo. His research on Motion Control optimization has been featured in TechCrunch."
  url: "https://linkedin.com/in/hanschen"
  avatar: "/images/authors/hans-chen.jpg"
```

**错误示例 - 团队署名**:
```yaml
author:
  name: "alici.ai Content Team"  # ❌ 禁止
```

---

### 3. Authoritativeness（权威性）+ 引用权威金字塔

**检查项**:
- [ ] 所有统计数字标注来源
- [ ] 内部测试数据标注："alici.ai testing, [date], n=[sample size]"
- [ ] 外部来源优先级：官方文档 > 行业权威 > 社区讨论
- [ ] 引用权威等级分布：Level 1-3 来源应占 50%+

#### 5 级引用权威金字塔

| Level | 权威度 | 来源示例 | 权重 |
|-------|--------|----------|------|
| **L1** | 最高 | YouTube Press, OpenAI Blog, Meta, TikTok Newsroom, Google/Alphabet, Anthropic | 5 |
| **L2** | 很高 | Statista, eMarketer, Forrester, Gartner, HubSpot Research, Wyzowl, Pew Research | 4 |
| **L3** | 高 | TechCrunch, AdWeek, Search Engine Journal, CNBC, The Verge, Wired, VentureBeat | 3 |
| **L4** | 中 | Wistia, VidYard, Ahrefs Blog, SEMrush, Backlinko, TubeBuddy, VidIQ | 2 |
| **L5** | 补充 | G2, Capterra, TrustPilot, Product Hunt | 1 |

#### 文章类型引用密度标准

| 文章类型 | 总引用数 | L1-3 比例目标 |
|----------|----------|---------------|
| Statistics | 135+ | 50%+ |
| Listicle | 10-20 | 40%+ |
| Tutorial | 5-10 | 30%+ |
| Guide | 15-25 | 40%+ |
| Vertical | 0-3 | N/A（内部为主） |

#### 权威评分计算

```
weighted_score = sum(citation_count[level] * weight[level]) / total_citations
```

| 分数 | 等级 | 含义 |
|------|------|------|
| 4.0+ | A | 优秀的权威分布 |
| 3.0-3.9 | B | 良好的权威性 |
| 2.0-2.9 | C | 中等 - 建议升级 |
| <2.0 | D | 低权威 - 需要改进 |

#### 引用格式规范

**行内超链接引用（最常用）**:
```markdown
According to [Wyzowl](https://www.wyzowl.com/video-marketing-statistics/), 91% of businesses use video.
```

**括号归因（密集数据区域）**:
```markdown
Video content generates 1200% more shares (**Brightcove, 2024**).
```

**混合引用（关键数据点）**:
```markdown
YouTube reports 1 billion hours watched daily ([YouTube Press](url), 2024).
```

#### 常见引用错误

| 错误类型 | 错误示例 | 正确示例 | 严重度 |
|----------|----------|----------|--------|
| 无来源统计 | "Video increases conversions by 80%." | "Video increases conversions by 80% ([Wyzowl, 2024](url))." | 高 |
| 过时数据 | "According to a 2019 study..." | "According to the latest 2024 data from Statista..." | 高 |
| 死链接 | HTTP 404/403 | 验证链接有效性 | 高 |
| 二手引用 | "According to HubSpot citing Wyzowl..." | "According to Wyzowl's 2024 report..." | 中 |
| 模糊归因 | "Studies show that..." | "A Gartner study found that..." | 中 |

**评分标准**:

| 等级 | 描述 |
|------|------|
| **A** | 所有数据有来源 + 内部测试标注 + L1-3 比例 ≥50% |
| **B** | 大部分数据有来源 + L1-3 比例 40-49% |
| **C** | 部分数据有来源 + L1-3 比例 30-39% |
| **D** | 大部分无来源 + L1-3 比例 <30% |
| **⛔ BLOCKING** | 虚假/误导性归因 |

---

### 4. Trustworthiness（可信度）

**检查项**:
- [ ] 产品声明准确 - 价格、功能与官方页面一致
- [ ] 时效性信息标注 - 易过时信息标注 "as of [date]" / "截至 [日期]"
- [ ] 利益披露 - 自家产品推荐需声明关系
- [ ] 局限性说明 - 诚实说明局限性、缺点、edge cases

**评分标准**:

| 等级 | 描述 |
|------|------|
| **A** | 准确 + 时效标注 + 利益披露 + 透明局限性 |
| **B** | 准确 + 时效标注 |
| **C** | 部分过时/未验证的产品声明 |
| **D** | 多处不准确或误导性声明 |
| **⛔ BLOCKING** | 可证伪的虚假信息或隐藏利益冲突 |

**披露声明模板**:
```markdown
## Disclosure

alici.ai is a product of our company. While we believe it offers competitive features,
we've included both strengths and limitations in our evaluation. Pricing and features
are accurate as of January 2026. We recommend verifying current information on
official product pages before making decisions.
```

---

## 原创测试案例写法

### 案例结构模板

```markdown
## Case Study: [描述性标题]

**Objective**: [测试目标]

**Test Setup**:
- Sample size: n=[数量]
- Duration: [时间范围]
- Tools/Models: [使用的工具]
- Date: [测试日期]

**Methodology**:
[描述测试过程]

**Results**:
| Metric | Result | Comparison |
|--------|--------|------------|
| [指标1] | [数值] | [对比基准] |
| [指标2] | [数值] | [对比基准] |

**Key Findings**:
1. [发现1]
2. [发现2]

**What to Copy**:
- [可复用规律1]
- [可复用规律2]
```

### 迭代示例模板

```markdown
## From v1 to v2: What We Learned

### Version 1 Approach
[描述初始方法]

**Result**: [结果/问题]

### Version 2 Improvement
[描述改进]

**Result**: [改进后结果]

### The Difference
| Aspect | v1 | v2 | Improvement |
|--------|----|----|-------------|
| [方面1] | [旧值] | [新值] | [提升幅度] |
```

---

## E-E-A-T 总体评估

| 总体等级 | 发布就绪? | 所需行动 |
|----------|-----------|----------|
| 全部 A-B | ✅ 是 | 可选改进 |
| 任何 C | ⚠️ 需要审核 | 发布前解决 C 级问题 |
| 任何 D | ❌ 否 | 必须修复 D 级问题 |
| 任何 BLOCKING | ⛔ 停止 | 关键修复，禁止发布 |

---

## 作者信息模板

### 命名作者（推荐）

```yaml
author:
  name: "Full Name"
  title: "Job Title"
  company: "Company Name"
  bio: |
    [1-2 sentences about relevant experience and expertise]
    [Specific achievements or credentials if applicable]
  url: "https://linkedin.com/in/username"  # or Twitter/personal site
  avatar: "/images/authors/name.jpg"
```

### 团队署名（仅限无法归因的内容）

```yaml
author:
  name: "alici.ai Research Team"
  bio: |
    The alici.ai Research Team tests AI video and image generation tools
    across 10,000+ prompts monthly. All findings are based on first-hand
    testing and reproducible methodologies.
  url: "https://alici.ai/about"
```

**注意**: 团队署名会降低 E-E-A-T 评分，仅在无法确定具体作者时使用。

---

## 快速检查清单

发布前检查：

### Experience
- [ ] ≥2 原创案例研究（含具体数据）
- [ ] ≥1 第一人称测试描述
- [ ] 至少 1 个 before/after 或迭代示例

### Expertise
- [ ] 作者有真实姓名
- [ ] Bio 包含具体职位 + 公司 + 年限/成就
- [ ] 作者 URL 可验证

### Authority
- [ ] 所有统计数据有来源
- [ ] 内部测试数据标注 n=X
- [ ] L1-3 引用比例 ≥ 目标值
- [ ] 无死链接

### Trust
- [ ] 产品信息与官方一致
- [ ] 时效性信息标注日期
- [ ] 利益关系披露
- [ ] 诚实说明局限性

---

## 相关文档

- [Editor v2.9 能力总览](./editor-v2.9-capabilities.md)
- [版本管理标准](./content-version-standard.md)
- [内部链接指南](./internal-linking-guide.md)
- 引用金字塔配置: `/.claude/skills/_shared/editor/prompts/citation-pyramid.yaml`

---

*文档维护: Editor Skill v2.9.3 | 最后同步: 2026-01-23*
