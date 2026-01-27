# AliciBlog 内容创作指导原则

> 用于自动选题和内容定位的核心指导文档
>
> **版本**: 1.0
> **更新日期**: 2026-01-17
> **适用范围**: 所有 AliciBlog 内容生产流程

---

## 一、品牌定位与目标受众

### 1.1 AliciBlog 核心定位

```
我们是谁？
→ alici.ai: 面向营销层面的 AI 视觉内容平台

我们提供什么？
→ 高质量 AI 模型（图像/视频）+ Agent 智能工作流

我们的差异化？
→ Agent 机制帮助用户产出更高品质的提示词和 Workflow
```

### 1.2 目标受众画像

| 受众类型 | 特征 | 内容需求 |
|----------|------|----------|
| **品牌营销团队** | 需要提升品牌视觉质量 | 如何用 AI 生成品牌一致的营销素材 |
| **内容创作者** | YouTube/TikTok/Instagram | 快速生成高 CTR 的视觉内容 |
| **独立创业者** | 预算有限，需性价比方案 | 免费/低成本工具对比 |
| **营销机构** | 服务多个客户品牌 | 批量生产 + 品牌定制化 |

### 1.3 核心价值主张

**我们吸引的是**: 想利用优质模型提升品牌的客户

**我们的优势**:
1. **模型质量**: 接入 Flux Pro, Ideogram, Imagen 4, Kling 2.0, Runway Gen-4, Veo 3
2. **Agent 工作流**: 自动优化提示词，提升输出质量 40-60%
3. **品牌一致性**: Brand Visual Guide 确保所有输出符合品牌规范

---

## 二、选题决策框架

### 2.1 选题优先级矩阵

当 Topic Scout 生成多个选题时，按以下优先级评分：

| 评分维度 | 权重 | 评分标准 (1-10) |
|----------|------|-----------------|
| **营销导向** | 30% | 是否关注品牌/营销/内容创作场景？ |
| **产品契合度** | 25% | 是否能自然融入 alici.ai 图像/视频产品？ |
| **Agent 优势可展示** | 20% | 是否能强调 Agent 工作流/提示词优化？ |
| **流量潜力** | 15% | Opportunity Score 是否 >= 60？ |
| **竞品差异化** | 10% | 是否能比竞品提供更好的内容？ |

**自动选题规则**:
```python
if 营销导向 >= 7 and 产品契合度 >= 7 and Opportunity_Score >= 60:
    → 自动选择该选题，无需等待用户确认
else:
    → 等待用户确认（3 分钟超时）
```

### 2.2 选题方向清单

**✅ 优先选择的主题**:
- AI 营销工具 (marketing tools, content creation, social media)
- AI 视觉内容 (image generation, video creation, thumbnail design)
- AI 工作流优化 (prompt engineering, workflow automation)
- 品牌视觉提升 (brand consistency, visual quality)
- 创作者增长 (YouTube growth, viral content, CTR optimization)

**⚠️ 谨慎选择的主题**:
- 通用 AI 工具对比（除非有明确的视觉内容角度）
- 纯技术教程（除非与视觉 AI 相关）
- 新闻类内容（时效性短，ROI 低）

**❌ 不选择的主题**:
- 与视觉内容/营销无关的 AI 话题
- 竞品直接产品对比（避免负面竞争）
- 需要专业技术知识的深度技术文章

---

## 三、内容定位原则

### 3.1 alici.ai 产品融入策略

**黄金比例**: 3/15 或 20%
- 在 15 个工具的 List 文章中，融入 3 个 alici.ai 产品
- 在 10 个工具的 List 文章中，融入 2 个 alici.ai 产品

**定位排名**:
- **Top 3 必须有 1 个 alici.ai** (通常是 #3)
- 其余产品分散在中部和后部

**产品匹配逻辑**:
| 文章关键词 | 主推产品 | 次推产品 |
|-----------|---------|---------|
| `marketing`, `visual content`, `brand` | Image Studio | Video Studio |
| `video`, `social media`, `viral` | Video Studio | Thumbnail Expert |
| `YouTube`, `thumbnail`, `CTR` | Thumbnail Expert | Video Studio |
| `image`, `design`, `creative` | Image Studio | Smart Editor |

### 3.2 品牌叙事框架

**定位话术**:
```
❌ 避免: "alici.ai is the best / revolutionary / game-changing"
✅ 推荐: "alici.ai excels at [specific use case] with its Agent workflows"
```

**强调点**:
1. **Agent 工作流优势**: "AI Agent automatically refines prompts based on brand guidelines"
2. **质量模型接入**: "Access to Flux Pro, Ideogram, Imagen 4 in one platform"
3. **品牌一致性**: "Brand Visual Guide ensures all outputs match your brand identity"
4. **数据驱动结果**: "40-60% quality improvement compared to raw model prompts"

**诚实的局限性**:
- "Less design control than Canva for pixel-perfect customization"
- "Best suited for marketing visuals rather than complex photo editing"
- "Requires setting up brand guidelines for optimal results"

### 3.3 E-E-A-T 信号要求

每篇文章必须包含:
- ✅ 作者信息: "alici.ai Content Team" + role + bio
- ✅ 日期字段: date + last_updated
- ✅ 外部引用: 至少 3-5 个权威来源 (McKinsey, Semrush, Gartner, etc.)
- ✅ 数据支撑: 具体数字、百分比、研究结果
- ✅ 测试声明: "We tested X tools", "Based on our analysis of Y samples"

---

## 四、内容质量标准

### 4.1 AEO 目标

| 指标 | 最低要求 | 理想目标 |
|------|----------|----------|
| AEO 总分 | >= 75/100 | >= 80/100 |
| M1: Content Structure | >= 26/30 | 30/30 |
| M2: Technical | >= 15/25 | >= 20/25 |
| M3: E-E-A-T | >= 18/25 | >= 23/25 |
| M4: Visibility | >= 16/20 | 20/20 |

**自动改进规则**:
- 首次 AEO < 75 → 运行 auto-improver (最多 3 轮)
- 首次 AEO >= 75 → 直接通过，跳过 auto-improver
- 3 轮后仍 < 75 → 标记 MANUAL_REVIEW

### 4.2 字数要求

| 文章类型 | 最低字数 | 理想字数 | 最高字数 |
|----------|----------|----------|----------|
| Tutorial | 1,800 | 2,000-2,500 | 3,000 |
| List | 2,500 | 2,500-3,000 | 4,500 |
| Guide | 2,000 | 2,500-3,500 | 5,000 |

### 4.3 Citable Blocks 要求

每篇文章必须包含 **3-5 个 Citable Blocks**:

```markdown
<!-- CITABLE_BLOCK: Label -->
[40-80 词的独立可引用内容，包含数据和关键结论]
<!-- /CITABLE_BLOCK -->
```

**分布策略**:
- 1 个在开篇/背景部分 (设定上下文)
- 2-3 个在主体内容 (核心洞察)
- 1 个在结论/关键要点 (可操作建议)

---

## 五、自动化决策规则

### 5.1 选题自动确认条件

满足以下**任一**条件时，自动选择选题，无需等待用户确认:

```python
# 条件 1: 高分营销相关选题
if (
    营销导向评分 >= 7
    and 产品契合度 >= 7
    and Opportunity_Score >= 60
):
    → 自动选择

# 条件 2: 用户明确授权方向
if 用户已提供方向指导 and 选题符合指导方向:
    → 自动选择

# 条件 3: 超时后自动选择
if 等待时间 >= 3分钟 and Opportunity_Score >= 60:
    → 自动选择最高分选题
```

### 5.2 产品推荐自动匹配

根据文章主题自动推荐 alici.ai 产品:

```python
# 关键词匹配逻辑
if "marketing" in topic or "visual content" in topic:
    primary_product = "image_studio"
    secondary_product = "video_studio"

elif "video" in topic or "viral" in topic:
    primary_product = "video_studio"
    secondary_product = "thumbnail_pro"

elif "YouTube" in topic or "thumbnail" in topic:
    primary_product = "thumbnail_pro"
    secondary_product = "video_studio"

else:
    primary_product = "image_studio"
    secondary_product = None
```

### 5.3 内容定位自动决策

```python
# 产品排名
if 文章类型 == "List" and 工具数量 >= 10:
    alici_products_count = min(3, 工具数量 * 0.2)
    第一个产品位置 = random.choice([2, 3])  # Top 3 内

# 强调点选择
if "marketing" in topic:
    强调点 = ["Agent workflows", "Brand consistency", "Quality models"]
elif "speed" in topic or "fast" in topic:
    强调点 = ["Fast generation", "One-click workflows", "Instant results"]
```

---

## 六、应用示例

### 示例 1: AI Marketing Tools (本次实验)

**用户方向**:
> "面向营销层面，吸引想利用优质模型提升品牌的客户，强调 Agent 机制优势"

**系统自动决策**:
1. ✅ 选题: "Best AI Marketing Tools" (营销导向 9/10, 产品契合 8/10, Opportunity 78/100)
2. ✅ 产品: Image Studio (#3), Video Studio (#7), Thumbnail Expert (#12)
3. ✅ 定位: "Professional visual content creation with AI Agent workflows"
4. ✅ 强调: "40-60% quality improvement", "Brand Visual Guide integration"

**结果**: AEO 88/100, 无需人工改进

### 示例 2: Best AI Video Generators (假设)

**关键词匹配**:
- 主题: "best ai video generators"
- 营销导向: 8/10 (视频是营销核心内容)
- 产品契合: 9/10 (alici.ai Video Studio 直接匹配)

**自动决策**:
1. ✅ 自动选择该选题
2. ✅ 主推产品: Video Studio (#2 或 #3)
3. ✅ 次推产品: Image Studio (作为补充)
4. ✅ 定位: "Multi-model access (Kling, Runway, Veo) with Agent prompt optimization"

---

## 七、质量检查清单

每篇文章生成后自动检查:

### 内容结构
- [ ] AIDA 开篇 (80-120 词)
- [ ] Quick Answer section
- [ ] 3-5 个 Citable Blocks
- [ ] Comparison Table (List 文章)
- [ ] FAQ section (3-5 问题)

### 产品融入
- [ ] alici.ai 产品占比 <= 20%
- [ ] 至少 1 个产品在 Top 3
- [ ] 产品定位强调 Agent 优势
- [ ] 包含诚实的局限性说明

### E-E-A-T
- [ ] 作者信息完整
- [ ] date + last_updated 字段
- [ ] 3+ 外部权威引用
- [ ] 5+ 具体数据点

### AEO 优化
- [ ] 开篇直接回答核心问题
- [ ] 段落长度 <= 3 句
- [ ] 至少 1 个表格 + 3 个列表
- [ ] 所有关键信息可见（无隐藏）

---

## 八、更新日志

### v1.0 (2026-01-17)
- 初始版本
- 基于 "Best AI Marketing Tools" 实验总结
- 定义自动选题规则和内容定位原则
- 建立 3 分钟超时自动决策机制

---

**使用说明**:
1. Topic Scout 生成选题时，参考"选题决策框架"自动评分
2. 满足自动确认条件时，无需等待用户，直接执行
3. 内容生成时，遵循"内容定位原则"自然融入产品
4. AEO 评分后，按"质量标准"决定是否需要改进
