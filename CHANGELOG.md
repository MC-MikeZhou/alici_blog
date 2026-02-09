# AliciBlog Changelog

> 完整版本历史。最近 2 个版本见 [CLAUDE.md](./CLAUDE.md)

---

## v2.9 交接准备 + 文档一致性校准（2026-02-08）

- ✅ **项目瘦身**: 删除视频文件 (~54 MB)、清理 .DS_Store、归档散落文件
- ✅ **README.md 全面更新**: 版本号、项目结构、Skills 表、工作流图、命令表同步至 v2.9
- ✅ **文档一致性校准**: CLAUDE.md / README.md / CHANGELOG.md 版本号统一为 v2.9
- ✅ **死链修复**: 移除不存在的 ONBOARDING.md / CONTRIBUTING.md 引用，替换为实际路径
- ✅ **路径修正**: `blueprint/` → `docs 项目文档/`、`reports/` → `reports 待发文章/`
- ✅ **ONBOARDING.md 路径更新**: `/blueprint/` → `/docs 项目文档/`、`/reports/` → `/reports 待发文章/`
- 🎯 **目的**: 项目打包交接准备，确保新同事拿到的文档与实际一致
- 📊 **版本号说明**: 对外交接版本统一标注为 v2.9，内部迭代历史保持原样

---

## v3.2 架构文档整理 + Art Scout 集成（2026-02-07）

- ✅ art-scout v1.1 注册到 Skills 表
- ✅ SmartLauncher v2.2 → v2.3 四轨制 (新增 Route D: 深度研究)
- ✅ CLAUDE.md Changelog 提取到独立 CHANGELOG.md (1,357→~550 行)
- ✅ 过时文档归档 (AliciBlog-Architecture-v2.2.md, 10-AUTO-PILOT-ARCHITECTURE.md)
- ✅ 02-SKILLS.md 更新至 v3.0+ (新增 showdown-writer + art-scout)

---

## v3.1 写作技能架构升级 — Showdown 独立 + 共享层（2026-02-07） ⭐⭐

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

---

## v3.0 blog-tutorial-writer v3.0 + blog-list-writer v3.0 双升级（2026-02-06） ⭐⭐⭐

- ✅ **blog-tutorial-writer v2.5 → v3.0**: Three-Tier 系统 + Citable Block Taxonomy v3.0 + Self-Check JSON
  - **Three-Tier 分级系统**: Tier 1 (1,800-2,200 词) / Tier 2 (2,200-2,800 词) / Tier 3 (2,800-3,500 词) 自动匹配复杂度
  - **Citable Block Taxonomy v3.0**: 7 种类型 (stat_callout, comparison_snapshot, definition_box, step_summary, expert_tip, data_table, key_takeaway)
  - **IMAGE_PLACEHOLDER v2.0**: 结构化占位符 (type, description, alt_text, suggested_source)
  - **CTA_CARD v2.0 摩擦对齐**: 根据内容阶段匹配 CTA 摩擦度
  - **experiment_pack**: 可选经验证据包 (实验数据、A/B 测试、性能基准)
  - **Self-Check JSON**: 自动生成结构化自检报告
  - **字数扩展**: 2,800-3,000 → 1,800-3,500（Tier 弹性范围）
- ✅ **blog-list-writer v2.4 → v3.0**: Blueprint 强制结构 + Plan Pack + Listicle Validator Gate
  - **4 种 Blueprint Profile**: A (Standard Listicle 4,500-5,500 词) / B (Prompt/Workflow Listicle 5,500-6,500 词) / C (Mega Listicle 8,000-9,500 词) / D (Alternatives Listicle 6,500-10,000 词)
  - **Plan Pack Bundle**: 4 文件输出 (plan.json + assets.json + validator-report.json + article-draft.md)
  - **Listicle Validator Gate**: PASS/FAIL 门禁 (Blueprint 合规性 + 结构完整性验证)
  - **methodology_level 护栏**: research_only / hybrid / hands_on 三级方法论控制
  - **字数扩展**: 2,500-3,500 → 4,500-10,000（Blueprint 驱动）
- 🎯 **核心突破**: Writer 从"单一模板"到"分级 + 强制结构 + 自检"的质量跃升
- 📊 **预期效果**:

| 维度 | v2.x | v3.0 | 提升 |
|------|------|------|------|
| Tutorial 字数弹性 | 固定 2,800-3,000 | Tier 1/2/3 (1,800-3,500) | 自动匹配复杂度 |
| Tutorial 引用块 | 3-5 通用型 | 7 类型 Taxonomy | +40% 引用多样性 |
| Tutorial 质量保证 | 人工审核 | Self-Check JSON 自动化 | 减少 Editor 迭代 |
| List 字数范围 | 2,500-3,500 | 4,500-10,000 | +186% 内容深度 |
| List 结构规范 | 自由格式 | Blueprint 强制 | 100% 结构一致性 |
| List 质量门禁 | 无 | Validator Gate PASS/FAIL | 发布前自动拦截 |

---

## v2.9 blog-tutorial-writer v2.5 + growth-topic-scout v2.4 升级（2026-02-05） ⭐⭐

- ✅ **blog-tutorial-writer v2.5**: Insight Pack 输入 + Market Context 章节 + Monetization Framework 章节
  - **Insight Pack 输入机制**: 结构化竞品分析数据（7 个字段）
  - **Market Context 章节（条件性）**: 市场规模 + CAGR + 指标对比表格 + 个人化价值主张（200-300 词）
  - **Monetization Framework 章节（条件性）**: 3-5 个收入流 + "How to start" 步骤 + 12 个月收入预测（400-600 词）
  - **字数扩展**: 2,000-2,500 → 2,800-3,000（含条件章节，+40%）
  - **AEO 清单**: +13 检查点（Insight Pack 集成 + Market Context + Monetization Framework）
- ✅ **growth-topic-scout v2.4**: competitive_insights 输出字段（top_competitors, content_gaps, data_points）
  - **自动提取**: 从竞品 URL 分析中提取结构化竞品数据
  - **与 blog-tutorial-writer v2.5 集成**: competitive_insights → Insight Pack 自动转换
- ✅ **新增共享文档**: `/skills/_docs/INSIGHT_PACK_SCHEMA.md` v1.0（完整 JSON Schema + 使用示例）
- 🎯 **核心突破**: 复合型变现导向选题（如 "AI Influencer + UGC Ads 赚钱"）从无结构 → 系统化框架
- 📊 **预期效果**:
  - 首次 AEO 评分: ~70 → ~85 (+15 分)
  - E-E-A-T 信号: 弱（缺数据来源）→ 强（完整引用链）
  - 变现路径: 分散提及 → 结构化框架（5 个收入流 + 具体收入范围 + 启动步骤）
  - 差异化程度: 低（话题驱动）→ 高（content_gaps 驱动差异化策略）
- 🧪 **测试验证**: 生成 2,950 词测试文章（AI Influencer + UGC Ads），所有 v2.5 功能验证通过

---

## v2.8.2 InVideo 原则系统化集成（2026-01-26） ⭐

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

---

## v2.8.1 SmartLauncher v2.2 意图前置架构发布（2026-01-26） ⭐

- ✅ **smart-launcher v2.2**: Step 1.5 素材使用意图 (洗稿/参考) + 意图驱动约束
- ✅ **AUTO_ROUTE.md**: rewrite_mode + reference_mode 配置 + 意图验证
- ✅ **MANUAL_ROUTE.md**: 参考模式扩展调研流程 + 三种扩展方向
- 🎯 **核心变化**: 内容类型不重要，重要的是用户想"洗稿还是参考"
- 📊 **用户定义**:
  - 洗稿: 80%+ 保留原内容，品牌换成 Alici AI
  - 参考: 作为起点，可以深挖扩展、补充新内容

---

## v2.8 SmartLauncher v2.1 三轨制发布（2026-01-25）

- ✅ **growth-topic-scout v2.3**: Seed D1/D2 + Direction 对象输出 + diversity_report
- ✅ **smart-launcher v2.1**: 三轨制入口 (全自动/手动/Seed)
- ✅ **DataForSEO 升级**: 新增 3 个 AEO/LLM 相关数据维度
- ✅ **新增 Schema 文件**: MISSION_CONFIG_SCHEMA.json, DIRECTION_SCHEMA.json
- 🎯 **核心突破**: 选题漏斗系统，50-100 关键词 → 2 个可执行方向
- 📊 **成本优化**: ~$2.59 → ~$0.47 (standard)

---

## v2.75 SmartLauncher v2.0 测试通过（2026-01-23）

- ✅ **双轨制流程测试通过**: 手动路线 7/7 PASS + 全自动路线 7/7 PASS
- ✅ **Phase 0 模式选择**: 问卷正确显示全自动/手动两个选项
- ✅ **手动路线验证**: DataForSEO 强制展示 + "vs" 自动识别 Tool Showdown + 5+ 标题选项
- ✅ **全自动路线验证**: 1-2 问题 + 洗稿模式 80%+ + 一键到 Preview
- ✅ **Writer 路由验证**: 4 种核心方向正确路由到对应 Writer
- 📊 **测试覆盖**: 14/14 验证点全部通过

---

## v2.74 SmartLauncher v2.0 双轨制架构（2026-01-23）

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

---

## case-roundup-writer v1.3 升级（2026-01-20） 🔥

- ✅ **Material Gate**: 强制索取真实素材，拒绝编造案例
- ✅ **多维度拓展**: 单一素材时多角度分析（工作流/场景/技巧/陷阱）
- ✅ **Prompts to Try**: 每篇文章包含 2-3 个可复用 Prompt 模板
- ✅ **标题确认**: 提供 5+ 标题选项（问题式/How-to/洞察式/数字式）
- ✅ **Visual Prompt Pack**: 生成可复用的图片 Prompt（角色演化系统）
- ✅ **Asset Plan Output**: 输出 asset_plan.json 数据契约给 Editor
- 🎯 **核心改进**: 解决 Phase A 测试中的案例编造问题，确保真实案例驱动
- 📊 **预期效果**: 单一视频也能写完整文章，用户获得可直接使用的 Prompt

---

## v2.73.2 Smart Launcher 架构统一（2026-01-22）

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

---

## v2.73.1 Editor v2.9.1 强制规则升级（2026-01-22）

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

---

## v2.73 Editor v2.9 Invideo 竞品 Review（2026-01-22）

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

---

## v2.72 YouTube URL 路由修复（2026-01-22） 🔧

- ✅ **smart-launcher v1.1**: YouTube URL 单独输入自动路由到 fetch-transcript
- ✅ **检测逻辑**: 支持标准 watch URL、短链接、嵌入链接
- ✅ **简单前缀**: 允许"抓取"、"获取"、"字幕"等前缀
- 🎯 **核心修复**: 解决 YouTube URL 输入时误入写作问卷的问题

---

## v2.71 Markdown-to-Framer 修复（2026-01-22） 🔧

- ✅ **markdown-to-framer v1.3**: 图片格式修复 (无 figure, alt 在 src 前)
- ✅ **特殊字符处理**: em dash/smart quotes 替换为兼容字符
- ✅ **cover 字段简化**: 只保留 url，移除 alt 和 metadata
- 🎯 **核心修复**: 解决 Framer CMS 导入错误 "TypeError: o is not iterable"

---

## v2.7 Tool Showdown + Version Verification 升级（2026-01-21）

- ✅ **smart-root v2.2**: 新增 Phase 0 版本验证，检测 "vs/对比/对决" 意图时自动 WebSearch 验证工具版本
- ✅ **blog-list-writer v2.2**: 新增 `tool_showdown` 内容类型，使用 10 固定 Headings 高对比度结构
- ✅ **TOOL_SHOWDOWN_TEMPLATE.md**: 新增共享模板，定义工具对决文章结构规范
- 🎯 **核心解决**: 版本滞后问题 (Kling 2.0 → 2.6) + 缺少高对比度模板 (Category Winners)
- 📊 **预期效果**: 工具版本准确性 100%，对决文章结构一致性 100%

---

## v2.2/v2.6/v2.1 版本继承升级（2026-01-18） ⭐

- ✅ **blog-tutorial-writer v2.2**: 版本继承机制，检测并保留 improved 版本的 E-E-A-T 内容
- ✅ **editor v2.6**: Module 7 版本对比检查 + Visual Asset System (asset_plan.json → asset_manifest.json)
- ✅ **auto-improver v2.1**: E-E-A-T 保护标记系统，标记需保留的内容
- 🎯 **核心修复**: 防止重写时丢失 E-E-A-T 投资（如 Sora 2 guide v1.1→v2.0 问题）
- 📊 **预期效果**: 编辑工作受保护，版本迭代不再丢失内容

---

## v2.0-v2.1 Higgsfield 洞察升级（2026-01-18）

- ✅ **growth-topic-scout v1.2**: 3 类型标题建议 (Listicle/How-to/Insights) + 年份验证 + CTR 预测
- ✅ **blog-list-writer v2.0**: 强制年份 + 数字标题 + 5 维度评测方法论 + Core Positioning 列
- ✅ **blog-tutorial-writer v2.1**: How-to 标题公式 + 7 要素 Prompt 结构章节（AI 教程）
- ✅ **BLOG_WRITING_PRINCIPLES v2.1**: 新增"标题与结构标准"章节（基于 Higgsfield）
- 📚 **新增文档**: `/docs 项目文档/00-CONTENT-PHILOSOPHY.md` - 内容策略哲学
- 🎯 **核心洞察**: 公式化标题 = SEO 可预测性，评测方法论 = E-E-A-T Authority 信号

---

## v2.3 升级（2026-01-17）

- ✅ **editor v2.3**: 新增 Module 6 (E-E-A-T 内容深度检查)，所有模块强制执行
- ✅ **aeo-analyzer v2.3**: M3 重组为结构信号(12分) + 内容深度(13分)
- 🎯 **关键改进**: 修复 Editor 模块跳过问题，E-E-A-T 评分不再只看结构
- 📊 **预期效果**: 文章质量门禁更严格，减少"高分低质"情况

---

## v2.0 升级（2026-01-16）

- ✅ **blog-tutorial-writer v2.0**: AIDA 开篇框架 + Citable Block 系统 + 强化 E-E-A-T
- 📊 **验证结果**: 首次 AEO 评分 73 → 82 分（+9 分），无需 auto-improver 迭代
- 📝 **Changelog**: 查看 `/skills/writers/blog-tutorial-writer/CHANGELOG.md`

---

## 实施路线图 — Phase 详情归档

### Phase 25 详情 (Writer v3.0 双升级 — Tier 系统 + Blueprint 强制结构) ⭐⭐⭐

- ✅ **blog-tutorial-writer v2.5 → v3.0**
  - Three-Tier 分级系统 (Tier 1/2/3 自动匹配话题复杂度)
  - Citable Block Taxonomy v3.0 (7 种类型: stat_callout, comparison_snapshot, definition_box, step_summary, expert_tip, data_table, key_takeaway)
  - IMAGE_PLACEHOLDER v2.0 (结构化占位符)
  - CTA_CARD v2.0 摩擦对齐
  - experiment_pack 可选经验证据
  - Self-Check JSON 自动生成
- ✅ **blog-list-writer v2.4 → v3.0**
  - 4 种 Blueprint Profile (A: Standard / B: Prompt/Workflow / C: Mega / D: Alternatives)
  - Plan Pack Bundle (4 文件输出)
  - Listicle Validator Gate (PASS/FAIL 门禁)
  - methodology_level 护栏 (research_only / hybrid / hands_on)
- ✅ **架构文档同步更新**
  - CLAUDE.md v3.0 版本头 + Skills 表 + 调用链 + Changelog + Roadmap
  - 00-CONTENT-PHILOSOPHY.md Writer 版本引用更新
  - WRITER-SELECTION-GUIDE.md v3.0 能力说明 + 输出结构更新
- 🎯 **核心突破**: Writer 从单一模板到分级强制结构 + 自动质量门禁

### Phase 24 详情 (Insight Pack + Market Context + Monetization Framework) ⭐

- ✅ **blog-tutorial-writer v2.4 → v2.5**
  - Insight Pack 可选输入
  - Market Context 章节（条件性）
  - Monetization Framework 章节（条件性）
  - 字数扩展：2,000-2,500 → 2,800-3,000
  - AEO 清单扩展：+13 检查点
- ✅ **growth-topic-scout v2.3 → v2.4**
  - 新增 competitive_insights 输出字段
  - 与 blog-tutorial-writer v2.5 Insight Pack 集成
- ✅ **新增文档**: `/skills/_docs/INSIGHT_PACK_SCHEMA.md` v1.0
- 🎯 **核心突破**: 复合型变现导向选题支持 + 竞品数据结构化传递

### Phase 23 详情 (InVideo 原则系统化集成) ⭐

- ✅ **6 个文件修改** (AUTO_ROUTE.md, TOOL_SHOWDOWN_TEMPLATE.md, opening-patterns.yaml, BLOG_WRITING_PRINCIPLES_v2.md, integration-levels.yaml, REWRITE_VALIDATION_TEMPLATE.md)
- ✅ **InVideo 6 大原则系统化**
- 🎯 **核心突破**: InVideo 原则从"隐式遵循"到"显式验证配置"

### Phase 22 详情 (SmartLauncher v2.2 意图前置架构) ⭐

- ✅ **smart-launcher v2.2**: Step 1.5 素材使用意图 + 意图驱动约束
- 🎯 **核心突破**: 从"隐式决定洗稿"到"用户明确选择使用意图"

### Phase 20-21 详情 (Seed Mode + 三轨制)

- ✅ **growth-topic-scout v2.3**: Mode D 新增 Seed Mode 选题漏斗
- ✅ **smart-launcher v2.1**: 三轨制入口
- 🎯 **核心突破**: 从"关键词扩展"升级为"选题漏斗"

### Phase 19 详情 (SmartLauncher v2.0 双轨制测试)

- ✅ 手动路线测试 7/7 PASS + 全自动路线测试 7/7 PASS
- 📊 **测试结果**: 14/14 验证点全部通过

### Phase 18 详情 (SmartLauncher v2.0 双轨制架构)

- ✅ **smart-launcher v2.0**: Phase 0 模式选择 + 全自动路线 + 手动路线
- 🎯 **核心突破**: 清晰的双轨制，用户明确知道自己在哪条路线

### Phase 17 详情 (SmartLauncher v1.2 架构统一)

- ✅ **Editor Gate 强制** + **Writer Feedback Loop** + **case-roundup-writer v1.5** + **editor v2.9.2 Module 10**
- 🎯 **核心突破**: 所有 Writer 输出必须经过 Editor Gate

### Phase 16 详情 (Editor v2.9.1 强制规则升级)

- ✅ 4 项规则从建议升级为强制 (Key Takeaways, Data Hook, 标题年份, CTA)

### Phase 15 详情 (Editor v2.9 Invideo 竞品 Review)

- ✅ **editor v2.9**: 24 种开篇模式 + 37 种标题公式 + L1-L20 植入检测 + 5 层引用金字塔
- ✅ **4 个新 YAML 配置文件**

### Phase 14 详情 (YouTube URL 路由修复) 🔧

- ✅ YouTube URL 单独输入时自动路由到 fetch-transcript

### Phase 13 详情 (Markdown-to-Framer v1.3 修复) 🔧

- ✅ 图片格式 + 特殊字符 + cover 字段修复

### Phase 12 详情 (SmartLauncher v1.0 架构升级)

- ✅ **smart-launcher v1.1**: 合并 smart-router v2.0 + smart-root v2.2
- ✅ **COMBOS.md** + **TITLE_FORMULAS.md** + **OPENING_PATTERNS.md** 发布

### Phase 11 详情 (Tool Showdown + Version Verification)

- ✅ **smart-root v2.2**: Phase 0 版本验证
- ✅ **blog-list-writer v2.2**: tool_showdown 内容类型
- ✅ **TOOL_SHOWDOWN_TEMPLATE.md** 发布

### Phase 10 详情 (质量保障升级)

- ✅ **output-path-builder** + **competitive-validator v1.0** + **trending-monitor v1.0** + **aeo-analyzer v2.4** + **smart-root v2.1**

### Phase 9 详情 (SmartRoot 交互式选题确认)

- ✅ smart-root v2.0 → v2.1: 4 步交互问卷 + DataForSEO 集成

### Phase 8 详情 (Visual Asset System)

- ✅ 数据契约: Writer v1.3 → asset_plan.json → Editor v2.6 → asset_manifest.json

### Phase 6 详情 (Phase A: MVP Core)

- ✅ case-roundup-writer v1.0 → v1.1: Material Gate + 多维度拓展 + Prompts to Try

### Phase 7 详情 (智能路由 + 批量处理)

- ✅ smart-router v1.0 → v2.0 + batch-processor v1.0

### Phase 5 详情

- ✅ blog-tutorial-writer v2.0: AIDA 开篇 + Citable Block + E-E-A-T 强化

---

*AliciBlog 完整版本历史 (v1.0 → v2.9，27 个 Phase，2026-01-11 → 2026-02-08)*
