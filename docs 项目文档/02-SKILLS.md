# 02 - Skills 清单

> 所有 Skills 的 High-Level 定义与分类 (v2.7 - 2026-01-21 更新)

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
├── core/                 # 核心入口 (5 个 Skills)
│   ├── smart-launcher/
│   ├── growth-topic-scout/
│   ├── aeo-analyzer/
│   ├── editor/
│   └── auto-improver/
│
├── writers/              # Writer 组 (4 个 Skills)
│   ├── blog-tutorial-writer/
│   ├── blog-list-writer/
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
| **smart-router** | v2.0 | 智能路由，自然语言意图识别 | 自动激活 | ✅ |
| **smart-root** | v2.2 🆕 | 交互式选题确认 + 版本验证 | "帮我写", "vs", "对比" | ✅ |
| **batch-processor** | v1.0 | 批量处理多 URL | "批量", "多个" | ✅ |
| **aeo-analyzer** | v2.4 | AEO 内容评估 (100 分制) | "AEO 分析" | ✅ |
| **auto-improver** | v2.1 | 基于 AEO 评分自动改进 | "改进文章" | ✅ |
| **growth-topic-scout** | v1.2 | 竞品分析 + 选题发现 | "竞品分析", "选题" | ✅ |
| **editor** | v2.6 | 图片生成 + 优化 + 版本检查 | "edit article" | ✅ |
| **competitive-validator** | v1.0 🆕 | 竞品验证 + PASS/FAIL 判定 | "竞品验证" | ✅ |
| **trending-monitor** | v1.0 🆕 | QDF 热点信号检测 | "热点监测" | ✅ |
| **markdown-to-framer** | v1.0 | 内容转 Framer CMS JSON | "convert to framer" | ✅ |
| **framer-previewer** | v1.0 | Framer 本地预览 | "preview framer" | ✅ |
| **youtube-transcript-fetcher** | v1.0 | YouTube 字幕抓取 | "抓取字幕", "transcript" | ✅ |

### smart-router v2.0

- **定位**: 智能路由层，自动识别用户意图并分发到对应工作流
- **输入**: 自然语言 | /命令 | URL
- **输出**: 路由到对应的 Skill 或命令
- **v2.0 升级**: 写作意图自动路由到 smart-root

### smart-root v2.2 🆕

- **定位**: 交互式选题确认 + 工具对决版本验证
- **输入**: 写作意图描述
- **输出**: 4 步问卷确认后全自动执行
- **流程**:
  1. Phase 0: 版本验证 (检测 vs/对比 → WebSearch 验证)
  2. Step 1: 内容类型选择 (含 Tool Showdown)
  3. Step 2: DataForSEO 搜索量验证
  4. Step 3: 标题选择 (5+ 选项)
  5. Step 4: 语言+配图确认
- **v2.2 升级**: 新增 Phase 0 版本验证，输出 verified_tools JSON

### batch-processor v1.0

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

### growth-topic-scout v1.2

- **定位**: 竞品内容分析，发现验证的选题机会
- **输入**: 竞品 URL
- **输出**: Top 10 选题 (100 分制) + Topic Brief
- **v1.2 升级**: 3 类型标题建议 + CTR 预测 + trending-monitor 集成

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
| **blog-tutorial-writer** | v2.2 | Tutorial 教程文章 | 1,800-2,500 | ✅ |
| **blog-list-writer** | v2.2 🆕 | List 榜单文章 + Tool Showdown | 2,500-3,500 | ✅ |
| **case-roundup-writer** | v1.3 | 案例汇总小博文 | 300-600 | ✅ |
| **chinese-previewer** | v1.0 | 中文预览版 | - | ✅ |

### blog-tutorial-writer v2.2

- **定位**: 生成 1,800-2,500 词的 Tutorial 教程文章
- **输入**: Topic Brief
- **输出**: 符合规范的 Tutorial 文章 + SEO 元数据
- **结构**: Direct Answer → Introduction → Background → Steps → [Prompt Structure (if AI)] → Mistakes → Tips → Conclusion → FAQ
- **v2.2 升级**: 版本继承机制，检测并保留 improved 版本的 E-E-A-T 内容

### blog-list-writer v2.2 🆕

- **定位**: 生成 2,500-3,500 词的 List 榜单文章
- **输入**: Topic Brief | verified_tools JSON (工具对决)
- **输出**: 符合规范的 List 文章 + 评测方法论 + 对比表格
- **结构**: Direct Answer → Introduction → Evaluation Methodology → Items → Comparison → How to Choose → FAQ
- **v2.2 升级**:
  - 新增 `tool_showdown` 内容类型
  - 10 固定 Headings 高对比度结构
  - Category Winners (Choose/Avoid) 格式
  - 2 表格 (Snapshot + Scorecard) + 3 CTA

### case-roundup-writer v1.3

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
| **TOOL_SHOWDOWN_TEMPLATE.md** 🆕 | 工具对决 10 Headings 结构 | blog-list-writer (tool_showdown) |
| **BLOG_CONTENT_REGISTRY.md** | 内容注册表 | smart-root |

---

## Skills 统计

| 类别 | 数量 | 已实现 |
|------|------|--------|
| 共用 Skills | 12 | 12 |
| Blog Skills | 4 | 4 |
| **总计** | **16** | **16** |

### v2.7 更新 (2026-01-21)

1. **smart-root v2.2** - Phase 0 版本验证 + verified_tools JSON
2. **blog-list-writer v2.2** - tool_showdown 模式 + 10 固定 Headings
3. **TOOL_SHOWDOWN_TEMPLATE.md** - 工具对决文章结构规范

### v2.6 更新 (2026-01-20)

1. **competitive-validator v1.0** - 竞品验证 + PASS/FAIL
2. **trending-monitor v1.0** - QDF 热点信号检测
3. **editor v2.6** - Visual Asset System
4. **aeo-analyzer v2.4** - Content Freshness Signals

---

**上一篇**: [01-ARCHITECTURE.md](./01-ARCHITECTURE.md) - 整体架构设计
**下一篇**: [03-AGENTS.md](./03-AGENTS.md) - Agents 清单与定义
