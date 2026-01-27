# Editor Skill v2.9 Package

> 可直接装入 Claude Code 使用的 Editor Skill 完整包

## 版本信息

- **版本**: v2.9.3
- **发布日期**: 2026-01-22
- **来源**: AliciBlog 项目

## 包含文件

```
editor-skill-package/
├── SKILL.md                           # 核心规范文件 (v2.9.3)
├── README.md                          # 本说明文件
└── prompts/
    ├── title-formulas.yaml            # 37 种标题公式
    ├── opening-patterns.yaml          # 24 种 AEO 开篇模式
    ├── integration-levels.yaml        # L1-L20 产品植入层级
    ├── citation-pyramid.yaml          # 5 层引用权威金字塔
    ├── link-parameter-rules.yaml      # 产品链接参数规则
    ├── format-suggestions.yaml        # 格式建议规则
    └── image-prompt-templates.yaml    # ICSB 图片 Prompt 模板
```

## 安装方法

### 方法一：完整安装（推荐）

将整个 `editor-skill-package/` 目录复制到你的 Claude Code 项目：

```bash
cp -r editor-skill-package/ /your-project/.claude/skills/_shared/editor/
```

### 方法二：手动安装

1. 将 `SKILL.md` 复制到 `/.claude/skills/_shared/editor/SKILL.md`
2. 将 `prompts/` 目录复制到 `/.claude/skills/_shared/editor/prompts/`

## 依赖文件

Editor Skill 运行需要以下外部依赖文件（需自行创建）：

| 文件 | 路径 | 用途 |
|------|------|------|
| BRAND_VISUAL_GUIDE.md | `/.claude/skills/_shared/` | 品牌视觉规范 |
| PRODUCT_CATALOG.md | `/.claude/skills/_shared/` | 产品目录和 CTA 映射 |
| BLOG_CONTENT_REGISTRY.md | `/.claude/skills/_shared/` | 内部链接索引 |

## 触发词

以下关键词会激活 Editor Skill：

- `edit article`
- `fill images`
- `optimize opening`
- `enhance AEO`
- `check E-E-A-T`
- `add internal links`

## 核心功能

### 10 个功能模块

| 模块 | 功能 | 版本 |
|------|------|------|
| Module 1 | Strategic Image Selection | v2.0 |
| Module 2 | ICSB Prompt Engineering | v2.2 |
| Module 3 | Opening Enhancement + AEO | v2.9.1 |
| Module 4 | AEO Summary Enhancement | v2.0 |
| Module 5 | Format + Title + Integration | v2.9.1 |
| Module 6 | E-E-A-T Depth Check | v2.9 |
| Module 7 | Version Inheritance Check | v2.4 |
| Module 8 | Internal Linking | v2.7 |
| Module 9 | CTA Enforcement | v2.9.1 |
| Module 10 | Writer Feedback Loop | v2.9.2 |

### v2.9.1 四项强制规则

| 规则 | 严重级别 | 说明 |
|------|----------|------|
| 标题年份 | BLOCKING | 标题必须包含 2026/2027 |
| Key Takeaways | BLOCKING | 必须在正文前展示要点 |
| Data Hook | WARNING | 开篇 150 词内必须有数据 |
| CTA Card | BLOCKING | 文末必须有 CTA 卡片 |

## YAML 配置文件说明

### title-formulas.yaml

37 种标题公式，按内容类型分类：
- Listicle (12 种)
- How-to (8 种)
- Comparison (4 种)
- Statistics (5 种)
- Guide (4 种)
- Vertical (4 种)

### opening-patterns.yaml

24 种 AEO 开篇模式：
- P1-P4: 经典模式
- P5-P8: How-to 模式
- P9-P11: Listicle 模式
- P12-P13: 统计/研究模式
- P14-P18: Guide 模式
- P19-P24: 高级模式

### integration-levels.yaml

L1-L20 产品植入层级：
- L1-L5: 基础植入（适用于 News/Statistics）
- L6-L10: 进阶植入（适用于 Tutorial/Listicle）
- L11-L15: 战略植入（适用于 Guide/Trends）
- L16-L20: 专家植入（适用于 Vertical/Philosophy）

### citation-pyramid.yaml

5 层引用权威金字塔：
- Level 1: 官方平台数据 (weight: 5)
- Level 2: 研究机构报告 (weight: 4)
- Level 3: 行业媒体 (weight: 3)
- Level 4: 工具厂商研究 (weight: 2)
- Level 5: 用户评价平台 (weight: 1)

## 使用示例

```bash
# 在 Claude Code 中
/edit-article /reports/2026-01-23-my-article/01-article-draft.md
```

## 输出文件

Editor 会生成以下输出：

```
/reports/{date}-{slug}/
├── 01-article-edited.md      # 编辑后的文章
└── 04-editor-report.md       # 编辑报告（含所有模块状态）
```

## 更多信息

详细规范请参阅 `SKILL.md` 文件。

---

*Editor Skill v2.9.3 - AliciBlog 项目*
