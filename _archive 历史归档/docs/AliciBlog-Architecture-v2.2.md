# AliciBlog 2.2 架构文档

> **AI 内容工厂的自动化博客生产系统 - 70%+ 自动化率**
>
> **版本**: v2.2
> **更新日期**: 2026-01-18
> **核心升级**: 版本继承系统 - 确保 E-E-A-T 投资永不丢失

---

## 一、系统运行机制

### 1.1 核心架构 (v2.2)

```
┌─────────────────────────────────────────────────────────────────┐
│                   AliciBlog 统一架构 (v2.2)                      │
├─────────────────────────────────────────────────────────────────┤
│  输入层 (手动触发): URL | Notion | Text | Topic Brief           │
│                            ↓                                    │
│  处理层 (Agent 自主): scout → writer → analyzer ⟷ improver      │
│                            ↓         ↑                          │
│                      版本继承检查 ←──┘                          │
│                            ↓                                    │
│  输出层 (手动确认): 中文预览 → 审核 → Framer JSON → 发布        │
└─────────────────────────────────────────────────────────────────┘
```

**自动化程度分层**:

| 层级 | 自动化程度 | 人工参与 |
|------|-----------|---------|
| 输入层 | 手动触发 | 选择输入源 |
| 处理层 | Agent 自主 | 仅 3 轮后仍 <75 分时介入 |
| 输出层 | 手动确认 | 中文预览 + 发布确认 |

### 1.2 版本继承流程 (v2.2 新增) ⭐

```
                    版本继承决策树
                          │
                    检测 improved 文件
                          │
            ┌─────────────┴─────────────┐
            │                           │
        存在 ✅                      不存在 ❌
            │                           │
    ┌───────┴───────┐                   │
    │ 版本继承模式  │             ┌─────┴─────┐
    │   (v2.2)     │             │ 正常模式  │
    └───────┬───────┘             └─────┬─────┘
            │                           │
    强制保留 E-E-A-T 内容           从 topic brief 生成
            │                           │
    ┌───────┴────────┐                  │
    │ • Author Info  │                  │
    │ • Case Studies │                  │
    │ • Testing Data │                  │
    │ • Sources      │                  │
    │ • Disclosure   │                  │
    │ • FAQ          │                  │
    └───────┬────────┘                  │
            │                           │
            └───────────┬───────────────┘
                        │
                    生成新版本
                        │
                 Editor Module 7
                   版本对比检查
                        │
            ┌───────────┴───────────┐
            │                       │
        PASS ✅                BLOCKING ⛔
            │                       │
      输出 edited 文件        仅输出 report
                              要求人工审核
```

### 1.3 工作流五阶段

```
阶段 1: 内容发现
├── growth-topic-scout v1.2
├── 输入: 竞品 URL / 主题关键词
└── 输出: Top 10 选题 + 3 类型标题 + CTR 预测

阶段 2: 内容生成
├── blog-tutorial-writer v2.2 (教程)
├── blog-list-writer v2.0 (榜单)
├── 输入: Topic Brief + [可选] improved 版本
└── 输出: 1,800-3,500 词初稿 + 版本继承标记

阶段 3: 内容优化
├── editor v2.4 (图片 + 格式 + Module 7 版本检查)
├── 输入: Draft 或重写版本
└── 输出: Edited 版本 或 BLOCKING 报告

阶段 4: 质量评估与迭代
├── aeo-analyzer v2.3 (M3 重组: 结构12分 + 内容深度13分)
├── auto-improver v2.1 (Path A: AEO优化 | Path B: E-E-A-T内容)
├── 输入: Edited 版本
└── 输出: Improved 版本 + E-E-A-T 保护标记

阶段 5: 发布准备
├── chinese-previewer v1.0 (中文审核摘要)
├── markdown-to-framer v1.0 (Framer CMS JSON)
└── framer-previewer v1.0 (本地预览)
```

### 1.4 自动闭环机制

```
┌──────────────┐
│   Scout      │ 发现选题
│   (Agent)    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Writer     │ 生成初稿 ← 检测 improved 版本 (v2.2)
│   (Skill)    │            版本继承模式
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Editor     │ 优化 + 图片
│   (Skill)    │ Module 7: 版本对比 (v2.4)
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐
│  AEO Analyzer│────▶│ Auto-improver│ Path B 添加
│   (Skill)    │     │   (Skill)    │ E-E-A-T 保护标记 (v2.1)
└──────────────┘     └──────┬───────┘
                            │
       ┌────────────────────┘
       │
       ▼
    评分 ≥75?
       │
   ┌───┴───┐
  YES     NO (最多3轮)
   │       │
   │       └──▶ 返回 improver
   │
   ▼
发布流程
```

**关键迭代规则**:
- AEO < 75 分 → 自动触发 auto-improver
- 最多 3 轮迭代，仍 < 75 分 → 人工介入
- 每轮迭代 improved 文件 → 成为下次重写的基准版本

---

## 二、核心要素说明

### 2.1 Skills 系统链条 (v2.2)

| Skill | 版本 | 触发词 | 核心功能 | v2.2 更新 |
|-------|------|--------|----------|-----------|
| **growth-topic-scout** | **v1.2** 🆕 | 竞品分析, 选题发现 | Top 10 选题 + 3 类型标题建议 | 新增 CTR 预测 + 年份验证 |
| **blog-tutorial-writer** | **v2.2** ⭐ | write tutorial | 1,800-2,500 词教程 | **版本继承机制** + How-to 标题公式 |
| **blog-list-writer** | **v2.0** 🆕 | write list | 2,500-3,500 词榜单 | 强制年份 + 5 维度评测方法论 |
| **editor** | **v2.4** ⭐ | edit article | 图片 + 优化 + 格式 | **Module 7 版本对比检查** |
| **aeo-analyzer** | **v2.3** 🆕 | AEO 分析 | 100 分评分 | M3 重组: 结构信号(12) + 内容深度(13) |
| **auto-improver** | **v2.1** ⭐ | 改进文章 | AEO优化 + E-E-A-T | **E-E-A-T 保护标记系统** |
| chinese-previewer | v1.0 | 中文预览 | 审核摘要 | - |
| markdown-to-framer | v1.0 | convert to framer | Framer CMS JSON | - |
| framer-previewer | v1.0 | preview framer | 本地预览 HTML | - |

**完整调用链**:
```
scout → writer (完整) → editor (Module 7) → aeo-analyzer ⟷ improver (E-E-A-T标记) → framer → preview
```

### 2.2 版本继承规则 (v2.2 核心升级) ⭐

#### 核心原则
**改进不可丢失 (Improvements Never Lost)**

#### 触发条件
当重写文章时，系统检测是否存在 `01-article-improved-*.md`：
- **存在** → 版本继承模式（强制保留 E-E-A-T 内容）
- **不存在** → 正常模式（从 topic brief 生成）

#### 强制保留内容清单

| 内容类型 | 保留规则 | E-E-A-T 信号 | 为什么不可丢失 |
|---------|---------|-------------|---------------|
| **Author Information** | YAML `author` block 完全一致 | **Experience** | 命名作者优于团队署名 |
| **Case Studies** | 所有案例研究完整保留 | **Experience** | 原创案例不可复现，是核心资产 |
| **Testing Methodology** | 所有 "n=X" 引用保留 | **Authority** | 测试数据建立可信度 |
| **External Sources** | 来源数量 >= 前版本 | **Authority** | 引用链可新增但不可删除 |
| **Disclosure** | 披露声明完全保留 | **Trust** | 透明度要求，法律合规 |
| **FAQ** | 问题数量 >= 前版本 | **AEO** 优化 | FAQ 是高引用率内容 |
| **Citable Blocks** | 所有标记块保留 | **Authority** | 可引用内容块，SEO 价值高 |

#### 可更新内容
以下内容可以重写以整合新方法论：
- ✅ 标题格式（使用最新 How-to 公式）
- ✅ 开篇框架（应用 AIDA 结构）
- ✅ 章节组织（重构 H2/H3 层级）
- ✅ Prompt 框架（添加 7 要素系统）
- ✅ 示例代码（更清晰的演示）

#### Editor v2.4 Module 7 验证检查

| 检查项 | 阈值 | 失败等级 | 后果 |
|--------|------|---------|------|
| Word Count | -20% max | ⛔ **BLOCKING** | 停止输出 edited 文件 |
| Author Name | 完全匹配 | ⛔ **BLOCKING** | 停止输出 edited 文件 |
| Case Studies | >= 前版本 | ⚠️ WARNING | 标记但允许输出 |
| Testing Refs (n=X) | 全部保留 | ⚠️ WARNING | 标记但允许输出 |
| External Sources | >= 前版本 | ⚠️ WARNING | 标记但允许输出 |
| FAQ Count | >= 前版本 | ⚠️ WARNING | 标记但允许输出 |

**BLOCKING 后果**: Editor 停止输出 `01-article-edited.md`，仅生成报告 `04-editor-report.md`，标记 `MANUAL_REVIEW` required

#### E-E-A-T 保护标记系统 (auto-improver v2.1)

Auto-improver Path B (E-E-A-T 优化) 输出时会添加保护标记：

```markdown
<!-- E-E-A-T_PROTECTED_CONTENT_START -->

## About the Author
[作者信息复述 frontmatter]

## Real-World Case Studies
[所有案例研究]

## Testing Methodology
[测试方法和数据，包含 n=X 引用]

## Sources
[外部来源列表]

## Disclosure
[利益披露声明]

<!-- E-E-A-T_PROTECTED_CONTENT_END -->
```

**标记作用**:
- 告诉 blog-tutorial-writer v2.2: 此内容受保护，必须保留
- 告诉 editor v2.4 Module 7: 验证这些内容是否完整
- 人工审核时高亮显示核心 E-E-A-T 投资

#### 版本链示例

**正确的版本演进**:
```
v1.0 draft (4,800 词)
    ↓ editor v2.3 + auto-improver (3h45m 工作)
v1.1 improved (5,500 词)  ← E-E-A-T 投资 ⭐
    ↓ blog-tutorial-writer v2.2 重写 (检测 improved, 继承 E-E-A-T)
v2.0 (5,400 词)  ← 框架更新 + E-E-A-T 完整保留 ✅
    ↓ editor v2.4 Module 7 (验证继承)
v2.0 编辑完成 ← PASS (所有内容保留) ✅
```

**错误的版本演进** (v2.2 前):
```
v1.0 draft (4,800 词)
    ↓ editor + auto-improver (3h45m 工作)
v1.1 improved (5,500 词)  ← E-E-A-T 投资 ⭐
    ↓ blog-tutorial-writer v2.1 重写 (忽略 improved)
v2.0 (4,100 词)  ← 丢失全部 E-E-A-T 内容 ❌
    ↓ 需手动合并 v1.1 + v2.0
v2.5 手动合并版 (5,500 词)  ← 浪费 2+ 小时
```

### 2.3 AEO 评分框架 (v2.3 更新)

**Module 3 重组** (v2.3 关键变化):

| 模块 | 旧版本 (v2.2) | 新版本 (v2.3) | 变化说明 |
|------|--------------|--------------|---------|
| M3 | 内容组织 (25分) | **结构信号 (12分)** + **内容深度 (13分)** | 拆分为结构 + 深度，E-E-A-T 不再只看结构 |
| M6 | 不存在 | **E-E-A-T 内容深度检查** (新增) | 所有模块强制执行 |

**完整评分结构 (v2.3)**:
```
M1: 开篇与首段优化 (10分)
M2: 标题与可扫描性 (15分)
M3a: 结构信号 (12分) ← 拆分
M3b: 内容深度 (13分) ← 拆分
M4: 多媒体优化 (20分)
M5: 语义 SEO 与实体 (18分)
M6: E-E-A-T 内容深度检查 (12分) ← 新增
────────────────────────────
总分: 100 分
```

**预期效果**:
- 修复"高分低质"问题（结构好但内容浅）
- E-E-A-T 评分更准确（M6 独立检查）
- 质量门禁更严格（减少 AEO 评分虚高）

### 2.4 Higgsfield 洞察集成 (v2.0-v2.1)

#### 标题公式化 (growth-topic-scout v1.2)

**3 类型标题建议**:

| 类型 | 公式 | 示例 | CTR 预测 |
|------|------|------|---------|
| **Listicle** | `[数字] Best [工具类别] in [年份]` | "10 Best AI Video Tools in 2026" | 8.5% |
| **How-to** | `How to [动作] with [工具] ([数字] Steps)` | "How to Create Viral Videos with Sora (7 Steps)" | 7.2% |
| **Insights** | `[工具] Review: [数字] [维度] Tested` | "Sora Review: 12 Features Tested" | 6.8% |

**年份验证**: 强制检查标题中的年份必须 = 当前年份或当前年份 + 1

#### 评测方法论 (blog-list-writer v2.0)

**5 维度评测框架**:
1. **Ease of Use** (易用性) - 上手难度、界面友好度
2. **Feature Set** (功能完整性) - 核心功能覆盖范围
3. **Output Quality** (输出质量) - 生成结果质量
4. **Pricing** (性价比) - 免费额度、付费计划
5. **Use Cases** (适用场景) - 最佳使用场景

**Core Positioning**: 每个工具必须有"一句话定位"，说明它在什么场景下是 #1 选择

#### 7 要素 Prompt 结构 (blog-tutorial-writer v2.1)

针对 AI 工具教程，Prompt 章节必须包含:
1. **Task** - 任务定义
2. **Context** - 背景信息
3. **Constraints** - 限制条件
4. **Output Format** - 输出格式
5. **Examples** - 示例
6. **Tone** - 语气风格
7. **Length** - 长度要求

---

## 三、文件命名规范

### 3.1 版本文件命名 (v2.2 更新)

| 版本类型 | 文件名 | 产生者 | 说明 |
|----------|--------|--------|------|
| 初稿 | `01-article-draft.md` | writer skill | Writer 直接输出 |
| 编辑版 | `01-article-edited.md` | editor skill | Editor 输出 |
| **改进版** | `01-article-improved-v1.md` | **auto-improver** | ⭐ **后续重写的基准版本** |
| 改进版迭代 | `01-article-improved-v2.md` | auto-improver | 第二轮改进输出 |
| 重写版 | `01-article-v2.md` | writer skill | 结构升级版本（必须继承 improved） |
| 手动合并版 | `01-article-v2.5.md` | 手动合并 | 框架 + E-E-A-T 合并（不推荐） |

**关键版本**: `01-article-improved-v*.md` - **必须被后续所有重写继承**

### 3.2 完整输出目录结构

```
/reports/[YYYY-MM-DD]-[topic-slug]/
├── 00-implementation.md           # 进度追踪 (必须)
├── 00-topic-scout-report.md       # 选题分析
├── 00-topic-brief.json            # Topic Brief
│
├── 01-article-draft.md            # 初稿
├── 01-article-edited.md           # 编辑版
├── 01-article-improved-v1.md      # ⭐ 改进版 (E-E-A-T 投资)
├── 01-article-improved-v2.md      # 改进版迭代 2
├── 01-article-v2.md               # 重写版 (必须继承 improved)
│
├── 02-chinese-preview.md          # 中文预览
├── 03-aeo-score.md                # 评分报告
├── 03-aeo-score-v2.md             # 评分报告 v2
├── 04-editor-report.md            # Editor 改进报告
├── 04-editor-report-module7.md    # Module 7 版本对比报告 (v2.4)
│
├── 06-article-final.json          # Framer CMS JSON
└── 07-preview.html                # Framer 可视化预览
```

### 3.3 版本号规则

**整数版本** (v1, v2, v3):
- 结构性重写
- 来自 writer skill
- **必须继承最新 improved 版本**

**小数版本** (v1.5, v2.5):
- 手动合并版本
- 通常合并框架 + E-E-A-T
- 临时解决方案（理想情况下 v2.2 后不应需要）

**improved 版本** (improved-v1, improved-v2):
- auto-improver 输出
- 基于 AEO 评分报告的迭代改进
- **后续重写的基准版本**

---

## 四、当前状态与检查点

### 4.1 系统成熟度

| 组件 | 状态 | 版本 | 成熟度 |
|------|------|------|--------|
| growth-topic-scout | ✅ 稳定 | v1.2 | 生产就绪 |
| blog-tutorial-writer | ✅ 稳定 | v2.2 | 生产就绪 + 版本继承 |
| blog-list-writer | ✅ 稳定 | v2.0 | 生产就绪 |
| editor | ✅ 稳定 | v2.4 | 生产就绪 + Module 7 |
| aeo-analyzer | ✅ 稳定 | v2.3 | 生产就绪 + M3 重组 |
| auto-improver | ✅ 稳定 | v2.1 | 生产就绪 + E-E-A-T 标记 |
| chinese-previewer | ✅ 稳定 | v1.0 | 生产就绪 |
| markdown-to-framer | ✅ 稳定 | v1.0 | 生产就绪 |
| framer-previewer | ✅ 稳定 | v1.0 | 生产就绪 |

### 4.2 版本继承检查点

**重写文章前必检查**:
- [ ] 是否存在 `01-article-improved-*.md` 文件？
- [ ] Writer v2.2 是否启用版本继承模式？
- [ ] 前版本的 Author、Case Studies、Testing 数据是否标记清楚？

**重写文章后必验证**:
- [ ] Editor v2.4 Module 7 状态是否 PASS？
- [ ] 字数减少是否 <= 20%？
- [ ] Author Name 是否完全一致？
- [ ] E-E-A-T 保护内容是否完整保留？

**发布前最终检查**:
- [ ] AEO 评分是否 >= 75 分？
- [ ] 中文预览是否已审核？
- [ ] Framer JSON 是否生成成功？
- [ ] 本地预览是否正常显示？

### 4.3 异常处理

| 异常情况 | 检测点 | 处理方式 |
|---------|--------|---------|
| **版本继承失败** | Writer v2.2 | 警告并回退到正常模式 |
| **Module 7 BLOCKING** | Editor v2.4 | 停止输出，生成报告，要求人工审核 |
| **AEO < 60 分** | aeo-analyzer | 立即标记，暂停流程，人工介入 |
| **图片生成失败** | editor | 标记占位符，继续流程，后续补充 |
| **E-E-A-T 内容丢失** | Editor Module 7 | BLOCKING，禁止发布 |

---

## 五、关键学习点与最佳实践

### 5.1 5 条黄金规则

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

### 5.2 版本继承最佳实践 (v2.2 新增)

**✅ 推荐做法**:
1. **始终从最新 improved 版本开始重写** - 检测 improved 文件 → 从 improved 重写 → 保留 E-E-A-T
2. **重写前运行 editor Module 7 预检** - 在 writer 输出后立即验证版本继承
3. **E-E-A-T 保护标记放置于文章末尾** - Conclusion/FAQ 之后添加保护标记
4. **定期审计版本链完整性** - 每周检查是否有孤立的 draft 文件未改进

**❌ 避免做法**:
1. **从 topic brief 重写 → 忽略 improved → 丢失 E-E-A-T** ❌
2. **跳过 Module 7 检查直接发布** ❌
3. **手动合并 improved + rewrite 版本**（v2.2 应自动继承）❌
4. **删除 improved 文件以"清理"目录**（这是基准版本！）❌

### 5.3 常用命令速查

| 命令 | 用途 | 推荐场景 |
|------|------|---------|
| `/full-workflow URL` | **完整流程（推荐入口）** | 从零开始生产一篇文章 |
| `/scout-topic URL` | 选题发现 | 竞品分析、寻找灵感 |
| `/write-tutorial` | 教程文章 | How-to、Guide 类文章 |
| `/write-list` | 榜单文章 | Best Tools、Top 10 类文章 |
| `/edit-article FILE` | 图片 + 优化 + Module 7 检查 | 初稿完成后必须执行 |
| `/analyze-aeo FILE` | 质量评分 | 验证是否达到 75 分门禁 |
| `/improve-article FILE` | 自动改进 | AEO < 75 时触发 |
| `/preview-chinese FILE` | 中文预览 | 发布前人工审核 |
| `/convert-to-framer FILE` | 输出 CMS JSON | 准备发布到 Framer |
| `/preview-framer FILE` | Framer 可视化预览 | 本地预览最终效果 |

**使用示例**:
```bash
# 完整工作流（推荐）
/full-workflow https://competitor.com/blog/ai-video

# 单独步骤
/scout-topic https://competitor.com/blog/ai-tools
/write-tutorial  # 需 topic brief
/edit-article /reports/2026-01-15-ai-video/01-article-draft.md
/analyze-aeo /reports/2026-01-15-ai-video/01-article-edited.md
/improve-article /reports/2026-01-15-ai-video/01-article-edited.md
/preview-framer /reports/2026-01-15-ai-video/01-article-improved-v2.md
```

### 5.4 版本继承故障排除 (v2.2 新增)

| 问题 | 症状 | 解决方案 |
|------|------|---------|
| **Writer 未检测到 improved** | 重写文章丢失 E-E-A-T | 1. 确认 improved 文件存在于同一目录<br>2. 确认 writer v2.2 启用<br>3. 手动传递 `previous_version` 参数 |
| **Module 7 误报 BLOCKING** | 内容完整但被标记 BLOCKING | 1. 检查阈值设置（-20% word count）<br>2. 检查 Author 名称完全一致<br>3. 如误报，手动批准 |
| **E-E-A-T 保护标记格式错误** | Writer/editor 无法识别标记 | 1. 确认标记格式正确<br>2. 确认标记成对出现<br>3. 确认标记之间有实际内容 |
| **版本链断裂** | 无法确定哪个版本是最新 | 1. 用文件修改时间确定最新版本<br>2. 读取 `00-implementation.md` 查看历史<br>3. 必要时手动标记 |

### 5.5 不要做的事

- ❌ 跳过 Plan 模式直接执行复杂任务
- ❌ 单会话处理多个不相关功能
- ❌ 忽略 AEO < 75 的文章直接发布
- ❌ 使用 "revolutionary", "game-changing" 等营销词
- ❌ 无 Topic Brief 直接写文章
- ❌ 手动修改 00-implementation.md（让 Claude 维护）
- ❌ **删除 improved 文件（v2.2 核心基准版本）** ⭐
- ❌ **重写时忽略 improved 版本（导致 E-E-A-T 丢失）** ⭐
- ❌ **跳过 Module 7 版本检查（失去版本继承保护）** ⭐

---

## 六、技术配置

### 6.1 图片生成

**服务**: FAL.ai nano-banana
- 脚本: `/scripts/fal_image_generator.py`
- API Key 配置: `.mcp.json` → `mcpServers.fal.env.FAL_API_KEY`
- 读取优先级: 环境变量 > .mcp.json 配置文件
- 持久化: 会话压缩后自动加载，无需手动 export
- 上传: `rsync` 到 `root@<YOUR_SERVER_IP>:/var/www/static/static/image/other/gen_images/`
- CDN: `https://ct2.alici.ai/static/image/other/gen_images/`

### 6.2 MCP 服务

**DataForSEO**:
- SERP 数据
- KEYWORDS_DATA

### 6.3 内容规范

**参考文档**: `blog_new_sam 11.20.2025/doc/` 下的 3 个 MD 文件

**核心规范文件**:
- `BLOG_WRITING_PRINCIPLES_v2.md` - 内容撰写原则 (v2.1 新增标题与结构标准)
- `PRODUCT_CATALOG.md` - 产品目录与 CTA 映射
- `EVALUATION_FRAMEWORK.md` - AEO 评分标准

---

## 七、版本演进历史

### v2.2 升级（2026-01-18）⭐

**核心修复**: 防止重写时丢失 E-E-A-T 投资

| 组件 | 版本 | 关键更新 |
|------|------|---------|
| **blog-tutorial-writer** | **v2.2** | 版本继承机制，检测并保留 improved 版本的 E-E-A-T 内容 |
| **editor** | **v2.4** | Module 7 版本对比检查，BLOCKING 如果关键内容丢失 |
| **auto-improver** | **v2.1** | E-E-A-T 保护标记系统，标记需保留的内容 |

**问题案例**: Sora 2 Prompt Guide v1.1→v2.0 重写时丢失全部 E-E-A-T 内容（3h45m 工作量 + 1,400 词）

**解决方案**: 三层保护机制
1. Writer v2.2 检测并继承 improved 版本
2. Auto-improver v2.1 添加 E-E-A-T 保护标记
3. Editor v2.4 Module 7 验证继承完整性

**预期效果**: 编辑工作受保护，版本迭代不再丢失内容

### v2.0-v2.1 Higgsfield 洞察升级（2026-01-18）🆕

| 组件 | 版本 | 关键更新 |
|------|------|---------|
| **growth-topic-scout** | **v1.2** | 3 类型标题建议 + 年份验证 + CTR 预测 |
| **blog-list-writer** | **v2.0** | 强制年份 + 数字标题 + 5 维度评测方法论 + Core Positioning |
| **blog-tutorial-writer** | **v2.1** | How-to 标题公式 + 7 要素 Prompt 结构章节（AI 教程） |

**核心洞察**: 公式化标题 = SEO 可预测性，评测方法论 = E-E-A-T Authority 信号

**新增文档**: `/blueprint/00-CONTENT-PHILOSOPHY.md` - 内容策略哲学

### v2.3 升级（2026-01-17）

| 组件 | 版本 | 关键更新 |
|------|------|---------|
| **editor** | **v2.3** | 新增 Module 6 (E-E-A-T 内容深度检查)，所有模块强制执行 |
| **aeo-analyzer** | **v2.3** | M3 重组为结构信号(12分) + 内容深度(13分) |

**关键改进**: 修复 Editor 模块跳过问题，E-E-A-T 评分不再只看结构

**预期效果**: 文章质量门禁更严格，减少"高分低质"情况

### v2.0 升级（2026-01-16）

| 组件 | 版本 | 关键更新 |
|------|------|---------|
| **blog-tutorial-writer** | **v2.0** | AIDA 开篇框架 + Citable Block 系统 + 强化 E-E-A-T |

**验证结果**: 首次 AEO 评分 73 → 82 分（+9 分），无需 auto-improver 迭代

---

## 八、文档索引

| 文档 | 位置 | 用途 |
|------|------|------|
| **版本继承规范** | `/blueprint/10-VERSION-INHERITANCE.md` | v2.2 版本继承详细规范 |
| 完整 Skills | `/blueprint/02-SKILLS.md` | 19 个 Skills 定义 |
| 最佳实践 | `/blueprint/07-BEST-PRACTICES.md` | 专家经验总结 |
| 团队上手 | `/blueprint/08-TEAM-ONBOARDING.md` | 新成员 10 分钟指南 |
| 故障排除 | `/blueprint/09-TROUBLESHOOTING.md` | 常见问题解决 |
| 内容策略哲学 | `/blueprint/00-CONTENT-PHILOSOPHY.md` | 内容策略与竞品洞察 |
| AEO 框架 | `/skills/core/aeo-analyzer/EVALUATION_FRAMEWORK.md` | 评分标准 |
| 产品目录 | `/skills/_docs/PRODUCT_CATALOG.md` | CTA 映射 |

---

## 九、成功指标

### 9.1 技术指标 (v2.2)

| 指标 | 目标 | 测量方法 |
|------|------|---------|
| **版本继承率** | 100% | (重写时检测到 improved) / (存在 improved 的重写) |
| **E-E-A-T 保留率** | 100% | (保留的 E-E-A-T 元素) / (前版本 E-E-A-T 元素) |
| **BLOCKING 误报率** | < 5% | (误报 BLOCKING) / (总 BLOCKING) |
| **字数损失率** | < 10% | avg((prev - curr) / prev) for all rewrites |
| **AEO 首次评分** | >= 75 | 首次 draft 经 editor 后的评分 |
| **自动化率** | >= 70% | (自动流程步骤) / (总流程步骤) |

### 9.2 业务指标

| 指标 | 目标 | 影响 |
|------|------|------|
| **编辑返工时间** | -80% | 减少手动合并需求 |
| **AEO 评分稳定性** | ±5 分 | 重写不降低评分 |
| **E-E-A-T 投资 ROI** | 持久 | 投资的内容不会丢失 |
| **发布周期** | 3-5 天/篇 | 从选题到发布 |
| **质量门禁通过率** | >= 80% | 首次 AEO >= 75 分的比例 |

---

## 十、未来改进路线图

### Phase 6 规划（待启动）

| 功能 | 优先级 | 说明 |
|------|--------|------|
| **自动版本链可视化** | 高 | 生成版本演进图，显示关键指标 |
| **版本 diff 工具** | 高 | 自动对比任意两个版本，高亮 E-E-A-T 变化 |
| **智能合并建议** | 中 | 检测 improved + rewrite 需要合并时自动建议 |
| **Notion URL 输入支持** | 中 | 扩展输入层，支持从 Notion 导入 |
| **75 分验证门禁** | 高 | 处理层自动拦截 < 75 分文章 |

### v3.0 愿景

1. **版本继承 CI/CD**
   - pre-commit hook 检查版本继承
   - 自动运行 Module 7 验证
   - BLOCKING 时禁止 commit

2. **E-E-A-T 内容库**
   - 集中管理所有 case studies
   - 可跨文章复用案例
   - 版本化案例管理

3. **完全自动化发布** (80%+ 自动化)
   - 只保留 1 个人工节点：发布审核
   - 选题确认改为 AI 推荐 + 自动触发

---

**Document Version**: v2.2
**Last Updated**: 2026-01-18
**Author**: AliciBlog Skills Team
**Changelog**: 详见 `/blueprint/CHANGELOG.md`

---

*发现 Claude 犯错或系统问题时，立即添加到「不要做的事」章节并更新相关 Skills 规范*
