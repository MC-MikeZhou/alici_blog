# Writer 选择指南

> 快速判断应该使用哪个 Writer Skill
> v2.0 — 四 Writer 架构 (Showdown 独立后)

---

## 一句话区分

| Writer | 核心定位 | 读者心态 |
|--------|----------|---------|
| **Showdown** | **帮人做决定** — "这 2-3 个里选哪个？" | 已缩小到 2-3 个候选，需要最终裁决 |
| **List** | **帮人看全景** — "这个领域有哪些好选择？" | 还在探索阶段，想看完整市场 |
| **Tutorial** | **教人做事** — "怎么用这个工具？" | 已选定工具，想学会使用 |
| **Roundup** | **展示发现** — "最近什么有效？" | 关注动态，想知道最新进展 |

---

## 场景决策树

```
用户输入包含对比意图?
├── YES → 检测工具数量
│   ├── ≤3 → blog-showdown-writer ✅
│   ├── = 4 → ⚠️ 边界: 询问用户 (Showdown or List?)
│   └── ≥5 → blog-list-writer ✅
│
├── NO → 检测其他信号
│   ├── "best/top/N个" → blog-list-writer ✅
│   ├── "how to/如何" → blog-tutorial-writer ✅
│   ├── "alternatives/替代" → blog-list-writer (Profile D) ✅
│   └── 案例/快讯/真实素材 → case-roundup-writer ✅
│
└── 不确定 → 询问用户
```

**快速判断法**：问自己"读者读完后要得到什么？"
- 得到**裁决** → Showdown
- 得到**全景** → List
- 得到**能力** → Tutorial
- 得到**洞察** → Roundup

---

## 四个 Writer 详细对比

| 维度 | Showdown | List | Tutorial | Roundup |
|------|----------|------|----------|---------|
| **核心哲学** | 帮你做最终决定 | 帮你看全景选择 | 教你怎么做 | 展示什么有效 |
| **搜索意图** | "Sora vs Runway" | "Best AI video generators" | "How to use Sora" | "What works..." |
| **漏斗位置** | **Decision 决策层** | **Consideration 考虑层** | **Interest 兴趣层** | **Awareness 洞察层** |
| **工具数量** | 2-3 个 (≤3 强制，4 需确认) | 5-29 个 (Profile A/B/C/D) | 单一工具/方法 | 2-5 个案例 |
| **字数** | 2,500-3,500 (固定) | 4,500-10,000 (Blueprint 驱动) | 1,800-3,500 (Tier 1/2/3) | 300-600 |
| **结构** | 11 固定标题 (不可变) | Blueprint 4 种 Profile (灵活) | Tier 分级 + Self-Check | 短小精悍 |
| **开头** | P4 Reframe 强制 | Hook 自由选择 | AIDA 框架 | Data Hook |
| **核心表格** | Snapshot + Scorecard 双表格 | Quick Comparison 单表格 | 无必须表格 | 无必须表格 |
| **决策辅助** | Category Winners + Decision Tree | Use Case Matching 表 | Troubleshooting Table | Prompts to Try |
| **信任机制** | evidence_level ⛔ + 引用 ≥5/千字 | methodology_level ⚠️ + 引用 ≥3/千字 | experiment_pack (可选) | Material Gate (必须) |
| **产品定位** | L4 Integrator (alici.ai 不是竞品) | L1 首位 (alici.ai 排第一) | 教程内自然植入 | 产品理念渗透 |
| **素材要求** | verified_tools JSON (版本验证) | Topic Brief + 竞品 URL | Topic Brief | 真实素材 (必须) |
| **计划输出** | showdown-plan.json | Plan Pack 4 文件 | Self-Check JSON | Insight/Case Pack |
| **Validator** | Showdown Validator Gate | Listicle Validator Gate | Self-Check Report | Material Gate |
| **AEO 基准** | ≥75 | ≥75 | ≥80 | ≥70 |
| **更新频率** | 季度 | 年度 | 年度 | 周/月级 |
| **当前版本** | v1.0 | v3.1 | v3.1 | v1.5 |

---

## 各 Writer 适用/不适用场景

### blog-showdown-writer (v1.0)

**适用场景** ✅
- 工具对决 ("Sora vs Runway vs Kling")
- 双雄对决 ("Midjourney vs DALL-E")
- 三方混战 ("ChatGPT vs Claude vs Gemini")
- 用户已缩小到 2-3 个候选，需要最终裁决

**不适用场景** ❌
- 4+ 工具对比 → 路由到 List Writer
- "Best X" 类查询 → 路由到 List Writer
- 替代品查询 "X alternatives" → 路由到 List Writer (Profile D)
- 单一工具评测 → 路由到 Tutorial Writer
- 无版本验证数据 → 阻断，要求先验证

**v1.0 核心能力** ⭐
- **11 固定标题结构**: Key Takeaways → Snapshot → Overviews → Scorecard → Category Winners → Decision Tree → FAQ → Verdict
- **P4 Reframe 强制开篇**: 常规认知 → 现实揭露 → 问题重定义 → 新视角
- **Showdown Plan**: showdown-plan.json (工具池 + 对比维度 + 证据链)
- **Showdown Validator Gate**: 11 标题顺序 + 表格 + CTA + Source 验证
- **evidence_level 护栏**: source_based / hybrid / hands_on (⛔ BLOCKING)
- **L4 Integrator 定位**: alici.ai 是聚合平台，不是竞品
- **Source Attribution**: 引用密度 ≥5/千字

---

### blog-list-writer (v3.1)

**适用场景** ✅
- 工具榜单 ("2026 年 10 大...")
- 年度盘点
- 大型工具评测 (5-29 个工具)
- 替代品文章 ("X alternatives")
- Prompt/工作流榜单

**不适用场景** ❌
- ≤3 工具 "A vs B vs C" → 路由到 Showdown Writer
- 单一工具深度教程 → 路由到 Tutorial Writer
- 时效性强的内容 → 路由到 Roundup Writer
- 纯数据统计类 (如 "135 Statistics") → 暂无 Writer

**v3.1 核心能力** ⭐
- **4 种 Blueprint Profile**:
  - A (Standard Listicle 4,500-5,500 词): 10-13 个工具标准榜单
  - B (Prompt/Workflow Listicle 5,500-6,500 词): 14-20 个工具 + Prompt 模板
  - C (Mega Listicle 8,000-9,500 词): 20+ 个工具分组榜单
  - D (Alternatives Listicle 6,500-10,000 词): 竞品替代方案
- **Plan Pack 输出**: 4 文件 Bundle (plan.json + assets.json + validator-report.json + article-draft.md)
- **Listicle Validator Gate**: PASS/FAIL 门禁，Blueprint 合规性 + 结构完整性自动验证
- **methodology_level 护栏**: research_only / hybrid / hands_on 三级方法论控制

---

### blog-tutorial-writer (v3.1)

**适用场景** ✅
- 操作指南 ("如何用 X 做 Y")
- 步骤教程 ("5 步完成...")
- AI 工具使用方法
- 技能养成类内容

**不适用场景** ❌
- 工具对比 → 应使用 Showdown 或 List
- 快讯类内容 → 应使用 Roundup
- 没有明确步骤的主题

**v3.1 核心能力** ⭐
- **Three-Tier 自动分级**: Tier 1 (1,800-2,200 词) / Tier 2 (2,200-2,800 词) / Tier 3 (2,800-3,500 词)，根据话题复杂度自动匹配
- **Prerequisites Check**: 自动检测前置条件并生成准备清单
- **Workflow Selector**: 根据内容类型自动选择最佳工作流模板
- **Troubleshooting Table**: 常见问题排查表自动生成
- **experiment_pack**: 可选经验证据包 (实验数据、A/B 测试、性能基准)
- **Self-Check JSON**: 结构化自检报告，减少 Editor 迭代
- **CTA_CARD v2.0**: 摩擦对齐，根据内容阶段匹配 CTA 类型
- **Citable Block Taxonomy v3.0**: 7 种引用块类型

---

### case-roundup-writer (v1.5)

**适用场景** ✅
- 新功能发布测评
- 病毒案例分析
- 有真实素材的洞察
- 快速验证某个假设

**不适用场景** ❌
- 没有真实素材时 (会被 Material Gate 阻止)
- 需要系统性覆盖的主题
- 长青内容 (evergreen content)

> ⚠️ **Material Gate**: Roundup 必须有真实素材支撑。如果只有想法没有素材，先收集素材再写。

---

## Showdown vs List: 关键边界区分

这是最常见的混淆场景，用以下规则判断：

| 场景 | 正确路由 | 原因 |
|------|---------|------|
| "Sora vs Runway vs Kling" (3 个) | **Showdown** | ≤3 工具，纯对决意图 |
| "Sora vs Runway vs Kling vs Veo" (4 个) | **询问用户** | 边界区，两种都可 |
| "5 Best AI Video Generators" (5 个) | **List** | ≥5 工具，全景意图 |
| "Top 10 Animoto Alternatives" | **List** (Profile D) | Alternatives ≠ 对决，动机是"找替代"不是"谁赢" |
| "Midjourney vs DALL-E" (2 个) | **Showdown** | 典型双雄对决 |
| "Best AI Art Tool" (暗含多个) | **List** | "Best" = 全景探索 |

### 增长视角差异

| 维度 | Showdown | List |
|------|----------|------|
| **增长角色** | **转化引擎** — 最后一步决策 | **流量基石** — 最大搜索量入口 |
| **核心 KPI** | CTR → 注册转化率 | 有机流量 + 品牌曝光 |
| **搜索量** | 中-低 (精准长尾) | 中-高 (商业意图) |
| **转化率** | 最高 | 中等 |
| **AEO 触发词** | "vs", "compared to", "which is better" | "best", "top", "recommend" |
| **AEO 回答模式** | 直接推荐: "Based on comparison, X wins for Y" | 列表推荐: "Top 5: 1. X 2. Y..." |
| **引用密度** | ≥5/千字 (更严格) | ≥3/千字 (标准) |

---

## 输出预期对照

### Showdown 输出结构
```
/reports 待发文章/YYYY-MM-DD-{topic}/
├── 01-article-draft.md       # 11 固定标题结构
├── showdown-plan.json        # Showdown Plan
├── showdown-validator.json   # Validator Report
└── assets/
```

**典型内容样式**：
- P4 Reframe 开篇
- Snapshot + Scorecard 双表格
- Category Winners (Choose/Avoid)
- Decision Tree (If you need X → choose A)
- 3 个固定 CTA 位置

---

### List 输出结构
```
/reports 待发文章/YYYY-MM-DD-{topic}/
├── 01-article-draft.md               # Blueprint 强制结构
├── 02-plan.json                      # Plan Pack
├── 03-assets.json                    # Assets Queue
└── 04-listicle-validator-report.json  # Validator Report
```

**典型内容样式**：
- 排名或分类明确
- 每个选项有优缺点
- Quick Pick 推荐
- 对比表格

---

### Tutorial 输出结构
```
/reports 待发文章/YYYY-MM-DD-{topic}/
├── 01-article-draft.md       # 主文章
├── 01-article-draft.json     # Self-Check Report
└── assets/
```

**典型内容样式**：
- 清晰的步骤编号
- 每步配截图/代码示例
- Pro Tips 穿插
- 结尾有 Next Steps

---

### Roundup 输出结构
```
/reports 待发文章/YYYY-MM-DD-{topic}/
├── 01-article-draft.md       # 主文章
├── 00-insight-pack.json      # Insight Pack
└── 00-case-pack.json         # Case Pack
```

**典型内容样式**：
- 短小精悍
- 以案例/数据开头
- 快速给出结论
- 附真实素材来源

---

## 快速命令参考

| 场景 | 命令 | 说明 |
|------|------|------|
| 写对决 | `/write-showdown` 或含 "vs" 触发 | 启动 Showdown Writer |
| 写榜单 | `/write-list` | 启动 List Writer |
| 写教程 | `/write-tutorial` | 启动 Tutorial Writer |
| 写案例 | `/write-roundup` | 启动 Roundup Writer |
| 不确定 | 说"帮我写..." | 让 smart-launcher 引导你选择 |

---

## 常见问题

**Q: 我的选题是"A vs B"，但也想覆盖更多工具，怎么选？**

A: 看核心读者需求。如果读者已经锁定了 A 和 B 两个候选想要裁决，选 Showdown；如果读者还在探索阶段，A vs B 只是入口，选 List 然后用 Profile A/B 覆盖更多工具。

**Q: Showdown 和 List 都能处理对比，核心区别是？**

A: Showdown 是"头对头对决"（≤3 工具，11 固定标题，双表格，Category Winners），List 是"逐一评测"（5+ 工具，Blueprint 灵活结构，Use Case Matching）。动机不同：Showdown 帮决策，List 帮探索。

**Q: "Top 10 Animoto Alternatives" 为什么不用 Showdown？**

A: Alternatives 文章不是"A vs B 谁赢"，而是"A 不好用，这些替代更好"。动机是找替代，不是做裁决。应使用 List Writer Profile D (Alternatives)。

**Q: 4 个工具的对比怎么处理？**

A: 4 个工具是边界区。如果内容本质是"头对头对决"（纯对比谁赢），可以用 Showdown（需用户确认）；如果更像"小型榜单"，用 List Writer。SmartLauncher 会自动询问用户选择。

**Q: 我的选题既有对比又有教程性质，怎么选？**

A: 看主要价值。如果读者核心目的是"学会做某事"，选 Tutorial，在文中简要对比工具；如果核心目的是"选出最合适的工具"，选 Showdown 或 List。

**Q: Roundup 和 Tutorial 都能写工具测评，区别是？**

A: Roundup 是"快速分享发现"，300-600 字，适合新功能速报；Tutorial 是"教会使用"，1,800+ 字，适合完整教程。

**Q: 没有足够素材但想写 Roundup 怎么办？**

A: 先用 `/fetch-transcript` 等工具收集素材，或者考虑选题是否更适合 Tutorial/List 形式。

---

*最后更新: 2026-02-07*
