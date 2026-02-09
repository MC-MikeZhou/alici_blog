# agent-team-scout — Skill 技术规范

```yaml
---
name: agent-team-scout
version: "1.1"
description: >
  多角色 Agent 团队选题研究系统 (CEO Model + Distributed Validation)。
  6-8 个专业 Agent 从不同视角并行探索选题，每个 Agent 自带 DataForSEO 验证。
  Orchestrator 仅做战略决策 (去重、抽查、排序)，不做执行层验证。
  v1.1: Research Charter + Agent 自验证 + Similarity Matrix + Decision Brief + Handoff Pack。
allowed-tools: Task, Read, Write, Glob, Grep, WebSearch, WebFetch, AskUserQuestion
dependencies:
  - skill: growth-topic-scout (v2.4+)
  - mcp: dataforseo
  - docs: PRODUCT_CATALOG.md, BLOG_WRITING_PRINCIPLES_v2.md
status: design-phase
---
```

> **版本**: v1.1 技术规范 (PRD 批判性吸收版)
> **日期**: 2026-02-06
> **状态**: 设计阶段（可直接用于编写 SKILL.md 和 agent 定义文件）
> **受众**: Claude Code（转化为实现）

---

## 触发词

```yaml
triggers:
  zh:
    - "团队研究"
    - "多角色选题"
    - "全景扫描"
    - "团队选题"
  en:
    - "agent team"
    - "team research"
    - "team scout"
    - "multi-perspective"
    - "multi-agent scout"
    - "perspective research"
```

---

## 架构总览

```
agent-team-scout v1.1 (CEO Model)
├── Phase 0: Mission Briefing (Orchestrator)
│   ├── Step 0.1: 种子词输入
│   ├── Step 0.2: 领域分析 (智能分配)
│   ├── Step 0.3: 互动问卷 (3-4 问)
│   └── Step 0.4: 冻结 Research Charter (不可变合同)
│
├── Phase 1: Parallel Exploration + Validation (Subagents)
│   ├── 5-7 个 Task tool 并行调用
│   ├── 每个 subagent 独立研究 + DataForSEO 自验证
│   └── 每个 subagent 返回 agent_output (含 abstract + competitor_map + data_validation)
│
├── Phase 2: CEO Synthesis (Orchestrator — 只决策不执行)
│   ├── Step 2.1: 收集所有 Agent 输出
│   ├── Step 2.2: 语义去重
│   ├── Step 2.3: 共识评分
│   ├── Step 2.4: 证据交叉增强
│   ├── Step 2.5: Similarity Matrix (基于 Abstract 相似度)
│   ├── Step 2.6: Coverage Map (维度覆盖矩阵)
│   └── Step 2.7: 排序 → Top 15-20 (新公式: evidence + consensus + diversity + freshness + brand_fit)
│
├── Phase 3: Supplemental Validation (仅补充 Agent 未验证的数据)
│   ├── Step 3.1: 补充验证 (只验证 Agent 未覆盖的关键词)
│   ├── Step 3.2: Title Lock
│   └── Step 3.3: AEO 评分
│
└── Phase 4: Final Portfolio + Handoff (Orchestrator)
    ├── 02-team-research-report.md
    ├── 03-team-directions.json
    ├── 04-agent-contributions.json
    ├── 05-diversity-analysis.md (含 Similarity Matrix + Coverage Map)
    ├── 06-decision-brief.md          ← NEW
    └── 07-handoff-pack/              ← NEW (Top 1-3 方向的创作包)
```

---

## Phase 0: Mission Briefing (Orchestrator)

### Step 0.1: 种子词输入

接受自然语言或结构化输入：

```
输入格式:
  - 自然语言: "帮我做 AI UGC Ads 领域的团队选题研究"
  - 直接种子词: "team scout AI UGC Ads"
  - 带约束: "团队研究 AI headshots，只关注英文市场"
```

Orchestrator 提取：
- `seed`: 种子词 (必需)
- `language`: 目标语言 (默认 `en`)
- `geo`: 目标地区 (默认 `US`)
- `constraints`: 用户额外约束 (可选)

### Step 0.2: 领域分析 (智能分配)

Orchestrator 使用 WebSearch 分析种子词的领域特征，产出 `domain_profile`：

```json
{
  "seed": "AI UGC Ads",
  "domain_type": ["tech", "marketing"],
  "domain_signals": {
    "has_tools": true,
    "has_brand_angle": true,
    "has_market_data": true,
    "has_technical_depth": true,
    "has_creative_element": false
  },
  "user_segments": [
    {
      "name": "Content Creators",
      "size": "large",
      "search_behavior": "how-to focused",
      "budget_level": "low-medium"
    },
    {
      "name": "Small Businesses",
      "size": "medium",
      "search_behavior": "ROI focused",
      "budget_level": "medium"
    },
    {
      "name": "Tech Entrepreneurs",
      "size": "small",
      "search_behavior": "market focused",
      "budget_level": "high"
    }
  ],
  "recommended_agents": {
    "fixed": ["topic_researcher", "content_strategist", "market_analyst"],
    "recommended": ["prompt_engineer", "brand_specialist"],
    "reasoning": {
      "prompt_engineer": "domain_signals.has_technical_depth = true",
      "brand_specialist": "domain_signals.has_brand_angle = true"
    }
  },
  "recommended_personas": [
    {
      "name": "大学生创作者",
      "name_en": "Student Creator",
      "traits": ["zero_budget", "mobile_first", "time_rich"],
      "search_patterns": ["how to make money with AI", "free AI tools", "no experience needed"],
      "pain_points": ["no budget", "no experience", "need quick results"],
      "priority": 1
    },
    {
      "name": "专业创作者",
      "name_en": "Pro Creator",
      "traits": ["efficiency_focused", "willing_to_pay", "experienced"],
      "search_patterns": ["best UGC tools", "AI video workflow", "professional UGC"],
      "pain_points": ["time constraints", "quality consistency", "client management"],
      "priority": 2
    }
  ]
}
```

#### 智能分配规则

```yaml
agent_activation_rules:
  # 固定成员 (always active)
  always_active:
    - topic_researcher
    - content_strategist
    - market_analyst

  # 按需成员 (conditional activation)
  conditional:
    prompt_engineer:
      activate_if:
        - "domain_signals.has_technical_depth = true"
        - "domain_type includes 'tech'"
        - "seed contains tool/software/AI/prompt/workflow"
      weight: 0.8  # 高概率推荐

    brand_specialist:
      activate_if:
        - "domain_signals.has_brand_angle = true"
        - "domain_type includes 'marketing'"
        - "seed contains brand/marketing/ads/campaign"
      weight: 0.7

  # 领域特定角色 (rare, user-initiated)
  domain_specific:
    - name: "法规专家"
      activate_if: "domain_type includes 'legal' or 'medical' or 'finance'"
    - name: "本地化专家"
      activate_if: "scope.geo != 'US' or scope.language != 'en'"
```

#### Persona 生成规则

```yaml
persona_generation:
  min_personas: 2
  max_personas: 4  # Deep 模式最多 4

  dimensions_to_consider:
    - budget_level: [zero, low, medium, high]
    - tech_savviness: [beginner, intermediate, advanced]
    - use_case: [personal, small_business, enterprise, creator, agency]
    - platform_preference: [mobile, desktop, cross_platform]
    - primary_goal: [learn, earn, save_time, build_product, grow_audience]

  selection_strategy:
    standard_mode:
      count: 2
      rule: "选最大用户群的 2 个代表，覆盖 60%+ 用户"
      diversity: "确保 budget_level 和 tech_savviness 至少各有 2 种不同值"
    deep_mode:
      count: 3-4
      rule: "standard 基础上增加 1-2 个长尾用户群"
      diversity: "确保至少 3 种不同 primary_goal"

  output_per_persona:
    - name: "string (中文名 + 英文名)"
    - traits: "array[string] (3-5 个特征标签)"
    - search_patterns: "array[string] (3-5 个典型搜索词)"
    - pain_points: "array[string] (2-3 个痛点)"
    - content_preferences: "string (偏好的内容格式)"
```

### Step 0.3: 互动问卷

使用 `AskUserQuestion` 工具，一次性问 3-4 个问题：

```json
{
  "questions": [
    {
      "question": "确认研究方向？",
      "header": "Seed",
      "multiSelect": false,
      "options": [
        {
          "label": "{extracted_seed} (推荐)",
          "description": "基于你的输入自动提取"
        },
        {
          "label": "修改种子词",
          "description": "输入新的种子词"
        }
      ]
    },
    {
      "question": "确认 Agent 阵容？(固定 3 + 推荐 N)",
      "header": "Team",
      "multiSelect": true,
      "options": [
        {
          "label": "推荐阵容 (Recommended)",
          "description": "{fixed_agents} + {recommended_agents} = {total} 位"
        },
        {
          "label": "只用固定成员",
          "description": "选题研究员 + 内容主编 + 市场分析员 (3 位)"
        },
        {
          "label": "全部启用",
          "description": "固定 + 推荐 + 全部 Persona (最多 8 位)"
        }
      ]
    },
    {
      "question": "研究深度？",
      "header": "Depth",
      "multiSelect": false,
      "options": [
        {
          "label": "Standard (Recommended)",
          "description": "每 Agent 5-8 选题，Persona 2 个"
        },
        {
          "label": "Deep",
          "description": "每 Agent 8-12 选题，Persona 3-4 个，Token 消耗更高"
        }
      ]
    }
  ]
}
```

### Step 0.4: 冻结 Research Charter

Research Charter = team_mission.json 的升级版，增加不可变约束声明。Charter 冻结后 Phase 1 开始，执行中不可修改核心参数。

```json
{
  "$schema": "research-charter-v1.1.json",
  "seed": "AI UGC Ads",
  "scope": {
    "language": "en",
    "geo": "US",
    "forbidden_zones": ["gambling", "adult"]
  },
  "charter_locked": true,
  "no_modify_after_lock": ["seed", "agents", "depth", "scope"],
  "team": {
    "orchestrator": "main",
    "agents": [
      {
        "agent_id": "topic_researcher",
        "role": "选题研究员",
        "type": "fixed",
        "tools": ["WebSearch", "WebFetch", "dataforseo"],
        "dataforseo_budget": 5,
        "topic_quota": 8
      },
      {
        "agent_id": "content_strategist",
        "role": "内容主编",
        "type": "fixed",
        "tools": ["WebSearch", "WebFetch", "dataforseo"],
        "dataforseo_budget": 5,
        "topic_quota": 8
      },
      {
        "agent_id": "market_analyst",
        "role": "市场分析员",
        "type": "fixed",
        "tools": ["WebSearch", "WebFetch", "dataforseo"],
        "dataforseo_budget": 5,
        "topic_quota": 6
      },
      {
        "agent_id": "prompt_engineer",
        "role": "Prompt 工程师",
        "type": "recommended",
        "tools": ["WebSearch", "WebFetch", "dataforseo"],
        "dataforseo_budget": 5,
        "topic_quota": 6
      },
      {
        "agent_id": "brand_specialist",
        "role": "品牌专家",
        "type": "recommended",
        "tools": ["WebSearch", "Read", "dataforseo"],
        "read_docs": ["PRODUCT_CATALOG.md"],
        "dataforseo_budget": 5,
        "topic_quota": 5
      },
      {
        "agent_id": "creator_persona_1",
        "role": "大学生创作者 Persona",
        "type": "persona",
        "persona_config": {
          "name": "大学生创作者",
          "traits": ["zero_budget", "mobile_first"],
          "search_patterns": ["how to make money with AI", "free AI tools"]
        },
        "tools": ["WebSearch", "dataforseo"],
        "dataforseo_budget": 5,
        "topic_quota": 5
      },
      {
        "agent_id": "creator_persona_2",
        "role": "专业创作者 Persona",
        "type": "persona",
        "persona_config": {
          "name": "专业创作者",
          "traits": ["efficiency_focused", "willing_to_pay"],
          "search_patterns": ["best UGC tools", "AI video workflow"]
        },
        "tools": ["WebSearch", "dataforseo"],
        "dataforseo_budget": 5,
        "topic_quota": 5
      }
    ],
    "total_agents": 7,
    "expected_raw_topics": "35-50"
  },
  "depth": "standard",
  "product_catalog_path": "/Users/H/Documents/AliciBlog/skills/_docs/PRODUCT_CATALOG.md",
  "writing_principles_path": "/Users/H/Documents/AliciBlog/skills/_docs/BLOG_WRITING_PRINCIPLES_v2.md",
  "created_at": "2026-02-06T10:00:00Z",
  "version": "1.1"
}
```

#### Charter 冻结规则

```yaml
charter_freeze_rules:
  locked_fields:
    - seed          # 种子词不可改
    - agents        # Agent 阵容不可改
    - depth         # 研究深度不可改
    - scope         # 语言/地区不可改
  mutable_fields:
    - topic_quota   # 可在执行中微调 (±2)
  enforcement: "Phase 1 开始后，任何对 locked_fields 的修改请求将被拒绝并记录"
```

---

## Phase 1: Parallel Exploration (Subagents)

### 执行方式

Orchestrator 使用 **Task tool** 并行发起 5-7 个 subagent。所有 subagent 在同一条消息中并行调用，利用 Tier 1 支持 ~7 concurrent subagents 的能力。

```
Orchestrator 发送单条消息：
  Task(agent_1_prompt) ← topic_researcher
  Task(agent_2_prompt) ← content_strategist
  Task(agent_3_prompt) ← market_analyst
  Task(agent_4_prompt) ← prompt_engineer
  Task(agent_5_prompt) ← brand_specialist
  Task(agent_6_prompt) ← creator_persona_1
  Task(agent_7_prompt) ← creator_persona_2

所有 Task 并行执行，各自独立返回结果。
```

### Agent 系统提示词模板

每个 subagent 通过 Task tool 的 `prompt` 参数接收完整的角色指令。以下是各 Agent 的系统提示词模板：

---

#### Agent 1: 选题研究员 (topic_researcher)

```
你通过搜索量与关键词数据的镜头研究选题。你看到的世界是由搜索词、月搜索量、趋势曲线和搜索意图构成的。

## 你的视角 (Lens)
你只从关键词数据和搜索量的角度思考。你关心的是：
- 哪些搜索词有高搜索量？
- 搜索趋势是上升还是下降？
- 长尾词有哪些机会？
- 搜索意图是什么（信息型/交易型/导航型）？

## 任务
基于种子词 "{seed}"，使用 WebSearch 研究并产出 {topic_quota} 个选题建议。
对你的 Top 3 选题，调用 DataForSEO 验证搜索量。

## 研究方法
1. 使用 WebSearch 搜索种子词相关的热门查询
2. 分析 autocomplete 建议和相关搜索
3. 识别搜索量高但竞品弱的机会
4. 关注 "how to"、"best"、"vs"、"alternative" 等高意图词
5. **验证**: 对 Top 3 选题调用 DataForSEO keywords_data 获取真实搜索量

## 数据验证要求
- 对 Top 3 选题调用 DataForSEO 验证 (最多 5 次调用)
- 如果 DataForSEO 调用失败，用 WebSearch 估算并标记 "estimated"
- confidence = "high" 需要 DataForSEO 验证; "medium" 可以是 WebSearch; "low" 需标注
- 禁止编造搜索量数据 (no hallucinated data)

## 竞品分析
从你的搜索量视角，记录你看到的竞品：
- 哪些内容在 SERP 上占据高位？
- 竞品在关键词覆盖上的弱点是什么？

## 约束
- 只从搜索量/关键词数据角度思考
- 不要考虑品牌适配、市场规模等其他维度（那是别人的工作）
- 每个选题必须有至少 1 个数据点（搜索量/趋势数据/竞品 URL）
- 语言: {language}, 地区: {geo}

## 输出格式
返回 JSON 格式（不要用 markdown），结构如下：

{agent_output_schema}
```

---

#### Agent 2: 内容主编 (content_strategist)

```
你通过内容格式与竞品空白的镜头研究选题。你看到的世界是由内容类型、竞品结构、SERP 覆盖缺口和内容质量层次构成的。

## 你的视角 (Lens)
你只从内容类型和竞品覆盖的角度思考。你关心的是：
- 竞品写了哪些类型的内容？（Tutorial/List/Roundup/News）
- 哪种内容格式效果最好？
- 哪些角度竞品没有覆盖？（空白机会）
- 现有内容有什么结构性问题？（过时/太浅/无FAQ）

## 任务
基于种子词 "{seed}"，使用 WebSearch 和 WebFetch 研究竞品内容，产出 {topic_quota} 个选题建议。
对你的 Top 3 选题，调用 DataForSEO SERP 验证竞品覆盖情况。

## 研究方法
1. WebSearch 搜索种子词，分析 Top 10 结果的内容类型
2. WebFetch 抓取 2-3 个代表性竞品文章，分析结构
3. 识别竞品的内容空白（缺少的角度/格式/深度）
4. 评估哪些内容类型最适合填补空白
5. **验证**: 对 Top 3 选题调用 DataForSEO SERP 分析竞品分布

## 数据验证要求
- 对 Top 3 选题调用 DataForSEO 验证 (最多 5 次调用)
- 如果 DataForSEO 调用失败，用 WebSearch 分析并标记 "estimated"
- 每个选题必须有至少 1 个竞品 URL 作为空白分析证据
- 禁止编造竞品数据 (no hallucinated data)

## 竞品分析
从你的内容格式视角，记录你看到的竞品：
- 内容层面的直接竞品（URL + 内容类型）
- 竞品在内容结构/深度/时效性上的主要弱点

## 约束
- 只从内容类型和竞品空白的角度思考
- 不要考虑搜索量（那是研究员的工作）
- 每个选题必须说明竞品空白在哪里
- 必须推荐内容类型（tutorial/list/roundup/comparison）

## 输出格式
返回 JSON 格式（不要用 markdown），结构如下：

{agent_output_schema}
```

---

#### Agent 3: 市场分析员 (market_analyst)

```
你通过市场数据与行业趋势的镜头研究选题。你看到的世界是由市场规模、增长率、融资动态、行业拐点和新兴玩家构成的。

## 你的视角 (Lens)
你只从市场数据和行业趋势的角度思考。你关心的是：
- 这个市场多大？增长速度如何？
- 有没有最近的行业报告/融资新闻？
- 哪些趋势正在改变这个领域？
- 哪些新玩家/新技术正在崛起？

## 任务
基于种子词 "{seed}"，使用 WebSearch 研究市场背景，产出 {topic_quota} 个选题建议。
对你的 Top 3 选题，调用 DataForSEO 验证相关关键词的搜索趋势。

## 研究方法
1. WebSearch 搜索市场报告、行业分析
2. 寻找最新融资新闻、产品发布
3. 识别行业拐点和趋势转折
4. 关注 Gartner/McKinsey/Forrester 等权威来源
5. **验证**: 对 Top 3 选题调用 DataForSEO keywords_data 验证趋势信号

## 数据验证要求
- 对 Top 3 选题调用 DataForSEO 验证 (最多 5 次调用)
- 如果 DataForSEO 调用失败，用 WebSearch 估算并标记 "estimated"
- 每个选题必须有市场数据支撑，数据必须标明来源
- 禁止编造市场数据 (no hallucinated data)

## 竞品分析
从你的市场趋势视角，记录你看到的竞品：
- 产品/服务层面的竞品（哪些工具/平台在争夺这个市场）
- 竞品在市场定位上的主要弱点

## 约束
- 只从市场数据和行业趋势角度思考
- 不要分析搜索量或内容格式（那是别人的工作）
- 每个选题必须有至少 1 个数据点
- 数据必须标明来源

## 输出格式
返回 JSON 格式（不要用 markdown），结构如下：

{agent_output_schema}
```

---

#### Agent 4: Prompt 工程师 (prompt_engineer)

```
你通过技术实操与工作流优化的镜头研究选题。你看到的世界是由提示词设计、工具链配置、自动化工作流和技术教程缺口构成的。

## 你的视角 (Lens)
你只从技术实操和工作流优化的角度思考。你关心的是：
- 用户需要什么样的提示词？
- AI 工具的工作流怎么优化？
- 哪些技术教程缺失？
- 哪些工具组合能提升效率？

## 任务
基于种子词 "{seed}"，使用 WebSearch 研究技术实操角度，产出 {topic_quota} 个选题建议。
对你的 Top 3 选题，调用 DataForSEO 验证技术教程类关键词的搜索量。

## 研究方法
1. WebSearch 搜索相关工具的使用教程、提示词指南
2. 分析现有教程的技术深度和完整性
3. 识别缺少的工作流教程、Prompt 模板
4. 关注工具链整合和自动化机会
5. **验证**: 对 Top 3 选题调用 DataForSEO keywords_data 验证搜索量

## 数据验证要求
- 对 Top 3 选题调用 DataForSEO 验证 (最多 5 次调用)
- 如果 DataForSEO 调用失败，用 WebSearch 估算并标记 "estimated"
- 每个选题必须有至少 1 个数据点
- 禁止编造数据 (no hallucinated data)

## 竞品分析
从你的技术实操视角，记录你看到的竞品：
- 现有教程/指南的竞品（URL + 技术深度评估）
- 竞品在技术准确性/工作流完整性上的弱点

## 约束
- 只从技术实操角度思考
- 每个选题必须有明确的技术知识点
- 关注 "how to"、"prompt"、"workflow"、"automate" 类角度

## 输出格式
返回 JSON 格式（不要用 markdown），结构如下：

{agent_output_schema}
```

---

#### Agent 5: 品牌专家 (brand_specialist)

```
你通过产品-内容适配的镜头研究选题。你看到的世界是由产品功能映射、CTA 策略空间、品牌差异化角度和竞品产品定位构成的。

## 你的视角 (Lens)
你只从产品-内容适配的角度思考。你关心的是：
- 哪些选题能自然提及 alici.ai 的产品？
- 产品的独特卖点如何与选题关联？
- CTA 策略怎么设计才不显得硬推？
- 竞品选题中有没有可以凸显 alici.ai 差异化的角度？

## 任务
基于种子词 "{seed}"，结合 alici.ai 产品目录，产出 {topic_quota} 个选题建议。
对你的 Top 3 选题，调用 DataForSEO 验证品牌相关关键词的搜索量。

## 产品目录 (摘要)
{product_catalog_summary}

## 研究方法
1. 阅读产品目录，理解 alici.ai 产品线
2. WebSearch 分析种子词领域中的产品评测类内容
3. 识别产品功能与用户需求的映射机会
4. 设计自然植入角度（非硬推）
5. **验证**: 对 Top 3 选题调用 DataForSEO keywords_data 验证搜索量

## 数据验证要求
- 对 Top 3 选题调用 DataForSEO 验证 (最多 5 次调用)
- 如果 DataForSEO 调用失败，用 WebSearch 估算并标记 "estimated"
- 每个选题必须有至少 1 个数据点
- 禁止编造产品功能或数据 (no hallucinated data)

## 竞品分析
从你的品牌适配视角，记录你看到的竞品：
- 产品竞品（哪些竞品产品在抢占用户）
- 竞品在产品定位/内容营销上的主要弱点

## 约束
- 只从产品-内容适配角度思考
- 每个选题必须有明确的产品关联
- 推荐 CTA 策略级别（subtle/balanced/aggressive）
- 不要编造产品功能

## 输出格式
返回 JSON 格式（不要用 markdown），结构如下：

{agent_output_schema}
```

---

#### Agent 6-8: 创作者 Persona (creator_persona_N)

```
你通过 "{persona.name}" 这个真实用户的镜头研究选题。你看到的世界是由这个用户的搜索习惯、痛点、预算约束和内容偏好构成的。

## 你的角色 (Lens)
- 角色名: {persona.name}
- 特征: {persona.traits}
- 搜索习惯: {persona.search_patterns}
- 痛点: {persona.pain_points}

## 你的任务
作为 "{persona.name}"，思考你在 "{seed}" 这个领域最想看到什么内容。
对你的 Top 3 选题，调用 DataForSEO 验证这类用户常搜的关键词。

## 思考方式
1. 我 ({persona.name}) 平时怎么搜索这个领域的信息？
2. 我最大的困惑和需求是什么？
3. 我会被什么标题吸引点进去？
4. 我看完一篇文章后会希望学到什么？
5. 现有的内容对我来说太难/太浅/太无聊了吗？

## 数据验证要求
- 对 Top 3 选题调用 DataForSEO 验证 (最多 5 次调用)
- 如果 DataForSEO 调用失败，用 WebSearch 估算并标记 "estimated"
- 每个选题必须有至少 1 个数据点
- 禁止编造数据 (no hallucinated data)

## 竞品分析
从你作为 {persona.name} 的视角，记录你看到的竞品：
- 你作为用户最常访问的内容来源（URL）
- 现有内容对你这类用户的主要不足

## 约束
- 完全从 {persona.name} 的视角思考
- 搜索词要像真实用户一样（口语化、非专业化）
- 关注这个角色特有的需求（别人不一定有的）
- 产出 {topic_quota} 个选题建议

## 输出格式
返回 JSON 格式（不要用 markdown），结构如下：

{agent_output_schema}
```

---

### Agent 输出 Schema (agent_output) — v1.1

所有 Agent 统一使用以下输出结构（v1.1 新增 `abstract`、`competitor_map`、`data_validation`）：

```json
{
  "agent_id": "topic_researcher",
  "agent_role": "选题研究员",
  "domain_seed": "AI UGC Ads",
  "abstract": "120-200 word summary of key findings and perspective. 例如: 从搜索量数据看，AI UGC 领域在 2026 Q1 呈现显著上升趋势。核心机会集中在工具对比类内容（月搜索量 8,100+），而 How-to 教程类长尾词（3,200/月）竞争度较低。主要发现: (1) 'AI UGC ad generator' 是最高搜索量的商业意图词; (2) 竞品内容普遍停留在 2025 版本; (3) 长尾词 'free AI UGC tools' 增长最快。",
  "competitor_map": {
    "content_competitors": ["https://example.com/best-ai-ugc-tools", "https://example2.com/ugc-guide"],
    "product_competitors": ["Synthesia", "HeyGen", "Creatify"],
    "key_weakness": "从搜索量视角看到的竞品主要弱点: 竞品文章多基于 2025 数据，缺少最新工具评测"
  },
  "data_validation": {
    "keywords_checked": [
      {"keyword": "AI UGC ad generator", "volume": 8100, "source": "DataForSEO"},
      {"keyword": "best UGC tools 2026", "volume": 3200, "source": "DataForSEO"},
      {"keyword": "free AI UGC tools", "volume": 1900, "source": "WebSearch estimate"}
    ],
    "serp_sampled": [
      {"keyword": "AI UGC ad generator", "top3_titles": ["Best AI UGC Generators...", "Top 10 UGC Tools...", "AI UGC Ads Guide..."]}
    ]
  },
  "findings": [
    {
      "topic_id": "TR-01",
      "title_suggestion": "Best AI UGC Ad Generators in 2026",
      "primary_keyword": "AI UGC ad generator",
      "rationale": "为什么这个选题有价值 (从我的视角)",
      "evidence": {
        "type": "search_trend",
        "data_points": ["DataForSEO: 8,100/月, rising trend", "Google autocomplete shows 5+ related queries"],
        "confidence": "high"
      },
      "recommended_content_type": "list",
      "target_audience": "创作者",
      "search_intent": "commercial_investigation"
    },
    {
      "topic_id": "TR-02",
      "title_suggestion": "...",
      "primary_keyword": "...",
      "rationale": "...",
      "evidence": {
        "type": "competitor_gap",
        "data_points": ["..."],
        "confidence": "medium"
      },
      "recommended_content_type": "tutorial",
      "target_audience": "企业",
      "search_intent": "informational"
    }
  ],
  "meta_observations": "跨选题的整体发现/趋势。例如：整体来看，UGC 领域的搜索热度在 2026 Q1 显著上升，尤其是 AI + UGC 的交叉词。"
}
```

#### 字段说明

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `agent_id` | string | ✅ | Agent 标识符 |
| `agent_role` | string | ✅ | 角色中文名 (保持直觉命名，给人看的) |
| `domain_seed` | string | ✅ | 种子词 |
| `abstract` | string | ✅ | **v1.1 NEW** 120-200 词的关键发现摘要，用于 Phase 2 相似度计算 |
| `competitor_map` | object | ✅ | **v1.1 NEW** 从该 Agent 视角看到的竞品画像 |
| `competitor_map.content_competitors` | array[string] | ✅ | 内容层面的竞品 URL |
| `competitor_map.product_competitors` | array[string] | ❌ | 产品层面的竞品名称 |
| `competitor_map.key_weakness` | string | ✅ | 从该 Agent 视角看到的竞品主要弱点 |
| `data_validation` | object | ✅ | **v1.1 NEW** Agent 自验证的数据记录 |
| `data_validation.keywords_checked` | array | ✅ | 已验证的关键词列表 (keyword + volume + source) |
| `data_validation.serp_sampled` | array | ❌ | SERP 采样结果 (keyword + top3_titles) |
| `findings` | array | ✅ | 选题列表 (5-12 个) |
| `findings[].topic_id` | string | ✅ | 选题 ID (格式: {2字母前缀}-{序号}) |
| `findings[].title_suggestion` | string | ✅ | 建议标题 |
| `findings[].primary_keyword` | string | ✅ | 主要关键词 |
| `findings[].rationale` | string | ✅ | 为什么有价值 (从该 Agent 视角) |
| `findings[].evidence` | object | ✅ | 支撑证据 |
| `findings[].evidence.type` | enum | ✅ | `search_trend` / `market_data` / `competitor_gap` / `user_need` / `product_fit` / `technical_gap` |
| `findings[].evidence.data_points` | array[string] | ✅ | 具体数据点或来源 (必须标明数据来源: DataForSEO / WebSearch / 报告名) |
| `findings[].evidence.confidence` | enum | ✅ | `high` (DataForSEO 验证) / `medium` (WebSearch 估算) / `low` (需标注) |
| `findings[].recommended_content_type` | enum | ✅ | `list` / `tutorial` / `roundup` / `comparison` / `guide` / `news` |
| `findings[].target_audience` | string | ✅ | 目标受众 |
| `findings[].search_intent` | enum | ❌ | `informational` / `commercial_investigation` / `transactional` / `navigational` |
| `meta_observations` | string | ✅ | 跨选题的整体发现 |

#### Agent 输出质量门禁 (Non-Negotiables)

```yaml
quality_gates:
  hard_requirements:
    - "每个选题必须有至少 1 个数据点 (搜索量/市场数据/竞品 URL)"
    - "禁止编造数据 (no hallucinated data)"
    - "data_validation.keywords_checked 至少 1 条记录"
    - "abstract 长度 120-200 词"

  confidence_rules:
    high: "必须有 DataForSEO 验证数据"
    medium: "可以是 WebSearch 估算，需标明 'estimated'"
    low: "需在 evidence.data_points 中标注数据不确定性"

  dataforseo_budget:
    per_agent: 5  # 每个 Agent 最多 5 次 DataForSEO 调用
    cost_per_call: "$0.015"
    max_per_agent: "$0.075"
```

#### Topic ID 前缀约定

| Agent | 前缀 | 示例 |
|-------|------|------|
| topic_researcher | TR | TR-01, TR-02 |
| content_strategist | CS | CS-01, CS-02 |
| market_analyst | MA | MA-01, MA-02 |
| prompt_engineer | PE | PE-01, PE-02 |
| brand_specialist | BS | BS-01, BS-02 |
| creator_persona_1 | P1 | P1-01, P1-02 |
| creator_persona_2 | P2 | P2-01, P2-02 |
| creator_persona_3 | P3 | P3-01, P3-02 |
| creator_persona_4 | P4 | P4-01, P4-02 |

---

## Phase 2: CEO Synthesis (Orchestrator — 只决策不执行)

> **CEO Model**: Orchestrator 不再做执行层验证（Agent 已自验证）。Orchestrator 只做战略决策：去重、相似度分析、覆盖度检查、排序。

### Step 2.1: 收集所有 Agent 输出

合并 5-7 个 agent_output 的 `findings` 数组，形成原始选题池：
- 预期: 30-50 个原始选题
- 每个选题保留 `agent_id` 来源标记
- **v1.1**: 同时收集每个 Agent 的 `abstract` 和 `competitor_map`

### Step 2.2: 语义去重

Orchestrator 对所有选题进行语义相似度判断（LLM 内部估算）：

```yaml
dedup_rules:
  # 相似标题/关键词合并为同一选题
  similarity_threshold: 0.65  # 高于此值视为同一选题

  merge_strategy:
    - 保留所有 Agent 的 evidence (证据叠加)
    - 保留所有 Agent 的 rationale
    - 标注贡献 Agent 列表 (contributing_agents)
    - 使用搜索量最高的 primary_keyword 作为代表
    - 使用最具吸引力的 title_suggestion 作为代表标题
    - "v1.1: 合并 data_validation 数据，已验证关键词不重复调用"

  output:
    - merged_topic_id: "MT-{序号}"  # Merged Topic ID
    - source_topics: ["TR-01", "CS-03", "BS-02"]  # 原始来源
    - contributing_agents: ["topic_researcher", "content_strategist", "brand_specialist"]
    - validated_keywords: ["合并所有 Agent 已验证的关键词，标记来源"]
```

### Step 2.3: 共识评分

```yaml
consensus_scoring:
  formula: "consensus_score = contributing_agents_count / total_agents"

  interpretation:
    - score >= 0.70: "高共识 — 多数 Agent 独立发现，可信度高"
    - score >= 0.40: "中共识 — 部分 Agent 发现，值得验证"
    - score < 0.40: "低共识 / 独家发现 — 可能是独特视角"

  # 独家发现加分 (单一 Agent 提出的选题不应被惩罚)
  uniqueness_bonus:
    single_agent_unique: true  # 标记为独家发现
    bonus_note: "单一 Agent 独家发现，可能是被忽视的机会"
```

### Step 2.4: 证据交叉增强

当同一选题被多个 Agent 发现时，Orchestrator 合并各 Agent 的证据为 `enriched_evidence_chain`：

```json
{
  "merged_topic_id": "MT-01",
  "title": "Best AI UGC Ad Generators in 2026",
  "primary_keyword": "AI UGC ad generator",
  "contributing_agents": ["topic_researcher", "brand_specialist", "creator_persona_1"],
  "consensus_score": 0.43,
  "enriched_evidence_chain": {
    "topic_researcher": {
      "perspective": "搜索量驱动",
      "insight": "月搜索量 8,100，上升趋势",
      "evidence_type": "search_trend",
      "confidence": "high"
    },
    "brand_specialist": {
      "perspective": "产品适配",
      "insight": "alici.ai Video Studio 直接匹配，可作为榜单项目",
      "evidence_type": "product_fit",
      "confidence": "high"
    },
    "creator_persona_1": {
      "perspective": "大学生创作者视角",
      "insight": "用户搜索 'free AI UGC tools'，关注零预算方案",
      "evidence_type": "user_need",
      "confidence": "medium"
    }
  },
  "merged_competitor_map": {
    "content_competitors": ["URL1", "URL2", "URL3"],
    "product_competitors": ["Tool1", "Tool2"],
    "weaknesses_by_lens": {
      "topic_researcher": "竞品内容过时",
      "brand_specialist": "竞品缺少产品植入",
      "creator_persona_1": "竞品忽略零预算用户"
    }
  }
}
```

### Step 2.5: Similarity Matrix (v1.1 NEW)

基于每个 Agent 的 `abstract` (120-200 词) 构建相似度矩阵，量化 Agent 间的视角重合度。

```yaml
similarity_matrix:
  input: "所有 Agent 的 abstract 字段"
  method: "LLM pairwise 判断 (0-1 scale)"
  threshold: 0.70  # 相似度 > 0.7 = 冗余信号

  output:
    matrix: |
      Agent pairwise similarity:
        TR ↔ CS: 0.45  (低重合 — 各看不同维度)
        TR ↔ MA: 0.30  (低重合)
        TR ↔ P1: 0.55  (中等重合 — 都关注搜索量)
        CS ↔ BS: 0.65  (中等重合 — 都看竞品)
        P1 ↔ P2: 0.72  (高重合！⚠️ — Persona 视角可能过于相似)

  action_on_high_similarity:
    - "相似度 > 0.7 的 Agent 对: 合并选题时优先去重"
    - "如果 2+ Persona 相似度 > 0.7: 在报告中建议下次减少 Persona 数量"
    - "不自动删除 Agent — 仅标记并在 05-diversity-analysis.md 中报告"
```

### Step 2.6: Coverage Map (v1.1 NEW)

从所有选题的 `target_audience` × `recommended_content_type` × `search_intent` 维度生成覆盖矩阵。

```yaml
coverage_map:
  dimensions:
    - target_audience: ["创作者", "企业", "开发者", "学生", "小企业主"]
    - content_type: ["list", "tutorial", "roundup", "comparison", "guide"]
    - search_intent: ["informational", "commercial_investigation", "transactional"]

  output: |
    Coverage Matrix (target_audience × content_type):
                   list  tutorial  roundup  comparison  guide
    创作者          ✅     ✅        ❌        ✅          ❌
    企业            ✅     ❌        ❌        ✅          ❌
    开发者          ❌     ✅        ❌        ❌          ❌
    学生            ❌     ✅        ❌        ❌          ❌
    小企业主        ❌     ❌        ❌        ❌          ❌     ← 空白！

  interpretation:
    covered: "✅ = 有选题覆盖该象限"
    gap: "❌ = 无选题覆盖 — 可能是遗漏，也可能是无需求"
    action: "在 05-diversity-analysis.md 中报告空白区域及原因分析"
```

### Step 2.7: 排序 → Top 15-20 (v1.1 升级公式)

```yaml
ranking_formula_v1_1:
  evidence_richness:
    weight: 0.30
    scoring:
      - 3+ evidence types: 40
      - 2 evidence types: 30
      - 1 evidence type: 20
      - high confidence bonus: +5 per high-confidence evidence
      - "v1.1: DataForSEO 验证过的关键词 +10"

  consensus_score:
    weight: 0.20
    scoring:
      - normalized 0-100 from consensus_score

  diversity_bonus:
    weight: 0.20
    scoring:
      - unique_perspective (单一 Agent 独家发现): +20
      - covers_underserved_audience: +15
      - novel_content_type (竞品未使用的格式): +10
      - "v1.1: 覆盖 Coverage Map 空白象限: +10"

  freshness_signal:
    weight: 0.15
    scoring:
      - "QDF 时效性 (0-10): 近期热点/新闻事件 = 10, 常青话题 = 5, 过时话题 = 0"
      - "normalized 0-100"

  brand_fit:
    weight: 0.15
    scoring:
      - "产品关联度 (0-10): 直接匹配产品功能 = 10, 间接关联 = 5, 无关联 = 0"
      - "normalized 0-100"

  risk_penalty:
    type: "penalty (非 weight)"
    scoring:
      - "high risk: -15 (竞争极激烈 / 数据不足 / 领域变化太快)"
      - "medium risk: -5"
      - "low risk: 0"

  final_score: "evidence × 0.30 + consensus × 0.20 + diversity × 0.20 + freshness × 0.15 + brand_fit × 0.15 - risk_penalty"
```

选取 Top 15-20 进入 Phase 3 补充验证。

---

## Phase 3: Supplemental Validation (补充验证 — v1.1 轻量化)

> **v1.1 变更**: Phase 3 从"全量验证"变为"补充验证"。Agent 在 Phase 1 已对各自 Top 3 关键词做了 DataForSEO 验证。Phase 3 只补充 Agent 未覆盖的关键词，重点放在 Title Lock 和 AEO 评分。

### Step 3.1: 补充验证 (仅验证 Agent 未覆盖的关键词)

```yaml
supplemental_validation:
  step_1: "收集所有 Agent 的 data_validation.keywords_checked"
  step_2: "提取 Top 15-20 merged topics 的 primary_keyword"
  step_3: "对比: 哪些 primary_keyword 已被 Agent 验证？哪些未验证？"
  step_4: "仅对未验证的关键词调用 DataForSEO"

  example:
    total_top_keywords: 15
    already_validated_by_agents: 8
    need_supplemental: 7
    estimated_calls: "~10 (含 alt_keywords)"
```

对未验证的关键词调用：

```
dataforseo.keywords_data:
  keywords: [... 仅未验证的关键词 ...]
  location_code: 2840  # US
  language_code: "en"
```

提取指标：
- `search_volume`
- `monthly_searches[]` (12 个月趋势)
- `cpc`
- `competition`

### Step 3.2: Title Lock

对每个通过排序的选题执行 Title Lock（复用 growth-topic-scout Phase 3 逻辑）。

Title Lock 需要 SERP 数据，因此对 Top 10 选题调用 SERP 分析：

```
dataforseo.serp:
  keyword: "..."
  location_code: 2840
  language_code: "en"
  device: "desktop"
```

提取：
- Top 5 竞品 URL + 标题
- AI Overview 有无
- People Also Ask 问题
- Featured Snippet 有无

Title Lock 验证：

| 验证项 | 检查内容 | 失败处理 |
|--------|---------|---------|
| 关键词命中 | 标题必须包含 primary_keyword | 自动重写 |
| 意图匹配 | 标题格式匹配搜索意图 | 自动重写 |
| SERP 对齐 | 参考 SERP Top 3 标题结构 | 提供对比证据 |
| 年份验证 | 年份有数据支持 | 不加年份或改为 "Latest" |

### Step 3.3: AEO 评分

为每个最终选题计算：
- SEO Score (0-100): 复用 growth-topic-scout 评分维度
- AEO Score (0-100): 复用 growth-topic-scout 评分维度
- Combined Priority: excellent / high_seo_first / high_aeo_first / good / low

### Phase 3 成本预估 (v1.1 — 补充验证模式)

| 操作 | 单价 | 用量 | 费用 |
|------|------|------|------|
| 补充 keywords_data | $0.015/keyword | ~10 keywords (仅未验证的) | ~$0.15 |
| Title Lock SERP | $0.002/query | ~10 queries | ~$0.02 |
| **Phase 3 小计** | | | **~$0.17** |

> 对比 v1.0: Phase 3 费用从 ~$0.33-0.49 降至 ~$0.17（因为大部分验证已在 Phase 1 由 Agent 完成）

---

## Phase 4: Final Portfolio + Handoff (Orchestrator)

### 输出文件结构 (v1.1)

```
/research 竞品分析/team-research/YYYY-MM-DD-{seed-slug}/
├── 00-research-charter.json          ← Phase 0 产出 (renamed from team-mission)
├── 01-agent-findings/                ← Phase 1 产出 (含 abstract + competitor_map + data_validation)
│   ├── topic-researcher.json
│   ├── content-strategist.json
│   ├── market-analyst.json
│   ├── prompt-engineer.json           (如启用)
│   ├── brand-specialist.json          (如启用)
│   ├── creator-persona-1.json
│   └── creator-persona-2.json
├── 02-team-research-report.md        ← Phase 4 产出 (人类可读)
├── 03-team-directions.json           ← Phase 4 产出 (机器可读)
├── 04-agent-contributions.json       ← Phase 4 产出 (贡献追踪)
├── 05-diversity-analysis.md          ← Phase 4 产出 (含 Similarity Matrix + Coverage Map)
├── 06-decision-brief.md              ← Phase 4 产出 NEW (Top 1-3 决策简报)
└── 07-handoff-pack/                  ← Phase 4 产出 NEW (Top 1-3 方向的创作包)
    ├── D01-brief.md                   # Direction 详情 + 写作指南
    ├── D01-outline.md                 # 完整文章大纲
    ├── D01-prompt-kit.md              # 可直接喂给 Writer 的 Prompt
    ├── D02-brief.md
    ├── D02-outline.md
    ├── D02-prompt-kit.md
    └── D03-brief.md                   (如有第 3 个 Top 方向)
```

### 03-team-directions.json 结构

兼容现有 `DIRECTION_SCHEMA.json` 的标准字段 + Team Scout 扩展字段：

```json
{
  "mode": "team_scout",
  "schema_version": "1.0",
  "seed": "AI UGC Ads",
  "team_stats": {
    "total_agents": 7,
    "raw_topics": 43,
    "after_dedup": 18,
    "after_validation": 8,
    "final_directions": 8
  },
  "final_directions": [
    {
      "rank": 1,
      "direction_id": "D01",
      "theme": "AI UGC Ad Tool Reviews",
      "locked_title": {
        "title": "Best AI UGC Ad Generators in 2026: Top 8 Tested",
        "primary_keyword": "AI UGC ad generator",
        "intent_matched": true,
        "serp_aligned": true,
        "year_validated": true,
        "formula_id": "listicle-1",
        "evidence": {
          "serp_titles": ["..."],
          "search_volume": 8100,
          "trend": "rising"
        }
      },
      "seo_score": 89,
      "aeo_score": 85,
      "combined_priority": "excellent",
      "evidence_chain": {
        "volume": 8100,
        "trend": "rising",
        "cpc_avg": 3.8,
        "competition_avg": 0.62,
        "serp_gap": "high",
        "competitor_weakness": ["outdated", "no_testing_methodology"]
      },
      "outline": {
        "h2_sections": [
          "Quick Comparison Table",
          "How We Tested",
          "Top 8 AI UGC Ad Generators",
          "Category Winners",
          "Pricing Comparison",
          "FAQ"
        ],
        "aeo_answer_block": "The best AI UGC ad generators in 2026 include...",
        "estimated_word_count": 4500
      },
      "recommended_skill": "blog-list-writer",
      "recommended_mode": "standard",
      "product_mapping": {
        "primary": "video_studio",
        "secondary": "video_prompt",
        "product_angle": "One platform to access all models"
      },

      "team_metadata": {
        "contributing_agents": ["topic_researcher", "brand_specialist", "creator_persona_1"],
        "primary_perspective": "topic_researcher",
        "consensus_score": 0.43,
        "perspective_evidence": {
          "topic_researcher": {
            "insight": "月搜索量 8,100，上升趋势",
            "data_points": ["DataForSEO: 8,100/月, rising"]
          },
          "brand_specialist": {
            "insight": "alici.ai Video Studio 直接匹配",
            "data_points": ["可作为榜单第 2-3 位推荐"]
          },
          "creator_persona_1": {
            "insight": "大学生搜索 'free AI UGC tools'",
            "data_points": ["DataForSEO: 1,900/月, rising"]
          }
        },
        "discovery_type": "multi_agent_consensus",
        "merged_from": ["TR-01", "BS-02", "P1-04"],
        "similarity_to_others": [
          {"direction_id": "D02", "similarity": 0.35},
          {"direction_id": "D03", "similarity": 0.22}
        ],
        "coverage_quadrant": "high_volume + list",
        "risk_assessment": {
          "level": "low",
          "factors": ["competition_moderate", "data_fresh", "brand_fit_strong"]
        }
      }
    }
  ]
}
```

#### team_metadata 字段说明 (v1.1)

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `contributing_agents` | array[string] | ✅ | 发现该选题的 Agent 列表 |
| `primary_perspective` | string | ✅ | 主要贡献 Agent |
| `consensus_score` | number (0-1) | ✅ | 共识度 |
| `perspective_evidence` | object | ✅ | 各 Agent 的证据 |
| `discovery_type` | enum | ✅ | `multi_agent_consensus` / `single_agent_unique` |
| `merged_from` | array[string] | ✅ | 合并前的原始 topic_id 列表 |
| `similarity_to_others` | array | ✅ | **v1.1 NEW** 与其他 Direction 的相似度 |
| `coverage_quadrant` | string | ✅ | **v1.1 NEW** 在 Coverage Map 中的位置 |
| `risk_assessment` | object | ✅ | **v1.1 NEW** 风险评估 (level + factors) |

### 02-team-research-report.md 模板

```markdown
# Team Research Report: {seed}

> Date: YYYY-MM-DD | Agents: {N} | Raw Topics: {N} | Final Directions: {N}
> Depth: {standard/deep} | Duration: ~{N} min | DataForSEO Cost: ~${N}

---

## Executive Summary

{3-5 句总结: 领域概况、关键发现、推荐行动}

---

## Agent 阵容

| 角色 | Agent ID | 类型 | 发现数 | 关键发现 |
|------|----------|------|--------|---------|
| 选题研究员 | topic_researcher | 固定 | {N} | {一句话关键发现} |
| 内容主编 | content_strategist | 固定 | {N} | {一句话关键发现} |
| 市场分析员 | market_analyst | 固定 | {N} | {一句话关键发现} |
| Prompt 工程师 | prompt_engineer | 推荐 | {N} | {一句话关键发现} |
| 品牌专家 | brand_specialist | 推荐 | {N} | {一句话关键发现} |
| 大学生 Persona | creator_persona_1 | Persona | {N} | {一句话关键发现} |
| 专业创作者 Persona | creator_persona_2 | Persona | {N} | {一句话关键发现} |

---

## Final Directions ({N} 个)

### D01: {locked_title}

| 维度 | 数据 |
|------|------|
| **SEO Score** | {score}/100 |
| **AEO Score** | {score}/100 |
| **共识度** | {score} ({N}/{total} Agents) |
| **发现者** | {agent_list} |
| **搜索量** | {volume}/月 |
| **趋势** | {trend} |
| **推荐格式** | {content_type} → {writer_skill} |

**多角度证据:**
- **研究员视角**: {evidence}
- **市场分析员视角**: {evidence}
- **创作者视角**: {evidence}

**竞品现状**: {Top 3 竞品及弱点}

---

### D02: {locked_title}
...

---

## 多样性分析

### 选题覆盖维度
| 维度 | 覆盖情况 |
|------|---------|
| 内容类型 | {list/tutorial/roundup/comparison 的分布} |
| 目标受众 | {创作者/企业/开发者 的分布} |
| 搜索意图 | {信息型/交易型/调查型 的分布} |
| 产品关联度 | {有关联/无关联 的分布} |

### 语义距离
- 最终选题间平均相似度: {score}
- 最大相似度对: {D0X vs D0Y} = {score}
- 未覆盖领域: {分析}

---

## Agent 独家发现

以下选题仅由单一 Agent 提出，可能是被忽视但有价值的方向：

### {title} (by {agent_role})
- **为什么独特**: {rationale}
- **数据**: 搜索量 {volume}, 趋势 {trend}
- **建议**: {是否值得进一步研究}

---

## 附录: 去重与筛选日志

| 阶段 | 数量 | 说明 |
|------|------|------|
| Phase 1 原始选题 | {N} | 各 Agent 产出总和 |
| Phase 2 去重后 | {N} | 语义去重 (-{N}%) |
| Phase 3 验证后 | {N} | DataForSEO 验证 (-{N}%) |
| 最终选题 | {N} | Top {N} by ranking formula |
```

### 04-agent-contributions.json 结构

```json
{
  "contributions": [
    {
      "agent_id": "topic_researcher",
      "role": "选题研究员",
      "raw_topics_count": 8,
      "topics_survived_dedup": 5,
      "topics_in_final": 3,
      "contribution_rate": 0.375,
      "unique_discoveries": 1,
      "meta_observation": "整体搜索热度上升，UGC + AI 交叉词增长明显"
    }
  ],
  "cross_agent_analysis": {
    "highest_consensus_topic": "MT-01 (3/7 agents)",
    "most_productive_agent": "topic_researcher (8 topics, 3 in final)",
    "most_unique_agent": "prompt_engineer (2 unique discoveries)",
    "persona_contribution_rate": 0.25
  }
}
```

### 05-diversity-analysis.md 结构 (v1.1 — 含 Similarity Matrix + Coverage Map)

```markdown
# Diversity Analysis: {seed}

## 选题多样性指标

| 指标 | 值 | 目标 | 状态 |
|------|-----|------|------|
| 内容类型覆盖 | {N}/5 种 | >= 3 | ✅/❌ |
| 受众覆盖 | {N} 个分群 | >= 2 | ✅/❌ |
| 搜索意图覆盖 | {N}/4 种 | >= 2 | ✅/❌ |
| 平均选题间相似度 | {score} | < 0.50 | ✅/❌ |
| 独家发现数量 | {N} | >= 1 | ✅/❌ |

## Similarity Matrix (v1.1 NEW)

Agent 间视角重合度 (基于 Abstract):

| | TR | CS | MA | PE | BS | P1 | P2 |
|---|---|---|---|---|---|---|---|
| TR | — | {score} | {score} | ... | ... | ... | ... |
| CS | | — | ... | ... | ... | ... | ... |
| ... | | | | | | | |

⚠️ 高重合对 (>0.7): {列出}
✅ 低重合对 (<0.3): {列出}

## Coverage Map (v1.1 NEW)

{target_audience × content_type 覆盖矩阵}

空白区域: {列出未覆盖的象限及原因分析}

## Agent 视角分布

{哪些 Agent 贡献了最多的最终选题？哪些 Agent 的选题被淘汰最多？原因分析。}

## 未覆盖区域

{基于领域分析，识别可能被遗漏的角度。}
```

### 06-decision-brief.md 模板 (v1.1 NEW)

```markdown
# Decision Brief: {seed}

> Date: YYYY-MM-DD | Team: {N} Agents | Final Directions: {N}

---

## Top 3 方向速览

### #1: {locked_title}
- **为什么值得写**: {1-2 句, 数据支撑。例: "月搜索量 8,100 且持续上升，竞品内容停留在 2025 版本，存在明显时效性空白。"}
- **为什么现在写**: {时效性/趋势/竞品弱点。例: "QDF 信号显示近 30 天搜索量增长 40%，竞品尚未更新。"}
- **主要风险**: {竞争激烈/数据不足/领域变化快。例: "中等竞争度 (0.62)，但 alici.ai 有产品差异化优势。"}
- **推荐下一步**: {用哪个 Writer, 预计字数, 重点章节。例: "blog-list-writer Blueprint B, ~5,500 词, 重点: 实测方法论 + Category Winners"}

### #2: {locked_title}
- **为什么值得写**: {...}
- **为什么现在写**: {...}
- **主要风险**: {...}
- **推荐下一步**: {...}

### #3: {locked_title}
- **为什么值得写**: {...}
- **为什么现在写**: {...}
- **主要风险**: {...}
- **推荐下一步**: {...}

---

## 放弃的方向 (排名 4-5 但未入选 Top 3 的)

| 方向 | 放弃原因 |
|------|---------|
| {title} | {竞争度太高 / 搜索量不足 / 品牌关联弱} |
| {title} | {...} |

---

## 决策建议

- **如果只写 1 篇**: 推荐 #{rank} — {locked_title}
- **如果写 2-3 篇**: 推荐 #{rank1} + #{rank2}，覆盖 {content_type1} + {content_type2} 两种格式
- **时效性提醒**: {是否有 QDF 窗口需要抓住}
```

### 07-handoff-pack/ 结构 (v1.1 NEW)

为 Top 1-3 方向各生成一组创作包，可直接喂给 Writer Skill。

#### D0X-brief.md

```markdown
# Direction Brief: {locked_title}

## 基本信息
| 字段 | 值 |
|------|-----|
| Direction ID | {D0X} |
| Primary Keyword | {primary_keyword} |
| Search Volume | {volume}/月 |
| Trend | {trend} |
| Content Type | {recommended_content_type} |
| Writer Skill | {recommended_skill} |
| Blueprint/Tier | {specific_blueprint_or_tier} |
| Estimated Words | {word_count} |

## 写作指南
- **核心论点**: {从证据链提炼的核心论点}
- **差异化角度**: {竞品没覆盖的角度}
- **必须包含**: {关键数据点/案例/对比}
- **避免**: {竞品常犯的错误}

## 产品植入
- **产品**: {product_mapping.primary}
- **植入角度**: {product_mapping.product_angle}
- **CTA 级别**: {subtle/balanced/aggressive}
```

#### D0X-outline.md

```markdown
# Article Outline: {locked_title}

## H2 结构
{从 outline.h2_sections 生成的完整大纲，每个 H2 附带 50-100 词描述}

## AEO Answer Block
{outline.aeo_answer_block}

## Key Takeaways (前置)
{3-5 个 Key Takeaway 建议}

## FAQ 建议
{基于 People Also Ask 的 3-5 个 FAQ}
```

#### D0X-prompt-kit.md

```markdown
# Prompt Kit: {locked_title}

## Writer Prompt (可直接喂给 {recommended_skill})

{完整的 Writer 启动 Prompt，包含:
- 标题
- Primary keyword
- Content type
- 大纲
- 产品植入指南
- 差异化要求
- 字数要求
- AEO 目标}

## 参考素材
- 竞品 URL 1: {url} — {弱点}
- 竞品 URL 2: {url} — {弱点}
- 数据来源: {DataForSEO / 市场报告 URL}
```

---

## 智能分配系统详细设计

### 领域分析引擎

Orchestrator 在 Phase 0 使用以下逻辑分析种子词：

```yaml
domain_analysis_workflow:
  step_1_websearch:
    query: "{seed} market overview 2026"
    extract:
      - market_size
      - growth_rate
      - key_players
      - recent_news

  step_2_classify:
    domain_types:
      tech: "tool, software, AI, API, platform, SaaS"
      marketing: "brand, ads, campaign, marketing, UGC, content"
      creative: "design, video, image, art, photography"
      business: "startup, enterprise, revenue, pricing, ROI"
      education: "learn, course, tutorial, guide, certification"

    signals:
      has_tools: "domain involves specific software tools"
      has_brand_angle: "can naturally mention alici.ai products"
      has_market_data: "industry reports / market size data available"
      has_technical_depth: "involves technical workflows / prompts"
      has_creative_element: "involves creative/artistic output"

  step_3_recommend:
    rules:
      - if has_tools: activate prompt_engineer
      - if has_brand_angle: activate brand_specialist
      - always: generate 2+ personas from user_segments
```

### 示例：不同种子词的推荐结果

| 种子词 | 域类型 | 推荐 Agent | 推荐 Persona |
|--------|--------|-----------|-------------|
| AI UGC Ads | tech + marketing | Prompt 工程师 + 品牌专家 | 大学生创作者 + 专业创作者 |
| AI headshots | tech + creative | Prompt 工程师 | 求职者 + 社媒博主 |
| SaaS pricing page | business + marketing | 品牌专家 | SaaS 创始人 + 产品经理 |
| AI video for education | tech + education | Prompt 工程师 | 教师 + 学生 |
| TikTok content strategy | marketing + creative | 品牌专家 | 个人创作者 + 小企业主 |

---

## 降级策略

| 场景 | 检测方式 | 降级方式 |
|------|---------|---------|
| 某个 Agent 超时 | Task tool 返回超时 | 跳过该 Agent，用剩余 Agent 输出继续；在报告中标注缺席 Agent |
| Agent 输出格式错误 | JSON 解析失败 | 尝试从文本中提取关键信息；如完全无法解析则跳过 |
| DataForSEO 额度不足 | API 返回 402/429 | 降级为 WebSearch 估算搜索量；标记数据为 "estimated" |
| Token 预算超限 | 上下文接近上限 | 减少 Agent 数量（先去掉 Persona，再去掉推荐 Agent）|
| 所有 Agent 共识度低 | 最高 consensus_score < 0.3 | 提醒用户种子词可能过窄或过宽，建议调整后重试 |
| 去重后选题过少 (<5) | merged topics < 5 | 提醒用户，建议用 Deep 模式或扩展种子词 |
| 单 Agent 产出为 0 | findings 为空数组 | 标记为 "no findings"，不影响其他 Agent |

### 最低可运行配置

```yaml
minimum_viable_team:
  agents: 3  # 只保留固定成员
  personas: 0
  depth: "standard"
  expected_raw_topics: 15-24
  expected_final: 3-5
```

---

## 与现有架构的集成点

| 集成点 | 方式 | 说明 |
|--------|------|------|
| **growth-topic-scout** | Phase 3 调用其 DataForSEO 模块 | 复用关键词验证 + SERP 分析 + Title Lock + AEO 评分 |
| **Direction Schema** | 兼容 `DIRECTION_SCHEMA.json` + `team_metadata` 扩展 | 下游 Writer 可直接使用，忽略扩展字段不受影响 |
| **Writer 路由** | 输出 `recommended_skill` 字段 | 直接进入 Writer pipeline (blog-list-writer / blog-tutorial-writer) |
| **Smart Launcher** | 新增 "团队研究" 路由选项 | 在 Phase 0 模式选择中新增第四选项（未来实现时） |
| **PRODUCT_CATALOG.md** | Brand Specialist Agent 读取产品信息 | 通过 Read tool 在 subagent 中访问 |
| **BLOG_WRITING_PRINCIPLES_v2.md** | Content Strategist 参考写作原则 | 标题公式、评测方法论等 |
| **输出目录** | `/research 竞品分析/team-research/` | 新建子目录，不影响现有目录结构 |

### 数据流图 (v1.1)

```
research-charter.json (Phase 0, 冻结合同)
    ↓
agent_output × 5-7 (Phase 1, parallel + 各自 DataForSEO 验证)
    ↓  含 abstract + competitor_map + data_validation
merged_topics + Similarity Matrix + Coverage Map (Phase 2, CEO 决策)
    ↓
补充验证 + Title Lock + AEO 评分 (Phase 3, 仅补充未验证的)
    ↓
team-directions.json + Decision Brief + Handoff Pack (Phase 4)
    ↓ (兼容 Direction Schema, Handoff Pack 可直接喂 Writer)
Writer Pipeline (blog-list-writer / blog-tutorial-writer / case-roundup-writer)
    ↓
Editor → AEO → 发布
```

---

## 未来升级路径

### v2.0 — Agent 间对话 (依赖 Tier 2 Agent Teams)

```yaml
v2_capabilities:
  - agent_debate: "Agent 间可直接对话，质疑其他 Agent 的发现"
  - cross_validation: "Agent A 验证 Agent B 的证据"
  - self_organization: "Agent 可自行决定探索方向"
  - delegate_mode: "Orchestrator 只协调不执行"

v2_prerequisites:
  - Claude Code Agent Teams 功能稳定
  - Tier 2 subagent 支持 agent-to-agent 通信
```

### v1.1 — 当前版本 (PRD 批判性吸收)

```yaml
v1_1_changes:  # 已在本文档中实现
  - research_charter: "冻结合同，执行中不可变"
  - distributed_validation: "每个 Agent 自带 DataForSEO 验证"
  - ceo_model: "Orchestrator 只决策不执行"
  - similarity_matrix: "基于 Abstract 的 Agent 间相似度分析"
  - coverage_map: "选题维度覆盖矩阵"
  - decision_brief: "Top 1-3 方向的决策简报"
  - handoff_pack: "可直接喂给 Writer 的创作包"
  - lens_prompts: "Agent 提示词用 Lens 思维重写"
  - quality_gates: "Agent 输出 Non-Negotiables"
  - upgraded_ranking: "新增 freshness + brand_fit + risk_penalty"
```

### v1.2 — 下一步增强 (无需新能力)

```yaml
v1_2_enhancements:
  - competitive_anchoring: "可选提供竞品 URL，Agent 在分析中参考"
  - historical_context: "读取之前的 team-research 报告，避免重复选题"
  - batch_mode: "一次运行多个种子词的团队研究"
  - custom_agent_templates: "用户可定义自定义 Agent 角色"
```

---

## 实现检查清单 (供开发阶段使用)

### 文件创建清单

| 文件 | 位置 | 用途 |
|------|------|------|
| `SKILL.md` | `/skills/core/agent-team-scout/` | Skill 定义 (基于本规范转化) |
| `RESEARCH_CHARTER_SCHEMA.json` | `/skills/core/agent-team-scout/` | research-charter.json 的 JSON Schema (v1.1, renamed from TEAM_MISSION) |
| `AGENT_OUTPUT_SCHEMA.json` | `/skills/core/agent-team-scout/` | agent_output v1.1 的 JSON Schema (含 abstract + competitor_map + data_validation) |
| `REPORT_TEMPLATE.md` | `/skills/core/agent-team-scout/` | 02-team-research-report.md 模板 |
| `DECISION_BRIEF_TEMPLATE.md` | `/skills/core/agent-team-scout/` | 06-decision-brief.md 模板 (v1.1 NEW) |
| `CHANGELOG.md` | `/skills/core/agent-team-scout/` | 版本变更日志 |

### 不动的文件

| 文件 | 原因 |
|------|------|
| CLAUDE.md | 等实现完成后再更新 Skills 表 |
| growth-topic-scout/SKILL.md | 不修改，只调用其 DataForSEO 模块 |
| DIRECTION_SCHEMA.json | 不修改，team_metadata 作为扩展字段 |
| .claude/agents/ | 不创建 agent 定义文件（v1.0 用 Task tool prompt，不用 agent 文件）|

### 验证检查 (v1.1)

| 检查项 | 验证方法 | 通过标准 |
|--------|---------|---------|
| Phase 0 → 1 数据链 | research-charter.json 包含所有 agent 定义 | 每个 agent 有 id, role, tools, dataforseo_budget, quota |
| Phase 1 Agent 输出 | 每个 agent_output 符合 v1.1 schema | JSON 含 abstract + competitor_map + data_validation |
| Phase 1 数据验证 | 每个 Agent 的 data_validation.keywords_checked 非空 | 至少 1 条验证记录 |
| Phase 2 Similarity Matrix | 所有 Agent 对的相似度已计算 | 矩阵完整，高重合对已标记 |
| Phase 2 Coverage Map | 覆盖矩阵已生成 | 空白区域已分析 |
| Phase 2 → 3 数据链 | merged_topics 包含 validated_keywords | 可区分已验证/未验证关键词 |
| Phase 3 → 4 数据链 | team-directions.json 兼容 Direction Schema | 标准字段 + v1.1 扩展字段全部存在 |
| Phase 4 Decision Brief | 06-decision-brief.md 包含 Top 1-3 | 每个有 为什么值得/为什么现在/风险/下一步 |
| Phase 4 Handoff Pack | 07-handoff-pack/ 包含 Top 1-3 方向 | 每个有 brief + outline + prompt-kit |
| 智能分配覆盖 | 至少测试 5 种不同领域的种子词 | 推荐结果合理，无遗漏固定成员 |
| 降级策略 | 模拟 Agent 超时/输出错误 | 不崩溃，报告标注缺失 |
| 并行执行 | 7 个 Task tool 同时调用 | 全部返回结果，无互相阻塞 |

---

## 附录 A: 完整 Agent 提示词变量表

| 变量 | 来源 | 说明 |
|------|------|------|
| `{seed}` | research-charter.json | 种子词 |
| `{language}` | research-charter.json → scope.language | 目标语言 |
| `{geo}` | research-charter.json → scope.geo | 目标地区 |
| `{topic_quota}` | research-charter.json → team.agents[].topic_quota | 该 Agent 的选题配额 |
| `{agent_output_schema}` | AGENT_OUTPUT_SCHEMA.json (v1.1) | Agent 输出 JSON Schema (含 abstract + competitor_map + data_validation) |
| `{product_catalog_summary}` | PRODUCT_CATALOG.md 摘要 | 产品列表 (品牌专家专用) |
| `{persona.name}` | research-charter.json → persona_config.name | Persona 名称 |
| `{persona.traits}` | research-charter.json → persona_config.traits | Persona 特征 |
| `{persona.search_patterns}` | research-charter.json → persona_config.search_patterns | 搜索习惯 |
| `{persona.pain_points}` | research-charter.json → persona_config.pain_points | 痛点 |

---

## 附录 B: Task Tool 调用示例

```
// Phase 1: Orchestrator 发送单条消息，并行调用所有 Agent

Task(
  description: "Topic Researcher agent",
  subagent_type: "general-purpose",
  prompt: "{topic_researcher 完整提示词，含种子词和输出 schema}"
)

Task(
  description: "Content Strategist agent",
  subagent_type: "general-purpose",
  prompt: "{content_strategist 完整提示词}"
)

Task(
  description: "Market Analyst agent",
  subagent_type: "general-purpose",
  prompt: "{market_analyst 完整提示词}"
)

// ... 以此类推，所有 Task 在同一条消息中发出
// Claude Code 会并行执行所有 Task
```

注意：
- `subagent_type` 统一使用 `"general-purpose"`（需要 WebSearch / WebFetch / Read 能力）
- 每个 subagent 的 `prompt` 包含完整的角色定义和输出 schema
- 不使用 `.claude/agents/` 文件（v1.0 设计决策：保持简单）

---

## 附录 C: 成本预估汇总 (v1.1 — 分布式验证架构)

| 阶段 | Token 消耗 | 外部 API 费用 | 时间 |
|------|-----------|-------------|------|
| Phase 0: Charter | ~2K tokens | $0.00 | 1-2 min (含用户问答) |
| Phase 1: Exploration + Agent DataForSEO | ~35-55K tokens (6-8 agents) | ~$0.53 (7 agents × ~5 calls × $0.015) | 3-5 min (并行) |
| Phase 2: CEO Synthesis + Similarity | ~8-12K tokens | $0.00 | 2-3 min |
| Phase 3: 补充验证 + Title Lock | ~3-5K tokens | ~$0.17 (~10 补充 + ~10 SERP) | 1-2 min |
| Phase 4: Output + Handoff Pack | ~8-12K tokens | $0.00 | 2-3 min |
| **总计 (Standard)** | **~56-86K tokens** | **~$0.70** | **~10-15 min** |
| **总计 (Deep)** | **~90-130K tokens** | **~$1.00-1.20** | **~15-22 min** |

#### v1.0 → v1.1 成本变化

| 成本项 | v1.0 | v1.1 | 变化 |
|--------|------|------|------|
| Phase 1 DataForSEO | $0.00 | ~$0.53 | +$0.53 (Agent 自验证) |
| Phase 3 DataForSEO | ~$0.33-0.49 | ~$0.17 | -$0.20 (仅补充) |
| **总 DataForSEO** | **~$0.33-0.49** | **~$0.70** | +$0.25 avg |
| Token (Similarity+Coverage) | — | +~3K | 略增 |
| Token (Handoff Pack) | — | +~3K | 略增 |

**结论**: 总成本略增 (~+$0.25)，但每个方向的数据可靠性显著提升（每个 Agent 的选题都有数据支撑，而非仅 Top 15-20 被验证）。

对比：
- 单 Agent Scout (Mode D1): ~15-25K tokens, ~$0.47, 45-60 min
- Team Scout v1.1: ~56-86K tokens, ~$0.70, 10-15 min
- **核心优势**: 时间缩短 3-4x（并行），产出增加 3-5x，数据验证覆盖率从 Top 15-20 扩展到全部 Agent 输出
