---
name: competitive-validator
version: "1.1"
description: >
  竞品对比验证 - 在文章完成后自动搜索并评估 Top 5 竞品，
  验证文章质量是否超过竞品平均水平。
  触发词: 竞品验证, 对比验证, competitive validation, validate against competitors
allowed-tools: WebSearch, WebFetch, Read, Write
dependencies:
  - capability: output-path-builder
---

# Competitive Validator Skill (v1.0)

## 设计理念

**核心问题**: 内部 AEO 评分无法验证文章是否真的比竞品好。

**解决方案**: 在文章完成后自动搜索 Top 5 竞品，进行快速 AEO 评分对比，生成验证报告。

## 触发条件

1. **自动触发**: 文章 AEO 评分 ≥ 75 后自动执行
2. **手动触发**: 用户说 "竞品验证" / "对比验证" / "validate against competitors"
3. **集成触发**: smart-root 在发布流程前调用

## 验证流程

```
文章完成 (AEO ≥ 75)
        ↓
Step 1: 提取主关键词 (从标题/H1)
        ↓
Step 2: WebSearch 搜索该关键词
        ↓
Step 3: 抓取 Top 5 结果内容 (WebFetch)
        ↓
Step 4: 对每个竞品进行快速 AEO 评分
        ↓
Step 5: 生成对比报告
        ↓
验证结果:
├── ✅ PASS: 我们的分数 ≥ 竞品平均 × 1.3 (超过 30%)
├── ⚠️ MARGINAL: 我们的分数 = 竞品平均 ± 10%
└── ❌ FAIL: 我们的分数 < 竞品平均 × 0.9 (低于 10%)
```

## 输入要求

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| article_path | string | 是 | 文章文件路径 |
| aeo_score | number | 是 | 文章的 AEO 分数 |
| target_keyword | string | 否 | 目标关键词（可自动提取） |

## 输出文件

```
/reports/YYYY-MM-DD-{topic}/
└── 08-competitive-validation.md   # 竞品验证报告
```

## Step 1: 关键词提取

从文章中提取主关键词：

```
提取优先级:
1. YAML frontmatter 中的 target_keyword
2. H1 标题中的核心词组
3. Title 标签内容
4. 前 100 词中出现频率最高的实词
```

**示例**:
```yaml
---
title: "How to Use Kling Motion Control for AI Videos (2026)"
target_keyword: "kling motion control"
---
```

## Step 2: 竞品搜索

使用 WebSearch 搜索目标关键词：

```
搜索查询: {target_keyword}
结果数量: Top 10 (取前 5 个可访问的)
过滤规则:
  - 排除视频 (YouTube, Vimeo)
  - 排除社交媒体 (Twitter, Reddit)
  - 排除论坛
  - 优先保留博客、指南、官方文档
```

## Step 3: 竞品内容抓取

对每个竞品 URL 使用 WebFetch：

```
抓取内容:
  - 标题
  - H2/H3 结构
  - 开篇 200 词
  - FAQ 部分（如有）
  - 作者信息（如有）
  - 发布/更新日期（如有）
  - 外部链接数量
```

## Step 4: 快速 AEO 评分

对每个竞品进行简化 AEO 评分（满分 50 分）：

详见 `QUICK_SCORE_FRAMEWORK.md`

| 维度 | 权重 | 检查项 |
|------|------|--------|
| **结构清晰度** | 15 | H2/H3 层级、列表使用、FAQ 存在 |
| **直接回答** | 10 | 开篇是否有 40-60 词直答 |
| **E-E-A-T 信号** | 15 | 作者信息、来源引用、案例研究 |
| **内容新鲜度** | 10 | 发布日期、数据时效性 |

## Step 5: 验证阈值

| 对比结果 | 阈值 | 状态 | 行动建议 |
|----------|------|------|---------|
| **优秀** | 我们 ≥ 竞品平均 × 1.5 | ✅ EXCELLENT | 直接发布 |
| **良好** | 我们 ≥ 竞品平均 × 1.3 | ✅ PASS | 推荐发布 |
| **合格** | 我们 ≥ 竞品平均 × 1.1 | ⚠️ ACCEPTABLE | 可发布，建议优化 |
| **边缘** | 我们 = 竞品平均 ± 10% | ⚠️ MARGINAL | 需人工审核 |
| **不合格** | 我们 < 竞品平均 × 0.9 | ❌ FAIL | 需重新改进 |

## 验证报告格式

```markdown
# 竞品验证报告

> 生成时间: 2026-01-20 14:30
> Skill 版本: competitive-validator v1.0

## 基本信息

| 项目 | 值 |
|------|-----|
| 文章标题 | How to Use Kling Motion Control |
| 目标关键词 | kling motion control |
| 我们的 AEO 分数 | 84/100 |

## 竞品分析

| 排名 | 来源 | 快速评分 | 结构 | 直答 | E-E-A-T | 新鲜度 |
|------|------|---------|------|------|---------|--------|
| 1 | higgsfield.ai | 38/50 | 12/15 | 8/10 | 10/15 | 8/10 |
| 2 | runway.com | 35/50 | 10/15 | 7/10 | 12/15 | 6/10 |
| 3 | creator.com | 32/50 | 11/15 | 6/10 | 9/15 | 6/10 |
| 4 | medium.com | 28/50 | 8/15 | 5/10 | 8/15 | 7/10 |
| 5 | techblog.com | 25/50 | 7/15 | 4/10 | 8/15 | 6/10 |

## 统计分析

| 指标 | 值 |
|------|-----|
| 竞品平均分 | 31.6/50 |
| 竞品平均分 (换算) | 63.2/100 |
| 我们的分数 | 84/100 |
| 差距 | **+32.9%** |

## 验证结果

```
═══════════════════════════════════════════════════
   ✅ PASS - 超过竞品平均 30% 以上
═══════════════════════════════════════════════════
```

## 竞争优势分析

### 我们领先的维度
- ✅ 结构清晰度: 优于 5/5 竞品
- ✅ 直接回答: 优于 4/5 竞品
- ✅ 内容新鲜度: 优于 5/5 竞品

### 需要加强的维度
- ⚠️ E-E-A-T 信号: 优于 3/5 竞品 (建议增加外部引用)

## 改进建议

1. 增加更多外部权威来源引用 (当前: 3, 建议: 5+)
2. 考虑添加案例研究增强 Experience 信号
3. 添加作者 LinkedIn 链接增强 Authority

## 下一步行动

- [ ] 发布文章
- [ ] 监测搜索排名变化
- [ ] 2 周后复查 AI 引用情况
```

## 错误处理

| 错误 | 原因 | 处理 |
|------|------|------|
| 搜索无结果 | 关键词太小众 | 扩展关键词后重试 |
| 抓取失败 | 网站屏蔽 | 跳过该竞品，记录原因 |
| 竞品 < 3 个 | 可抓取竞品不足 | 标记为 "LOW_COMPETITION"，仍输出报告 |
| AEO 分数未提供 | 未运行 AEO 分析 | 先触发 aeo-analyzer |

## 与其他 Skill 集成

### smart-root 调用

```
smart-root 流程:
Writer → Editor → AEO Analyzer
                       ↓
              (AEO ≥ 75?)
              ├── Yes → Competitive Validator ← 新增
              │              ↓
              │         (PASS?)
              │         ├── Yes → Framer → 发布
              │         └── No → Auto-improver → 重新验证
              └── No → Auto-improver
```

### aeo-analyzer 后置

```
aeo-analyzer 完成后:
1. 读取 AEO 分数
2. 若 ≥ 75，自动触发 competitive-validator
3. 将验证结果追加到 03-aeo-score.md
```

## 使用示例

### 自动触发（推荐）

```bash
# AEO 分析完成后自动触发
/analyze-aeo /reports/2026-01-20-kling-motion-control/01-article-edited.md
# → AEO: 84/100 ✅
# → 自动触发竞品验证...
# → 竞品验证: PASS (+32.9%)
```

### 手动触发

```bash
/validate-competitors /reports/2026-01-20-kling-motion-control/01-article-edited.md
```

### 指定关键词

```bash
竞品验证 --keyword "kling motion control tutorial"
```

## Changelog

### v1.0 (2026-01-20)
- 初始版本
- 快速 AEO 评分框架
- 自动竞品搜索与抓取
- 阈值验证与报告生成
- smart-root 集成支持
