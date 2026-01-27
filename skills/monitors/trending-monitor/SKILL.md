---
name: trending-monitor
version: "1.1"
description: >
  热点监测与内容新鲜度追踪 - 发现 QDF 信号，推荐时效性内容策略。
  触发词: 热点监测, trending topics, QDF 信号, 内容日历, content freshness
allowed-tools: WebSearch, WebFetch, Read, Write
dependencies:
  - capability: output-path-builder
---

# Trending Monitor Skill (v1.0)

## 设计理念

**核心问题**: 缺少热点追踪和内容新鲜度策略，难以吸引热点关注者和 AI 爱好者。

**解决方案**: 建立热点监测机制，检测 QDF 信号，制定内容日历和新鲜度策略。

## 触发条件

1. **定期触发**: 建议每周一检查热点趋势
2. **手动触发**: 用户说 "热点监测" / "trending topics" / "今天有什么热点"
3. **选题前触发**: growth-topic-scout 执行前可调用获取趋势信息

## QDF 信号检测

### 什么是 QDF?

**QDF (Query Deserves Freshness)** 是 Google 算法的一部分，当检测到以下信号时，会优先展示新鲜内容：

| 信号类型 | 检测方式 | 示例 |
|----------|---------|------|
| **新闻爆发** | 多家新闻网站同时报道 | "Sora 2 发布" |
| **博客频率** | 博客发帖量突然上升 | "Kling 新功能教程" |
| **搜索峰值** | 搜索量短期内急剧上升 | "ChatGPT o3" |

### QDF 检测流程

```
Step 1: 定义监测关键词列表 (AI Tools 核心领域)
        ↓
Step 2: WebSearch 检查近 24-48h 新闻
        ↓
Step 3: 分析搜索结果的发布时间分布
        ↓
Step 4: 识别 QDF 触发条件
        ↓
Step 5: 输出热点推荐报告
```

## 监测范围

### 核心监测关键词

| 类别 | 关键词 | 监测频率 |
|------|--------|---------|
| **AI 视频生成** | Sora, Kling, Runway, Pika, Luma | 每日 |
| **AI 图片生成** | Midjourney, DALL-E, Stable Diffusion, Flux | 每日 |
| **AI 聊天/助手** | ChatGPT, Claude, Gemini | 每日 |
| **AI 创意工具** | Synthesia, HeyGen, D-ID | 每周 |
| **通用 AI 趋势** | AI news, artificial intelligence | 每周 |

### 监测数据源

| 数据源 | 用途 | 集成方式 |
|--------|------|---------|
| Google News | 新闻报道检测 | WebSearch (site:news.google.com) |
| Google Trends | 搜索量趋势 | WebSearch (trends.google.com) |
| Twitter/X | 社交热点 | 已有 twitter-timeline-fetcher |
| Product Hunt | 新工具发布 | WebFetch |
| TechCrunch/TheVerge | AI 行业新闻 | WebFetch |
| Reddit r/artificial | 社区讨论热度 | WebSearch |

## 内容策略矩阵

### 基于新鲜度的内容类型

| 内容类型 | 字数 | 响应时间 | 触发条件 | 目标受众 |
|----------|------|---------|---------|---------|
| **Breaking News Roundup** | 300-600 | 24h 内 | QDF 信号强 | 热点关注者 |
| **Feature Update Guide** | 1800-2500 | 48h 内 | 产品发布新功能 | AI 爱好者 |
| **Weekly Trending Digest** | 800-1200 | 每周一 | 定期 | 内容创作者 |
| **Monthly Tool Ranking** | 2500-3500 | 每月末 | 定期 | 购买决策者 |
| **Evergreen Tutorial** | 1800-2500 | 任意 | 持续需求 | 新手 |

### 内容日历建议

```
周一: 检查上周热点 → 规划本周 Case Roundup
      └── 工具: trending-monitor → growth-topic-scout

周三: 发布 Breaking News Roundup (如有 QDF 信号)
      └── 工具: case-roundup-writer (300-600 词)

周五: 发布 Feature Update Guide (如有新功能发布)
      └── 工具: blog-tutorial-writer (1800-2500 词)

月末: 更新 Monthly Tool Ranking
      └── 工具: blog-list-writer (2500-3500 词)

持续: 监测 QDF 信号 → 快速响应
      └── 工具: trending-monitor (自动通知)
```

## 热点监测报告格式

```markdown
# 热点监测报告

> 生成时间: 2026-01-20 09:00
> 监测范围: AI 视频生成工具

## QDF 信号检测结果

### 🔥 高优先级 (24h 内响应)

| 热点 | 信号强度 | 来源数量 | 建议内容 |
|------|---------|---------|---------|
| Kling 2.0 发布 | ⬆️⬆️⬆️ | 15+ 篇新闻 | Breaking Roundup |
| Sora API 开放 | ⬆️⬆️ | 8 篇新闻 | Feature Guide |

### 📈 中优先级 (本周处理)

| 热点 | 信号强度 | 来源数量 | 建议内容 |
|------|---------|---------|---------|
| Runway Gen-3 更新 | ⬆️ | 3 篇新闻 | Tutorial 更新 |
| Pika 2.0 beta | ⬆️ | 5 篇博客 | 观察中 |

### 📊 趋势观察 (跟踪)

| 话题 | 趋势方向 | 搜索量变化 | 备注 |
|------|---------|-----------|------|
| AI video generator | 稳定 | +5% | 持续关注 |
| text to video | 上升 | +15% | 潜力话题 |

## 本周内容建议

### 立即行动
1. **Kling 2.0 发布** → 使用 case-roundup-writer
   - 预估关键词: "kling 2.0 features", "kling 2.0 vs runway"
   - 内容角度: 新功能演示 + 对比

### 本周计划
1. 更新 "Best AI Video Generators 2026" 榜单
2. 发布 Runway Gen-3 新功能教程

### 下周关注
1. Pika 2.0 正式发布 (预计)
2. OpenAI 发布会 (1/25)

## 数据来源

- Google News: 检索时间 2026-01-20 09:00 UTC
- Google Trends: 7 天趋势数据
- Twitter: #AIVideo 话题热度
```

## 新鲜度评估矩阵

### 现有内容新鲜度检查

对已发布的内容进行新鲜度评估：

| 检查项 | 评分标准 | 行动建议 |
|--------|---------|---------|
| **发布日期** | >6 个月 = 需更新 | 更新日期和数据 |
| **版本引用** | 非最新版本 = 需更新 | 更新版本和截图 |
| **价格信息** | 与官网不符 = 需更新 | 验证并更新 |
| **功能描述** | 已过时 = 需更新 | 添加新功能 |
| **竞品对比** | 缺少新竞品 = 需更新 | 添加新工具 |

### 更新优先级

```
更新紧急度 = 话题热度 × 内容过时程度

高紧急度 (立即更新):
- 热门话题 + 信息过时 (如价格变化、功能变化)

中紧急度 (本周更新):
- 热门话题 + 轻微过时 (如版本落后 1-2 个)

低紧急度 (本月更新):
- 长尾话题 + 信息过时
```

## 与其他 Skill 集成

### growth-topic-scout 前置调用

```
用户: "帮我找选题"
       ↓
smart-router: 检测到选题意图
       ↓
trending-monitor: 获取当前热点和 QDF 信号
       ↓
growth-topic-scout: 结合热点进行竞品分析
       ↓
输出: 带热点标记的选题报告
```

### case-roundup-writer 快速响应

```
trending-monitor 检测到 QDF 信号 (高强度)
       ↓
通知用户: "检测到 [话题] 热点，建议 24h 内发布 Roundup"
       ↓
用户确认 → case-roundup-writer 启动
       ↓
300-600 词快速 Roundup
       ↓
发布并标记为 "Breaking"
```

## 使用示例

### 周一热点检查

```bash
/trending-monitor
# 或
热点监测 AI 视频工具
```

### 指定关键词监测

```bash
/trending-monitor --keywords "sora 2, kling, runway gen-3"
```

### 检查内容新鲜度

```bash
/check-freshness /reports/2025-12-15-best-ai-video-tools/01-article-edited.md
```

## 输出文件

```
/reports/trending/
└── YYYY-MM-DD-trending-report.md   # 热点监测报告

/reports/YYYY-MM-DD-{topic}/
└── 00-freshness-check.md           # 内容新鲜度检查报告
```

## Changelog

### v1.0 (2026-01-20)
- 初始版本
- QDF 信号检测机制
- 内容策略矩阵
- 内容日历建议
- growth-topic-scout 集成
- case-roundup-writer 快速响应
