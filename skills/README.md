# AliciBlog Skills

> 22 Skills + 6 共享文档，按功能分组

## 目录结构

```
skills/
├── README.md                 ← 本文件
├── _docs/                    ← 共享文档 (6 个)
├── core/                     ← 核心入口 (5 个 Skills)
├── writers/                  ← Writer 组 (4 个 Skills)
├── utilities/                ← 工具组 (8 个 Skills)
└── monitors/                 ← 监控分析组 (5 个 Skills)
```

---

## _docs/ - 共享文档

所有 Skills 的共享依赖文档。

| 文档 | 用途 | 依赖者 |
|------|------|--------|
| `BLOG_CONTENT_REGISTRY.md` | 内容类型注册表 | 所有 Writer |
| `BLOG_WRITING_PRINCIPLES.md` | 写作原则 v1 | 所有 Writer |
| `BLOG_WRITING_PRINCIPLES_v2.md` | 写作原则 v2 (标题公式、评测方法论) | 所有 Writer |
| `BRAND_VISUAL_GUIDE.md` | 绿色视觉规范、ICSB 框架 | Editor |
| `PRODUCT_CATALOG.md` | CTA 映射、产品定价 | 所有 Writer |
| `TOOL_SHOWDOWN_TEMPLATE.md` | 工具对决 10 Headings 结构 | blog-list-writer |

---

## core/ - 核心入口

统一入口和核心流程控制。

| Skill | 版本 | 触发词 | 用途 |
|-------|------|--------|------|
| **smart-launcher** | v2.1 | 帮我写, 写一篇, vs, 对比, seed mode | 三轨制入口 (全自动/手动/Seed) |
| **growth-topic-scout** | v2.2 | 竞品分析, 选题发现, seed mode | Top 10 选题 + Seed Mode 漏斗 |
| **aeo-analyzer** | v2.4 | AEO 分析 | 100 分评分系统 |
| **editor** | v2.9.2 | edit article | 图片 + Invideo Review + 4 项强制规则 |
| **auto-improver** | v2.2 | 改进文章 | 改进版 + Changelog + E-E-A-T 保护 |

---

## writers/ - Writer 组

四种文章类型的专用 Writer。

| Skill | 版本 | 触发词 | 输出 |
|-------|------|--------|------|
| **blog-tutorial-writer** | v2.4 | write tutorial | 1,800-2,500 词教程 |
| **blog-list-writer** | v2.4 | write list, vs, showdown | 2,500-3,500 词榜单 + tool_showdown |
| **case-roundup-writer** | v1.5 | 写小博文, case roundup | 300-600 词案例汇总 |
| **chinese-previewer** | v1.1 | 中文预览 | 审核摘要 |

---

## utilities/ - 工具组

辅助工具和格式转换。

| Skill | 版本 | 触发词 | 用途 |
|-------|------|--------|------|
| **youtube-transcript-fetcher** | v1.1 | 抓取字幕 | YouTube 字幕获取 |
| **markdown-to-framer** | v1.3 | convert to framer | Framer CMS JSON 输出 |
| **framer-previewer** | v1.1 | preview framer | 本地预览 HTML |
| **batch-processor** | v1.1 | 批量, batch | 队列执行 + 进度追踪 |
| **blog-cover-generator** | v1.0 | 生成封面, blog cover | 6 种背景类型 + Prompt 模板 |
| **image-sourcer** | v1.0 | 找配图, source images | Web 真实图片搜索 + 5 维评分 |
| **image-generator** | - | - | 图片生成 |
| **image-placeholder-filler** | - | - | 图片占位符填充 |

---

## monitors/ - 监控分析组

竞品监控和数据分析。

| Skill | 版本 | 触发词 | 用途 |
|-------|------|--------|------|
| **competitive-validator** | v1.1 | 竞品验证 | Top 5 竞品对比 + PASS/FAIL |
| **competitive-insights** | - | - | 竞品洞察分析 |
| **trending-monitor** | v1.1 | 热点监测 | QDF 信号检测 |
| **batch-competitor-analyzer** | - | - | 批量竞品分析 |
| **keyword-matrix-generator** | - | - | 关键词矩阵生成 |

---

## 调用链

```
smart-launcher v2.1 (三轨制)
    ↓
growth-topic-scout v2.3 (Seed D2 可选)
    ↓
writer 路由 (tutorial/list/roundup)
    ↓
editor gate → aeo-analyzer ⟷ improver
    ↓
competitive-validator → framer → preview
```

---

## 迁移说明

本目录结构于 2026-01-26 从 `.claude/skills/` 迁移而来。

旧路径映射:
- `.claude/skills/_shared/` → `skills/core/` + `skills/utilities/` + `skills/monitors/`
- `.claude/skills/blog/` → `skills/writers/`
- `.claude/skills/_shared/*.md` (文档) → `skills/_docs/`
