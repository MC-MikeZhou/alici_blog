# AliciBlog 统一决策文档 (历史)

> 最后更新：2025-01-14
> 版本：2.0
> 状态：历史决策记录 - 当前架构见 [01-ARCHITECTURE.md](./01-ARCHITECTURE.md)

---

## 零、架构决策摘要 (2025-01-14)

**核心决策：合并为单一系统，SAMBlog 归档**

```
┌─────────────────────────────────────────────────────────────────┐
│                   AliciBlog 统一架构 (v2.0)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              输入层 (手动触发)                           │   │
│  │  URL 抓取 | Notion Public | Text 文件 | Topic Brief     │   │
│  └─────────────────────────┬───────────────────────────────┘   │
│                            ↓                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              处理层 (Agent 自主闭环)                     │   │
│  │  scout → writer → analyzer ⟷ improver (≥75分自动通过)   │   │
│  └─────────────────────────┬───────────────────────────────┘   │
│                            ↓                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              输出层 (手动确认)                           │   │
│  │  中文预览 → 人工审核 → Framer CMS JSON → 发布           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 层级 | 自动化 | 人工参与 |
|------|--------|---------|
| 输入层 | 手动触发 | 选择输入源 |
| 处理层 | Agent 自主 | 仅 3 轮后仍 <75 分时介入 |
| 输出层 | 手动确认 | 中文预览 + 发布确认 |

---

## 一、核心背景约束 (Must-Know)

### 1.1 Framer CMS 输出要求 (P0)

**AliciBlog 的最终输出必须是 Framer CMS 兼容的 JSON 格式**

- alici.ai 官网静态页和 Blog 系统建立在 [Framer](https://www.framer.com/) 之上
- 无论使用哪条工作流，最终都需要生成 `./output/${title}_${时间戳}_output.json`
- JSON 格式参考：`blog_new_sam 11.20.2025/doc/blog.json`

**关键字段结构**：
```json
{
  "slug": "url-friendly-path",
  "title": "Article Title",
  "TLNR": "AEO-focused summary with keywords",
  "sub_title": "Subtitle",
  "cover": "https://...",
  "cover_alt": "SEO-friendly alt text",
  "date": "YYYY-MM-DD",
  "main_category": "news|tutorial|list",
  "read_time": "X",
  "CTA_alici_link": "https://app.alici.ai/...",
  "CTA_button": "Try It NOW",
  "article_body_content": "<Framer CMS HTML format>",
  "meta_title": "SEO Title",
  "meta_description": "SEO Description",
  "tag_for_SEO": "keyword1, keyword2, keyword3"
}
```

### 1.2 半自动化定位

**当前阶段：人工审核不可省略**

工作流中以下节点必须保留人工参与：
| 节点 | 原因 |
|------|------|
| HIP-2: 选题筛选 | 业务判断需要人工 |
| HIP-3: 中文预览审核 | 内容方向确认 |
| HIP-5: 发布确认 | 最终质量把关 |

### 1.3 Notion 中间件价值

**Notion 作为素材来源的优势**：

1. **Web Clipper 一键采集** - 快速收集竞品内容、案例素材
2. **团队协作** - 多人可同时编辑和标注
3. **稳定抓取** - 避免直接 URL 抓取失败的问题
4. **版本管理** - 保留素材修改历史

**使用场景**：
- 直接 URL 无法抓取时的备选方案
- 需要多人协作整理的复杂素材
- 需要 double-check 的重要内容

---

## 二、统一工作流 (v2.0)

### 2.1 SAMBlog 归档说明

**决策：SAMBlog 归档，Skills System 成为唯一系统**

| 组件 | 处置方式 |
|------|---------|
| `blog_new_sam 11.20.2025/` | 归档，不再维护 |
| 内容规范文档 (3份) | 继续作为 Source of Truth |
| Framer JSON 格式 | 迁移到 Skills System |
| FAL.ai 图片生成 | 后续迁移 |

### 2.2 输入层支持

Skills System 现在支持多种输入源：

| 输入源 | 场景 | 优先级 |
|--------|------|--------|
| **URL 直接抓取** | 主要路径 | P0 |
| **Notion Public URL** | URL 抓取失败 / 用户主动选择 | P1 |
| **Text 文件** | 已有素材输入 | P1 |
| **Topic Brief** | growth-topic-scout 输出 | P0 |

### 2.3 内容规范来源

```
blog_new_sam 11.20.2025/doc/  (Source of Truth)
├── 4_Tutorial类内容规范.md
├── 5_List类内容规范.md
├── 6_News类内容规范.md
└── blog.json                ← Framer JSON 模板
```

**注意**：内容规范仍在 SAMBlog 目录下，作为单一来源。Skills System 通过引用使用。

---

## 三、内容规范差异分析

### 3.1 一致性 (无冲突)

以下方面两条工作流**完全一致**：

| 维度 | 规范内容 |
|------|---------|
| **Tutorial 字数** | 1,800-2,500 词 |
| **List 字数** | 2,000-3,000 词 |
| **News 字数** | 1,200-1,800 词 |
| **品牌语气** | 专业、友好、实用、自信、以用户为中心 |
| **避免用词** | "revolutionary", "game-changing" 等 |
| **SEO 关键词密度** | 1-2% |
| **结构要求** | Introduction → Main Body → Conclusion → FAQ |

### 3.2 Skills System 增强部分

Skills System 在原有规范基础上**新增**了以下内容：

| 增强项 | 描述 | SAMBlog 等效 |
|--------|------|-------------|
| **AEO 开篇** | 前 50 词必须包含直接答案 | 无强制要求 |
| **FAQ 章节** | 3-5 个独立可引用的问答 | 可选 |
| **product_mapping** | 自动匹配产品 CTA | 手动填写 `CTA_alici_link` |
| **Pro Tip 格式** | Callout 块格式 | 无统一格式 |

### 3.3 SAMBlog 独有部分

SAMBlog 包含 Skills System **暂未集成**的内容：

| 独有项 | 描述 | 是否需要迁移 |
|--------|------|-------------|
| **图片生成流程** | FAL.ai API + rsync 上传 | 建议后续集成 |
| **JSON 格式规范** | Framer CMS 兼容的 HTML | **必须** - 新链需增加转换步骤 |
| **中文预览流程** | `./chinese_preview.html` 输出 | 已有 chinese-previewer skill |

### 3.4 需要同步的规范更新

如果更新内容规范，以下文件需要**同步修改**：

**原始规范 (Source of Truth)**:
- `blog_new_sam 11.20.2025/doc/4_Tutorial类内容规范.md`
- `blog_new_sam 11.20.2025/doc/5_List类内容规范.md`
- `blog_new_sam 11.20.2025/doc/6_News类内容规范.md`

**Skills 引用 (需同步)**:
- `skills/writers/blog-tutorial-writer/SKILL.md`
- `skills/writers/blog-list-writer/SKILL.md`
- (待创建) `skills/writers/blog-news-writer/SKILL.md`

---

## 四、实施路线图

### Phase 1: 输出层统一 (P0 - 进行中)

**目标**：Skills System 直接输出 Framer CMS JSON

**任务**：
- [ ] 创建 `markdown-to-framer` skill
- [ ] 从 `blog.json` 提取字段映射规则
- [ ] 支持 `article_body_content` 的 HTML 格式转换

### Phase 2: 输入层扩展 (P1)

**目标**：支持 Notion Public URL 作为输入源

**任务**：
- [ ] 更新 blog-writer 支持 Notion URL
- [ ] 处理 Notion 特有的图片 URL 格式
- [ ] 添加 Text 文件输入支持

### Phase 3: 处理层门禁 (P2)

**目标**：选题验证阶段增加 75 分门禁

**任务**：
- [ ] growth-topic-scout 输出评分
- [ ] 低于 75 分的选题自动建议调整

### Phase 4: 图片能力迁移 (P3)

**目标**：将 FAL.ai 图片生成迁移到 Skills System

**任务**：
- [ ] 封装 FAL.ai 调用为 skill
- [ ] 集成 rsync 上传逻辑

---

## 五、文件索引

### 5.1 项目结构

```
/Users/H/Documents/AliciBlog/
├── .claude/
│   └── skills/
│       ├── _shared/
│       │   ├── growth-topic-scout/   # 选题发现
│       │   ├── aeo-analyzer/         # AEO 评分
│       │   ├── auto-improver/        # 自动改进
│       │   └── PRODUCT_CATALOG.md    # 产品-关键词映射
│       └── blog/
│           ├── blog-tutorial-writer/ # Tutorial 生成
│           ├── blog-list-writer/     # List 生成
│           └── chinese-previewer/    # 中文预览
├── blog_new_sam 11.20.2025/          # SAMBlog 原始链
│   ├── doc/
│   │   ├── 4_Tutorial类内容规范.md   # 共享规范
│   │   ├── 5_List类内容规范.md       # 共享规范
│   │   ├── 6_News类内容规范.md       # 共享规范
│   │   └── blog.json                 # Framer JSON 模板
│   ├── input/                        # 素材输入
│   ├── output/                       # JSON 输出
│   └── readme.txt                    # SAMBlog 使用说明
├── blueprint/
│   ├── 00-ARCHITECTURE.md            # 本文档
│   ├── 01-OVERVIEW.md                # 项目概述
│   └── 02-SKILLS.md                  # Skills 清单
└── aeo-analyzer-skill/               # AEO 评分器详细规范
```

### 5.2 快速跳转

| 需求 | 文件 |
|------|------|
| 了解项目全貌 | `blueprint/00-ARCHITECTURE.md` (本文档) |
| 使用 SAMBlog | `blog_new_sam 11.20.2025/readme.txt` |
| 查看产品映射 | `skills/_docs/PRODUCT_CATALOG.md` |
| 内容规范 (Tutorial) | `blog_new_sam 11.20.2025/doc/4_Tutorial类内容规范.md` |
| 内容规范 (List) | `blog_new_sam 11.20.2025/doc/5_List类内容规范.md` |
| 内容规范 (News) | `blog_new_sam 11.20.2025/doc/6_News类内容规范.md` |
| Framer JSON 格式 | `blog_new_sam 11.20.2025/doc/blog.json` |

---

## 六、决策日志

### 2025-01-14: 双工作流架构确认

**背景**：
- SAMBlog (Notion 输入) 和 Skills System (Topic Brief 输入) 并行存在
- 用户需要了解两者关系和使用场景

**决策**：
- 保持双工作流并行，服务不同场景
- 共享内容规范，避免重复维护
- Skills System 新增 AEO 闭环和产品 CTA 自动化
- 后续集成 Framer JSON 转换能力

**待办**：
- [ ] 创建 markdown-to-framer converter
- [ ] 集成图片生成能力到 Skills System
- [ ] 统一内容规范的引用机制

---

## 七、常见问题

### Q1: 两条工作流产出的内容质量一样吗？

**答**：内容结构和规范一致（共用规范文档），但 Skills System 多了：
- AEO 评分保障 (≥75 分)
- 自动产品 CTA 匹配
- Agent 自我改进闘环

### Q2: Notion 素材还需要用吗？

**答**：是的，以下场景仍推荐使用 Notion：
- 直接 URL 抓取失败时
- 需要团队协作整理的素材
- 需要版本管理的重要内容

### Q3: 如何选择使用哪条工作流？

**答**：简单决策树：
```
有现成 Notion 素材？ → 是 → SAMBlog
                     → 否 → 需要 AEO 评分闭环？ → 是 → Skills System
                                              → 否 → 紧急/简单内容？ → 是 → SAMBlog
                                                                   → 否 → Skills System
```

### Q4: 更新规范时需要改几个文件？

**答**：
- 原始规范：`blog_new_sam 11.20.2025/doc/` 下的 3 个 MD 文件
- Skills 引用：对应的 `SKILL.md` 文件（如有硬编码的规范内容）
- 建议：在 Skills 中通过相对路径引用原始规范，避免重复维护
