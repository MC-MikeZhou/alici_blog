# 02 - Skills 清单

> 所有 Skills 的 High-Level 定义与分类 (v3.2 - 2026-02-07 更新)

---

## Skills 组织结构

```
skills/
├── _docs/                # 共享文档 (6 个文件)
│   ├── BLOG_CONTENT_REGISTRY.md
│   ├── BLOG_WRITING_PRINCIPLES.md
│   ├── BLOG_WRITING_PRINCIPLES_v2.md
│   ├── BRAND_VISUAL_GUIDE.md
│   ├── PRODUCT_CATALOG.md
│   └── TOOL_SHOWDOWN_TEMPLATE.md
│
├── core/                 # 核心入口 (6 个 Skills)
│   ├── smart-launcher/
│   ├── growth-topic-scout/
│   ├── art-scout/            # 🆕 v1.1 Agent Team 多角色研究
│   ├── aeo-analyzer/
│   ├── editor/
│   └── auto-improver/
│
├── writers/              # Writer 组 (5 个 Skills + 共享层)
│   ├── _shared/              # 🆕 共享组件 (CTA_CARD, IMAGE_PLACEHOLDER, WRITER_COMPONENTS)
│   ├── blog-tutorial-writer/
│   ├── blog-list-writer/
│   ├── blog-showdown-writer/ # 🆕 v1.0 独立 Showdown 技能
│   ├── case-roundup-writer/
│   └── chinese-previewer/
│
├── utilities/            # 工具组 (7 个 Skills)
│   ├── youtube-transcript-fetcher/
│   ├── markdown-to-framer/
│   ├── framer-previewer/
│   ├── batch-processor/
│   ├── blog-cover-generator/
│   ├── image-generator/
│   └── image-placeholder-filler/
│
└── monitors/             # 监控分析组 (5 个 Skills)
    ├── competitive-validator/
    ├── competitive-insights/
    ├── trending-monitor/
    ├── batch-competitor-analyzer/
    └── keyword-matrix-generator/
```

---

## 共用 Skills

三条生产线共享的基础能力。

| Skill | 版本 | 用途 | 触发关键词 | 状态 |
|-------|------|------|------------|------|
| **smart-launcher** | v2.3 ⭐ | 四轨制统一入口 + 意图前置 | "帮我写", "vs", "对比", "seed mode" | ✅ |
| **growth-topic-scout** | v2.4 | 竞品分析 + 选题发现 + Seed D2 多样性发散 | "竞品分析", "选题", "seed mode" | ✅ |
| **art-scout** | v1.1 🆕 | Agent Team 多角色并行研究 | "团队研究", "全景扫描", "agent team" | ✅ |
| **batch-processor** | v1.1 | 批量处理多 URL | "批量", "多个" | ✅ |
| **aeo-analyzer** | v2.4 | AEO 内容评估 (100 分制) | "AEO 分析" | ✅ |
| **auto-improver** | v2.2 | 基于 AEO 评分自动改进 | "改进文章" | ✅ |
| **editor** | v2.9.2 | 图片生成 + 优化 + Editor Gate + Writer Feedback | "edit article" | ✅ |
| **competitive-validator** | v1.1 | 竞品验证 + PASS/FAIL 判定 | "竞品验证" | ✅ |
| **trending-monitor** | v1.1 | QDF 热点信号检测 | "热点监测" | ✅ |
| **markdown-to-framer** | v1.3 | 内容转 Framer CMS JSON | "convert to framer" | ✅ |
| **framer-previewer** | v1.1 | Framer 本地预览 | "preview framer" | ✅ |
| **youtube-transcript-fetcher** | v1.1 | YouTube 字幕抓取 | "抓取字幕", "transcript" | ✅ |

### smart-launcher v2.3 ⭐

- **定位**: 四轨制统一入口，意图前置架构
- **输入**: 自然语言 | /命令 | URL | 种子词
- **输出**: 路由到对应模式 → Writer → 全自动执行
- **v2.3 升级**: 新增 Route D 深度研究 (art-scout 集成)
- **四轨制**:
  1. [A] 全自动模式 - URL → 洗稿 → 一键到 Preview
  2. [B] 手动模式 - 5 步确认 + DataForSEO
  3. [C] Seed 模式 - 选题漏斗 (2-3 方向)
  4. [D] 深度研究 - art-scout 5 Agent 并行 (5-8 方向)
- **合并组件**: smart-router v2.0 + smart-root v2.2 (已废弃)

### art-scout v1.1 🆕

- **定位**: Agent Team 多角色并行选题研究
- **输入**: 种子词 + 3 个问题 (受众/目标/产品)
- **输出**: 5-8 个 Direction + Decision Brief + DataForSEO 验证数据
- **架构**: 5 Agent 并行 (keyword_scout, content_strategist, market_analyst, tech_specialist, user_persona) → CEO 综合
- **独立触发**: 团队研究, 多角色选题, 全景扫描, agent team
- **SmartLauncher 集成**: Route D 深度研究模式

### batch-processor v1.1

- **定位**: 批量处理多个 URL
- **输入**: URL 列表 (手动或文件)
- **输出**: 每个 URL 的独立输出目录 + 汇总报告
- **特性**: 队列管理 + 进度追踪 + 错误恢复

### aeo-analyzer v2.4

- **定位**: AEO (Answer Engine Optimization) 内容质量评估
- **输入**: 文章内容
- **输出**: 100 分制评分 + 改进建议
- **v2.4 升级**: 新增 Module 5 Content Freshness Signals (20 bonus points)

### auto-improver v2.1

- **定位**: 基于 AEO 评分自动改进文章
- **输入**: 原文章 + AEO 报告
- **输出**: 改进版 + Changelog
- **v2.1 升级**: E-E-A-T 保护标记系统

### growth-topic-scout v2.3

- **定位**: 竞品内容分析，发现验证的选题机会
- **输入**: 竞品 URL / 种子关键词（含发散选题）
- **输出**:
  - Mode A: Top 10 选题 + Topic Brief
  - Mode B: 关键词矩阵 + Top 20 选题 + 差距报告
  - Seed D1: 2 个 Direction（可直接开写）
  - Seed D2: 3 个 Direction + `diversity_report`（可量化多样性）
- **v2.3 升级**: 新增 Seed D2（多策略发散 → 语义聚类去重 → 多样性门禁 → DataForSEO 验证）

### editor v2.6

- **定位**: 图片生成 + 格式优化 + 版本继承检查
- **输入**: 文章草稿 + asset_plan.json (可选)
- **输出**: 编辑版文章 + asset_manifest.json
- **v2.6 升级**:
  - Module 7 版本对比检查
  - Visual Asset System (批量图片生成)
  - 数据契约: asset_plan.json → asset_manifest.json

### competitive-validator v1.0 🆕

- **定位**: 竞品验证，确保文章质量超越竞争对手
- **输入**: 文章 + 目标关键词
- **输出**: Top 5 竞品对比 + 快速 AEO 评分 + PASS/FAIL 判定
- **验证阈值**: PASS (≥30% 超过竞品)

### trending-monitor v1.0 🆕

- **定位**: QDF (Query Deserves Freshness) 热点信号检测
- **输入**: 话题/关键词
- **输出**: QDF 信号 (HIGH/MEDIUM/LOW/NONE) + 热点优先级 + 内容日历建议

---

## Blog 专用 Skills

Blog 生产线特有的内容生成能力。

| Skill | 版本 | 用途 | 字数 | 状态 |
|-------|------|------|------|------|
| **blog-tutorial-writer** | v3.1 ⭐ | Tutorial 教程文章 (Three-Tier) | 1,800-3,500 | ✅ |
| **blog-list-writer** | v3.1 ⭐ | List 榜单文章 (Blueprint 强制) | 4,500-10,000 | ✅ |
| **blog-showdown-writer** | v1.0 🆕 | Tool Showdown 工具对决 | 2,500-3,500 | ✅ |
| **case-roundup-writer** | v1.5 | 案例汇总小博文 | 300-600 | ✅ |
| **chinese-previewer** | v1.1 | 中文预览版 | - | ✅ |

### blog-tutorial-writer v3.1 ⭐

- **定位**: 生成 1,800-3,500 词的 Tutorial 教程文章
- **输入**: Topic Brief | Insight Pack (可选)
- **输出**: 符合规范的 Tutorial + SEO 元数据 + Self-Check JSON
- **v3.1 特性**:
  - Three-Tier 分级 (Tier 1/2/3 自动匹配复杂度)
  - Citable Block Taxonomy v3.0 (7 种引用块类型)
  - CTA/IMAGE 引用共享组件 (`/skills/writers/_shared/`)
  - experiment_pack 可选经验证据

### blog-list-writer v3.1 ⭐

- **定位**: 生成 4,500-10,000 词的 List 榜单文章
- **输入**: Topic Brief
- **输出**: Blueprint 强制结构 + Plan Pack Bundle + Validator Gate 报告
- **v3.1 特性**:
  - 4 种 Blueprint Profile (A/B/C/D)
  - Plan Pack Bundle (4 文件输出)
  - Listicle Validator Gate (PASS/FAIL)
  - methodology_level 护栏
  - tool_showdown 模式已独立为 blog-showdown-writer

### blog-showdown-writer v1.0 🆕

- **定位**: 生成 2,500-3,500 词的 Tool Showdown 工具对决文章
- **输入**: Topic Brief + verified_tools JSON
- **输出**: 11 固定标题结构 + Showdown Plan + Showdown Validator Gate
- **v1.0 特性**:
  - 从 blog-list-writer tool_showdown 模式独立
  - P4 Reframe 强制开篇 + L4 Integrator 定位
  - evidence_level 护栏 (source_based / hybrid / hands_on)
  - Source Attribution 章节

### case-roundup-writer v1.5

- **定位**: 生成 300-600 词的案例汇总小博文
- **输入**: Real Material (视频 URL、字幕、观察案例) - **必需**
- **输出**: micro_roundup 文章
- **v1.3 升级**:
  - Material Gate (强制真实素材)
  - 多维度拓展 (单一素材处理)
  - Prompts to Try (可复用 Prompt 模板)
  - 标题确认 (5+ 选项)

### chinese-previewer v1.0

- **定位**: 生成用于人工审核的中文预览版本
- **输入**: 英文文章
- **输出**: 中文要点预览 + AEO 亮点检查 + 审核清单

---

## 共享资源文件

Skills 共享的配置和参考文档。

| 文件 | 用途 | 依赖者 |
|------|------|--------|
| **PRODUCT_CATALOG.md** | CTA 映射、产品定价 | 所有 Writer Skills |
| **BRAND_VISUAL_GUIDE.md** | 绿色视觉规范、ICSB 框架 | Editor |
| **BLOG_WRITING_PRINCIPLES_v2.md** | 标题公式、评测方法论 | 所有 Writer Skills |
| **TOOL_SHOWDOWN_TEMPLATE.md** | 工具对决 11 Headings 结构 | blog-showdown-writer |
| **BLOG_CONTENT_REGISTRY.md** | 内容注册表 | smart-root |

---

## Skills 统计

| 类别 | 数量 | 已实现 |
|------|------|--------|
| 共用 Skills | 13 | 13 |
| Blog Skills | 5 | 5 |
| **总计** | **18** | **18** |

### v3.2 更新 (2026-02-07)

1. **art-scout v1.1** - Agent Team 多角色并行研究 (SmartLauncher Route D)
2. **blog-showdown-writer v1.0** - 独立 Showdown 技能 (从 blog-list-writer 分离)
3. **smart-launcher v2.3** - 四轨制架构 (新增深度研究)
4. **blog-tutorial-writer v3.1** + **blog-list-writer v3.1** - 共享组件层
5. **case-roundup-writer v1.5** - Editor Gate 集成

---

**上一篇**: [01-ARCHITECTURE.md](./01-ARCHITECTURE.md) - 整体架构设计
**下一篇**: [03-AGENTS.md](./03-AGENTS.md) - Agents 清单与定义
