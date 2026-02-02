# CLAUDE.md

> AliciBlog: alici.ai AI 内容工厂，70%+ 自动化博客生产

## 核心架构

重要新增：模式选择除了下面的3种模式，新增一种thumbnail mode ,具体请查看thumbnail.md，然后启动

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    AliciBlog v2.8.2 (InVideo 原则集成)                    │
├─────────────────────────────────────────────────────────────────────────┤
│  输入层: 自然语言 | /命令 | URL | 批量 URL | Topic Brief | YouTube | Seed │
│                            ↓                                            │
│  smart-launcher v2.2 (意图前置架构):                                      │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │ Step 1.5: 素材使用意图 (v2.2 NEW) ⭐                            │     │
│  │   ┌─────────────────────────────────────────────────────────┐  │     │
│  │   │ Q: 你想如何使用这个素材？                                 │  │     │
│  │   │ [A] 洗稿 - 80%+ 保留原内容，品牌换 Alici AI               │  │     │
│  │   │ [B] 参考 - 作为起点，可以深挖扩展                         │  │     │
│  │   └─────────────────────────────────────────────────────────┘  │     │
│  │                          ↓                                     │     │
│  │ Phase 0: 模式选择 (根据意图推荐)                                │     │
│  │   ┌─────────────────────────────────────────────────────────┐  │     │
│  │   │ [A] 全自动模式 ← 洗稿推荐                                 │  │     │
│  │   │     URL → 1-2 问题 → 一口气到 Preview                     │  │     │
│  │   ├─────────────────────────────────────────────────────────┤  │     │
│  │   │ [B] 手动模式 ← 参考推荐                                   │  │     │
│  │   │     标题/方向 → DataForSEO 确认 → 选择 Writer             │  │     │
│  │   ├─────────────────────────────────────────────────────────┤  │     │
│  │   │ [C] Seed 模式 (选题漏斗)                                  │  │     │
│  │   │     种子词 → 竞品锚定 → 意图扩散 → 2 个选题               │  │     │
│  │   └─────────────────────────────────────────────────────────┘  │     │
│  └────────────────────────────────────────────────────────────────┘     │
│          ┌──────────────┼──────────────┼──────────────┐                 │
│          ↓              ↓              ↓              │                 │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐  │                 │
│  │ 全自动路线  │ │ 手动路线    │ │ Seed 路线 🆕    │  │                 │
│  │ URL+1-2问题 │ │ 5步确认     │ │ 6 Phase 漏斗    │  │                 │
│  │ 80%+ 洗稿   │ │ DataForSEO  │ │ 竞品锚定+验证   │  │                 │
│  └──────┬──────┘ └──────┬──────┘ └────────┬────────┘  │                 │
│         └───────────────┴─────────────────┘           │                 │
│                         ↓                             │                 │
│  执行阶段 (三条路线共享):                                                 │
│  Writer → **Editor Gate** → AEO ⟷ Improver → 竞品验证 →                  │
│  Preview → Framer JSON → (可选) Video JSON                                 │
│                                                                         │
│  非写作意图 (直接执行，不经 SmartLauncher 问卷):                         │
│  ├── 分析/选题 → scout-topic                                           │
│  ├── 评分/AEO → analyze-aeo                                            │
│  ├── 改进 → improve-article                                            │
│  ├── YouTube URL 单独输入 → fetch-transcript                           │
│  ├── 视频集成嵌入 → 查看/skills/utilities/convert-to-video-framer-json/skill.md                           │
│  └── 其他工具命令 → 直接执行                                            │
└─────────────────────────────────────────────────────────────────────────┘
```

| 层级 | 自动化程度 | 人工参与 |
|------|-----------|---------|
| 输入层 | 手动触发/自然语言 | 选择输入源或直接描述需求 |
| **SmartLauncher v2.2** | **意图前置 + 三轨制** ⭐ | **Step 1.5: 洗稿/参考 → 全自动/手动/Seed 推荐** |
| 处理层 | Agent 自主 | 仅 3 轮后仍 <75 分时介入 |
| 输出层 | 手动确认 | 中文预览 + 发布确认 |

---

## 5 条黄金规则

1. **Plan 模式优先** - 复杂任务 shift+tab×2
   > 好计划 = 返工率 -60% (Boris Cherny)

2. **30% 上下文警戒线** - 超过就 /compact
   > 模型 30% 开始退化，不是 100%

3. **验证闭环** - 必须过 aeo-analyzer
   > 有反馈 = 质量 2-3 倍 (Boris)

4. **外部记忆** - 进度写 00-implementation.md
   > Claude 无状态，文件是跨会话记忆

5. **一会话一主题** - 不混合任务
   > 上下文污染降低质量

---

## Skills 系统

| Skill | 版本 | 触发词 | 输出 |
|-------|------|--------|------|
| **smart-launcher** | **v2.2** ⭐ | 帮我写, 写一篇, vs, 对比, 对决, **YouTube URL**, **seed mode, 种子模式, 选题漏斗, 帮我找选题** | **意图前置架构** + **洗稿/参考模式** + **三轨制** + **4 种 Writer 路由** |
| **batch-processor** | **v1.1** | 批量, 多个, batch | 队列执行 + 进度追踪 + 汇总报告 |
| **growth-topic-scout** | **v2.2** 🆕 | 竞品分析, 选题发现, **seed mode, topic funnel** | Top 10 选题 + 3 类型标题 + CTR 预测 + **Mode D Seed Mode** + **Direction 对象** |
| **blog-tutorial-writer** | **v2.4** ⭐ | write tutorial | 1,800-2,500 词教程 + **版本继承** |
| **blog-list-writer** | **v2.4** 🆕 | write list, vs, showdown | 2,500-3,500 词榜单 + **tool_showdown 模式** + 版本验证集成 |
| **case-roundup-writer** | **v1.5** 🔥 | 写小博文, case roundup, 案例汇总 | 300-600 词案例汇总 + **Editor 集成** + **真实素材驱动** + **可复用 Prompt** |
| **editor** | **v2.9.2** ⭐ | edit article | 图片 + Invideo Review + **4 项强制规则** + **Module 10 Writer Feedback** |
| **aeo-analyzer** | **v2.4** | AEO 分析 | 100 分评分 (M3 新增内容深度检查) |
| **auto-improver** | **v2.2** ⭐ | 改进文章 | 改进版 + Changelog + **E-E-A-T 保护标记** |
| chinese-previewer | v1.1 | 中文预览 | 审核摘要 |
| markdown-to-framer | **v1.3** 🔧 | convert to framer | Framer CMS JSON (**修复**: 图片格式 + 特殊字符) |
| convert-to-video-framer-json | **v0.9** 🆕 | video framer json | 在现有 JSON 基础上插入视频，输出 *-video.json |
| framer-previewer | v1.1 | preview framer | 本地预览 HTML |
| **youtube-transcript-fetcher** | **v1.1** | 抓取字幕, YouTube transcript | YouTube 字幕 + 时间戳 + 保存至 /reports 待发文章/transcripts/ |
| **competitive-validator** 🆕 | **v1.1** | 竞品验证, competitive validation | Top 5 竞品对比 + 快速 AEO 评分 + PASS/FAIL 判定 |
| **trending-monitor** 🆕 | **v1.1** | 热点监测, QDF 信号 | QDF 信号检测 + 热点优先级 + 内容日历建议 |
| **blog-cover-generator** 🆕 | **v1.0** | 生成封面, blog cover, 封面图 | 6 种背景类型 + 青绿色品牌规范 + Prompt 模板 |
| **human-review-checklist** 🆕 | **v1.0** | 人工审核, 发布前检查, /human-review | 8 个检查模块 + **6 个自动修复** + **Writer Feedback Loop** + 竞品推荐检测 ⛔ BLOCKING |
| **mission-brief** 🆕 | **v1.0** | mission brief, 创建 brief, 定义需求 | 7 问智能问卷 + **自动推断** + mission-brief.json |
| **source-parser** 🆕 | **v1.0** | source parser, 解读素材, 分析素材 | **八维分析框架** (5 理解层 + 3 应用层) + 事实核查 |

**调用链 (v2.8.4 Updated)**:
- **前置准备流程 (可选)**: `mission-brief → source-parser` → 带着结构化素材进入写作
- **写作流程**: `smart-launcher v2.2 → growth-topic-scout v2.2 → writer路由 → editor gate → aeo-analyzer ⟷ improver → human-review-checklist → competitive-validator → framer → preview`

---

## 非写作指令：视频集成（convert-to-video-framer-json）
查看/skills/utilities/convert-to-video-framer-json/skill.md

---

## 版本继承规则 (v2.2/v2.4/v2.1 新增) ⭐

**核心原则**: 改进不可丢失 (Improvements Never Lost)

### 触发条件

当重写文章时，系统将检测是否存在 `01-article-improved-*.md`（improved 版本）:
- **存在** → 版本继承模式（必须保留 E-E-A-T 内容）
- **不存在** → 正常模式（从 topic brief 生成）

### 强制保留内容 (blog-tutorial-writer v2.2)

当 improved 版本存在时，以下内容 **必须保留**:

| 内容类型 | 保留规则 | 为什么 |
|---------|---------|--------|
| **Author Information** | YAML `author` block 完全一致 | E-E-A-T 信号 - 命名作者优于团队 |
| **Case Studies** | 所有案例研究完整保留 | Experience 证据 - 原创案例不可复现 |
| **Testing Methodology** | 所有 "n=X" 引用保留 | Authority 信号 - 测试数据建立可信度 |
| **External Sources** | 来源数量 >= 前版本 | 引用链 - 可以新增但不可删除 |
| **Disclosure** | 披露声明完全保留 | Trust 信号 - 透明度要求 |
| **FAQ** | 问题数量 >= 前版本 | AEO 优化 - FAQ 是高引用率内容 |

### 可更新内容

以下内容可以重写以整合新方法论:
- ✅ 标题格式（使用最新 How-to 公式）
- ✅ 开篇框架（应用 AIDA 结构）
- ✅ 章节组织（重构 H2/H3 层级）
- ✅ Prompt 框架（添加 7 要素系统）
- ✅ 示例代码（更清晰的演示）

### 验证检查 (editor v2.4 Module 7)

Editor 在输出前会自动验证版本继承:

| 检查项 | 阈值 | 失败等级 |
|--------|------|---------|
| Word Count | -20% max | ⛔ BLOCKING |
| Author Name | 完全匹配 | ⛔ BLOCKING |
| Case Studies | >= 前版本 | ⚠️ WARNING |
| Testing Refs (n=X) | 全部保留 | ⚠️ WARNING |
| External Sources | >= 前版本 | ⚠️ WARNING |
| FAQ Count | >= 前版本 | ⚠️ WARNING |

**BLOCKING 后果**: Editor 停止输出 `01-article-edited.md`，仅生成报告，需人工审核

### E-E-A-T 保护标记 (auto-improver v2.1)

Auto-improver Path B (E-E-A-T 优化) 输出时会添加保护标记:

```markdown
<!-- E-E-A-T_PROTECTED_CONTENT_START -->

## About the Author
[作者信息]

## Real-World Case Studies
[原创案例研究]

## Testing Methodology
[测试方法和数据]

## Sources
[外部来源引用]

## Disclosure
[利益披露声明]

<!-- E-E-A-T_PROTECTED_CONTENT_END -->
```

这些标记告诉后续 writer/editor: **此内容受保护，必须保留**

### 版本链示例

```
v1.0 draft (4,800 词)
    ↓ editor + auto-improver (3h45m 工作)
v1.1 improved (5,500 词)  ← E-E-A-T 投资 ⭐
    ↓ writer v2.2 重写 (检测 improved, 继承 E-E-A-T)
v2.0 (5,400 词)  ← 框架更新 + E-E-A-T 完整保留 ✅
    ↓ editor v2.4 Module 7 (验证继承)
v2.0 编辑完成 ← PASS (所有内容保留) ✅
```

### 文件命名

| 版本类型 | 文件名 | 说明 |
|----------|--------|------|
| 初稿 | `01-article-draft.md` | Writer 直接输出 |
| 改进版 | `01-article-improved-v1.md` | auto-improver 输出 ⭐ 后续基准 |
| 重写版 | `01-article-v2.md` | Writer 重写（必须继承 improved） |
| 编辑版 | `01-article-edited.md` | Editor 最终输出 |

**详细规范**: `/docs 项目文档/10-VERSION-INHERITANCE.md`

---

## 数据契约系统 (v1.3/v2.6 新增) 🆕

**核心理念**: Writer ↔ Editor 之间的标准化数据传递

### Writer v1.3 → Editor v2.6 契约

**Writer v1.3 输出**:
```
/reports 待发文章/YYYY-MM-DD-{topic}/
├── 01-article-draft.md          # 正文（含图片占位符）
├── asset_plan.json              # 给 Editor 的生成清单 🆕
└── prompt_pack.md               # 给读者的 copy-paste 包 🆕
```

**asset_plan.json 结构**:
```json
{
  "images": [
    {
      "id": "hero-image",
      "prompt": "detailed prompt for image generation",
      "role": "hero/inline/comparison",
      "placeholder": "![Image description](placeholder)",
      "context": "where this image appears in article"
    }
  ],
  "metadata": {
    "total_images": 5,
    "article_slug": "topic-slug",
    "generated_at": "2026-01-20T10:00:00Z"
  }
}
```

**Editor v2.6 输出**:
```
/reports 待发文章/YYYY-MM-DD-{topic}/
├── /assets/{slug}/              # 图片文件
│   ├── hero-image.png
│   ├── inline-1.png
│   └── comparison-grid.png
├── asset_manifest.json          # 资产清单 🆕
├── prompts_used.md              # 使用的 prompts 🆕
└── 01-article-edited.md         # 回填后的文章
```

**asset_manifest.json 结构**:
```json
{
  "images": [
    {
      "id": "hero-image",
      "original_prompt": "from asset_plan.json",
      "final_prompt": "potentially adjusted prompt",
      "file_path": "/assets/slug/hero-image.png",
      "cdn_url": "https://ct2.alici.ai/static/image/...",
      "generation_model": "fal-ai/banana-pro",
      "status": "success"
    }
  ],
  "summary": {
    "total_planned": 5,
    "total_generated": 5,
    "success_rate": "100%"
  }
}
```

### Visual Prompt Pack (Writer v1.3)

**prompt_pack.md 输出**:
- 包含 2-5 个可复用的图片生成 Prompt
- 基于文章内容和角色演化系统
- 用户可直接复制到其他工具（如 Midjourney, DALL-E）

**示例**:
```markdown
## Visual Prompt Pack

### Hero Image Prompt
A futuristic AI dashboard with holographic displays...
[Style: modern, professional | Ratio: 16:9]

### Workflow Diagram Prompt
Step-by-step flowchart showing the AI workflow...
[Style: clean, minimalist | Ratio: 4:3]
```

### Asset Pack Mode (Editor v2.6)

**批量图片生成流程**:
1. 读取 `asset_plan.json`
2. 对每个图片调用 FAL.ai API
3. 上传到 CDN
4. 生成 `asset_manifest.json`
5. 回填文章中的占位符
6. 输出 `prompts_used.md`（记录实际使用的 Prompt）

**错误处理**:
- 如果某个图片生成失败，保留占位符并在 manifest 中标记状态为 "failed"
- 生成汇总报告显示成功率

**详细规范**: `/docs 项目文档/11-DATA-CONTRACTS.md`

---

## Insight-Driven Blog Writer (Phase 6 - NEW) 🆕

**发布日期**: 2026-01-20
**核心理念**: Show, Don't Tell - 通过真实案例展示"what works"

### 新增工作流分支

```
传统：URL → Scout → Writer (1800-2500词) → Editor → Analyzer
新增：[交互式 Insight 收集] → Case Roundup Writer (300-600词) → Analyzer (micro rubric)
```

### case-roundup-writer v1.3 特性 🔥

**v1.3 改进（2026-01-20）**:
- ✅ **Material Gate**: 强制索取真实素材，拒绝编造案例
- ✅ **多维度拓展**: 单一素材时从多角度分析（工作流/场景/技巧/陷阱）
- ✅ **Prompts to Try**: 生成 2-3 个可复用 Prompt 模板
- ✅ **标题确认**: 提供 5+ 标题选项让用户选择

**输入**:
- **Real Material**（必需）: 视频 URL、字幕、观察案例
- Insight Pack（交互式收集或手动提供）
- Case Pack（从素材提取或多维度拓展）

**输出**:
- micro_roundup 文章（300-600 词）
- 结构：Direct Answer → Key Takeaways → Case Studies → **Prompts to Try** → How to Try It → Mini FAQ

**交互式 Insight Pack 收集** (6 个问题):
1. 核心观点（thesis）
2. 为什么现在值得写（why_now）
3. 关键要点（key_takeaways, 3-5 个）
4. 需要避免的信息（do_not_say, 可选）
5. 产品理念（product_lens）
6. 目标读者（audience）

**Case Pack 结构**:
- case_title: 案例标题
- what_happens: 发生了什么（80-100 词）
- why_it_works: 为什么有效（30-40 词）
- what_to_copy: 可复用规律（2-3 条）
- tags: 案例标签

**产品理念渗透机制**:
- 不是 CTA，而是教育性叙事
- 在 "Why it works" 中自然提及范式转移
- 在 "How to Try It" 中体现 One-prompt 理念
- 在工具选择中提及多模型一站式

**质量目标**:
- 字数: 300-600
- AEO 目标: ≥ 70 (micro_roundup 评分标准)
- 案例数: 2-5 个

**使用示例**:
```bash
/write-roundup https://www.youtube.com/watch?v=xxx https://www.youtube.com/watch?v=yyy
/write-roundup 写一篇关于 Kling Motion Control 的案例汇总
```

**文件存储**:
- Insight Pack: `/research 竞品分析/insights/YYYY-MM-DD-{topic-slug}.json`
- Case Pack: `/research 竞品分析/case-packs/YYYY-MM-DD-{topic-slug}_roundup-{number}.json`
- Article: `/reports 待发文章/YYYY-MM-DD-{topic}/01-article-draft.md`

**下一步 (Phase B/C/D)**:
- Phase B: 视频内容提取（transcript-to-case, 未来 Gemini 2.5 Flash）
- Phase C: AEO Analyzer 扩展（micro_roundup 专用评分标准）
- Phase D: 混合模式（URL + Insight Pack 融合）

**详细实施文档**: `/_archive 历史归档/00-PHASE-A-IMPLEMENTATION.md`

---

- **v2.8.4 前置准备流程（2026-02-02）** 🆕:
  - 🆕 `mission-brief v1.0` 上线：7 问智能问卷 + 自动推断 + mission-brief.json
  - 🆕 `source-parser v1.0` 上线：八维分析框架 (5 理解层 + 3 应用层) + 事实核查
  - 📐 **八维分析架构**：
    - Part A 素材理解层：核心内容 / 背景语境 / 批判性审视 / 价值提取 / 写作技巧
    - Part B SEO/AEO 应用层：SEO/AEO 信号 / 可复用数据 / 品牌适配
  - 🎯 **核心理念**：理解先于提取 - 先深度理解素材，再做 SEO/AEO 提取
  - 📁 **新增目录**：`/skills/preparation/` 存放前置准备类 skill

- **v2.8.3 视频集成后处理（2026-01-27）** ⭐:
  - 🆕 `convert-to-video-framer-json v0.9` 上线：在现有 Framer JSON 基础上插入视频，输出 `*-video.json`（非破坏性）。
  - 🔒 严格对齐 `blog_scheme_example.json`/`FIELD_SCHEMA.md`：仅新增 `video_link_1..10` 与 `article_body_content_2..10`，其余字段值全部来自源 JSON（缺失即中止）。
- 🧭 交互增强：展示“视频列表 + 段落预览（段1..段N）”，按“第 K 段之前/正文顶部”映射到 `video_link_N`（如第三段之前→`video_link_3`）。
- 🧰 上传改为手动：移除上传脚本依赖；文档改为 rsync 示例，要求先上传后粘贴 CDN 链接。
- 📚 文档与路由更新：`SKILL.md/AGENTS.md/CLAUDE.md` 增加非写作指令与反馈模板；`FIELD_SCHEMA.md` 补齐 example 中的字段说明。

**v2.8.2 InVideo 原则系统化集成（2026-01-26）** ⭐:
- ✅ **AUTO_ROUTE.md v2.3**: 新增 rewrite_constraints (source_attribution, no_fabricated_data, validate_claim_accuracy)
- ✅ **TOOL_SHOWDOWN_TEMPLATE.md v1.2**: Source Attribution 章节 + Reframe 开篇强制 + L4 模板
- ✅ **opening-patterns.yaml v2.1**: P4 tool_showdown_mandatory + pattern_requirements 章节
- ✅ **BLOG_WRITING_PRINCIPLES_v2.md v2.2**: Section 10 (Citation Standards) + Section 11 (洗稿哲学)
- ✅ **integration-levels.yaml v2.1**: L4 invideo_enhancement (模板 + validation + positioning_rules)
- ✅ **REWRITE_VALIDATION_TEMPLATE.md v1.0**: 洗稿模式 6 原则验证检查清单
- 🎯 **核心变化**: InVideo 原则从"隐式遵循"到"显式验证配置"
- 📊 **6 大原则**:
  - Key Takeaways 前置 (⛔ BLOCKING)
  - Reframe 开篇 P4 强制 (⛔ BLOCKING)
  - Source Attribution 章节 (⛔ BLOCKING)
  - 无虚假声明 (⛔ BLOCKING)
  - L4 整合者定位 (⚠️ WARNING)
  - 引用密度 ≥5/千字 (⚠️ WARNING)

**v2.8.1 SmartLauncher v2.2 意图前置架构发布（2026-01-26）** ⭐:
- ✅ **smart-launcher v2.2**: Step 1.5 素材使用意图 (洗稿/参考) + 意图驱动约束
- ✅ **AUTO_ROUTE.md**: rewrite_mode + reference_mode 配置 + 意图验证
- ✅ **MANUAL_ROUTE.md**: 参考模式扩展调研流程 + 三种扩展方向
- 🎯 **核心变化**: 内容类型不重要，重要的是用户想"洗稿还是参考"
- 📊 **用户定义**:
  - 洗稿: 80%+ 保留原内容，品牌换 Alici AI，禁止新增
  - 参考: 作为起点，可以深挖扩展、补充新内容

**v2.8 SmartLauncher v2.1 三轨制发布（2026-01-25）**:
- ✅ **growth-topic-scout v2.2**: Mode D Seed Mode + Direction 对象输出
- ✅ **smart-launcher v2.1**: 三轨制入口 (全自动/手动/Seed)
- ✅ **DataForSEO 升级**: 新增 3 个 AEO/LLM 相关数据维度
- ✅ **新增 Schema 文件**: MISSION_CONFIG_SCHEMA.json, DIRECTION_SCHEMA.json
- 🎯 **核心突破**: 选题漏斗系统，50-100 关键词 → 2 个可执行方向
- 📊 **成本优化**: ~$2.59 → ~$0.47 (standard)

**v2.75 SmartLauncher v2.0 测试通过（2026-01-23）**:
- ✅ **双轨制流程测试通过**: 手动路线 7/7 PASS + 全自动路线 7/7 PASS
- ✅ **Phase 0 模式选择**: 问卷正确显示全自动/手动两个选项
- ✅ **手动路线验证**: DataForSEO 强制展示 + "vs" 自动识别 Tool Showdown + 5+ 标题选项
- ✅ **全自动路线验证**: 1-2 问题 + 洗稿模式 80%+ + 一键到 Preview
- ✅ **Writer 路由验证**: 4 种核心方向正确路由到对应 Writer
- 📊 **测试覆盖**: 14/14 验证点全部通过

**v2.74 SmartLauncher v2.0 双轨制架构（2026-01-23）**:
- ✅ **smart-launcher v2.0**: 双轨制入口 - 全自动 vs 手动模式
- ✅ **全自动路线**: URL → 1-2 问题 → 洗稿模式 (80%+ 参考) → 一键到 Preview
- ✅ **手动路线**: 5 步确认 + 强制 DataForSEO 展示确认 + 用户选择 Writer
- ✅ **强制 growth-topic-scout**: 两条路线都必须调用，不再被绕过
- ✅ **明确 Writer 路由**: Tool Showdown / Listicle / Tutorial / Case Study
- ✅ **新增文件**: AUTO_ROUTE.md, MANUAL_ROUTE.md
- ✅ **COMBOS.md 简化**: 9 种组合 → 4 种核心方向
- 🎯 **核心变化**:
  - 用户入口处选择模式，清楚知道自己在哪条路线
  - 全自动模式主打高速批量洗稿
  - 手动模式提供精细控制和数据确认
- 📊 **预期效果**:
  - 用户模式感知: 不清楚 → 100% 清晰
  - growth-topic-scout 调用率: 可变 → 100%
  - DataForSEO 确认率 (手动): 0% → 100%
  - Writer 路由正确率: 可变 → 100%

**case-roundup-writer v1.3 升级（2026-01-20）** 🔥:
- ✅ **Material Gate**: 强制索取真实素材，拒绝编造案例
- ✅ **多维度拓展**: 单一素材时多角度分析（工作流/场景/技巧/陷阱）
- ✅ **Prompts to Try**: 每篇文章包含 2-3 个可复用 Prompt 模板
- ✅ **标题确认**: 提供 5+ 标题选项（问题式/How-to/洞察式/数字式）
- ✅ **Visual Prompt Pack**: 生成可复用的图片 Prompt（角色演化系统）
- ✅ **Asset Plan Output**: 输出 asset_plan.json 数据契约给 Editor
- 🎯 **核心改进**: 解决 Phase A 测试中的案例编造问题，确保真实案例驱动
- 📊 **预期效果**: 单一视频也能写完整文章，用户获得可直接使用的 Prompt

**v2.73.2 Smart Launcher 架构统一（2026-01-22）** 🆕:
- ✅ **smart-launcher v1.2**: 统一 Editor Gate - 所有 Writer 必须经过 Editor
- ✅ **smart-launcher v1.2**: 新增 Step 3.5 Writer Feedback Loop
- ✅ **case-roundup-writer v1.5**: 加入 Editor 流程，不再跳过
- ✅ **editor v2.9.2**: 新增 Module 10 Writer Feedback 机制
- 🎯 **核心变化**:
  - Editor 从"可选"升级为"强制"
  - 新增 BLOCKING → Writer 反馈循环
  - 用户首次看到的是 01-article-edited.md (通过 Editor)
- 📊 **预期效果**:
  - Editor 覆盖率: 67% (2/3 Writers) → 100% (3/3 Writers)
  - 强制规则遵守率: 可变 → 100%
  - 首次输出质量: 提前修复所有 BLOCKING 问题

**v2.73.1 Editor v2.9.1 强制规则升级（2026-01-22）**:
- ✅ **Module 3 增强**: Key Takeaways 强制前置 (⛔ BLOCKING)
- ✅ **Module 3 增强**: Data Hook 开篇强制 (⚠️ WARNING → 自动修复)
- ✅ **Module 5 增强**: 标题年份从 WARNING 升级为 ⛔ BLOCKING
- ✅ **Module 9 新增**: CTA Enforcement - 文末必须有 CTA 卡片
- 🎯 **核心变化**: 4 项从"建议"升级为"强制"的规则
- 📊 **基于**: Kling Motion Control 文章 v1.0→v2.0 优化洞察
- 📊 **预期效果**:
  - 标题年份覆盖率: 可变 → 100%
  - Key Takeaways 存在率: 可变 → 100%
  - Data Hook 开篇率: ~30% → 90%+
  - CTA 卡片覆盖率: 可变 → 100%

**v2.73 Editor v2.9 Invideo 竞品 Review（2026-01-22）**:
- ✅ **editor v2.9** 发布
  - **Module 3 增强**: 开篇优化 + 24 种 Invideo AEO 模式
  - **Module 5 增强**: 格式演化 + 37 种标题公式验证 + L1-L20 植入层级检测
  - **Module 6 增强**: E-E-A-T + 5 层引用权威金字塔评分
  - **自动修复**: 问题检测后自动优化（标题/开篇/CTA），引用仅建议
- ✅ **新增 YAML 配置文件**
  - `title-formulas.yaml`: 37 种标题公式（基于 invideo 竞品洞察）
  - `opening-patterns.yaml`: 24 种 AEO 开篇模式 + 选择矩阵
  - `integration-levels.yaml`: L1-L20 产品植入层级定义
  - `citation-pyramid.yaml`: 5 层引用权威金字塔 + 密度标准
- ✅ **报告模板更新**: `04-editor-report.md` 新增 Competitive Review Results 章节
- 🎯 **核心理念**: 将 Invideo 竞品洞察植入 Editor 的自动 Review 机制
- 📊 **预期效果**:
  - 标题公式匹配: 0% → 100% 验证
  - 开篇模式识别: 无 → 24 种模式检测
  - 植入层级: 无标准 → L3+ 目标
  - 引用权威: 无评分 → Level 1-3 ≥50% 目标

**v2.72 YouTube URL 路由修复（2026-01-22）** 🔧:
- ✅ **smart-launcher v1.1**: YouTube URL 单独输入自动路由到 fetch-transcript
- ✅ **检测逻辑**: 支持标准 watch URL、短链接、嵌入链接
- ✅ **简单前缀**: 允许"抓取"、"获取"、"字幕"等前缀
- 🎯 **核心修复**: 解决 YouTube URL 输入时误入写作问卷的问题

**v2.71 Markdown-to-Framer 修复（2026-01-22）** 🔧:
- ✅ **markdown-to-framer v1.3**: 图片格式修复 (无 figure, alt 在 src 前)
- ✅ **特殊字符处理**: em dash/smart quotes 替换为兼容字符
- ✅ **cover 字段简化**: 只保留 url，移除 alt 和 metadata
- 🎯 **核心修复**: 解决 Framer CMS 导入错误 "TypeError: o is not iterable"

**v2.7 Tool Showdown + Version Verification 升级（2026-01-21）** 🆕:
- ✅ **smart-root v2.2**: 新增 Phase 0 版本验证，检测 "vs/对比/对决" 意图时自动 WebSearch 验证工具版本
- ✅ **blog-list-writer v2.2**: 新增 `tool_showdown` 内容类型，使用 10 固定 Headings 高对比度结构
- ✅ **TOOL_SHOWDOWN_TEMPLATE.md**: 新增共享模板，定义工具对决文章结构规范
- 🎯 **核心解决**: 版本滞后问题 (Kling 2.0 → 2.6) + 缺少高对比度模板 (Category Winners)
- 📊 **预期效果**: 工具版本准确性 100%，对决文章结构一致性 100%

**v2.2/v2.6/v2.1 版本继承升级（2026-01-18）** ⭐:
- ✅ **blog-tutorial-writer v2.2**: 版本继承机制，检测并保留 improved 版本的 E-E-A-T 内容
- ✅ **editor v2.6**: Module 7 版本对比检查 + Visual Asset System (asset_plan.json → asset_manifest.json)
- ✅ **auto-improver v2.1**: E-E-A-T 保护标记系统，标记需保留的内容
- 🎯 **核心修复**: 防止重写时丢失 E-E-A-T 投资（如 Sora 2 guide v1.1→v2.0 问题）
- 📊 **预期效果**: 编辑工作受保护，版本迭代不再丢失内容

**v2.0-v2.1 Higgsfield 洞察升级（2026-01-18）** 🆕:
- ✅ **growth-topic-scout v1.2**: 3 类型标题建议 (Listicle/How-to/Insights) + 年份验证 + CTR 预测
- ✅ **blog-list-writer v2.0**: 强制年份 + 数字标题 + 5 维度评测方法论 + Core Positioning 列
- ✅ **blog-tutorial-writer v2.1**: How-to 标题公式 + 7 要素 Prompt 结构章节（AI 教程）
- ✅ **BLOG_WRITING_PRINCIPLES v2.1**: 新增"标题与结构标准"章节（基于 Higgsfield）
- 📚 **新增文档**: `/docs 项目文档/00-CONTENT-PHILOSOPHY.md` - 内容策略哲学
- 🎯 **核心洞察**: 公式化标题 = SEO 可预测性，评测方法论 = E-E-A-T Authority 信号

**v2.3 升级（2026-01-17）**:
- ✅ **editor v2.3**: 新增 Module 6 (E-E-A-T 内容深度检查)，所有模块强制执行
- ✅ **aeo-analyzer v2.3**: M3 重组为结构信号(12分) + 内容深度(13分)
- 🎯 **关键改进**: 修复 Editor 模块跳过问题，E-E-A-T 评分不再只看结构
- 📊 **预期效果**: 文章质量门禁更严格，减少"高分低质"情况

**v2.0 升级（2026-01-16）**:
- ✅ **blog-tutorial-writer v2.0**: AIDA 开篇框架 + Citable Block 系统 + 强化 E-E-A-T
- 📊 **验证结果**: 首次 AEO 评分 73 → 82 分（+9 分），无需 auto-improver 迭代
- 📝 **Changelog**: 查看 `/skills/writers/blog-tutorial-writer/CHANGELOG.md`

---

## 自然语言快速启动 (v2.74 Updated)

**不知道用哪个命令？** 直接描述你的需求，Claude 会自动路由到正确的工作流：

| 你说的话 | Claude 自动执行 |
|----------|----------------|
| "帮我写一篇关于 X 的文章" | → `smart-launcher v2.0` → 模式选择 (全自动/手动) |
| "https://competitor.com/blog/xxx" (URL) | → `smart-launcher` 全自动模式 (洗稿) |
| "Sora vs Runway vs Kling 对比" | → `smart-launcher` 手动模式推荐 (Tool Showdown) |
| "我有一个 YouTube 视频想写成博客" | → `smart-launcher` 全自动模式 |
| "https://youtube.com/watch?v=xxx" (单独 URL) | → `fetch-transcript` (直接获取字幕) |
| "帮我分析 higgsfield.ai 的博客内容" | → `/scout-topic` (仅分析，不写作) |
| "批量处理这 3 个竞品 URL" | → `batch-processor` 批量模式 |

### SmartLauncher v2.2 意图前置架构 ⭐

写作任务现在首先询问**素材使用意图（洗稿/参考）**，再推荐模式：

```
你: "https://www.youtube.com/watch?v=xxx 帮我写一篇文章"
       ↓
SmartLauncher v2.2:
  Step 1.5: 素材使用意图 (v2.2 NEW) ⭐
  ┌─────────────────────────────────────────────────┐
  │ Q: 你想如何使用这个素材？                        │
  │ [A] 洗稿 - 80%+ 保留原内容，品牌换 Alici AI     │
  │ [B] 参考 - 作为起点，可以深挖扩展               │
  └─────────────────────────────────────────────────┘
       ↓ (根据意图推荐模式)
  Phase 0: 模式选择
  ┌─────────────────────────────────────────────────┐
  │ [A] 全自动模式 ← 洗稿推荐                        │
  │     URL → 1-2 问题 → 一口气到 Preview           │
  ├─────────────────────────────────────────────────┤
  │ [B] 手动模式 ← 参考推荐                          │
  │     标题/方向 → 扩展调研 → 选择 Writer          │
  ├─────────────────────────────────────────────────┤
  │ [C] Seed 模式 (选题漏斗)                         │
  │     种子词 → 竞品锚定 → 意图扩散 → 2 个选题      │
  └─────────────────────────────────────────────────┘
       ↓
  [洗稿+全自动] 严格约束 → 禁止新增 → 品牌替换 → 快速执行
  [参考+手动] 扩展调研 → growth-topic-scout → DataForSEO
  [Seed] 6 Phase 漏斗: Mission → 竞品 → 扩散 → 验证 → 裁剪 → Lock
       ↓
═══════════════════════════════════════
▶ 执行阶段 (三条路线共享)
═══════════════════════════════════════
Writer → Editor Gate → AEO → Improver → 竞品验证 → Framer → Preview
```

**洗稿模式特点** (推荐全自动):
- 80%+ 保留原内容，品牌换成 Alici AI
- 禁止新增工具/场景，保持原结构
- 严格验证：检查新工具、新场景、字数范围
- 无需扩展调研，快速执行

**参考模式特点** (推荐手动):
- 作为起点，可以深挖扩展、补充新内容
- 调用 growth-topic-scout 扩展方向
- DataForSEO 验证关键词数据
- 用户选择扩展策略（原素材扩展/横向拓展/纵向深入）

**Seed 模式特点**:
- 从种子关键词出发，自动发现选题方向
- 竞品锚定 (3 个竞品博客) + 意图扩散 (60-80 关键词)
- DataForSEO 验证 (含 3 个 AEO/LLM 维度)
- 输出 2 个可直接开写的 Direction 对象
- 成本 ~$0.47 (standard)

> 💡 直通命令 (`/write-tutorial`、`/write-list` 等) 跳过 SmartLauncher，直接执行对应 Writer

### Seed Mode (选题漏斗) v2.2 🆕

**触发词**: seed mode, 种子模式, topic funnel, 选题漏斗, 帮我找选题

**用途**: 从一个种子关键词出发，通过竞品锚定 + 意图扩散 + 数据验证，产出 2 个可直接开写的选题方向

**6 Phase 流程**:
| Phase | 名称 | 输入 | 输出 |
|-------|------|------|------|
| 0 | Mission Config | Seed + 3 问题 | 00-mission-config.json |
| 0.5 | 竞品意图发现 | 3 竞品博客 | 5-8 种意图模式 |
| 1 | 意图扩散 | 意图模式 | 60-80 关键词 |
| 2 | DataForSEO 验证 | 关键词列表 | 验证数据 (含 3 个 AEO 维度) |
| 2.5 | Scope 裁剪 | 60 关键词 | 10 方向 |
| 3 | Title Lock | 10 方向 | 2 个锁定选题 |

**输出**: 2 个完整的 Direction 对象，包含：
- `locked_title` - 验证过的标题（含 SERP 证据）
- `evidence_chain` - 数据证据链（搜索量、趋势、竞品弱点）
- `recommended_skill` - 推荐的 Writer (blog-list-writer / blog-tutorial-writer)
- `outline` - 建议的文章结构

**成本**: ~$0.47 (standard) / ~$1.52 (deep)

---

## 命令速查

| 命令 | 用途 |
|------|------|
| `/batch-workflow URLs` | **批量处理多个 URL** 🆕 |
| `/full-workflow URL` | **完整流程（推荐入口）** |
| `/scout-topic URL` | 选题发现 |
| `/write-tutorial` | 教程文章 (1,800-2,500 词) |
| `/write-list` | 榜单文章 (2,500-3,500 词) |
| `/write-roundup` | **案例汇总小博文 (300-600 词)** |
| `/edit-article FILE` | 图片 + 优化 |
| `/analyze-aeo FILE` | 质量评分 |
| `/improve-article FILE` | 自动改进 |
| `/preview-chinese FILE` | 中文预览 |
| `/convert-to-framer FILE` | 输出 CMS JSON |
| `/convert-to-video-framer-json FILE` | (可选) 在现有 JSON 基础上插入视频，输出 `*-video.json` |
| `/preview-framer FILE` | Framer 可视化预览 |
| `/fetch-transcript URL` | 获取 YouTube 字幕 |
| `/generate-cover FILE` | **生成封面图 (6 种背景类型)** 🆕 |
| `/human-review FILE` | **人工审核 + 自动修复 (8 个检查模块)** 🆕 |
| `seed mode [关键词]` | **选题漏斗（从种子词发现 2 个可执行选题）** 🆕 |
| `mission brief URL` | **定义文章需求（7 问智能问卷 + 自动推断）** 🆕 |
| `source parser URL` | **八维素材分析（理解层 + 应用层 + 事实核查）** 🆕 |

**使用示例**:
```bash
# 批量处理 (v2.3 NEW)
/batch-workflow https://competitor1.com/blog https://competitor2.com/blog https://competitor3.com/blog

# 单个完整流程
/full-workflow https://competitor.com/blog/ai-video
/scout-topic https://competitor.com/blog/ai-tools
/write-roundup https://www.youtube.com/watch?v=xxx https://www.youtube.com/watch?v=yyy
/fetch-transcript https://www.youtube.com/watch?v=dQw4w9WgXcQ
/edit-article "/reports 待发文章/2026-01-15-ai-video/01-article-draft.md"
/human-review "/reports 待发文章/2026-01-15-ai-video/01-article-edited.md"
/preview-framer "/reports 待发文章/2026-01-15-ai-video/01-article-reviewed.md"

# 前置准备流程 (v2.8.4 NEW)
mission brief https://invideo.io/blog/kling-vs-runway  # 定义文章需求
source parser https://invideo.io/blog/kling-vs-runway  # 八维素材分析
```

---

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| Claude 死循环 | /clear → 简化任务 → 给最小示例 |
| 输出质量下降 | 检查上下文 >30% → /compact → 新会话 |
| AEO 卡在 70 | 检查 FAQ 章节 → 开篇直答 → /improve-article |
| 会话中断 | 读 00-implementation.md → 从中断点继续 |

> 详细故障排除见 `/docs 项目文档/09-TROUBLESHOOTING.md`

---

## 输出目录约束 (MANDATORY) 🔒

> **依赖能力**: `output-path-builder` capability v1.0.0

### 强制约束声明

⚠️ **所有 Skill 输出必须遵循以下规则，违反将被阻止**：

| 规则 | 约束 | 验证方式 |
|------|------|---------|
| **基础目录** | 必须在 `/reports 待发文章/`, `/research 竞品分析/insights/`, `/research 竞品分析/case-packs/`, `/research 竞品分析/mission-briefs/`, `/research 竞品分析/parsed-sources/` 之一 | 写入前检查 |
| **日期格式** | 必须是 `YYYY-MM-DD` 前缀 | 自动修正 |
| **Slug 格式** | 小写、连字符分隔、≤50 字符 | 自动修正 |
| **目录创建** | 不存在则自动创建 | 自动执行 |
| **冲突处理** | 存在则追加时间戳 `{HHmm}` | 自动追加 |

### 禁止行为

以下操作会被 **阻止** 并报错：

- ❌ 写入项目根目录 (`/Users/H/Documents/AliciBlog/`)
- ❌ 写入 `/reports 待发文章/` 以外的非标准位置（如 `AliciBlog Report/`）
- ❌ 使用非标准命名（如 `report-1`, `新文章/`, `article_draft`）
- ❌ 使用中文或特殊字符作为目录名
- ❌ 跳过目录存在性检查直接写入

### 冲突解决策略

```
目录已存在?
├── 同一会话 → 复用现有目录 ✅
└── 不同会话 → 追加时间戳
    └── 格式: {YYYY-MM-DD}-{topic-slug}-{HHmm}
    └── 示例: 2026-01-20-kling-motion-control-1430
```

### 写入前检查清单

每次写入文件前，系统自动执行：

1. [ ] 验证基础目录是否合规
2. [ ] 验证日期格式是否正确
3. [ ] 验证 slug 格式是否符合规范
4. [ ] 检查目录是否存在（不存在则创建）
5. [ ] 检查是否有冲突（有则追加时间戳）
6. [ ] 记录最终路径到 `00-implementation.md`

---

## 输出目录结构

```
# 单任务输出
/reports 待发文章/[YYYY-MM-DD]-[topic-slug]/
├── 00-implementation.md      # 进度追踪 (必须)
├── 00-topic-scout-report.md  # 选题分析
├── 00-topic-brief.json       # Topic Brief (tutorial/list)
├── 00-insight-pack.json      # Insight Pack (roundup)
├── 00-case-pack.json         # Case Pack (roundup)
├── 01-article-draft.md       # 初稿
├── 01-article-edited.md      # 编辑版
├── 02-chinese-preview.md     # 中文预览
├── 03-aeo-score.md           # 评分报告
├── 04-editor-report.md       # Editor 改进报告
├── 05-article-improved.md    # 改进版
├── 06-cover-image.png        # 封面图片 🆕
├── 06-cover-metadata.json    # 封面元数据 🆕
├── 07-article-final.json     # Framer CMS JSON (含 cover_image_url)
├── 07-article-final-video.json  # (可选) 视频集成版本 (输入名 + -video.json)
├── 08-preview.html           # Framer 可视化预览
├── 09-human-review-checklist.md  # 人工审核报告 (检查 + 修复记录) 🆕
└── 01-article-reviewed.md    # 修复后版本 (human-review 输出) 🆕

# 批量任务输出 (v2.3 NEW)
/reports 待发文章/batch-[YYYY-MM-DD]-[id]/
├── 00-batch-manifest.json    # 批量任务清单 (核心追踪文件)
├── 00-batch-summary.md       # 汇总报告 (完成后生成)
├── [YYYY-MM-DD]-[topic-1]/   # URL1 输出目录
├── [YYYY-MM-DD]-[topic-2]/   # URL2 输出目录
└── [YYYY-MM-DD]-[topic-3]/   # URL3 输出目录

/research 竞品分析/insights/   # Insight Pack 备份
└── [YYYY-MM-DD-{topic-slug}.json]

/research 竞品分析/case-packs/ # Case Pack 备份
└── [YYYY-MM-DD-{topic-slug}_roundup-{number}.json]

/research 竞品分析/mission-briefs/  # Mission Brief (v2.8.4 NEW)
└── YYYY-MM-DD-{topic-slug}/
    ├── mission-brief.json      # 结构化需求定义
    └── mission-brief.md        # 人类可读摘要

/research 竞品分析/parsed-sources/  # Parsed Source (v2.8.4 NEW)
└── YYYY-MM-DD-{topic-slug}/
    ├── parsed-source.json      # 八维分析结果
    ├── parsed-source.md        # 人类可读报告
    ├── raw-content.md          # 原始内容备份
    └── assets/                 # 提取的表格/图片
```

---

## 实施路线图

| Phase | 目标 | 状态 | 日期 |
|-------|------|------|------|
| 1 | 输出层统一 (markdown-to-framer) | ✅ 已完成 | 2025-12 |
| 2 | 输入层扩展 (Notion URL 支持) | ⏳ 待开始 | - |
| 3 | 处理层门禁 (75 分验证) | ⏳ 待开始 | - |
| 4 | 图片能力迁移 (editor v2.0) | ✅ 已完成 | 2025-12 |
| **5** | **Writer v2.0 升级 (AIDA + Citable Blocks)** | ✅ **已完成** | **2026-01-16** |
| **6** | **Insight-Driven Blog Writer (Case Roundup MVP)** | ✅ **已完成** | **2026-01-20** |
| **7** | **智能路由 + 批量处理 (smart-router + batch-processor)** | ✅ **已完成** | **2026-01-20** |
| **8** | **Visual Asset System (Writer v1.3 + Editor v2.6)** | ✅ **已完成** | **2026-01-20** |
| **9** | **SmartRoot 交互式选题确认 (smart-root v2.0)** | ✅ **已完成** | **2026-01-20** |
| **10** | **质量保障升级 (竞品验证 + 时效性策略)** | ✅ **已完成** | **2026-01-20** |
| **11** | **Tool Showdown + Version Verification** | ✅ **已完成** | **2026-01-21** |
| **12** | **SmartLauncher v1.0 架构升级** | ✅ **已完成** | **2026-01-22** |
| **13** | **Markdown-to-Framer v1.3 修复** | ✅ **已完成** | **2026-01-22** |
| **14** | **YouTube URL 路由修复** | ✅ **已完成** | **2026-01-22** |
| **15** | **Editor v2.9 Invideo 竞品 Review** | ✅ **已完成** | **2026-01-22** |
| **16** | **Editor v2.9.1 强制规则升级** | ✅ **已完成** | **2026-01-22** |
| **17** | **SmartLauncher v1.2 架构统一** | ✅ **已完成** | **2026-01-22** |
| **18** | **SmartLauncher v2.0 双轨制架构** | ✅ **已完成** | **2026-01-23** |
| **19** | **SmartLauncher v2.0 双轨制测试通过** | ✅ **已完成** | **2026-01-23** |
| **20** | **Growth Topic Scout v2.2 Seed Mode** | ✅ **已完成** | **2026-01-25** |
| **21** | **SmartLauncher v2.1 三轨制架构** | ✅ **已完成** | **2026-01-25** |
| **22** | **SmartLauncher v2.2 意图前置架构** | ✅ **已完成** | **2026-01-26** |
| **23** | **InVideo 原则系统化集成** | ✅ **已完成** | **2026-01-26** |

**Phase 23 详情** (InVideo 原则系统化集成) ⭐:
- ✅ **6 个文件修改**
  - AUTO_ROUTE.md v2.2 → v2.3
  - TOOL_SHOWDOWN_TEMPLATE.md v1.1 → v1.2
  - opening-patterns.yaml v2.0 → v2.1
  - BLOG_WRITING_PRINCIPLES_v2.md v2.1 → v2.2
  - integration-levels.yaml v1.0 → v2.1
  - REWRITE_VALIDATION_TEMPLATE.md v1.0 (新建)
- ✅ **InVideo 6 大原则系统化**
  - Key Takeaways 前置: Editor Module 3 验证
  - Reframe 开篇 P4 强制: Pattern Requirements 映射
  - Source Attribution 章节: Template 新增 Heading #3
  - 无虚假声明: banned_patterns 列表
  - L4 整合者定位: invideo_enhancement 模板
  - 引用密度 ≥5/千字: Citation Standards Section 10
- ✅ **REWRITE_VALIDATION_TEMPLATE.md**
  - 洗稿模式 6 原则验证检查清单
  - 自动化验证 vs 手动审核分类
  - 报告格式模板
- 🎯 **核心突破**: InVideo 原则从"隐式遵循"到"显式验证配置"
- 📊 **预期效果**:
  - 洗稿模式 Source Attribution: 可选 → **强制**
  - Tool Showdown 开篇模式: 任意 → **Reframe 强制**
  - 虚假声明检测: 无 → **自动验证**
  - L4 植入法: 隐含 → **显式模板**
  - 引用密度验证: ≥3/千字 → ≥5/千字 (Showdown)

**Phase 22 详情** (SmartLauncher v2.2 意图前置架构) ⭐:
- ✅ **smart-launcher v2.2** 发布
  - **Step 1.5 素材使用意图 (NEW)**: 用户输入 URL 后首先询问意图
  - **两种意图**: 洗稿 (80%+ 保留) / 参考 (可扩展)
  - **意图 → 约束配置**: 洗稿严格约束 / 参考宽松允许扩展
  - **意图 → 模式推荐**: 洗稿推荐全自动 / 参考推荐手动或 Seed
- ✅ **AUTO_ROUTE.md v2.2** 更新
  - **rewrite_mode 配置**: preserve_structure, no_new_tools, no_new_scenarios, brand_swap
  - **reference_mode 配置**: allow_expansion, call_growth_topic_scout, call_dataforseo
  - **validate_output_by_intent()**: 根据意图选择验证策略
- ✅ **MANUAL_ROUTE.md v2.2** 更新
  - **Step 1.5 参考模式扩展调研**: 调用 growth-topic-scout + DataForSEO
  - **三种扩展方向**: 原素材扩展 / 横向拓展 / 纵向深入
  - **扩展调研配置**: reference_expansion 配置块
- 🎯 **核心突破**: 从"隐式决定洗稿"到"用户明确选择使用意图"
- 📊 **预期效果**:
  - 用户意图感知: 不清楚 → 100% 明确
  - 洗稿模式: 严格约束，禁止新增
  - 参考模式: 扩展调研，数据验证
  - 模式推荐: 基于意图自动推荐

**Phase 20-21 详情** (Seed Mode + 三轨制):
- ✅ **growth-topic-scout v2.2** 发布
  - **Mode D 新增**: Seed Mode 选题漏斗
  - **6 Phase 架构**: Mission Config → 竞品意图 → 扩散 → 验证 → 裁剪 → Title Lock
  - **输出升级**: Direction 对象含 locked_title + evidence_chain
  - **DataForSEO 升级**: 新增 3 个 AEO/LLM 相关数据维度
- ✅ **smart-launcher v2.1** 发布
  - **三轨制入口**: 全自动 / 手动 / Seed 模式
  - **Phase 0 更新**: 新增 Seed 模式选项
- ✅ **新增 Schema 文件**
  - `MISSION_CONFIG_SCHEMA.json` - Mission Config 结构
  - `DIRECTION_SCHEMA.json` - Direction 对象结构
- 🎯 **核心突破**: 从"关键词扩展"升级为"选题漏斗"
- 📊 **预期效果**:
  - 选题产出: 50-100 关键词 → 2 个可执行方向
  - 人工确认: 全量审核 → 只确认 2 个
  - 成本: ~$2.59 → ~$0.47 (standard)

**Phase 19 详情** (SmartLauncher v2.0 双轨制测试):
- ✅ **手动路线测试** 7/7 PASS
  - Phase 0 模式选择问卷正确
  - Step 2 DataForSEO 数据强制展示
  - Step 3 "vs" 自动识别为 Tool Showdown
  - Step 4 展示 5+ 标题选项
  - Step 5 配置摘要完整
  - 路由到 blog-list-writer (tool_showdown)
- ✅ **全自动路线测试** 7/7 PASS
  - 只问 1-2 个问题
  - 自动调用 growth-topic-scout
  - 自动选择正确的 Writer
  - 洗稿模式 80%+ 参考
  - 一口气执行到 Preview HTML
  - 呈现 Preview + 报告摘要
- 🎯 **核心验证**: 双轨制架构规范与实现一致
- 📊 **测试结果**: 14/14 验证点全部通过

**Phase 18 详情** (SmartLauncher v2.0 双轨制架构):
- ✅ **smart-launcher v2.0** 发布
  - **Phase 0 模式选择**: 入口处明确选择全自动 vs 手动模式
  - **全自动路线**: URL + 1-2 问题 → 洗稿模式 (80%+ 参考) → 一键到 Preview
  - **手动路线**: 5 步确认流程 + 强制 DataForSEO 展示确认
  - **强制 growth-topic-scout**: 两条路线都必须调用
  - **明确 Writer 路由**: 4 种方向 (Tool Showdown/Listicle/Tutorial/Case Study)
- ✅ **AUTO_ROUTE.md** 新增
  - 洗稿模式配置
  - 素材自动抓取流程
  - 批量模式支持
- ✅ **MANUAL_ROUTE.md** 新增
  - 5 步流程详细规范
  - DataForSEO 强制确认
  - 标题选择问卷
- ✅ **COMBOS.md** 简化
  - 9 种组合 → 4 种核心方向
  - 对齐 Writer 路由表
- 🎯 **核心突破**: 清晰的双轨制，用户明确知道自己在哪条路线
- 📊 **预期效果**:
  - 用户模式感知: 不清楚 → 100% 清晰
  - growth-topic-scout 调用率: 可变 → 100%
  - DataForSEO 确认率 (手动): 0% → 100%
  - Writer 路由正确率: 可变 → 100%

**Phase 17 详情** (SmartLauncher v1.2 架构统一):
- ✅ **smart-launcher v1.2** 发布
  - **Phase 3 Step 3**: Editor Gate 强制 - 所有 Writer 必须经过 Editor
  - **Phase 3 Step 3.5**: Writer Feedback Loop - BLOCKING 时自动反馈重写
  - **架构图更新**: 显示 Editor Gate + Feedback Loop
- ✅ **case-roundup-writer v1.5** 发布
  - **修复**: 加入 Editor 流程，与其他 Writer 一致
  - **新增**: Editor Integration 章节
  - **更新**: Workflow Chain 包含 Editor 步骤
- ✅ **editor v2.9.2** 发布
  - **Module 10 NEW**: Writer Feedback Loop
  - **无法自动修复场景**: Key Takeaways/CTA/引用/标题年份
  - **循环限制**: 最大 2 次，超过则 MANUAL_REVIEW
- 🎯 **核心突破**: 所有 Writer 输出必须经过 Editor Gate，用户首次看到的是编辑后版本
- 📊 **预期效果**:
  - Editor 覆盖率: 67% (2/3 Writers) → 100% (3/3 Writers)
  - 强制规则遵守率: 可变 → 100%
  - 首次输出质量: 提前修复所有 BLOCKING 问题
  - BLOCKING 处理: 手动介入 → 自动反馈循环

**Phase 16 详情** (Editor v2.9.1 强制规则升级):
- ✅ **editor v2.9.1** 发布
  - **Module 3 增强**: Key Takeaways 强制前置 (⛔ BLOCKING)
  - **Module 3 增强**: Data Hook 开篇强制 (⚠️ WARNING → 自动修复)
  - **Module 5 增强**: 标题年份验证从 WARNING 升级为 ⛔ BLOCKING
  - **Module 9 新增**: CTA Enforcement - 文末必须有 CTA 卡片
- ✅ **opening-patterns.yaml** 更新 - Data Hook 优先设置
- ✅ **title-formulas.yaml** 更新 - 年份验证 BLOCKING
- ✅ **sample-edit-report.md** 更新 - Module 9 状态
- 🎯 **核心突破**: 基于 Kling 文章优化洞察，4 项规则从建议升级为强制
- 📊 **预期效果**:
  - 标题年份覆盖率: 可变 → 100%
  - Key Takeaways 存在率: 可变 → 100%
  - Data Hook 开篇率: ~30% → 90%+
  - CTA 卡片覆盖率: 可变 → 100%

**Phase 15 详情** (Editor v2.9 Invideo 竞品 Review):
- ✅ **editor v2.9** 发布
  - Module 3 增强: 24 种 AEO 开篇模式 + 自动重写
  - Module 5 增强: 37 种标题公式验证 + L1-L20 植入检测
  - Module 6 增强: 5 层引用权威金字塔评分
- ✅ **4 个新 YAML 配置文件**
  - `title-formulas.yaml` (37 种公式)
  - `opening-patterns.yaml` (24 种模式 + 选择矩阵)
  - `integration-levels.yaml` (L1-L20 定义)
  - `citation-pyramid.yaml` (5 层权威 + 密度标准)
- ✅ **报告模板更新** - Competitive Review Results 章节
- 🎯 **核心突破**: Invideo 竞品洞察 → Editor 自动 Review 机制
- 📊 **预期效果**:
  - 标题公式: 未验证 → 100% 匹配检测
  - 开篇模式: 无检测 → 24 种模式识别
  - 植入层级: 无标准 → L3+ 目标验证
  - 引用权威: 无评分 → L1-3 ≥50% 门禁

**Phase 14 详情** (YouTube URL 路由修复) 🔧:
- ✅ **smart-launcher v1.1** 发布
  - **修复**: YouTube URL 单独输入时自动路由到 fetch-transcript
  - **新增**: YouTube URL 检测逻辑（支持 watch/短链接/embed）
  - **新增**: 简单前缀允许（抓取/获取/字幕/帮我/请等）
- ✅ **架构图 Step 2** 更新 - 非写作意图检测增加 YouTube URL
- ✅ **非写作意图表** 更新 - 字幕获取增加 URL 检测
- 🎯 **核心修复**: 解决 YouTube URL 输入时误入写作问卷的问题
- 📊 **预期效果**:
  - YouTube URL 路由: 误入问卷 → 自动调用 fetch-transcript
  - 用户体验: 需说明意图 → 直接粘贴 URL 即可

**Phase 13 详情** (Markdown-to-Framer v1.3 修复) 🔧:
- ✅ **markdown-to-framer v1.3** 发布
  - **修复**: 图片格式 - `<img alt="..." src="...">` (无 figure 包裹，alt 在 src 前)
  - **新增**: 特殊字符处理 - em dash/en dash/smart quotes/ellipsis 替换
  - **修复**: cover 字段只保留 `url`，移除 `alt` 和 `cover_image_metadata`
  - **简化**: 单路径输出
- ✅ **CONVERSION_RULES.md** 更新
  - 图片处理规则修正
  - 新增第 11 节特殊字符处理
  - 常见错误表更新
- ✅ **FIELD_SCHEMA.md** 更新
  - JSON 数组格式强调
  - cover.url 禁止 alt 说明
- ✅ **convert-to-framer.md** 命令更新至 v1.1
- 🎯 **核心修复**: 解决 Framer CMS 导入 "TypeError: o is not iterable" 错误
- 📊 **预期效果**:
  - Framer 图片显示: 失败 → 正常
  - 封面图导入: 报错 → 正常
  - JSON 解析: 特殊字符错误 → 正常

**Phase 12 详情** (SmartLauncher v1.0 架构升级) 🆕:
- ✅ **smart-launcher v1.1** 发布
  - 合并 smart-router v2.0 + smart-root v2.2
  - Phase 0: 目标识别（帮人选择/教人做事/展示发现/建立权威）
  - Phase 1: 组合选择（9 种预设组合）
  - Phase 2: 选题验证（DataForSEO + 标题确认）
  - Phase 3: 全自动执行
- ✅ **COMBOS.md** 发布
  - 9 种预设组合定义
  - 目标 → 组合映射
  - 组合 → 配置映射
- ✅ **TITLE_FORMULAS.md** 发布
  - 37 种标题公式索引
  - 基于 invideo.io 竞品洞察
- ✅ **OPENING_PATTERNS.md** 发布
  - 24 种开篇模式索引
  - 基于 invideo.io AEO 最佳实践
- ✅ **删除旧组件**
  - 删除 smart-router v2.0
  - 删除 smart-root v2.2
- 🎯 **核心突破**: 目标导向 × 组合预设 × 一键启动
- 📊 **预期效果**:
  - 启动问卷步数: 4 步 → 2-3 步
  - 组件数量: 2 → 1
  - 预设组合: 0 → 9 种
  - 内容类型覆盖: 4 种 → 8 种
  - 标题公式库: 5 种 → 37 种
  - 开篇模式库: 4 种 → 24 种

**Phase 11 详情** (Tool Showdown + Version Verification) 🆕:
- ✅ **smart-root v2.2** 发布
  - Phase 0: 版本验证（"vs/对比/对决" 意图自动触发）
  - WebSearch 验证工具最新版本
  - 版本差异通知 + 用户确认
  - 输出 `verified_tools` JSON 给 Writer
- ✅ **blog-list-writer v2.2** 发布
  - 新增 `tool_showdown` 内容类型
  - 10 固定 Headings 高对比度结构
  - Category Winners (Choose/Avoid) 格式
  - Decision Tree (If/Then) 格式
  - 2 表格 (Snapshot + Scorecard) + 3 CTA
- ✅ **TOOL_SHOWDOWN_TEMPLATE.md** 发布
  - 定义工具对决文章标准结构
  - 版本验证集成要求
  - 发布前检查清单
- 🎯 **核心突破**: 版本准确性 + 高对比度结构
- 📊 **预期效果**:
  - 工具版本准确性: 未知 → 100% (WebSearch 验证)
  - 对决文章结构一致性: 变化大 → 100% (固定模板)
  - 读者决策速度: 慢 → 快 (Category Winners)

**Phase 10 详情** (质量保障升级):
- ✅ **output-path-builder capability v1.0** 发布
  - 统一路径生成
  - 冲突检测与自动追加时间戳
  - 写入前验证检查
- ✅ **competitive-validator skill v1.0** 发布
  - 搜索 Top 5 竞品
  - 快速 AEO 评分 (50 分制)
  - 验证阈值: PASS (≥30% 超过竞品)
  - 输出: `08-competitive-validation.md`
- ✅ **trending-monitor skill v1.0** 发布
  - QDF 信号检测 (HIGH/MEDIUM/LOW/NONE)
  - 热点优先级标记
  - 内容日历建议
- ✅ **aeo-analyzer v2.4** 升级
  - 新增 Module 5: Content Freshness Signals (20 bonus points)
  - 发布时效、数据新鲜度、版本准确性、趋势相关性
- ✅ **smart-root v2.1** 升级
  - 竞品验证层集成
  - AEO ≥ 目标后自动触发验证
- ✅ **growth-topic-scout v1.2** 升级
  - trending-monitor 集成
  - Trend Relevance 评分维度 (10 bonus points)
- 🎯 **核心突破**: 输出目录 100% 一致性 + 质量超越率可量化 (≥30%)
- 📊 **预期效果**:
  - 输出目录一致性: ~60% → 100%
  - 竞品对比覆盖率: 0% → 100%
  - 质量超越率: 未知 → ≥30% (可衡量)
  - 热点响应速度: 无策略 → 24-48h 内

**Phase 9 详情** (SmartRoot 交互式选题确认):
- ✅ smart-root skill v2.0 发布
  - 4 步交互式问卷（内容类型/选题/标题/规格）
  - DataForSEO 集成（搜索量验证）
  - 5+ 标题选项供用户选择
  - 确认后全自动执行
- ✅ smart-router v2.0 升级
  - 写作意图自动路由到 smart-root
  - 非写作意图直接执行
- ✅ CLAUDE.md 架构图更新至 v2.5
- 🎯 **核心突破**: "启动、讨论、选题 = 交互式 / 进入后 = 全自动"
- 📊 **预期效果**:
  - 选题匹配率 ~60% → ~90% (用户确认)
  - 标题满意度 ~70% → ~95% (用户选择)
  - 中途中断率 ~30% → ~5% (前期确认)

**Phase 8 详情** (Visual Asset System):
- ✅ case-roundup-writer v1.3 升级：Visual Prompt Pack（角色演化系统）
- ✅ editor v2.6 升级：Asset Pack Mode（批量图片生成）
- ✅ 数据契约：Writer v1.3 → asset_plan.json → Editor v2.6 → asset_manifest.json
- ✅ prompt_pack.md 输出：给读者的 copy-paste Prompt 包
- 🎯 **核心突破**: Writer 和 Editor 之间建立标准化数据契约，可复用 Prompt
- 📊 **预期效果**: 用户可直接复制 Prompt 生成图片，Editor 自动批量处理

**Phase 6 详情** (Phase A: MVP Core):
- ✅ case-roundup-writer skill v1.0 发布（2026-01-20）
- ✅ **case-roundup-writer skill v1.1 升级**（2026-01-20）🔥
  - Material Gate（强制真实素材）
  - 多维度拓展（单一素材处理）
  - Prompts to Try（可复用 Prompt）
  - 标题确认（5+ 选项）
- ✅ /write-roundup 命令创建
- ✅ insights/ 和 case-packs/ 数据目录创建
- ✅ 交互式 Insight Pack 收集流程（6 个问题）
- ✅ Case Pack 数据结构定义（2-5 个案例）
- ✅ micro_roundup 内容规范（300-600 词）
- ✅ 产品理念自然渗透机制
- 📋 下一步：Phase B (视频内容提取) / Phase C (AEO 适配)

**Phase 7 详情** (智能路由 + 批量处理):
- ✅ smart-router skill v1.0 发布（2026-01-20）→ **v2.0 升级**（Phase 9）
  - 自然语言意图识别
  - URL 类型检测（YouTube/竞品）
  - 多 URL 自动触发批量模式
  - 关键词 → 工作流映射
  - **v2.0**: 写作意图路由到 smart-root
- ✅ batch-processor skill v1.0 发布（2026-01-20）
  - 队列管理（依次/并行执行）
  - 进度追踪（manifest.json）
  - 错误恢复（会话中断后继续）
  - 汇总报告（batch-summary.md）
- ✅ /batch-workflow 命令创建
- ✅ CLAUDE.md 架构图更新至 v2.3 → **v2.5**（Phase 9）

**Phase 5 详情**:
- ✅ blog-tutorial-writer v2.0 发布
- ✅ AIDA 开篇框架（Attention → Interest → Desire → Action）
- ✅ Citable Block 标记系统（3-5 个/文章）
- ✅ 强化 E-E-A-T 信号（7 个外部引用 + 完整作者信息）
- ✅ 验证通过：首次 AEO 评分 73 → 82 (+9 分)
- ✅ blog-list-writer v2.0 升级（2026-01-18 完成）

---

## 不要做的事

- ❌ 跳过 Plan 模式直接执行复杂任务
- ❌ 单会话处理多个不相关功能
- ❌ 忽略 AEO < 75 的文章直接发布
- ❌ 使用 "revolutionary", "game-changing" 等营销词
- ❌ 无 Topic Brief 直接写文章
- ❌ 手动修改 00-implementation.md（让 Claude 维护）

---

## 关键配置

**图片生成**: FAL.ai nano-banana
- 脚本: `/scripts/fal_image_generator.py`
- API Key 配置: `.mcp.json` → `mcpServers.fal.env.FAL_API_KEY`
- 读取优先级: 环境变量 > .mcp.json 配置文件
- 持久化: 会话压缩后自动加载，无需手动 export
- 生成的图片会返回 fal的图片链接，可以直接使用

**图片上传**: 
- 上传视频，如果用户使用本地的图片，请通过以下方式上传获得云端链接。
首先要有本地图片的路径
比如 ：前置目录/${name}.png
上传使用ssh命令：
ssh命令：
rsync -a -r -v -p -e 'ssh -p 22'  --exclude='.DS_Store'  --progress ${完整前置路径}/${name}.png root@45.76.70.215:/var/www/static/static/image/other/gen_images/
password:  5A_p@cjpX74H(LJM

最终获得的链接如下：
https://ct2.alici.ai/static/image/other/gen_images/${name}.png

请使用命令上传视频，不要让用户自己上传。
请使用命令上传视频，不要让用户自己上传。


**MCP**: DataForSEO (SERP + KEYWORDS_DATA)

**内容规范**: `_archive 历史归档/blog_new_sam 11.20.2025/doc/` 下的 3 个 MD 文件

---

## 文档索引

### 核心配置文档 (Skills 共享依赖)

**优先级最高** - 这些文档是所有 Skills 的共享依赖，修改时需谨慎

| 文档 | 位置 | 用途 | 依赖者 |
|------|------|------|--------|
| **PRODUCT_CATALOG.md** | `/skills/_docs/` | CTA 映射、产品定价 | 所有 Writer Skills |
| **BRAND_VISUAL_GUIDE.md** | `/skills/_docs/` | 绿色视觉规范、ICSB 框架 | Editor Skill |
| **BLOG_WRITING_PRINCIPLES_v2.md** | `/skills/_docs/` | 标题公式、评测方法论、Section 10-11 InVideo 原则 | 所有 Writer Skills |
| **TOOL_SHOWDOWN_TEMPLATE.md** | `/skills/_docs/` | 工具对决 10 Headings 结构 | blog-list-writer (tool_showdown) |
| **smart-launcher/SKILL.md** | `/skills/core/smart-launcher/` | v2.2 意图前置架构 + 洗稿/参考模式 + 三轨制 | 所有写作流程 |
| **smart-launcher/AUTO_ROUTE.md** | `/skills/core/smart-launcher/` | 全自动路线: 意图驱动约束 + rewrite_mode/reference_mode | SmartLauncher |
| **smart-launcher/MANUAL_ROUTE.md** | `/skills/core/smart-launcher/` | 手动路线: 参考模式扩展调研 + 5 步确认 | SmartLauncher |
| **smart-launcher/COMBOS.md** | `/skills/core/smart-launcher/` | 4 种 Writer 路由配置 | SmartLauncher |
| **smart-launcher/TITLE_FORMULAS.md** | `/skills/core/smart-launcher/` | 37 种标题公式索引 | 所有 Writer Skills |
| **smart-launcher/OPENING_PATTERNS.md** | `/skills/core/smart-launcher/` | 24 种开篇模式索引 | 所有 Writer Skills |
| **blog-cover-generator/SKILL.md** | `/skills/utilities/blog-cover-generator/` | 封面生成 6 类型 + Prompt 模板 | SmartLauncher 全自动流程 |
| **growth-topic-scout/MISSION_CONFIG_SCHEMA.json** | `/skills/core/growth-topic-scout/` | Mission Config JSON Schema | Seed Mode |
| **growth-topic-scout/DIRECTION_SCHEMA.json** | `/skills/core/growth-topic-scout/` | Direction 对象 JSON Schema | Seed Mode |
| **mission-brief/SKILL.md** 🆕 | `/skills/preparation/mission-brief/` | 7 问智能问卷 + 自动推断 + mission-brief.json | 前置准备流程 |
| **source-parser/SKILL.md** 🆕 | `/skills/preparation/source-parser/` | 八维分析框架 + 事实核查 + parsed-source.json | 前置准备流程 |

### 哲学与策略文档

这些文档定义了内容策略的底层逻辑，理解它们有助于做出更好的决策

| 文档 | 位置 | 用途 |
|------|------|------|
| 内容策略哲学 | `/docs 项目文档/00-CONTENT-PHILOSOPHY.md` | Higgsfield 洞察、4 大原则 |
| 竞品洞察 - 标题 | `/skills/monitors/competitive-insights/higgsfield-blog/01-TITLE_FORMULAS.md` | 标题验证规则 |
| 竞品洞察 - 评测 | `/skills/monitors/competitive-insights/higgsfield-blog/02-EVALUATION_FRAMEWORK.md` | 5 维度评测 |
| 竞品洞察 - Prompt | `/skills/monitors/competitive-insights/higgsfield-blog/03-PROMPT_STRUCTURE_TEMPLATE.md` | 7 要素框架 |
| **invideo 洞察 - 内容框架** | `/research 竞品分析/invideo-blog/01-content-framework.md` | 8 种内容类型 + 37 种标题公式 |
| **invideo 洞察 - AEO 开篇** | `/research 竞品分析/invideo-blog/03-aeo-opening-patterns.md` | 24 种开篇模式 |
| **Editor 标题公式** | `/skills/core/editor/prompts/title-formulas.yaml` | 37 种标题公式验证 (v2.9) |
| **Editor 开篇模式** | `/skills/core/editor/prompts/opening-patterns.yaml` | 24 种 AEO 模式 + 选择矩阵 (v2.9) |
| **Editor 植入层级** | `/skills/core/editor/prompts/integration-levels.yaml` | L1-L20 产品植入定义 + L4 InVideo Enhancement (v2.1) |
| **Editor 引用金字塔** | `/skills/core/editor/prompts/citation-pyramid.yaml` | 5 层权威 + 密度标准 (v2.9) |
| **洗稿验证模板** | `/skills/_docs/REWRITE_VALIDATION_TEMPLATE.md` | 洗稿模式 6 原则验证检查清单 (v1.0) |

### 系统与操作文档

| 文档 | 位置 | 用途 |
|------|------|------|
| Skills 索引 | `/skills/README.md` | 21 个 Skills 分组索引 |
| 完整 Skills | `/docs 项目文档/02-SKILLS.md` | Skills 详细定义 |
| 最佳实践 | `/docs 项目文档/07-BEST-PRACTICES.md` | 专家经验总结 |
| 团队上手 | `/getting-started 上手指南/08-TEAM-ONBOARDING.md` | 新成员 10 分钟指南 |
| 故障排除 | `/docs 项目文档/09-TROUBLESHOOTING.md` | 常见问题解决 |
| AEO 框架 | `/skills/core/aeo-analyzer/EVALUATION_FRAMEWORK.md` | 评分标准 |

---

*发现 Claude 犯错时，立即添加到本文件的「不要做的事」*
