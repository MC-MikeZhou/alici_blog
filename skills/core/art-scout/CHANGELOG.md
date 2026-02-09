# art-scout Changelog

## v1.3 (2026-02-08)

**Opus PRD Critical Inheritance** — Seed Dimensions + Divergent/Convergent Agents + Soft Diversity Gate

### Philosophy: Critical Inheritance over Copying

v1.3 is a **批判性继承** (critical inheritance) upgrade based on the Opus PRD "Art Scout v1.2 Diversity Engine 升级". We inherit **思想而非方案** (ideas, not blueprints) — taking what works and rejecting over-engineering.

**✅ 继承清单 (What We Inherited)**:
1. **Seed Dimension Mapping** (§2.1) — Lightweight 5-dimension exploration framework (NOT full CoT decomposition)
2. **Divergent/Convergent Labels** (§2.2) — Agent mission clarity (escape gravity vs go deep)
3. **Soft Diversity Gate** (§2.3) — Three-tier thresholds with user-informed decisions (NOT hard blocking)
4. **Expanded Diversity Metrics** (§2.5) — 4 new fields for cross-run comparison

**❌ 拒绝清单 (What We Rejected)**:
1. **3+2 Mixed Formation** — v1.2's 5-agent lineup already validated (diversity_score=0.74)
2. **Persona Rotator Agent** — audience_advocate's 3-tier mechanism is sufficient
3. **Full CoT Seed Deconstruction** — 25-40 variants is over-engineering; data-driven Phase 0.5 is enough
4. **Hard Diversity Gate (avg < 0.45)** — Fixed thresholds don't adapt to different seed types
5. **Automatic Supplementation** — Increases uncertainty and cost; preserve human control
6. **Diversity Bonus as Cosine Metrics** — v1.2's semantic dimensions (unique_perspective, unserved_audience) are more meaningful than numerical similarity
7. **Mollick Protocol Threshold (0.243)** — Research context (idea generation) differs from SEO topic research
8. **New Files (00-seed-deconstruction.json, 02-diversity-gate-report.json)** — Lightweight approach doesn't need separate files

### Core Changes

**1. Phase 0.2: Seed Dimension Mapping (ENHANCED)**
- **NEW**: `seed_dimensions` field in `domain_profile` output
- **Purpose**: Provide 3-5 key exploration dimensions to guide Agent thinking without heavy CoT
- **Dimensions**: `user_type`, `content_format`, `competitive_angle`, `business_context`, `temporal_dimension`
- **Usage**: Injected into Agent Shared Preamble as lightweight cognitive framing
- **Not**: Complete CoT decomposition (Opus proposed 25-40 variants; we keep it minimal)

**2. Phase 1: Divergent/Convergent Agent Labels (ENHANCED)**

| Agent | Mission Label | Instruction |
|-------|--------------|-------------|
| **trend_scout** | **DIVERGENT** ⭐ | "Your role is to ESCAPE the seed's gravity field. Find adjacent, non-obvious opportunities." |
| **audience_advocate** | **DIVERGENT** ⭐ | "Find unserved audiences beyond the typical ICP. Discover audiences competitors have ignored." |
| **keyword_validator** | **CONVERGENT** ⭐ | "Your role is to go DEEP into the seed's core territory. Validate Data Landscape for high-value opportunities." |
| **gap_hunter** | **CONVERGENT** ⭐ | "Deconstruct competitors in the seed's core SERP. Go deep into what they're doing wrong." |
| workflow_architect | - | No label (maintains neutral technical focus) |

**3. Phase 2.5: Diversity Gate (Soft Gate) (UPGRADED)**

**v1.2 → v1.3**:
- v1.2: Passive diversity scoring (informational only)
- v1.3: **Soft Gate** with three thresholds + actionable alerts

**Three-Tier Soft Gate**:

| avg_pairwise_similarity | Gate Status | Action |
|------------------------|-------------|--------|
| ≤ 0.55 | `PASS` | ✅ Diversity is good, proceed normally |
| 0.55 - 0.65 | `WARNING` | ⚠️ Mark in decision-brief, suggest user review |
| > 0.65 | `ALERT` | 🚨 Recommend user intervention (consider changing seed or manual supplement) |

**Soft Gate Philosophy**:
- ❌ No hard blocking (preserves human control)
- ❌ No automatic supplementation (avoids cost/uncertainty)
- ✅ Transparent warnings (user-informed decisions)
- ✅ Actionable recommendations (clear next steps)

**4. Phase 4: diversity_report Expansion (ENHANCED)**

**v1.2 → v1.3 New Fields**:

| Field | Type | Purpose |
|-------|------|---------|
| `avg_pairwise_similarity` | number | Average similarity across all direction pairs (0-1 scale) |
| `diversity_gate_status` | enum | "PASS" / "WARNING" / "ALERT" based on three-tier thresholds |
| `intent_type_distribution` | object | Count by intent type (informational / commercial_investigation / transactional) |
| `source_agent_distribution` | object | Contribution count per agent (detects over/under-production) |

**Why These Fields**:
- Enable **cross-run comparison** (compare v1.3 run #1 vs run #2 for same seed)
- Detect **systemic issues** (e.g., one agent producing 0 directions, or 100% commercial intent)
- Support **data-driven iteration** (track diversity improvements across versions)

### Output Schema Changes (v1.3)

**Enhanced**:
- `domain_profile.seed_dimensions` (5 dimensions): NEW in Phase 0.2
- `diversity_report` in `03-team-directions.json`: +4 fields (avg_pairwise_similarity, diversity_gate_status, intent_type_distribution, source_agent_distribution)

**Agent Prompt Changes**:
- All agents receive `seed_dimensions` in Shared Preamble
- trend_scout + audience_advocate: +DIVERGENT mission instructions
- keyword_validator + gap_hunter: +CONVERGENT mission instructions

### Why Not Full Opus PRD?

**Opus PRD 背景**:
- Written by Claude Opus 4.6 based on v1.1 diagnostic data
- Many proposals aimed to fix issues **already solved in v1.2** via different approaches
- v1.2 achieved diversity_score=0.74 (GOOD) without Opus's proposed architecture

**v1.2 vs Opus Approach**:

| Issue | Opus Solution | v1.2 Solution | v1.3 Decision |
|-------|--------------|--------------|--------------|
| Low diversity | 3+2 mixed formation (D1/D2 divergent + C1/C2/C3 convergent) | 5 strong role constraints + sub-cluster assignment | ✅ Keep v1.2, add labels |
| Seed clustering | Full CoT seed deconstruction (25-40 variants) | Phase 0.5 data-driven sub-clusters | ✅ Keep v1.2, add lightweight dimensions |
| Diversity scoring | Hard gate (avg < 0.45, auto-supplement) | Passive scoring (informational) | ✅ Upgrade to soft gate (no hard block) |
| Metrics | Diversity Bonus as cosine similarity | Semantic dimensions (unique_perspective, unserved_audience) | ✅ Keep v1.2 (more meaningful) |

**v1.3's Approach**:
- **Light touch**: Add cognitive labels and thresholds, don't rebuild architecture
- **Preserve wins**: v1.2's data-driven Phase 0.5 + role constraints already work
- **Human control**: Soft gates over hard gates, warnings over auto-fixes
- **Meaningful metrics**: Semantic diversity over mathematical similarity

### Cost Analysis (v1.2 → v1.3)

| Phase | v1.2 | v1.3 | 变化 |
|-------|------|------|------|
| Phase 0 | $0 | $0 | - |
| Phase 0.5 | $0.77 | $0.77 | - |
| Phase 1 (Agents) | $1.50 | $1.50 | - (prompts +15 words, negligible) |
| Phase 2 | $0 | $0 | - |
| Phase 3 | $0.10 | $0.10 | - |
| Phase 4 | $0 | $0 | - |
| **总计** | **$2.37** | **$2.37** | **$0 (no cost increase)** |

**ROI**:
- **Investment**: $0 (architectural refinement, no new API calls)
- **Gains**:
  1. Clearer agent guidance (seed_dimensions + divergent/convergent labels)
  2. Proactive diversity warnings (soft gate vs passive scoring)
  3. Cross-run metrics (expanded diversity_report for version comparison)

### Breaking Changes

**Not a breaking change** — v1.3 is fully backward compatible with v1.2:
- No schema changes (only additions to optional fields)
- No agent removal or renaming
- No new dependencies
- Prompts enhanced but input/output contracts unchanged

### Migration Guide

**From v1.2 → v1.3**:

1. **No action required** — v1.3 is a drop-in upgrade
2. **Optional**: Review diversity_gate_status in first run to understand new thresholds
3. **Optional**: Use expanded diversity_report fields for cross-run analysis

### Known Issues

- **Soft gate thresholds (0.55 / 0.65)**: Chosen based on v1.2 first-run data (avg=0.48, one pair >0.50). May need calibration after more runs
- **Seed dimensions auto-generation**: Currently example-based; future versions may use domain-specific templates

### What's Next (Not in v1.3)

**From v1.2 first-run findings**:
1. **Phase 1 optimization**: Reduce max_turns (15→12) to cut runtime (~55 min → ~40 min)
2. **Consensus score calibration**: D1/D2/D4/D8 consensus_score all 0.20 may indicate agents are over-specialized
3. **SC-01 coverage**: SC-01 (品牌对比) produced 0 directions — investigate sub-cluster assignment
4. **Showdown awareness**: blog-showdown-writer v1.0 exists but agents don't know to recommend it

### Documentation Updates

- **ENHANCED**: Phase 0.2 Domain Analysis (seed_dimensions field)
- **ENHANCED**: Phase 1 Agent prompts (divergent/convergent labels)
- **ENHANCED**: Phase 2.5 Diversity Gate (soft gate thresholds + philosophy)
- **ENHANCED**: Phase 4 diversity_report (4 new fields)
- **NEW**: v1.3 Architecture Overview (updated diagram)

### Contributors

- **Critical Inheritance Analysis**: Based on Opus PRD "Art Scout v1.2 Diversity Engine 升级" (user + Opus 4.6 discussion)
- **Design**: H (批判性继承方案设计)
- **Implementation**: H
- **Testing**: Pending (v1.3 first production run — rerun v1.2 seed for comparison)

---

## v1.2 (2026-02-07)

**Major Architecture Upgrade** — DataForSEO Landscape-First + Content Registry Integration + Agent Role Overhaul

### Core Changes

**1. Phase 0.5: DataForSEO 数据景观 (NEW)**
- **keywords_for_keywords** (limit=50, $0.75): 获取真实搜索量数据，替代 Agent WebSearch 估算
- **Sub-Cluster Discovery** (3-5 clusters): 语义聚类识别子种子簇（品牌对比、使用场景、创作流程、成本/ROI、新兴/相邻）
- **SERP Landscape** (seed + 3 high-volume keywords, $0.02): 提前获取竞品 Top 10 + AI Overview + PAA
- **Agent Sub-Cluster Assignment**: 为每个 Agent 分配特定探索簇，避免盲目重叠
- **Output**: `00-data-landscape.json` (50 keywords + 5 clusters + 4 SERP analyses)

**2. Phase 0: CONTENT_REGISTRY.md 审计 (ENHANCED)**
- **Step 0.4 NEW**: 读取 `/CONTENT_REGISTRY.md` (24 篇线上文章)
- **语义匹配 Seed**: 提取与 seed 重叠度 ≥50% 的已有文章
- **注入 Agent Prompts**: 所有 Agent 收到 `existing_content_risks` 列表 + 蚕食风险标注规则
- **蚕食规则**: ≥70% → HIGH, 50-70% → MEDIUM (需差异化), <50% → LOW

**3. 5 Agents 角色重定位 (ROLE CHANGE)**

| Agent | v1.1 角色 | v1.2 角色 | 核心变化 |
|-------|----------|----------|---------|
| Agent 1 | keyword_scout | **keyword_validator** | 数据验证员：标注蚕食风险 + 发现被忽略的高价值词 (CPC 高 + 竞争低) + 长尾发现 |
| Agent 2 | content_strategist | **gap_hunter** | 竞品解构师：SERP Top 10 竞品内容缺口分析 + Alici 产品映射 |
| Agent 3 | market_analyst | **trend_scout** | 趋势猎人：**强制产出 ≥2 个"非显而易见"方向** (TF-IDF 相似度 < 0.3, 相邻赛道) |
| Agent 4 | tech_specialist | **workflow_architect** | 工作流架构师：保持不变，聚焦 How-to 类选题 |
| Agent 5 | user_persona | **audience_advocate** | 受众代言人：**强制产出 ≥1 个"被忽略的受众"方向** (非典型 ICP) |

**4. Phase 1: 数据驱动的 Agent Prompts (ENHANCED)**
- **Shared Preamble** 增强: +Data Landscape (sub-cluster specific) + Existing Content Risks (~450 words total)
- **Agent-Specific Data**: 每个 Agent 仅接收其负责的 Sub-Clusters 数据
- **强制多样性约束**: 6 个选题中不允许超过 2 个聚焦同一子话题 + 至少 1 个与 seed 语义距离较远
- **强制蚕食标注**: 每个 topic 必须输出 `cannibalization_risk` + `differentiation` (if MEDIUM/HIGH)

**5. Phase 2: 语义距离 + 蚕食过滤 (ENHANCED)**
- **Step 2.5 NEW**: 语义距离打分 (Top 15 方向两两相似度 0-1 scale)
  - 识别高相似度对 (>0.60) → Orchestrator 决定合并/替换/保留
  - 输出 diversity_score + diversity_assessment (EXCELLENT/GOOD/FAIR/POOR)
- **Step 2.6 NEW**: 蚕食过滤 (vs CONTENT_REGISTRY.md)
  - ≥70% 重叠 → **BLOCKED** (移除)
  - 50-70% → **WARNING** (保留，需验证 differentiation)
  - <50% → **SAFE**
  - 输出 `06-cannibalization-check.json`

**6. Phase 3: 优化验证流程 (OPTIMIZED)**
- **Gap Fill Validation**: 仅验证 Phase 0.5 未覆盖的关键词 (~3-5 keywords vs v1.1's ~10)
- **Title Lock**: 复用 Phase 0.5 SERP 数据，减少重复查询
- **Cost Reduction**: Phase 3 成本从 $0.17 降至 $0.10 (-41%)

**7. 输出增强 (ENHANCED)**
- **NEW**: `00-data-landscape.json` (Phase 0.5 数据景观)
- **NEW**: `06-cannibalization-check.json` (蚕食评估详情)
- **ENHANCED**: `02-team-research-report.md` (增加 Cannibalization Analysis 章节)
- **ENHANCED**: `03-team-directions.json` (增加 `cannibalization_assessment` 字段)
- **ENHANCED**: `04-decision-brief.md` (增加蚕食治理建议)

### Agent Output Schema Changes (v1.2)

**新增字段**:
- `assigned_sub_clusters`: Agent 负责的 Sub-Cluster IDs
- `findings[].primary_keyword_data`: 从 Data Landscape 引用的完整数据 (volume, cpc, competition, source, cluster_id)
- `findings[].cannibalization_risk`: "HIGH" / "MEDIUM" / "LOW" (mandatory)
- `findings[].differentiation`: 如果 risk = MEDIUM/HIGH，说明差异 (conditional)

**Agent-Specific Fields**:
- `keyword_validator.findings[].long_tail_opportunity`: Data Landscape 未覆盖的长尾词
- `gap_hunter.findings[].competitor_weakness`: SERP 竞品弱点
- `gap_hunter.findings[].content_gap`: 竞品未覆盖的角度
- `trend_scout.findings[].market_data`: {market_size, cagr, key_players, funding, source}
- `trend_scout.findings[].non_obvious`: true/false (是否为"非显而易见"方向)
- `audience_advocate.findings[].unserved_audience`: true/false (是否针对"被忽略的受众")
- `audience_advocate.findings[].unserved_audience_description`: 如果 true，描述受众

### Ranking Formula Changes (v1.2)

| Dimension | v1.1 Weight | v1.2 Weight | 说明 |
|----------|-------------|-------------|------|
| Evidence Richness | 30% | 25% | 略降，为 anti-cannibalization 腾出空间 |
| Consensus Score | 20% | 18% | 略降 |
| Diversity Bonus | 20% | 20% | 保持，增加 non_obvious + unserved_audience 加分 |
| Freshness Signal | 15% | 15% | 保持 |
| Brand Fit | 15% | 12% | 略降 |
| **Anti-Cannibalization Bonus** | - | **10%** | **NEW**: SAFE +10, WARNING +5, BLOCKED -100 |
| Risk Penalty | Penalty | Penalty | 保持 |

### Cost Analysis (v1.1 → v1.2)

| Phase | v1.1 | v1.2 | 变化 |
|-------|------|------|------|
| Phase 0 | $0 | $0 | - |
| **Phase 0.5** | - | **$0.77** | **+$0.77** (keywords_for_keywords + SERP×4) |
| Phase 1 (Agents) | $1.50 | $1.50 | 不变 |
| Phase 2 | $0 | $0 | - |
| Phase 3 | $0.17 | $0.10 | **-$0.07** (优化，减少重复验证) |
| Phase 4 | $0 | $0 | - |
| **总计** | **$1.67** | **$2.37** | **+$0.70 (+42%)** |

**ROI 分析**:
- **投资**: +$0.70 (+42%)
- **换取**:
  1. Phase 0.5 数据景观 ($0.77): 50 真实关键词 + 子种子簇 + SERP 竞品 → Agent 方向清晰
  2. Phase 0 内容审计 ($0): 蚕食检测 → 避免浪费资源
  3. Phase 2.6 蚕食过滤 ($0): 自动移除高重叠 → 保护已有内容
  4. Phase 3 优化 (-$0.07): 减少重复验证
- **预期效果**: 蚕食风险从 62.5% (v1.1 实测) 降至 <15%，数据可靠性从 ~20% 提升至 ~85%

### Breaking Changes

**不兼容变更**:
1. **Agent 名称变更**: `keyword_scout` → `keyword_validator`, `content_strategist` → `gap_hunter`, `market_analyst` → `trend_scout`, `tech_specialist` → `workflow_architect`, `user_persona` → `audience_advocate`
2. **新增依赖**: `CONTENT_REGISTRY.md` (必须存在于项目根目录，否则退化到 v1.1 模式)
3. **Output Schema 变更**: 新增 mandatory fields (`cannibalization_risk`, `primary_keyword_data`, `assigned_sub_clusters`)
4. **Agent 强制约束**: trend_scout 必须产出 ≥2 non_obvious, audience_advocate 必须产出 ≥1 unserved_audience

**向后兼容**:
- 如果 CONTENT_REGISTRY.md 缺失 → warning only，继续执行（无蚕食检测）
- 如果 DataForSEO Phase 0.5 失败 → degrade to v1.1 mode (agents use WebSearch estimates)
- `03-team-directions.json` 兼容 `DIRECTION_SCHEMA.json` + v1.2 extension fields

### Migration Guide

**从 v1.1 升级到 v1.2**:

1. **创建 CONTENT_REGISTRY.md**:
```bash
# 在项目根目录创建
CONTENT_REGISTRY.md
# 参考 Part 1 of this implementation plan
```

2. **更新 research-charter.json** (如果使用自定义 charter):
```json
{
  "content_registry_path": "CONTENT_REGISTRY.md",
  "team": {
    "agents": [
      {"agent_id": "keyword_validator", ...},  // 原 keyword_scout
      {"agent_id": "gap_hunter", ...},         // 原 content_strategist
      {"agent_id": "trend_scout", ...},        // 原 market_analyst
      {"agent_id": "workflow_architect", ...}, // 原 tech_specialist
      {"agent_id": "audience_advocate", ...}   // 原 user_persona
    ]
  }
}
```

3. **预算调整**:
- Standard mode: $1.67 → $2.37 (+$0.70)
- Deep mode: ~$2.20 → ~$3.50 (+$1.30)

4. **输出文件处理**:
- 新增 2 个文件: `00-data-landscape.json`, `06-cannibalization-check.json`
- `02-team-research-report.md` 新增 Cannibalization Analysis 章节
- `03-team-directions.json` 新增 `cannibalization_assessment` 字段

### Known Issues

- **Phase 0.5 keywords_for_keywords limit=50**: 某些 niche 领域可能词汇量不足，建议 Deep mode 使用 limit=75
- **Cannibalization 误报**: 语义匹配可能将差异化充分的选题误判为 WARNING，需人工审核
- **Sub-Cluster Assignment**: 自动聚类可能不完美，未来版本考虑支持手动调整

### Deprecations

- **v1.1 Agent 名称**: `keyword_scout`, `content_strategist`, `market_analyst`, `tech_specialist`, `user_persona` 已弃用（使用新名称）
- **Phase 1 分散 DataForSEO**: v1.1 的 Agent 内 DataForSEO 调用模式已弃用（集中到 Orchestrator）

### Documentation Updates

- **NEW**: Phase 0.5 数据景观规范 (Step 0.5.1-0.5.5)
- **NEW**: Phase 0.4 内容审计规范
- **NEW**: Agent 强制约束 (non_obvious, unserved_audience, 多样性)
- **ENHANCED**: Agent Output Schema v1.2 field reference
- **ENHANCED**: Cost estimate + ROI analysis

### Contributors

- Design: H (based on user feedback from Alici vs GPT-5 Pro 对比分析)
- Implementation: H
- Testing: Pending (v1.2 first production run)

---

## v1.1 (2026-02-07)

**SubAgent-Optimized CEO Model** — Baseline architecture

### Features

**Phase 0-4 架构**: Mission Briefing → Parallel Exploration → CEO Synthesis → Concentrated Validation → Final Portfolio

### Known Issues (Fixed in v1.2)

- **数据可靠性低**: Agent 用 WebSearch 估算搜索量，约 20% 准确率
- **蚕食风险高**: 实测 5/8 方向与已有文章重叠 (62.5%)
- **方向重叠**: Agent 探索方向盲目，缺乏子种子分配
- **关键词质量差**: 5/10 关键词搜索量 0

---

## v1.0 (2026-02-06)

**Initial release** — Agent Research Teams Scout v1

### Features
- **CEO Model architecture**: Orchestrator sets mission and makes strategic decisions; agents do ground-level research
- **Phase 0: Mission Briefing**: Seed input + domain analysis + smart agent allocation + interactive questionnaire + Research Charter freeze
- **Phase 1: Parallel Exploration**: 5-7 general-purpose subagents via Claude Code Task tool, foreground parallel-sync execution
- **Phase 2: CEO Synthesis**: Semantic dedup + consensus scoring + evidence cross-enrichment + Similarity Matrix + Coverage Map + 5-dimension ranking formula
- **Phase 3: Supplemental Validation**: Gap-fill only (agents already self-validate in Phase 1) + Title Lock + AEO scoring
- **Phase 4: Final Portfolio + Handoff**: 7 output files including Decision Brief and Handoff Pack (brief + outline + prompt-kit for Top 1-3 directions)

### Agent Types
- **Fixed (always active)**: Topic Researcher, Content Strategist, Market Analyst
- **Conditional**: Prompt Engineer (tech domains), Brand Specialist (marketing domains)
- **Personas**: 2-4 Creator Personas generated based on domain analysis

### Technical Implementation
- Built on Claude Code Task tool with `subagent_type: "general-purpose"`
- Foreground mode (no `run_in_background`) to ensure DataForSEO MCP inheritance
- Recommended `model: "sonnet"` for cost efficiency
- `max_turns: 25` per agent
- Single-layer architecture (no nested subagents)

### Output Schema
- `agent_output` v1.1: Includes `abstract`, `competitor_map`, `data_validation` fields
- `team-directions.json`: Compatible with `DIRECTION_SCHEMA.json` + `team_metadata` extension
- 7 degradation strategies for fault tolerance

### Based On
- `AGENT-TEAM-SCOUT-SKILL-SPEC.md` v1.1 (1832 lines)
- `AGENT-TEAM-SCOUT-概念设计.md` v1.1
- `growth-topic-scout` v2.4 patterns

### Cost
- Standard mode: ~$0.70 DataForSEO, ~56-86K tokens, ~10-15 min
- Deep mode: ~$1.00-1.20 DataForSEO, ~90-130K tokens, ~15-22 min
