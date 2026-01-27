# AliciBlog 全自动内容生产架构 (Auto-Pilot Mode)

> **版本**: 1.0
> **设计日期**: 2026-01-17
> **目标**: 实现从 URL 输入到内容发布的近乎全自动流程，人工介入降至最低

---

## 一、核心设计理念

### 1.1 设计哲学

```
传统模式: 人工主导，AI 辅助
        ↓
Auto-Pilot: AI 主导，人工监督（可选）
```

**关键原则**:
1. **默认自动化**: 所有环节默认自动执行，除非明确需要人工确认
2. **智能超时**: 设置合理等待窗口，超时后自动继续
3. **可追溯性**: 所有自动决策都有日志和理由，方便事后审计
4. **容错机制**: 自动决策失败时降级为人工确认，而非中断流程

### 1.2 人工介入点分级

| 级别 | 说明 | 超时策略 | 应用场景 |
|------|------|----------|----------|
| **L0: 完全自动** | 无需人工确认 | N/A | 格式转换、文件生成、评分 |
| **L1: 可选确认** | 可确认，可跳过 | 3 分钟自动继续 | 选题确认、产品推荐 |
| **L2: 建议确认** | 强烈建议确认 | 5 分钟自动继续 | 首次发布新类型内容 |
| **L3: 必须确认** | 必须人工批准 | 无限等待 | 品牌敏感内容、法律合规 |

---

## 二、完整流程架构

### 2.1 流程总览

```
┌─────────────────────────────────────────────────────────────┐
│                   Auto-Pilot Workflow                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [INPUT] URL                                                │
│      ↓                                                       │
│  Phase 1: Topic Scout (L0 - 完全自动)                        │
│      ├─ 竞品分析                                             │
│      ├─ 生成 Top 10 选题                                     │
│      └─ 自动评分 (营销导向 + 产品契合 + Opportunity)          │
│      ↓                                                       │
│  Phase 2: Topic Selection (L1 - 可选确认)                    │
│      ├─ 检查: 是否满足自动确认条件？                          │
│      │   ├─ YES → 自动选择最高分                             │
│      │   └─ NO → 等待 3 分钟 → 超时自动选择                   │
│      └─ 输出: 选中的 Topic Brief                             │
│      ↓                                                       │
│  Phase 3: Content Generation (L0 - 完全自动)                 │
│      ├─ 应用 blog-list-writer v2.0                          │
│      ├─ 融入 alici.ai 产品 (自动匹配)                        │
│      └─ 输出: 完整文章 Markdown                              │
│      ↓                                                       │
│  Phase 4: Quality Loop (L0 - 完全自动)                       │
│      ├─ AEO 评分                                             │
│      ├─ < 75? → auto-improver (最多 3 轮)                    │
│      ├─ >= 75? → 通过                                        │
│      └─ 3 轮后仍 < 75? → 标记 MANUAL_REVIEW                  │
│      ↓                                                       │
│  Phase 5: Visual Assets (L0 - 完全自动)                      │
│      ├─ 生成 Hero 封面图                                     │
│      ├─ 生成 1-2 张辅助图 (可选)                             │
│      └─ 上传到 CDN (失败则本地预览)                          │
│      ↓                                                       │
│  Phase 6: Export & Preview (L0 - 完全自动)                   │
│      ├─ 转换为 Framer JSON                                   │
│      ├─ 生成 HTML 预览                                       │
│      └─ 输出: 可发布资产                                     │
│      ↓                                                       │
│  Phase 7: Publish Decision (L2 - 建议确认)                   │
│      ├─ AEO >= 80? → 自动建议发布                           │
│      ├─ 等待 5 分钟用户确认                                  │
│      └─ 超时 → 保存草稿，通知用户审核                        │
│      ↓                                                       │
│  [OUTPUT] 已发布文章 / 草稿待审核                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 各阶段详细设计

#### Phase 1: Topic Scout (完全自动)

**输入**: 竞品 URL
**输出**: Top 10 选题 + Opportunity Score

**自动化决策**:
```python
def topic_scout(competitor_url):
    # 1. 抓取竞品内容
    content = web_fetch(competitor_url)

    # 2. 生成选题种子
    topics = generate_topic_seeds(content)  # 20-60 个

    # 3. 市场验证 (DataForSEO / WebSearch)
    validated_topics = []
    for topic in topics:
        score = calculate_opportunity_score(topic)
        validated_topics.append((topic, score))

    # 4. 排序并返回 Top 10
    return sorted(validated_topics, key=lambda x: x[1], reverse=True)[:10]
```

**无人工介入**: 此阶段纯数据处理，无需等待

---

#### Phase 2: Topic Selection (可选确认 - 3 分钟超时)

**输入**: Top 10 选题
**输出**: 选中的 Topic Brief

**自动确认条件**:
```python
def should_auto_select(topic, user_guidance):
    # 读取 BLOG_WRITING_PRINCIPLES.md
    principles = load_principles()

    # 评分维度
    marketing_score = evaluate_marketing_orientation(topic)  # 1-10
    product_fit = evaluate_product_fit(topic)                # 1-10
    opportunity = topic.opportunity_score                    # 0-100

    # 自动确认条件
    if (
        marketing_score >= 7
        and product_fit >= 7
        and opportunity >= 60
    ):
        return True, "High-score marketing topic"

    if user_guidance and matches_guidance(topic, user_guidance):
        return True, "Matches user guidance"

    return False, "Requires confirmation"

# 执行逻辑
auto_select, reason = should_auto_select(top_topic, user_guidance)

if auto_select:
    selected_topic = top_topic
    log(f"Auto-selected: {reason}")
else:
    # 发送确认请求
    send_confirmation_request(user, top_3_topics)

    # 等待 3 分钟
    response = wait_for_response(timeout=180)

    if response:
        selected_topic = response.selected
    else:
        # 超时自动选择
        selected_topic = top_topic
        log("Timeout: auto-selected highest-score topic")
```

**用户通知方式**:
- Slack/Email: "选题已生成，3 分钟内回复可修改，否则自动选择 Top 1"
- CLI: 显示倒计时 "Waiting for confirmation... 2:47 remaining"

---

#### Phase 3: Content Generation (完全自动)

**输入**: Topic Brief
**输出**: 完整文章 Markdown

**自动化逻辑**:
```python
def generate_content(topic_brief):
    # 1. 读取写作原则
    principles = load_blog_writing_principles()

    # 2. 自动匹配 alici.ai 产品
    products = auto_match_products(topic_brief.keywords)
    # 返回: [("image_studio", position=3), ("video_studio", position=7)]

    # 3. 调用 blog-list-writer v2.0
    article = blog_list_writer.generate(
        topic_brief=topic_brief,
        alici_products=products,
        positioning=principles.positioning_strategy,
        word_count_target=3000
    )

    return article
```

**无人工介入**: 完全基于 Topic Brief 和 BLOG_WRITING_PRINCIPLES.md 自动生成

---

#### Phase 4: Quality Loop (完全自动 + 自动改进)

**输入**: 文章 Markdown
**输出**: AEO 评分 + 改进版文章 (如需)

**自动改进循环**:
```python
def quality_assurance(article, target_score=75):
    max_rounds = 3

    for round in range(1, max_rounds + 1):
        # AEO 评分
        score = aeo_analyzer.evaluate(article)

        if score.total >= target_score:
            log(f"✅ Pass: {score.total}/100 (Round {round})")
            return article, score, "APPROVED"

        # 自动改进
        log(f"⚠️ Score: {score.total}/100 < {target_score}, improving...")
        article = auto_improver.improve(article, score.recommendations)

    # 3 轮后仍不达标
    final_score = aeo_analyzer.evaluate(article)
    if final_score.total < target_score:
        return article, final_score, "MANUAL_REVIEW_REQUIRED"

    return article, final_score, "APPROVED"
```

**自动改进策略**:
- Round 1: 修复明显问题 (缺少 FAQ, 开篇不直接)
- Round 2: 增强 E-E-A-T (添加引用, 完善作者信息)
- Round 3: 优化结构 (调整段落长度, 增加 Citable Blocks)

**人工介入点**:
- 仅当 3 轮后仍 < target_score 时，标记 MANUAL_REVIEW
- 用户收到通知: "Article needs manual review (Score: 72/100)"

---

#### Phase 5: Visual Assets (完全自动 + 容错)

**输入**: 文章内容
**输出**: 生成的图片 + CDN URLs

**自动生成策略**:
```python
def generate_visual_assets(article):
    # 根据 Editor Skill v2.2 "Less is More" 原则
    # 只生成 1-3 张战略性图片

    images_needed = []

    # 1. Hero 封面图 (必须)
    hero_prompt = generate_hero_prompt(article.title, article.category)
    images_needed.append(("hero", hero_prompt, "2K"))

    # 2. 概念图 (可选 - 仅当文章有复杂概念)
    if has_complex_concepts(article):
        concept_prompt = generate_concept_prompt(article.key_concepts)
        images_needed.append(("concept", concept_prompt, "1K"))

    # 3. 对比图 (可选 - 仅当有对比表格)
    if has_comparison_table(article):
        comparison_prompt = generate_comparison_prompt(article.comparison)
        images_needed.append(("comparison", comparison_prompt, "1K"))

    # 并行生成
    images = parallel_generate(images_needed)

    # 尝试上传 CDN
    cdn_urls = []
    for image in images:
        try:
            url = upload_to_cdn(image)
            cdn_urls.append(url)
        except CDNError:
            # 容错: CDN 失败则使用本地路径
            local_url = f"file://{image.local_path}"
            cdn_urls.append(local_url)
            log(f"⚠️ CDN upload failed, using local: {local_url}")

    return cdn_urls
```

**容错机制**:
- CDN 上传失败 → 使用本地 file:// 路径生成预览
- 图片生成失败 → 使用占位符继续流程
- 不因图片问题中断整体流程

---

#### Phase 6: Export & Preview (完全自动)

**输入**: 文章 + 图片
**输出**: Framer JSON + HTML 预览

**自动流程**:
```python
def export_and_preview(article, images):
    # 1. 插入图片 URLs
    article_with_images = insert_images(article, images)

    # 2. 转换为 Framer JSON
    framer_json = markdown_to_framer.convert(article_with_images)

    # 3. 验证 JSON
    validation = validate_framer_json(framer_json)
    if not validation.passed:
        # 自动修复
        framer_json = auto_fix_json(framer_json, validation.errors)

    # 4. 生成 HTML 预览
    preview_html = framer_previewer.generate(article_with_images)

    return {
        "json": framer_json,
        "preview": preview_html,
        "summary": {
            "word_count": count_words(article),
            "aeo_score": article.aeo_score,
            "images": len(images),
            "ready_to_publish": True
        }
    }
```

**无人工介入**: 完全自动化

---

#### Phase 7: Publish Decision (建议确认 - 5 分钟超时)

**输入**: 最终文章资产
**输出**: 发布 / 保存草稿

**自动决策逻辑**:
```python
def decide_publish(article_assets):
    # 检查质量门禁
    if article_assets.aeo_score >= 80:
        auto_publish = True
        recommendation = "RECOMMENDED_PUBLISH"
    elif article_assets.aeo_score >= 75:
        auto_publish = False
        recommendation = "SUGGEST_REVIEW"
    else:
        auto_publish = False
        recommendation = "MANUAL_REVIEW_REQUIRED"

    if auto_publish:
        # 发送确认请求
        send_publish_confirmation(user, article_assets.preview_url)

        # 等待 5 分钟
        response = wait_for_response(timeout=300)

        if response and response.action == "publish":
            return publish_to_framer(article_assets)
        elif response and response.action == "reject":
            return save_as_draft(article_assets, "User rejected")
        else:
            # 超时 → 保存草稿 + 通知
            draft = save_as_draft(article_assets, "Timeout, awaiting review")
            notify_user(f"Article saved as draft: {draft.url}")
            return draft
    else:
        # 不满足自动发布条件，直接保存草稿
        return save_as_draft(article_assets, recommendation)
```

**用户通知**:
```
Subject: 文章已完成，建议发布
Body:
  标题: 15 Best AI Marketing Tools in 2026
  AEO 评分: 88/100 ✅
  字数: 4,296
  预览: [点击查看]

  5 分钟内无回复将自动保存为草稿，等待您审核。

  回复:
  - "publish" 立即发布
  - "draft" 保存草稿
  - "review" 需要修改
```

---

## 三、超时机制详细设计

### 3.1 超时配置表

| 阶段 | 默认超时 | 可配置 | 超时后行为 |
|------|----------|--------|-----------|
| Topic Selection | 3 分钟 | ✅ | 自动选择最高分选题 |
| Publish Decision | 5 分钟 | ✅ | 保存草稿 + 通知 |
| Manual Review | 无限 | ❌ | 等待人工介入 |

### 3.2 超时倒计时显示

**CLI 模式**:
```
⏰ Waiting for topic selection... 2:47 remaining
   Press Enter to confirm, or wait for auto-selection

   Top 3 Topics:
   1. [Score: 78] Best AI Marketing Tools ⭐ Recommended
   2. [Score: 75] AI Marketing Tools for Small Business
   3. [Score: 72] Free AI Marketing Tools
```

**Slack 通知**:
```
🤖 AliciBlog Auto-Pilot

选题已生成，请在 3 分钟内确认:

1️⃣ Best AI Marketing Tools (推荐)
   - 营销导向: 9/10
   - 产品契合: 8/10
   - Opportunity: 78/100

2️⃣ AI Marketing Tools for Small Business
   ...

⏰ 倒计时: 2:45

👉 回复数字选择，或等待自动选择 #1
```

### 3.3 用户配置

允许用户自定义超时行为:

```yaml
# .claude/config/auto-pilot.yml
auto_pilot:
  enabled: true

  timeouts:
    topic_selection: 180  # 3 分钟 (秒)
    publish_decision: 300  # 5 分钟

  auto_behaviors:
    topic_selection_on_timeout: "select_top_1"  # 或 "skip", "notify_only"
    publish_on_timeout: "save_draft"            # 或 "publish", "notify_only"

  quality_gates:
    min_aeo_score: 75
    auto_publish_threshold: 80
    max_improver_rounds: 3
```

---

## 四、知识库架构

### 4.1 核心文档

```
/skills/
├── _docs/
│   ├── BLOG_WRITING_PRINCIPLES.md    # 写作指导原则
│   ├── PRODUCT_CATALOG.md             # 产品映射规则
│   └── BRAND_VISUAL_GUIDE.md          # 品牌视觉规范
└── core/aeo-analyzer/
    ├── EVALUATION_FRAMEWORK.md    # AEO 评分标准
    └── REPORT_TEMPLATE.md         # 报告模板
```

### 4.2 BLOG_WRITING_PRINCIPLES.md 作用

**在流程中的调用点**:

1. **Phase 2 (Topic Selection)**
   ```python
   principles = load_blog_writing_principles()
   auto_confirm = check_auto_confirm_conditions(topic, principles)
   ```

2. **Phase 3 (Content Generation)**
   ```python
   products = principles.auto_match_products(topic.keywords)
   positioning = principles.get_positioning_strategy(topic.category)
   ```

3. **Phase 4 (Quality Loop)**
   ```python
   quality_standards = principles.get_quality_standards()
   if aeo_score < quality_standards.min_score:
       improve()
   ```

**文档更新机制**:
- 每次成功生产后，自动记录决策和结果
- 用户可以手动编辑原则，系统立即生效
- 版本控制: 每次修改自动备份到 `.claude/history/`

---

## 五、实施路线图

### 5.1 Phase 1: 核心自动化 (当前已完成 ✅)

- ✅ Topic Scout 全自动
- ✅ Content Generation 全自动
- ✅ AEO 评分 + auto-improver 循环
- ✅ Visual Assets 生成
- ✅ Framer Export + Preview

### 5.2 Phase 2: 超时机制 (下一步)

**优先级**: P0

**任务清单**:
- [ ] 实现 3 分钟超时选题确认
- [ ] 实现 5 分钟超时发布确认
- [ ] 添加倒计时 CLI 显示
- [ ] 添加 Slack/Email 通知
- [ ] 创建用户配置文件 `auto-pilot.yml`

**预计时间**: 2-3 天

### 5.3 Phase 3: 知识库沉淀 (并行)

**优先级**: P0

**任务清单**:
- ✅ 创建 BLOG_WRITING_PRINCIPLES.md
- [ ] 在各 Skills 中引用 BLOG_WRITING_PRINCIPLES
- [ ] 实现自动学习机制（记录成功案例）
- [ ] 版本控制和备份

**预计时间**: 1-2 天

### 5.4 Phase 4: 批量生产 (长期)

**优先级**: P1

**任务清单**:
- [ ] 支持批量 URL 输入
- [ ] 并行执行多个任务
- [ ] 队列管理和优先级
- [ ] 成本和配额控制

**预计时间**: 1 周

---

## 六、监控与审计

### 6.1 实时监控仪表盘

```
┌─────────────────────────────────────────────────────┐
│          AliciBlog Auto-Pilot Dashboard             │
├─────────────────────────────────────────────────────┤
│                                                     │
│  📊 今日生产统计:                                    │
│  • 文章数: 12                                       │
│  • 成功率: 91.7% (11/12)                           │
│  • 平均 AEO: 84/100                                │
│  • 平均耗时: 16 分钟                                │
│  • 总成本: $3.60                                    │
│                                                     │
│  🔄 当前运行任务:                                    │
│  • Task #1: Best AI Video Tools (Phase 4: 评分中)   │
│  • Task #2: Free AI Image Generators (Phase 2: 等待确认 1:23) │
│                                                     │
│  ⏸️  待审核草稿: 1 篇                               │
│  • "AI Marketing Automation Guide" (AEO: 73/100)   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 6.2 审计日志

每个任务生成完整的决策日志:

```json
{
  "task_id": "2026-01-17-best-ai-marketing-tools",
  "timestamp": "2026-01-17T10:30:00Z",
  "input_url": "https://perfectcorp.com/...",
  "decisions": [
    {
      "phase": "topic_selection",
      "decision": "auto_select",
      "reason": "High-score marketing topic (9/10, 8/10, 78/100)",
      "timeout": false,
      "selected_topic": "Best AI Marketing Tools"
    },
    {
      "phase": "product_matching",
      "decision": "auto_match",
      "matched_products": [
        {"product": "image_studio", "position": 3, "score": 9.5},
        {"product": "video_studio", "position": 7, "score": 9.1},
        {"product": "thumbnail_pro", "position": 12, "score": 9.0}
      ]
    },
    {
      "phase": "quality_loop",
      "aeo_score": 88,
      "improver_rounds": 0,
      "decision": "approved_first_pass"
    },
    {
      "phase": "publish_decision",
      "decision": "timeout_save_draft",
      "timeout": true,
      "wait_duration": 300
    }
  ],
  "final_status": "draft_awaiting_review",
  "metrics": {
    "word_count": 4296,
    "aeo_score": 88,
    "cost": 0.30,
    "duration_seconds": 900
  }
}
```

---

## 七、成功案例回顾

### 案例: Best AI Marketing Tools (2026-01-17)

**用户输入**:
```
URL: https://www.perfectcorp.com/.../best-ai-marketing-tools
方向: "面向营销，吸引品牌客户，强调 Agent 优势"
```

**系统自动执行**:
1. ✅ Topic Scout: 3 分钟，生成 10 个选题
2. ✅ Auto-Select: "Best AI Marketing Tools" (营销导向 9/10, 产品契合 8/10, Opportunity 78/100)
3. ✅ Content Gen: 5 分钟，4,296 词，融入 3 个 alici.ai 产品
4. ✅ AEO 评分: 88/100，首次通过（无需 improver）
5. ✅ 图片生成: 3 分钟，Hero 封面图
6. ✅ 预览生成: 1 分钟

**总耗时**: 15 分钟
**人工介入**: 0 次（用户授权后全自动）
**最终质量**: AEO 88/100

**关键成功因素**:
- 用户提供明确方向 → 系统自动匹配选题
- BLOG_WRITING_PRINCIPLES.md 沉淀了决策逻辑
- v2.0 框架首次 AEO 达标，无需迭代

---

## 八、下一步行动

### 立即执行 (本周)

1. **实现超时机制**
   - [ ] 修改 growth-topic-scout/SKILL.md，添加超时逻辑
   - [ ] 修改 full-workflow command，集成超时等待
   - [ ] 测试超时自动选择功能

2. **完善知识库**
   - [x] 创建 BLOG_WRITING_PRINCIPLES.md
   - [ ] 在各 Skill 中引用该文档
   - [ ] 编写使用说明

3. **创建配置文件**
   - [ ] 添加 `.claude/config/auto-pilot.yml`
   - [ ] 允许用户自定义超时时间
   - [ ] 允许用户配置自动行为

### 中期目标 (本月)

1. **批量生产能力**
   - 支持输入 10 个 URL，自动批量生产
   - 并行执行，成本和时间优化

2. **智能学习**
   - 记录每次成功生产的选题和决策
   - 自动更新 BLOG_WRITING_PRINCIPLES.md

3. **监控仪表盘**
   - 实时显示任务进度
   - 成本和质量统计

---

**结论**: 通过超时机制 + 知识库沉淀，AliciBlog 可以实现从 URL 到发布的近乎全自动流程，人工介入降至最低，大幅提升内容生产效率。
