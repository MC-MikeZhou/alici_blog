# Editor Skill v2.9 能力总览

> **版本**: v2.9.3
> **最后更新**: 2026-01-23
> **文档用途**: 供团队成员了解 Editor Skill 的完整能力和使用方式

---

## 核心定位

Editor Skill 是 AliciBlog 内容生产流水线的**质量门禁**，负责：
- 战略性图片生成与品牌一致性
- AEO（AI Engine Optimization）优化
- E-E-A-T 内容深度验证
- 版本继承保护
- 内部链接网络构建
- CTA 强制执行

**核心理念**: 少即是多（Less is More）— 3 张高质量图片胜过 10 张平庸图片。

---

## 核心评估维度

### AEO（AI Engine Optimization）

优化文章以适应 AI 搜索引擎（Perplexity、Google AI Overview）抓取：

| 元素 | 要求 |
|------|------|
| 直接回答 | 前 60 词可独立提取作为答案 |
| 数据点 | 包含具体数字（价格、评分、数量） |
| FAQ 回答 | 每个答案是独立段落 |
| 列表结构 | 使用编号列表便于解析 |
| 实体提及 | 品牌/产品名称一致性 |

### E-E-A-T（Experience, Expertise, Authority, Trust）

| 维度 | 检查项 | 评分标准 |
|------|--------|----------|
| **Experience** | 原创案例 ≥2、第一人称叙述、迭代示例 | A-D + BLOCKING |
| **Expertise** | 命名作者、具体 Bio、可验证 URL | A-D + BLOCKING |
| **Authority** | 数据来源标注、引用权威等级 | A-D + BLOCKING |
| **Trust** | 产品声明准确、时效性标注、利益披露 | A-D + BLOCKING |

---

## 8 个功能模块

### Module 1: Strategic Image Selection
**目的**: 选择 3-5 个战略位置生成高质量图片

| 文章类型 | 最少 | 最多 | 推荐 |
|----------|------|------|------|
| Tutorial | 2 | 4 | 3 |
| List | 3 | 5 | 4 |
| News | 1 | 3 | 2 |

**战略位置**:
```
Article Position:  0%          33%          66%          100%
                   ↓           ↓            ↓            ↓
                   Hero        Concept      Comparison   CTA/Summary
                   Cover       Diagram      Visual       (optional)
                   (REQUIRED)  (RECOMMENDED) (RECOMMENDED)
```

### Module 2: ICSB Prompt Engineering
**框架**: Image Type → Content → Style → Brand Layer

- **I** - Image Type: 指定格式（infographic、product shot、diagram）
- **C** - Content: 定义 3-5 个信息元素及关系
- **S** - Style: 描述视觉美学和技术参数
- **B** - Brand Layer: 应用 alici.ai 视觉规范（绿色为主、极简、符号化）

**品牌规范**:
- ✅ 绿色渐变（深翠绿 → 薄荷绿 → 浅绿）
- ✅ 40%+ 负空间
- ✅ 单一清晰焦点
- ❌ 禁止蓝紫色调
- ❌ 禁止拥挤布局

### Module 3: Opening Enhancement + AEO Patterns
**v2.9.1 强制规则**:

| 规则 | 严重级别 | 处理方式 |
|------|----------|----------|
| Key Takeaways 前置 | ⛔ BLOCKING | 自动生成/移动 |
| Data Hook 开篇 | ⚠️ WARNING | 自动重写 |
| 弱开篇模式检测 | ⚠️ WARNING | 自动替换 |

**24 种 AEO 开篇模式** (基于 Invideo 竞品研究)：
- Problem-Solution (P1)
- Data Hook (P2) - 优先
- Pain Point Question (P3)
- Reframe (P4)
- 等等...

### Module 4: AEO Summary Enhancement
- 首 60 词可提取为独立答案
- 数据点（价格、评分、数量）
- FAQ 自包含段落
- 编号列表结构
- 实体名称一致性

### Module 5: Format Evolution + Title Formula + Integration Level
**v2.9.1 强制规则**:

| 规则 | 严重级别 | 处理方式 |
|------|----------|----------|
| 标题年份 (2026/2027) | ⛔ BLOCKING | 自动添加 |
| 37 种标题公式验证 | ⚠️ WARNING | 建议修改 |
| L1-L20 植入层级检测 | ⚠️ WARNING | 自动添加 CTA |

**文章类型目标层级**:
| 类型 | 目标 | 最低 |
|------|------|------|
| News | L2-L3 | L2+ |
| Statistics | L3-L5 | L3+ |
| Listicle | L5-L10 | L5+ |
| Tutorial | L5-L10 | L5+ |
| Guide | L10-L15 | L10+ |

### Module 6: E-E-A-T Depth Check
详见 [E-E-A-T 强化指南](./eeat-optimization-guide.md)

**5 层引用权威金字塔**:
| Level | 权威度 | 来源示例 | 权重 |
|-------|--------|----------|------|
| L1 | 最高 | YouTube Press, OpenAI Blog | 5 |
| L2 | 很高 | Statista, Gartner, Wyzowl | 4 |
| L3 | 高 | TechCrunch, AdWeek | 3 |
| L4 | 中 | Wistia, Ahrefs Blog | 2 |
| L5 | 补充 | G2, Capterra | 1 |

### Module 7: Version Inheritance Check
详见 [版本管理标准](./content-version-standard.md)

**受保护内容**:
- Author Information
- Case Studies
- Testing Data (n=X)
- External Sources
- Disclosure
- FAQ Section
- Citable Blocks

### Module 8: Internal Linking
详见 [内部链接指南](./internal-linking-guide.md)

**链接规范**:
| 链接方向 | 数量 | 位置 |
|----------|------|------|
| Cluster → Pillar | 1-2 | 导言/结论 |
| Cluster ↔ Cluster | 2-3 | 相关章节 |
| Article → Product | 1-2 | CTA 位置 |

---

## 协作流程

### v1.0 → v2.0 → v3.0 版本演化

```
v1.0 draft (Writer 输出)
    ↓ Editor Skill (图片 + 优化 + 验证)
v1.0 edited
    ↓ AEO Analyzer (评分)
    ↓ Auto-Improver (若 <75 分)
v1.1 improved ← E-E-A-T 投资
    ↓ Writer v2.x 重写 (继承 E-E-A-T)
v2.0 (框架更新 + E-E-A-T 保留)
    ↓ Editor Module 7 (验证继承)
v2.0 edited ← PASS ✅
```

### SmartLauncher v1.2 集成

```
SmartLauncher Phase 3:
├── Step 3: Editor Gate (⛔ 强制)
│   └── 所有 Writer 必须经过 Editor
│       └── BLOCKING 且无法自动修复?
│           └── YES → Step 3.5 (Writer Feedback Loop)
└── Step 3.5: Writer Feedback Loop
    ├── Editor Module 10 生成反馈
    ├── Writer 重写
    └── 返回 Step 3
```

---

## 触发词与使用方式

### 触发词

```
edit article, fill images, optimize opening, enhance AEO, check E-E-A-T, add internal links
```

### 命令调用

```bash
/edit-article /reports/2026-01-20-topic/01-article-draft.md
```

### 输入

- `01-article-draft.md` 或 `01-article-v*.md`
- 可选: `asset_plan.json` (Asset Pack Mode)

### 输出

```
/reports/YYYY-MM-DD-topic/
├── 01-article-edited.md     # 编辑后版本
├── 04-editor-report.md      # 编辑报告 (含所有模块状态)
├── asset_manifest.json      # 资产清单 (Asset Pack Mode)
└── prompts_used.md          # 使用的 Prompts (Asset Pack Mode)
```

---

## 必需依赖文档

| 文档 | 路径 | 用途 |
|------|------|------|
| BRAND_VISUAL_GUIDE.md | `/.claude/skills/_shared/` | ICSB Brand Layer |
| PRODUCT_CATALOG.md | `/.claude/skills/_shared/` | CTA URL 映射 |
| BLOG_CONTENT_REGISTRY.md | `/.claude/skills/_shared/` | 内部链接索引 |
| title-formulas.yaml | `/.claude/skills/_shared/editor/prompts/` | 37 种标题公式 |
| opening-patterns.yaml | `/.claude/skills/_shared/editor/prompts/` | 24 种开篇模式 |
| integration-levels.yaml | `/.claude/skills/_shared/editor/prompts/` | L1-L20 植入层级 |
| citation-pyramid.yaml | `/.claude/skills/_shared/editor/prompts/` | 引用权威金字塔 |
| link-parameter-rules.yaml | `/.claude/skills/_shared/editor/prompts/` | 产品链接参数规则 |

---

## 版本历史

| 版本 | 日期 | 主要更新 |
|------|------|----------|
| v2.9.3 | 2026-01-22 | 产品链接参数规则 |
| v2.9.2 | 2026-01-22 | Module 10 Writer Feedback Loop |
| v2.9.1 | 2026-01-22 | 4 项强制规则 (Key Takeaways/Data Hook/年份/CTA) |
| v2.9 | 2026-01-22 | Invideo 竞品 Review 集成 |
| v2.7 | 2026-01-21 | Module 8 Internal Linking |
| v2.6 | 2026-01-20 | Asset Pack Mode |
| v2.4 | 2026-01-18 | Module 7 Version Inheritance |
| v2.3 | 2026-01-17 | Module 6 E-E-A-T Depth Check |

---

*文档维护: Editor Skill v2.9.3 | 最后同步: 2026-01-23*
