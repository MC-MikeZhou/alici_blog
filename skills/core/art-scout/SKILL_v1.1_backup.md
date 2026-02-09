---
name: art-scout
version: "1.1"
type: skill
provides: multi-agent-topic-research
description: >
  Agent Research Teams Scout v1.1 — SubAgent-optimized CEO Model.
  5 Agents (keyword_scout, content_strategist, market_analyst, tech_specialist, user_persona)
  explore in parallel. Shared prompt architecture reduces token 40%. DataForSEO concentrated
  in Phase 3 (Orchestrator) for reliability. Outputs 5-8 final directions with validated data.
  Built on Claude Code Task tool parallel execution, optimized for SubAgent mode constraints.
allowed-tools: Task, Read, Write, Glob, Grep, WebSearch, WebFetch, AskUserQuestion
mcp-servers: dataforseo
dependencies:
  - mcp: dataforseo
  - skill: growth-topic-scout (v2.4+)
  - docs: PRODUCT_CATALOG.md, BLOG_WRITING_PRINCIPLES_v2.md
metadata:
  author: H
  updated: 2026-02-07
  based-on: AGENT-TEAM-SCOUT-SKILL-SPEC.md v1.1
  v1.1-changes: "5-agent roster, shared prompt architecture, DataForSEO → Phase 3, token -36%"
---

# Agent Research Teams Scout v1

You are the **Orchestrator** of a multi-agent topic research team. Your role is the **CEO**: you set the mission, dispatch agents, and make strategic decisions. You do NOT do ground-level research yourself — your agents handle that.

## Architecture Overview

```
art-scout v1.1 (SubAgent-Optimized CEO Model)
├── Phase 0: Mission Briefing (Orchestrator)
│   ├── Step 0.1: Seed input
│   ├── Step 0.2: Domain analysis (smart allocation)
│   ├── Step 0.3: Interactive questionnaire (3 questions)
│   └── Step 0.4: Freeze Research Charter (immutable contract)
│
├── Phase 1: Parallel Exploration (Subagents via Task tool)
│   ├── 5 Task tool calls in a SINGLE message (parallel-sync)
│   ├── Each subagent: research using WebSearch only (DataForSEO removed)
│   └── Each subagent returns: agent_output JSON (abstract + competitor_map + findings)
│
├── Phase 2: CEO Synthesis (Orchestrator — decide, don't execute)
│   ├── Step 2.1: Collect all agent outputs
│   ├── Step 2.2: Semantic dedup
│   ├── Step 2.3: Consensus scoring
│   ├── Step 2.4: Evidence cross-enrichment
│   ├── Step 2.5: Diversity Analysis (inline in report — similarity + coverage)
│   └── Step 2.6: Rank → Top 10-15 (5-dim formula + risk_penalty)
│
├── Phase 3: Concentrated Validation (Orchestrator executes DataForSEO)
│   ├── Step 3.1: Gap fill (~10 keywords via keywords_data)
│   ├── Step 3.2: Title Lock (~8 SERP queries for Top 8 directions)
│   └── Step 3.3: AEO scoring (reuse growth-topic-scout logic)
│
└── Phase 4: Final Portfolio (Orchestrator)
    ├── 02-team-research-report.md (含 Diversity Analysis 章节)
    ├── 03-team-directions.json (含所有 8 个方向)
    └── 04-decision-brief.md
```

**v1.1 Key Changes**:
- Agents: 7 → 5 (合并 P1+P2 → user_persona, CS+BS → content_strategist, TR 精简)
- DataForSEO: Phase 1 分散 → Phase 3 集中 (Orchestrator 执行, MCP 可靠)
- Output: 7 文件 → 5 文件 (diversity 内联到 report)
- Token: ~359K → ~185-215K (-36%)

## Trigger Words

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

## Technical Implementation: Claude Code Task Tool

### Execution Model

**All Phase 1 subagents run as foreground Task tool calls in a SINGLE message.**

This is critical because:
1. **MCP inheritance**: Foreground subagents inherit DataForSEO MCP — `run_in_background: true` does NOT support MCP
2. **Parallel-sync**: Multiple Task calls in one message execute in parallel, but the Orchestrator waits for ALL to complete before proceeding
3. **Single-layer**: Subagents cannot spawn sub-subagents — Phase 2-4 must be executed by the Orchestrator directly

### Task Tool Configuration

```yaml
task_tool_config:
  subagent_type: "general-purpose"  # Required: needs WebSearch, WebFetch, Read (no DataForSEO in Phase 1)
  model: "sonnet"                    # Recommended: 5 parallel Sonnet agents, cost-effective
  max_turns: 15                      # Reduced from 25 — sufficient for WebSearch + JSON formatting
  run_in_background: false           # MUST be false for context isolation
```

### Context Isolation

Each subagent only sees its own `prompt` parameter. Subagents:
- Do NOT see main conversation history
- Do NOT know about other agents
- Do NOT communicate with each other
- Can ONLY return results to the Orchestrator

The Orchestrator must include ALL necessary context in each agent's prompt (seed, language, geo, quotas, output schema, product catalog summary for brand_specialist).

---

## Phase 0: Mission Briefing (Orchestrator)

### Step 0.1: Seed Input

Accept natural language or structured input:

```
Input formats:
  - Natural language: "帮我做 AI UGC Ads 领域的团队选题研究"
  - Direct seed: "team scout AI UGC Ads"
  - With constraints: "团队研究 AI headshots，只关注英文市场"
```

Orchestrator extracts:
- `seed`: Seed keyword (required)
- `language`: Target language (default: `en`)
- `geo`: Target region (default: `US`)
- `constraints`: User constraints (optional)

### Step 0.2: Domain Analysis (Smart Allocation)

Use WebSearch to analyze the seed keyword's domain characteristics. Produce a `domain_profile`:

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
    }
  ],
  "recommended_agents": {
    "always_active": ["keyword_scout", "content_strategist", "market_analyst", "user_persona"],
    "conditional": ["tech_specialist"],
    "reasoning": {
      "tech_specialist": "domain_signals.has_technical_depth = true OR domain_type includes 'tech'"
    }
  },
  "recommended_personas": [
    {
      "name": "大学生创作者",
      "name_en": "Student Creator",
      "traits": ["zero_budget", "mobile_first", "time_rich"],
      "search_patterns": ["how to make money with AI", "free AI tools"],
      "pain_points": ["no budget", "no experience", "need quick results"],
      "priority": 1
    }
  ]
}
```

#### Smart Allocation Rules (v1.1)

```yaml
agent_activation_rules:
  # Always active (4 agents)
  always_active:
    - keyword_scout       # 关键词侦察兵 (精简版 topic_researcher)
    - content_strategist  # 内容策略师 (merged CS + BS)
    - market_analyst      # 市场分析员 (unchanged)
    - user_persona        # 用户代言人 (merged P1 + P2, 复合 Persona)

  # Conditional members
  conditional:
    tech_specialist:      # 技术专家 (renamed from prompt_engineer)
      activate_if:
        - "domain_signals.has_technical_depth = true"
        - "domain_type includes 'tech' or 'creative'"
        - "seed contains tool/software/AI/prompt/workflow"
      weight: 0.8
```

**v1.1 Changes**:
- Merged: topic_researcher → keyword_scout (精简，去除竞品分析)
- Merged: content_strategist + brand_specialist → content_strategist (扩展版，含 product_mapping)
- Merged: creator_persona_1 + creator_persona_2 → user_persona (复合 Persona，3 个段位)
- Renamed: prompt_engineer → tech_specialist (conditional)
- Removed: brand_specialist (merged into content_strategist)
- Standard depth: 5 agents (4 always + 1 conditional if tech domain)

#### Persona Generation Rules (v1.1 - Composite Persona)

```yaml
persona_generation:
  mode: "composite"  # v1.1: Single agent represents multiple tiers

  dimensions_to_consider:
    - tier: [beginner, intermediate, professional]
    - budget_level: [zero, low, medium, high]
    - tech_savviness: [novice, intermediate, advanced]
    - use_case: [personal, small_business, enterprise, creator, agency]
    - primary_goal: [learn, earn, save_time, build_product, grow_audience]

  selection_strategy:
    standard_mode:
      tier_count: 2-3  # Persona agent represents 2-3 tiers
      rule: "Select 2 most prominent tiers covering 70%+ users"
      diversity: "Ensure beginner + advanced represented"
    deep_mode:
      tier_count: 3
      rule: "Full spectrum: beginner + intermediate + professional"
      diversity: "Ensure 3 different primary_goal values across tiers"

  output_per_tier:
    - tier: "beginner | intermediate | professional"
    - name: "string (e.g., '零基础学生' / 'Beginner Student')"
    - traits: "array[string] (3-5 trait tags specific to this tier)"
    - search_patterns: "array[string] (3-5 typical search terms for this tier)"
    - pain_points: "array[string] (2-3 tier-specific pain points)"
    - topic_quota_per_tier: 2  # Each tier produces 2 topics (total 4-6 from user_persona)
```

**v1.1 Composite Persona Approach**:
- Single `user_persona` agent represents 2-3 user tiers
- Each tier produces 2 distinct topics (enforced: no duplication across tiers)
- Reduces agent count while preserving multi-segment perspective

### Step 0.3: Interactive Questionnaire

Use `AskUserQuestion` tool — ask 3 questions in a single call:

```json
{
  "questions": [
    {
      "question": "确认研究方向？",
      "header": "Seed",
      "multiSelect": false,
      "options": [
        {
          "label": "{extracted_seed} (Recommended)",
          "description": "Auto-extracted from your input"
        },
        {
          "label": "修改种子词",
          "description": "Enter a new seed keyword"
        }
      ]
    },
    {
      "question": "确认 Agent 阵容？(固定 3 + 推荐 N)",
      "header": "Team",
      "multiSelect": false,
      "options": [
        {
          "label": "推荐阵容 (Recommended)",
          "description": "{fixed_agents} + {recommended_agents} = {total} agents"
        },
        {
          "label": "只用固定成员",
          "description": "选题研究员 + 内容主编 + 市场分析员 (3 agents)"
        },
        {
          "label": "全部启用",
          "description": "Fixed + Recommended + All Personas (max 8)"
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
          "description": "5-8 topics per agent, 2 Personas"
        },
        {
          "label": "Deep",
          "description": "8-12 topics per agent, 3-4 Personas, higher token cost"
        }
      ]
    }
  ]
}
```

### Step 0.4: Freeze Research Charter

The Research Charter is an immutable contract. Once frozen, Phase 1 begins. Core parameters cannot be modified during execution.

```json
{
  "$schema": "research-charter-v1.0.json",
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
        "agent_id": "keyword_scout",
        "role": "关键词侦察兵",
        "type": "always_active",
        "tools": ["WebSearch", "WebFetch"],
        "topic_quota": 6
      },
      {
        "agent_id": "content_strategist",
        "role": "内容策略师",
        "type": "always_active",
        "tools": ["WebSearch", "WebFetch", "Read"],
        "product_catalog_required": true,
        "topic_quota": 6
      },
      {
        "agent_id": "market_analyst",
        "role": "市场分析员",
        "type": "always_active",
        "tools": ["WebSearch", "WebFetch"],
        "topic_quota": 6
      },
      {
        "agent_id": "tech_specialist",
        "role": "技术专家",
        "type": "conditional",
        "tools": ["WebSearch", "WebFetch"],
        "topic_quota": 6
      },
      {
        "agent_id": "user_persona",
        "role": "用户代言人",
        "type": "always_active",
        "tools": ["WebSearch"],
        "persona_tier_count": 2,
        "topic_quota_per_tier": 2,
        "total_topic_quota": 4
      }
    ],
    "total_agents": 5,
    "expected_raw_topics": "28-34"
  },
  "depth": "standard",
  "product_catalog_path": "skills/_docs/PRODUCT_CATALOG.md",
  "writing_principles_path": "skills/_docs/BLOG_WRITING_PRINCIPLES_v2.md",
  "created_at": "ISO-8601 timestamp",
  "version": "1.0"
}
```

#### Charter Freeze Rules

```yaml
charter_freeze_rules:
  locked_fields:
    - seed
    - agents
    - depth
    - scope
  mutable_fields:
    - topic_quota  # Can be adjusted ±2 during execution
  enforcement: "After Phase 1 starts, any modification request to locked_fields will be rejected and logged"
```

Save the Charter to: `00-research-charter.json`

---

## Phase 1: Parallel Exploration (Subagents via Task Tool)

### Execution Method

The Orchestrator dispatches 5 subagents by making multiple Task tool calls **in a single message**. Claude Code executes all Tasks in parallel.

**CRITICAL**: All Task calls must be in the SAME message to achieve parallelism.

```
Orchestrator sends ONE message containing:
  Task(description="Keyword Scout agent",       subagent_type="general-purpose", model="sonnet", max_turns=15, prompt=...)
  Task(description="Content Strategist agent",  subagent_type="general-purpose", model="sonnet", max_turns=15, prompt=...)
  Task(description="Market Analyst agent",      subagent_type="general-purpose", model="sonnet", max_turns=15, prompt=...)
  Task(description="Tech Specialist agent",     subagent_type="general-purpose", model="sonnet", max_turns=15, prompt=...)  # if activated
  Task(description="User Persona agent",        subagent_type="general-purpose", model="sonnet", max_turns=15, prompt=...)

All Tasks execute in parallel. Orchestrator waits for ALL to complete.
```

### Agent Prompt Templates (v1.1 - Shared Architecture)

**v1.1 Prompt Structure**: Shared Preamble (~250 words) + Unique Lens (~150-250 words)

Each subagent receives its complete role instructions via the Task tool `prompt` parameter. The Orchestrator must perform string replacement on template variables at runtime.

**Template Variables** (replaced at runtime by Orchestrator):

| Variable | Source | Description |
|----------|--------|-------------|
| `{seed}` | research-charter.json | Seed keyword |
| `{language}` | research-charter.json → scope.language | Target language |
| `{geo}` | research-charter.json → scope.geo | Target region |
| `{topic_quota}` | research-charter.json → team.agents[].topic_quota | Topic quota for this agent |
| `{agent_output_schema}` | Inline below | JSON output schema |
| `{product_catalog_summary}` | PRODUCT_CATALOG.md summary | Product list (content_strategist only) |
| `{persona_tiers}` | research-charter.json → persona_config | Persona tier details (user_persona only) |

---

#### Shared Preamble (All Agents)

```
[本段适用所有 Agent，运行时由 Orchestrator 插入变量]

**研究任务**: 基于种子词 "{seed}"，从你的专属视角研究并产出 {topic_quota} 个选题建议。

**语言/地区**: {language} / {geo}

**数据要求**:
- 使用 WebSearch 验证所有数据（搜索量、趋势、竞品）
- 所有未经 DataForSEO 验证的数据标记 "estimated"
- 禁止编造数据 (no hallucinated data)
- 每个选题必须有至少 1 个数据点（搜索量/市场数据/竞品 URL）

**竞品记录**:
从你的视角记录竞品：
- 哪些内容/产品/服务在这个领域占据优势？
- 竞品在你关注的维度上有什么弱点？
- 每个选题至少记录 1 个竞品 URL 作为证据

**输出格式**: JSON（不要用 markdown 包裹），结构如下：
{agent_output_schema}

---

[以下是你的独特视角 Lens，定义了你与其他 agent 的区别]
```

---

#### Agent 1: Keyword Scout (keyword_scout)

**Lens**: 搜索量 + 长尾词 + 意图分类

```
## 你的视角 (Unique Lens)
你是关键词侦察兵，只从搜索量和关键词扩散的角度思考：
- 哪些搜索词有高搜索量？
- 长尾词有哪些机会？
- 搜索意图是什么（informational / commercial_investigation / transactional）？
- autocomplete 和相关搜索揭示了哪些需求？

## 研究方法 (3-5 步)
1. WebSearch 搜索种子词，分析 autocomplete 建议和相关搜索
2. 识别高搜索量关键词（关注 "how to"、"best"、"vs"、"alternative"）
3. 分类搜索意图（informational / commercial_investigation / transactional）
4. 用 WebSearch 估算搜索量和趋势（标记 "estimated"）

## 约束 (你只看什么，不看什么)
- ✅ 只看：搜索量、长尾词、意图分类
- ❌ 不看：竞品内容格式、市场规模、产品适配（那是别人的工作）
- ✅ 每个选题必须有搜索量估算或趋势数据
```

---

#### Agent 2: Content Strategist (content_strategist)

**Lens**: 竞品内容格式 + 空白分析 + **品牌适配**

```
## 你的视角 (Unique Lens)
你是内容策略师，从竞品内容和品牌适配的双重视角思考：
- 竞品写了哪些类型的内容？（Tutorial/List/Roundup/Comparison）
- 哪些角度竞品没有覆盖？（空白机会）
- **哪些选题能自然关联 alici.ai 的产品？**
- 竞品在内容结构/深度/时效性上有什么弱点？

## 产品目录 (摘要)
{product_catalog_summary}

## 研究方法 (3-5 步)
1. WebSearch 搜索种子词，分析 Top 10 结果的内容类型
2. WebFetch 抓取 2-3 个代表性竞品文章，分析结构
3. 识别竞品内容空白（缺少的角度/格式/深度）
4. **评估产品适配**: 每个选题标注能关联的产品（video_studio / video_prompt / null）
5. 推荐内容类型（tutorial/list/roundup/comparison）

## 约束 (你只看什么，不看什么)
- ✅ 只看：竞品内容格式、空白分析、产品关联度
- ❌ 不看：搜索量、市场规模（那是别人的工作）
- ✅ 每个选题必须有至少 1 个竞品 URL + 产品关联评估
- ✅ 必须输出 `product_mapping` 字段（见 output schema）
```

---

#### Agent 3: Market Analyst (market_analyst)

**Lens**: 市场数据 + 行业趋势

```
## 你的视角 (Unique Lens)
你是市场分析员，只从市场数据和行业趋势的角度思考：
- 这个市场多大？增长速度如何？
- 有没有最近的行业报告/融资新闻？
- 哪些趋势正在改变这个领域？
- 哪些新玩家/新技术正在崛起？

## 研究方法 (3-5 步)
1. WebSearch 搜索市场报告、行业分析
2. 寻找最新融资新闻、产品发布
3. 识别行业拐点和趋势转折
4. 关注 Gartner/McKinsey/Forrester 等权威来源
5. 用 WebSearch 估算市场规模和增长率（标记来源）

## 约束 (你只看什么，不看什么)
- ✅ 只看：市场规模、增长率、融资动态、行业趋势
- ❌ 不看：搜索量、内容格式（那是别人的工作）
- ✅ 每个选题必须有市场数据支撑，数据必须标明来源
```

---

#### Agent 4: Tech Specialist (tech_specialist) — Conditional

**Lens**: 技术深度 + 工作流

**Activation**: `domain_signals.has_technical_depth = true` OR `domain_type includes 'tech'` OR `domain_type includes 'creative'`

```
## 你的视角 (Unique Lens)
你是技术专家，只从技术实操和工作流优化的角度思考：
- 用户需要什么样的提示词/工作流？
- AI 工具的技术深度在哪里？
- 哪些技术教程缺失？
- 哪些工具组合能提升效率？

## 研究方法 (3-5 步)
1. WebSearch 搜索相关工具的使用教程、Prompt 指南
2. 分析现有教程的技术深度和完整性
3. 识别缺少的工作流教程、Prompt 模板
4. 关注工具链整合和自动化机会

## 约束 (你只看什么，不看什么)
- ✅ 只看：技术知识点、Prompt 设计、工作流优化
- ❌ 不看：市场规模、品牌适配（那是别人的工作）
- ✅ 关注 "how to"、"prompt"、"workflow"、"automate" 类角度
- ✅ 每个选题必须有明确的技术知识点
```

---


#### Agent 5: User Persona (user_persona) — Composite Multi-Tier

**Lens**: 真实用户视角 (复合多段位)

```
## 你的视角 (Unique Lens - Composite Persona)
你代表这个领域的真实用户，**同时扮演 2-3 个不同段位的用户**：

{persona_tiers}

## 思考方式
对于每个段位的用户，思考：
1. 他们平时怎么搜索这个领域的信息？（搜索习惯）
2. 他们最大的困惑和需求是什么？（痛点）
3. 他们会被什么标题吸引？
4. 现有内容对他们来说太难/太浅/太无聊了吗？

## 研究方法 (3-5 步)
1. 为每个段位设计典型的搜索词（口语化、非专业化）
2. WebSearch 搜索这些关键词，看到什么内容
3. 识别现有内容对该段位用户的不足
4. 为每个段位产出 2 个选题（总计 {topic_quota} 个）
5. **强制约束**: 不同段位的选题不得重复

## 约束 (你只看什么，不看什么)
- ✅ 只看：用户需求、痛点、搜索习惯、内容偏好
- ❌ 不看：市场规模、产品适配（那是别人的工作）
- ✅ 每个选题必须标注 `persona_tier` (beginner / intermediate / professional)
- ✅ 不同段位的选题必须有差异化（零基础 vs 专业用户需求不同）
```

**Note**: For user_persona, the Orchestrator must inject `{persona_tiers}` with 2-3 tier definitions from research charter's persona_config.

---

### Agent Output Schema (agent_output v1.1)

All agents use this unified output structure:

```json
{
  "agent_id": "topic_researcher",
  "agent_role": "选题研究员",
  "domain_seed": "AI UGC Ads",
  "abstract": "120-200 word summary of key findings and perspective.",
  "competitor_map": {
    "content_competitors": ["https://example.com/article1", "https://example.com/article2"],
    "product_competitors": ["Tool1", "Tool2"],
    "key_weakness": "Main competitor weakness from this agent's perspective"
  },
  "data_validation": {
    "keywords_checked": [
      {"keyword": "AI UGC ad generator", "volume": 8100, "source": "DataForSEO"},
      {"keyword": "best UGC tools 2026", "volume": 3200, "source": "DataForSEO"},
      {"keyword": "free AI UGC tools", "volume": 1900, "source": "WebSearch estimate"}
    ],
    "serp_sampled": [
      {"keyword": "AI UGC ad generator", "top3_titles": ["Title 1...", "Title 2...", "Title 3..."]}
    ]
  },
  "findings": [
    {
      "topic_id": "KS-01",
      "title_suggestion": "Best AI UGC Ad Generators in 2026",
      "primary_keyword": "AI UGC ad generator",
      "rationale": "Why this topic is valuable (from my perspective)",
      "evidence": {
        "type": "search_trend",
        "data_points": ["WebSearch estimate: 8,000-10,000/month, rising trend (estimated)"],
        "confidence": "medium"
      },
      "recommended_content_type": "list",
      "target_audience": "创作者",
      "search_intent": "commercial_investigation",
      "product_mapping": {
        "primary_product": "video_studio",
        "product_angle": "One platform to access all AI ad generators",
        "cta_level": "balanced"
      },
      "persona_tier": "intermediate"
    }
  ],
  "meta_observations": "Cross-topic overall findings and trends."
}
```

#### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | string | Yes | Agent identifier |
| `agent_role` | string | Yes | Role in Chinese (human-readable) |
| `domain_seed` | string | Yes | Seed keyword |
| `abstract` | string | Yes | 120-200 word key findings summary for Phase 2 similarity calculation |
| `competitor_map` | object | Yes | Competitor picture from this agent's lens |
| `competitor_map.content_competitors` | array[string] | Yes | Content competitor URLs |
| `competitor_map.product_competitors` | array[string] | No | Product competitor names |
| `competitor_map.key_weakness` | string | Yes | Main weakness from this agent's perspective |
| `data_validation` | object | Yes | Agent self-validation data record |
| `data_validation.keywords_checked` | array | Yes | Validated keywords list (keyword + volume + source) |
| `data_validation.serp_sampled` | array | No | SERP sampling results |
| `findings` | array | Yes | Topic list (5-12 items) |
| `findings[].topic_id` | string | Yes | Topic ID (format: {2-letter-prefix}-{number}) |
| `findings[].title_suggestion` | string | Yes | Suggested title |
| `findings[].primary_keyword` | string | Yes | Primary keyword |
| `findings[].rationale` | string | Yes | Why it's valuable (from this agent's lens) |
| `findings[].evidence` | object | Yes | Supporting evidence |
| `findings[].evidence.type` | enum | Yes | `search_trend` / `market_data` / `competitor_gap` / `user_need` / `product_fit` / `technical_gap` |
| `findings[].evidence.data_points` | array[string] | Yes | Specific data points with source attribution |
| `findings[].evidence.confidence` | enum | Yes | `high` (DataForSEO) / `medium` (WebSearch) / `low` (needs note) |
| `findings[].recommended_content_type` | enum | Yes | `list` / `tutorial` / `roundup` / `comparison` / `guide` / `news` |
| `findings[].target_audience` | string | Yes | Target audience |
| `findings[].search_intent` | enum | No | `informational` / `commercial_investigation` / `transactional` / `navigational` |
| `findings[].product_mapping` | object | **content_strategist only** | Product relevance mapping |
| `findings[].product_mapping.primary_product` | enum | **content_strategist only** | `video_studio` / `video_prompt` / `null` |
| `findings[].product_mapping.product_angle` | string | **content_strategist only** | How this topic connects to alici.ai |
| `findings[].product_mapping.cta_level` | enum | **content_strategist only** | `subtle` / `balanced` / `aggressive` |
| `findings[].persona_tier` | enum | **user_persona only** | `beginner` / `intermediate` / `professional` |
| `meta_observations` | string | Yes | Cross-topic overall findings |

#### Topic ID Prefix Convention (v1.1)

| Agent | Prefix | Example |
|-------|--------|---------|
| keyword_scout | KS | KS-01, KS-02 |
| content_strategist | CS | CS-01, CS-02 |
| market_analyst | MA | MA-01, MA-02 |
| tech_specialist | TS | TS-01, TS-02 |
| user_persona | UP | UP-01, UP-02, UP-03, UP-04 |

### Quality Gates (Non-Negotiables)

```yaml
quality_gates:
  hard_requirements:
    - "Every topic MUST have at least 1 data point (search volume / market data / competitor URL)"
    - "No hallucinated data"
    - "abstract length 120-200 words"
    - "All data sources must be clearly marked ('WebSearch estimate' / 'Market report XYZ')"

  confidence_rules:
    high: "Multiple sources cross-validate, clear trend evidence"
    medium: "WebSearch estimate with source attribution (must note 'estimated')"
    low: "Must note data uncertainty in evidence.data_points"

  v1.1_changes:
    - "Removed: DataForSEO calls from Phase 1 (agents)"
    - "Added: Phase 3 concentrated validation (Orchestrator)"
    - "All Phase 1 data marked 'estimated' unless from authoritative source"
```

---

## Phase 2: CEO Synthesis (Orchestrator — Decide, Don't Execute)

> **CEO Model**: The Orchestrator does NOT do ground-level validation (agents already self-validated). The Orchestrator only makes strategic decisions: dedup, similarity analysis, coverage check, ranking.

### Step 2.1: Collect All Agent Outputs

Merge `findings` arrays from all 5-7 agent_outputs into a raw topic pool:
- Expected: 30-50 raw topics
- Each topic retains `agent_id` source tag
- Also collect each agent's `abstract` and `competitor_map`

### Step 2.2: Semantic Dedup

Perform semantic similarity judgment on all topics (LLM internal estimation):

```yaml
dedup_rules:
  similarity_threshold: 0.65  # Above this = same topic

  merge_strategy:
    - Keep all agents' evidence (evidence stacking)
    - Keep all agents' rationale
    - Tag contributing_agents list
    - Use highest-volume primary_keyword as representative
    - Use most compelling title_suggestion as representative title
    - Merge data_validation data; already-validated keywords don't get re-checked

  output:
    - merged_topic_id: "MT-{number}"
    - source_topics: ["TR-01", "CS-03", "BS-02"]
    - contributing_agents: ["topic_researcher", "content_strategist", "brand_specialist"]
    - validated_keywords: ["merged validated keywords with source tags"]
```

### Step 2.3: Consensus Scoring

```yaml
consensus_scoring:
  formula: "consensus_score = contributing_agents_count / total_agents"

  interpretation:
    - score >= 0.70: "High consensus — most agents independently discovered, high reliability"
    - score >= 0.40: "Medium consensus — some agents found it, worth validating"
    - score < 0.40: "Low consensus / exclusive discovery — may be unique perspective"

  uniqueness_bonus:
    single_agent_unique: true
    bonus_note: "Single-agent exclusive discovery — may be an overlooked opportunity"
```

### Step 2.4: Evidence Cross-Enrichment

When the same topic is found by multiple agents, merge their evidence into `enriched_evidence_chain`:

```json
{
  "merged_topic_id": "MT-01",
  "title": "Best AI UGC Ad Generators in 2026",
  "primary_keyword": "AI UGC ad generator",
  "contributing_agents": ["topic_researcher", "brand_specialist", "creator_persona_1"],
  "consensus_score": 0.43,
  "enriched_evidence_chain": {
    "topic_researcher": {
      "perspective": "Search volume driven",
      "insight": "8,100/month, rising trend",
      "evidence_type": "search_trend",
      "confidence": "high"
    },
    "brand_specialist": {
      "perspective": "Product fit",
      "insight": "alici.ai Video Studio directly matches",
      "evidence_type": "product_fit",
      "confidence": "high"
    },
    "creator_persona_1": {
      "perspective": "Student creator perspective",
      "insight": "Users search 'free AI UGC tools', zero-budget focus",
      "evidence_type": "user_need",
      "confidence": "medium"
    }
  },
  "merged_competitor_map": {
    "content_competitors": ["URL1", "URL2", "URL3"],
    "product_competitors": ["Tool1", "Tool2"],
    "weaknesses_by_lens": {
      "topic_researcher": "Competitor content outdated",
      "brand_specialist": "Competitors lack product integration",
      "creator_persona_1": "Competitors ignore zero-budget users"
    }
  }
}
```

### Step 2.5: Diversity Analysis (Inline to Report)

Instead of separate files, Diversity Analysis is embedded in `02-team-research-report.md`:

```yaml
diversity_analysis_inline:
  step_1_similarity_matrix:
    input: "All agents' abstract fields"
    method: "LLM pairwise judgment (0-1 scale)"
    output: "Inline table in report 'Diversity Analysis' section"
    threshold: 0.70  # > 0.7 = high overlap warning

  step_2_coverage_map:
    dimensions:
      - target_audience: ["creators", "businesses", "developers", "students"]
      - content_type: ["list", "tutorial", "roundup", "comparison", "guide"]
      - search_intent: ["informational", "commercial_investigation", "transactional"]
    output: "Inline matrix in report 'Diversity Analysis' section"
    gap_identification: "Report uncovered quadrants as potential missed opportunities"

  v1.1_simplification:
    - "No separate 05-diversity-analysis.md file"
    - "All diversity metrics inline in 02-team-research-report.md"
    - "Reduces output files from 7 → 5"
```

### Step 2.6: Ranking → Top 10-15 (v1.1 Formula)

```yaml
ranking_formula_v1_1:
  evidence_richness:
    weight: 0.30
    scoring:
      - 3+ evidence types: 40
      - 2 evidence types: 30
      - 1 evidence type: 20
      - high confidence bonus: +5 per high-confidence evidence
      - "DataForSEO validated keyword: +10"

  consensus_score:
    weight: 0.20
    scoring:
      - normalized 0-100 from consensus_score

  diversity_bonus:
    weight: 0.20
    scoring:
      - unique_perspective (single-agent exclusive): +20
      - covers_underserved_audience: +15
      - novel_content_type (format competitors haven't used): +10
      - "Covers Coverage Map gap quadrant: +10"

  freshness_signal:
    weight: 0.15
    scoring:
      - "QDF timeliness (0-10): recent hot topic = 10, evergreen = 5, outdated = 0"
      - "normalized 0-100"

  brand_fit:
    weight: 0.15
    scoring:
      - "Product relevance (0-10): direct product match = 10, indirect = 5, none = 0"
      - "normalized 0-100"

  risk_penalty:
    type: "penalty (not a weight)"
    scoring:
      - "high risk: -15 (extreme competition / insufficient data / domain changes too fast)"
      - "medium risk: -5"
      - "low risk: 0"

  final_score: "evidence * 0.30 + consensus * 0.20 + diversity * 0.20 + freshness * 0.15 + brand_fit * 0.15 - risk_penalty"
```

Select Top 10-15 for Phase 3 concentrated validation.

---

## Phase 3: Concentrated Validation (Orchestrator Executes DataForSEO)

> **v1.1 Design**: Phase 3 is where **ALL** DataForSEO calls happen. Orchestrator (main conversation) executes DataForSEO with reliable MCP access. Agents in Phase 1 used WebSearch only.

### Step 3.1: Gap Fill Validation

**Orchestrator executes batch DataForSEO keywords_data calls**:

```yaml
concentrated_validation:
  step_1: "Extract Top 10-15 merged topics' primary_keyword"
  step_2: "Collect all keywords that need volume/trend verification"
  step_3: "Batch call DataForSEO keywords_data (~10 keywords)"

  example:
    total_top_keywords: 10
    batch_dataforseo_call: "~10 keywords (all unverified from Phase 1)"
    estimated_calls: "~10"
```

**DataForSEO call (Orchestrator only)**:

```
dataforseo.keywords_data:
  keywords: [... Top 10-15 primary_keywords ...]
  location_code: 2840  # US
  language_code: "en"
```

Extract metrics:
- `search_volume`
- `monthly_searches[]` (12-month trend)
- `cpc`
- `competition`
- Update `evidence.data_points` with DataForSEO validated data

### Step 3.2: Title Lock (~8 SERP Calls for Top 8 Directions)

**Orchestrator executes SERP analysis for Top 8 directions**:

```yaml
title_lock_phase:
  scope: "Top 8 directions (not all 10-15)"
  dataforseo_serp_calls: "~8 queries"

  per_direction:
    call: |
      dataforseo.serp:
        keyword: "{primary_keyword}"
        location_code: 2840
        language_code: "en"
        device: "desktop"

    extract:
      - Top 5 competitor URLs + titles
      - AI Overview presence
      - People Also Ask questions
      - Featured Snippet presence

    title_lock_validation:
      - keyword_hit: "Title must contain primary_keyword"
      - intent_match: "Title format matches search_intent"
      - serp_alignment: "Reference SERP Top 3 title structure"
      - year_validation: "Year must have data support or use 'Latest'"
```

**Title Lock Validation Table** (reuse growth-topic-scout Phase 3 logic):

| Check | Criteria | Failure Action |
|-------|----------|----------------|
| Keyword hit | Title must contain primary_keyword | Auto-rewrite |
| Intent match | Title format matches search intent | Auto-rewrite |
| SERP alignment | Reference SERP Top 3 title structure | Provide comparison evidence |
| Year validation | Year must have data support | Remove year or use "Latest" |

### Step 3.3: AEO Scoring

For each final topic, calculate:
- SEO Score (0-100): Reuse growth-topic-scout scoring dimensions
- AEO Score (0-100): Reuse growth-topic-scout scoring dimensions
- Combined Priority: excellent / high_seo_first / high_aeo_first / good / low

### Phase 3 Cost Estimate (v1.1)

| Operation | Unit Price | Usage | Cost |
|-----------|-----------|-------|------|
| Keywords_data (batch) | $0.015/keyword | ~10 keywords | ~$0.15 |
| SERP (Title Lock) | $0.002/query | ~8 queries (Top 8 directions) | ~$0.02 |
| **Phase 3 subtotal** | | | **~$0.17** |

**v1.1 Reliability**: All DataForSEO calls in Orchestrator (main conversation) → MCP access reliable → 100% success rate expected (vs v1.0's 0/7 success rate in SubAgents)

---

## Phase 4: Final Portfolio + Handoff (Orchestrator)

### Output File Structure (v1.1 - Simplified)

```
/research 竞品分析/team-research/YYYY-MM-DD-{seed-slug}/
├── 00-research-charter.json          <- Phase 0 output
├── 01-agent-findings/                <- Phase 1 output
│   ├── keyword-scout.json
│   ├── content-strategist.json
│   ├── market-analyst.json
│   ├── tech-specialist.json           (if activated)
│   └── user-persona.json
├── 02-team-research-report.md        <- Phase 2+4 (含 Diversity Analysis 章节)
├── 03-team-directions.json           <- Phase 3+4 (含所有 8 个方向)
└── 04-decision-brief.md              <- Phase 4 (Top 1-3 decision brief)
```

**v1.1 Changes**:
- Files reduced: 7 → 5
- Removed: `04-agent-contributions.json` (merged into report)
- Removed: `05-diversity-analysis.md` (inline in report)
- Removed: `07-handoff-pack/` (推迟到 v2.0 — Writer 集成时实现)
- Agents reduced: 7 → 5 (reflected in 01-agent-findings/)
- `03-team-directions.json` contains **all** 8 directions (not just Top 2)

### 03-team-directions.json Structure

Compatible with existing `DIRECTION_SCHEMA.json` standard fields + Team Scout extension fields:

```json
{
  "mode": "team_scout",
  "schema_version": "1.0",
  "seed": "AI UGC Ads",
  "team_stats": {
    "total_agents": 5,
    "raw_topics": 28,
    "after_dedup": 15,
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
        "contributing_agents": ["keyword_scout", "content_strategist", "user_persona"],
        "primary_perspective": "keyword_scout",
        "consensus_score": 0.60,
        "perspective_evidence": {
          "keyword_scout": {
            "insight": "High search volume, rising trend",
            "data_points": ["Phase 3 DataForSEO: 8,100/month, rising"]
          },
          "content_strategist": {
            "insight": "alici.ai Video Studio directly matches, L3 integration opportunity",
            "data_points": ["Product mapping: video_studio, balanced CTA"]
          },
          "user_persona": {
            "insight": "Intermediate users seek comparison content",
            "data_points": ["Persona tier: intermediate"]
          }
        },
        "discovery_type": "multi_agent_consensus",
        "merged_from": ["KS-01", "CS-02", "UP-02"],
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

### 02-team-research-report.md Template

```markdown
# Team Research Report: {seed}

> Date: YYYY-MM-DD | Agents: {N} | Raw Topics: {N} | Final Directions: {N}
> Depth: {standard/deep} | Duration: ~{N} min | DataForSEO Cost: ~${N}

---

## Executive Summary

{3-5 sentence summary: domain overview, key findings, recommended actions}

---

## Agent Roster

| Role | Agent ID | Type | Findings | Key Insight |
|------|----------|------|----------|-------------|
| 关键词侦察兵 | keyword_scout | Always Active | {N} | {one-line key finding} |
| 内容策略师 | content_strategist | Always Active | {N} | {one-line key finding} |
| 市场分析员 | market_analyst | Always Active | {N} | {one-line key finding} |
| 技术专家 | tech_specialist | Conditional | {N} | {one-line key finding} |
| 用户代言人 | user_persona | Always Active | {N} | {one-line key finding} |

---

## Final Directions ({N} total)

### D01: {locked_title}

| Dimension | Data |
|-----------|------|
| **SEO Score** | {score}/100 |
| **AEO Score** | {score}/100 |
| **Consensus** | {score} ({N}/{total} Agents) |
| **Discovered by** | {agent_list} |
| **Search Volume** | {volume}/month |
| **Trend** | {trend} |
| **Recommended Format** | {content_type} -> {writer_skill} |

**Multi-perspective Evidence:**
- **Researcher perspective**: {evidence}
- **Market analyst perspective**: {evidence}
- **Creator perspective**: {evidence}

**Competitor Status**: {Top 3 competitors and weaknesses}

---

### D02: {locked_title}
...

---

## Diversity Analysis

### Topic Coverage
| Dimension | Coverage |
|-----------|----------|
| Content Types | {list/tutorial/roundup/comparison distribution} |
| Target Audiences | {creator/business/developer distribution} |
| Search Intents | {informational/commercial/transactional distribution} |
| Product Relevance | {with/without product tie-in distribution} |

### Semantic Distance
- Average similarity between final topics: {score}
- Most similar pair: {D0X vs D0Y} = {score}
- Uncovered areas: {analysis}

---

## Exclusive Discoveries

Topics found by only one agent — may be valuable overlooked directions:

### {title} (by {agent_role})
- **Why unique**: {rationale}
- **Data**: Search volume {volume}, Trend {trend}
- **Recommendation**: {worth further research?}

---

## Appendix: Dedup & Filtering Log

| Stage | Count | Notes |
|-------|-------|-------|
| Phase 1 raw topics | {N} | Sum of all agent outputs |
| Phase 2 after dedup | {N} | Semantic dedup (-{N}%) |
| Phase 3 after validation | {N} | DataForSEO validation (-{N}%) |
| Final directions | {N} | Top {N} by ranking formula |
```

**Note on Diversity Analysis**: v1.1 inlines these sections into `02-team-research-report.md` under a "Diversity Analysis" heading. This includes:
- Agent contribution breakdown
- Similarity matrix
- Coverage map
- Uncovered areas

### 06-decision-brief.md Template

```markdown
# Decision Brief: {seed}

> Date: YYYY-MM-DD | Team: {N} Agents | Final Directions: {N}

---

## Top 3 Directions Overview

### #1: {locked_title}
- **Why write this**: {1-2 sentences, data-supported}
- **Why write NOW**: {timeliness / trend / competitor weakness}
- **Main risk**: {competition / data gaps / domain volatility}
- **Recommended next step**: {which Writer, estimated word count, key sections}

### #2: {locked_title}
- **Why write this**: {...}
- **Why write NOW**: {...}
- **Main risk**: {...}
- **Recommended next step**: {...}

### #3: {locked_title}
- **Why write this**: {...}
- **Why write NOW**: {...}
- **Main risk**: {...}
- **Recommended next step**: {...}

---

## Passed-Over Directions (ranked 4-5 but not in Top 3)

| Direction | Reason for passing |
|-----------|-------------------|
| {title} | {too competitive / low volume / weak brand fit} |
| {title} | {...} |

---

## Decision Guidance

- **If writing only 1 article**: Recommend #{rank} — {locked_title}
- **If writing 2-3 articles**: Recommend #{rank1} + #{rank2}, covering {content_type1} + {content_type2}
- **Timeliness alert**: {any QDF windows to catch?}
```

### 07-handoff-pack/ Structure

For Top 1-3 directions, generate a creation pack that can be fed directly to a Writer Skill.

#### D0X-brief.md

```markdown
# Direction Brief: {locked_title}

## Basic Info
| Field | Value |
|-------|-------|
| Direction ID | {D0X} |
| Primary Keyword | {primary_keyword} |
| Search Volume | {volume}/month |
| Trend | {trend} |
| Content Type | {recommended_content_type} |
| Writer Skill | {recommended_skill} |
| Blueprint/Tier | {specific_blueprint_or_tier} |
| Estimated Words | {word_count} |

## Writing Guidelines
- **Core thesis**: {extracted from evidence chain}
- **Differentiation angle**: {what competitors don't cover}
- **Must include**: {key data points / cases / comparisons}
- **Avoid**: {common competitor mistakes}

## Product Integration
- **Product**: {product_mapping.primary}
- **Integration angle**: {product_mapping.product_angle}
- **CTA level**: {subtle/balanced/aggressive}
```

#### D0X-outline.md

```markdown
# Article Outline: {locked_title}

## H2 Structure
{Complete outline from outline.h2_sections, each H2 with 50-100 word description}

## AEO Answer Block
{outline.aeo_answer_block}

## Key Takeaways (Front-loaded)
{3-5 Key Takeaway suggestions}

## FAQ Suggestions
{3-5 FAQs based on People Also Ask}
```

#### D0X-prompt-kit.md

```markdown
# Prompt Kit: {locked_title}

## Writer Prompt (feed directly to {recommended_skill})

{Complete Writer startup prompt including:
- Title
- Primary keyword
- Content type
- Outline
- Product integration guidelines
- Differentiation requirements
- Word count target
- AEO goals}

## Reference Materials
- Competitor URL 1: {url} — {weakness}
- Competitor URL 2: {url} — {weakness}
- Data source: {DataForSEO / market report URL}
```

---

## Degradation Strategies

| Scenario | Detection | Fallback |
|----------|-----------|----------|
| Agent timeout | Task tool returns timeout | Skip agent, continue with remaining outputs; note absent agent in report |
| Agent output format error | JSON parse failure | Attempt to extract key info from text; if completely unparseable, skip |
| DataForSEO quota exceeded | API returns 402/429 | Degrade to WebSearch volume estimates; mark data as "estimated" |
| Token budget exceeded | Context approaching limit | Reduce agent count (remove Personas first, then recommended agents) |
| All agents low consensus | Highest consensus_score < 0.3 | Alert user that seed may be too narrow or broad; suggest adjustment |
| Too few topics after dedup (<5) | merged topics < 5 | Alert user; suggest Deep mode or broadening the seed |
| Single agent produces 0 topics | findings is empty array | Mark as "no findings"; doesn't affect other agents |

### Minimum Viable Team

```yaml
minimum_viable_team:
  agents: 3  # Fixed members only
  personas: 0
  depth: "standard"
  expected_raw_topics: 15-24
  expected_final: 3-5
```

---

## Integration Points

| Integration | Method | Description |
|-------------|--------|-------------|
| **growth-topic-scout** | Phase 3 reuses its DataForSEO modules | Keyword validation + SERP analysis + Title Lock + AEO scoring |
| **Direction Schema** | Compatible with `DIRECTION_SCHEMA.json` + `team_metadata` extension | Downstream Writers can use directly; extension fields ignored if not needed |
| **Writer routing** | Outputs `recommended_skill` field | Direct entry to Writer pipeline (blog-list-writer / blog-tutorial-writer) |
| **PRODUCT_CATALOG.md** | Brand Specialist reads product info | Via Read tool in subagent |
| **BLOG_WRITING_PRINCIPLES_v2.md** | Content Strategist references writing principles | Title formulas, review methodology, etc. |
| **Output directory** | `/research 竞品分析/team-research/` | New subdirectory; doesn't affect existing structure |

### Data Flow

```
research-charter.json (Phase 0, frozen contract)
    |
agent_output x 5-7 (Phase 1, parallel + each agent's DataForSEO validation)
    |  includes abstract + competitor_map + data_validation
merged_topics + Similarity Matrix + Coverage Map (Phase 2, CEO decisions)
    |
supplemental validation + Title Lock + AEO scoring (Phase 3, only unverified gaps)
    |
team-directions.json + Decision Brief + Handoff Pack (Phase 4)
    | (compatible with Direction Schema; Handoff Pack can feed Writer directly)
Writer Pipeline (blog-list-writer / blog-tutorial-writer / case-roundup-writer)
    |
Editor -> AEO -> Publish
```

---

## Cost Estimate (v1.1)

| Phase | Token Usage | External API Cost | Time |
|-------|------------|-------------------|------|
| Phase 0: Charter | ~5K tokens | $0.00 | 1-2 min (with user Q&A) |
| Phase 1: Exploration (5 agents) | ~150-180K tokens | $0.00 | 3 min (parallel) |
| Phase 2: CEO Synthesis + Diversity | ~12K tokens | $0.00 | 2-3 min |
| Phase 3: Concentrated DataForSEO | ~8K tokens | ~$0.17 (~10 keywords + ~8 SERP) | 1-2 min |
| Phase 4: Output Generation | ~10K tokens | $0.00 | 2-3 min |
| **Total (Standard)** | **~185-215K tokens** | **~$0.17** | **~10 min** |

**v1.1 vs v1.0 Comparison**:

| Metric | v1.0 (Actual) | v1.0 (Predicted) | v1.1 (Predicted) | Change |
|--------|---------------|------------------|------------------|--------|
| Agents | 7 | 7 | 5 | **-29%** |
| Avg Token/Agent | 43K | 6-8K | 30-36K | Still 4x over |
| Total Tokens | 359K | 56-86K | 185-215K | **-36%** |
| DataForSEO Cost | $0 (0/7 success) | $0.70 | $0.17 | **-76%** |
| DataForSEO Success | 0% | 100% (expected) | 100% (Orchestrator) | **+100%** |
| Output Files | 3/7 generated | 7 | 5 | **-29%** |
| Time | ~10 min | 10-15 min | ~10 min | Same |

**Key Improvements**:
- Token reduction: ~359K → ~215K (-36% from agent reduction + prompt simplification)
- DataForSEO reliability: 0% → 100% (concentrated in Orchestrator)
- Cost reduction: $0.70 → $0.17 (-76% from reduced calls)
- Output simplification: 7 files → 5 files

---

## Appendix: Task Tool Invocation Example (v1.1)

This is the actual runnable Task tool invocation pattern for Phase 1:

```
// Phase 1: Orchestrator sends a SINGLE message with ALL Task calls in parallel (5 agents)

// Agent 1: Keyword Scout
Task(
  description: "Keyword Scout agent",
  subagent_type: "general-purpose",
  model: "sonnet",
  max_turns: 15,
  prompt: "[Shared Preamble] + [Keyword Scout Lens: 搜索量 + 长尾词 + 意图分类]"
)

// Agent 2: Content Strategist
Task(
  description: "Content Strategist agent",
  subagent_type: "general-purpose",
  model: "sonnet",
  max_turns: 15,
  prompt: "[Shared Preamble + {product_catalog_summary}] + [Content Strategist Lens: 竞品格式 + 空白 + 品牌适配]"
)

// Agent 3: Market Analyst
Task(
  description: "Market Analyst agent",
  subagent_type: "general-purpose",
  model: "sonnet",
  max_turns: 15,
  prompt: "[Shared Preamble] + [Market Analyst Lens: 市场数据 + 行业趋势]"
)

// Agent 4: Tech Specialist (conditional — only if tech/creative domain)
Task(
  description: "Tech Specialist agent",
  subagent_type: "general-purpose",
  model: "sonnet",
  max_turns: 15,
  prompt: "[Shared Preamble] + [Tech Specialist Lens: 技术深度 + 工作流]"
)

// Agent 5: User Persona (composite multi-tier)
Task(
  description: "User Persona agent",
  subagent_type: "general-purpose",
  model: "sonnet",
  max_turns: 15,
  prompt: "[Shared Preamble + {persona_tiers}] + [User Persona Lens: 复合多段位用户视角]"
)

// All 5 Tasks execute in parallel.
// Orchestrator receives all results after ALL complete.
// Each result is a text string containing the agent's JSON output.
// Orchestrator parses each result as JSON for Phase 2.
```

**v1.1 Important Notes**:
- `subagent_type` must be `"general-purpose"` — needs WebSearch / WebFetch / Read (no DataForSEO in Phase 1)
- **Shared Preamble** (~250 words) injected into all agents → reduces prompt redundancy
- **Unique Lens** (~150-250 words) defines each agent's perspective
- `run_in_background` is NOT set (defaults to false)
- `model: "sonnet"` is cost-effective for 5 parallel agents
- `max_turns: 15` reduced from 25 — sufficient for WebSearch + JSON formatting (no DataForSEO)
- Do NOT use `.claude/agents/` files — v1.1 uses inline Task tool prompts
- DataForSEO calls moved to Phase 3 (Orchestrator executes in main conversation)
