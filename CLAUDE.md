# CLAUDE.md

> AliciBlog: alici.ai AI 内容工厂，70%+ 自动化博客生产

## 核心架构

重要新增：模式选择除了下面的3种模式，新增一种thumbnail mode ,具体请查看easy_mode.md，然后启动

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          AliciBlog v2.9                                    │
├─────────────────────────────────────────────────────────────────────────┤
│  输入层: 自然语言 | /命令 | URL | 批量 URL | Topic Brief | YouTube | Seed │
│                            ↓                                            │
│  smart-launcher v2.3 (四轨制架构):                                        │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │ Step 1.5: 素材使用意图 (v2.2) ⭐                                │     │
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
│  │   ├─────────────────────────────────────────────────────────┤  │     │
│  │   │ [D] 深度研究 (Agent Team) 🆕                              │  │     │
│  │   │     5 专家并行 → 8 方向 → DataForSEO → Direction          │  │     │
│  │   └─────────────────────────────────────────────────────────┘  │     │
│  └────────────────────────────────────────────────────────────────┘     │
│          ┌──────────┼──────────┼──────────┼──────────┐                 │
│          ↓          ↓          ↓          ↓          │                 │
│  ┌───────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐│                 │
│  │ 全自动    │ │ 手动     │ │ Seed     │ │ 深度研究 ││                 │
│  │ URL+1-2问 │ │ 5步确认  │ │ 6P 漏斗  │ │ 5Agent   ││                 │
│  │ 80%+ 洗稿 │ │ DataFor  │ │ 竞品锚定 │ │ CEO综合  ││                 │
│  └─────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘│                 │
│        └────────────┴────────────┴─────────────┘     │                 │
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
| **SmartLauncher v2.3** | **意图前置 + 四轨制** ⭐ | **Step 1.5: 洗稿/参考 → 全自动/手动/Seed/深度研究** |
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
| **smart-launcher** | **v2.3** ⭐ | 帮我写, 写一篇, vs, 对比, 对决, **YouTube URL**, **seed mode, 种子模式, 选题漏斗, 帮我找选题** | **意图前置架构** + **洗稿/参考模式** + **四轨制** + **5 种 Writer 路由** |
| **art-scout** | **v1.1** 🆕 | 团队研究, 多角色选题, 全景扫描, agent team | 5 Agent 并行研究 + CEO 综合 + DataForSEO 验证 + 8 Direction 输出 |
| **batch-processor** | **v1.1** | 批量, 多个, batch | 队列执行 + 进度追踪 + 汇总报告 |
| **growth-topic-scout** | **v2.4** 🆕 | 竞品分析, 选题发现, **seed mode / seed mode v2** | Top 10/20 选题 + 双评分（SEO+AEO）+ **Seed D1(2)/D2(3)** Direction + diversity_report + **competitive_insights 输出** |
| **blog-tutorial-writer** | **v3.1** ⭐ | write tutorial | 1,800-3,500 词教程 (Tier 1/2/3) + **Citable Block Taxonomy v3.0** + **experiment_pack** + **CTA_CARD v2.0 摩擦对齐** + **Self-Check JSON** |
| **blog-list-writer** | **v3.1** ⭐ | write list | 4,500-10,000 词榜单 (Blueprint A/B/C/D) + **Plan Pack 输出** + **Listicle Validator Gate** + **methodology_level 护栏** |
| **blog-showdown-writer** | **v1.0** 🆕 | vs, showdown, 对比, 对决 | 2,500-3,500 词工具对决 + **11 固定标题** + **Showdown Plan** + **Showdown Validator Gate** + **L4 Integrator 定位** + **P4 Reframe 强制开篇** |
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



| **human-review-checklist** 🆕 | **v1.0** | 人工审核, 发布前检查, /human-review | 8 个检查模块 + **6 个自动修复** + 
**Writer Feedback Loop** + 竞品推荐检测 ⛔ BLOCKING |
| **mission-brief** 🆕 | **v1.0** | mission brief, 创建 brief, 定义需求 | 7 问智能问卷 + **自动推断** + mission-brief.json |
| **source-parser** 🆕 | **v1.0** | source parser, 解读素材, 分析素材 | **八维分析框架** (5 理解层 + 3 应用层) + 事实核查 |

**调用链 (v2.8.4 Updated)**:
- **前置准备流程 (可选)**: `mission-brief → source-parser` → 带着结构化素材进入写作
- **写作流程**: `smart-launcher v2.2 → growth-topic-scout v2.2 → writer路由 → editor gate → aeo-analyzer ⟷ improver → human-review-checklist → competitive-validator → framer → preview`

---

## 非写作指令：视频集成（convert-to-video-framer-json）
查看/skills/utilities/convert-to-video-framer-json/skill.md

| **image-sourcer** 🆕 | **v1.0** | 找配图, source images, 配图, image research | Web 真实图片搜索 + 5 维评分 + 专家选图 |
| **basecamp-link-ops** 🆕 | **v1.0** | basecamp url, bc链接, 读取basecamp | OAuth 读写 Basecamp 4 内容 (documents/todolists/vaults) |

**调用链 (v2.9 Updated)**:
```
smart-launcher v2.3 (四轨制) →
  Route A-C: growth-topic-scout v2.4 → writer 路由
  Route D: art-scout v1.1 → direction 选择 → writer 路由
→ writer (tutorial v3.1 / list v3.1 / showdown v1.0 / roundup v1.5)
→ validator gate → editor gate → aeo-analyzer ⟷ improver → competitive-validator → framer → preview
```


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

**v2.9 架构文档整理 + Art Scout 集成（2026-02-07）**:
- ✅ art-scout v1.1 注册到 Skills 表
- ✅ SmartLauncher v2.2 → v2.3 四轨制 (新增 Route D: 深度研究)
- ✅ CLAUDE.md Changelog 提取到独立 CHANGELOG.md (1,357→~550 行)
- ✅ 过时文档归档 (AliciBlog-Architecture-v2.2.md, 10-AUTO-PILOT-ARCHITECTURE.md)
- ✅ 02-SKILLS.md 更新至 v3.0+ (新增 showdown-writer + art-scout)


**v3.1 写作技能架构升级 — Showdown 独立 + 共享层（2026-02-07）** ⭐⭐:
- ✅ **blog-showdown-writer v1.0**: 从 blog-list-writer tool_showdown 模式独立为完整技能
  - 独立 SKILL.md (~900 行) + SHOWDOWN_TEMPLATE.md + CHANGELOG.md
  - Showdown Plan (showdown-plan.json) — 从 Listicle Plan Pack 模式吸收
  - Showdown Validator Gate — 从 Listicle Validator 模式吸收
  - evidence_level 护栏 (source_based / hybrid / hands_on)
  - 保留: P4 Reframe 强制开篇 + L4 Integrator 定位 + Source Attribution + 11 固定标题
- ✅ **共享组件层 `/skills/writers/_shared/`**:
  - CTA_CARD_v2.0.md — 摩擦对齐 CTA 系统 (3 种放置策略)
  - IMAGE_PLACEHOLDER_v2.0.md — 结构化图片占位 (6 类型 8 属性)
  - WRITER_COMPONENTS.md — 组件索引 + 版本号 + 引用关系
- ✅ **blog-list-writer v3.0 → v3.1**: 删除 tool_showdown 模式 (~130 行)，引用共享组件
- ✅ **blog-tutorial-writer v3.0 → v3.1**: CTA/IMAGE 引用共享组件 (~220 行精简)
- ✅ **路由更新**: COMBOS.md Showdown → blog-showdown-writer (不再经 blog-list-writer)
- ✅ **_docs/TOOL_SHOWDOWN_TEMPLATE.md**: 标记已迁移到 blog-showdown-writer
- 🎯 **核心突破**: 三技能独立 + 共享基础设施，消除维护同步问题
- 📊 **预期效果**:

| 维度 | v3.0 | v3.1 | 改进 |
|------|------|------|------|
| Showdown 独立性 | 依附 blog-list-writer | 完整独立技能 | 可独立迭代 |
| CTA/IMAGE 维护 | 2 处重复定义 | 1 处共享 + 3 处引用 | 单点修改 |
| Showdown 质量门禁 | 无 Validator | Showdown Validator Gate | 发布前自动拦截 |
| Showdown 计划 | 无 Plan Pack | showdown-plan.json | 结构化可验证 |
| 代码行数 | ~3,527 行重复 | ~3,100 行 (-12%) | 减少重复 |

> 完整版本历史 (v1.0 → v2.9，27 个版本): [CHANGELOG.md](./CHANGELOG.md)

---

## 自然语言快速启动 (v2.74 Updated)


**不知道用哪个命令？** 直接描述你的需求，Claude 会自动路由到正确的工作流：

| 你说的话 | Claude 自动执行 |
|----------|----------------|
| "帮我写一篇关于 X 的文章" | → `smart-launcher v2.3` → 模式选择 (全自动/手动/Seed/深度研究) |
| "https://competitor.com/blog/xxx" (URL) | → `smart-launcher` 全自动模式 (洗稿) |
| "Sora vs Runway vs Kling 对比" | → `smart-launcher` → `blog-showdown-writer` (独立 Showdown 技能) |
| "我有一个 YouTube 视频想写成博客" | → `smart-launcher` 全自动模式 |
| "https://youtube.com/watch?v=xxx" (单独 URL) | → `fetch-transcript` (直接获取字幕) |
| "帮我分析 higgsfield.ai 的博客内容" | → `/scout-topic` (仅分析，不写作) |
| "批量处理这 3 个竞品 URL" | → `batch-processor` 批量模式 |

### SmartLauncher v2.3 意图前置 + 四轨制架构 ⭐

写作任务现在首先询问**素材使用意图（洗稿/参考）**，再推荐模式：

```
你: "https://www.youtube.com/watch?v=xxx 帮我写一篇文章"
       ↓
SmartLauncher v2.3:
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
  ├─────────────────────────────────────────────────┤
  │ [D] 深度研究 (Agent Team) 🆕                     │
  │     5 专家并行 → 8 方向 → DataForSEO → Direction  │
  └─────────────────────────────────────────────────┘
       ↓
  [洗稿+全自动] 严格约束 → 禁止新增 → 品牌替换 → 快速执行
  [参考+手动] 扩展调研 → growth-topic-scout → DataForSEO
  [Seed] 6 Phase 漏斗: Mission → 竞品 → 扩散 → 验证 → 裁剪 → Lock
  [深度研究] art-scout → 5 Agent 并行 → CEO 综合 → 8 Direction 输出
       ↓
═══════════════════════════════════════
▶ 执行阶段 (四条路线共享)
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
- 竞品锚定 (5 个竞品博客，默认；支持 3–5) + 意图扩散 (60-80 关键词)
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
| 0.5 | 竞品意图发现 | 5 竞品博客（默认；支持 3–5） | 5-8 种意图模式 |
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

- ❌ 写入项目根目录 (项目根目录)
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
| **24** | **blog-tutorial-writer v2.5 + growth-topic-scout v2.4 升级** | ✅ **已完成** | **2026-02-05** |
| **25** | **blog-tutorial-writer v3.0 + blog-list-writer v3.0 双升级** | ✅ **已完成** | **2026-02-06** |
| **26** | **写作技能架构升级 — Showdown 独立 + 共享层** | ✅ **已完成** | **2026-02-07** |
| **27** | **架构文档整理 + Art Scout 集成** | ✅ **已完成** | **2026-02-07** |

> Phase 详情见 [CHANGELOG.md](./CHANGELOG.md)

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
| **TOOL_SHOWDOWN_TEMPLATE.md** | `/skills/_docs/` → 已迁移到 `/skills/writers/blog-showdown-writer/` | 工具对决 11 Headings 结构 | blog-showdown-writer |
| **smart-launcher/SKILL.md** | `/skills/core/smart-launcher/` | v2.3 意图前置架构 + 洗稿/参考模式 + 四轨制 | 所有写作流程 |
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
