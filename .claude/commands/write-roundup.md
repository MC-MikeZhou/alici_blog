# /write-roundup - 生成 Case Roundup 文章

使用 case-roundup-writer Skill (v1.1) 生成 300-600 词的洞察驱动小博文。

**v1.1 新特性**:
- ✅ 强制索取真实素材（Material Gate）
- ✅ 单一素材多维度拓展（不编造案例）
- ✅ 生成可复用 Prompt（2-3 个）
- ✅ 标题确认（5+ 选项）

## 预置上下文

```bash
# 检查 insights/ 和 case-packs/ 目录
ls -la insights/ 2>/dev/null | tail -3
ls -la case-packs/ 2>/dev/null | tail -3

# 当前日期
echo "发布日期: $(date +%Y-%m-%d)"
```

## 输入要求

**选项 A**: 提供视频 URL（推荐）
- YouTube 视频链接（1-5 个）
- 系统将自动提取字幕/内容并生成 Case Pack
- 进入交互式 Insight Pack 收集模式

**选项 B**: 提供完整 Insight Pack + Case Pack
- Insight Pack JSON（来自交互式收集或手动提供）
- Case Pack JSON（2-5 个案例）

## 工作流 (v1.1)

```
Step 0: 索取真实素材（强制）
    ↓
Step 1: 分析素材 & 提取 Case Pack
    ├─ 单一素材 → 多维度拓展（工作流/场景/技巧/陷阱）
    └─ 多个素材 → 每个素材提取一个案例
    ↓
Step 2: 生成可复用 Prompt（2-3 个）
    ↓
Step 3: 交互式收集 Insight Pack（6 个问题）
    ↓
Step 4: 标题确认（5+ 选项让用户选择）
    ↓
Step 5-12: 生成文章（300-600 词 + Prompts to Try 章节）
    ↓
AEO 评分（content_profile: micro_roundup）
    ↓
[如需要] 自动改进
```

## 文章结构 (v1.1)

```
[问题式标题 40-60字符] →
[直答 2-3句 40-60词] →
[Key Takeaways 3-5点] →
[Case Studies 2-5个案例 OR 多维度分析] →
[Prompts to Try 2-3个可复用 Prompt] ← NEW →
[How to Try It 最多4步] →
[Mini FAQ 3问] →
[Source Note + 产品理念渗透]
```

## Insight Pack 收集（交互式）

如果未提供 Insight Pack，系统将询问：

1. **核心观点**（一句话）
2. **为什么现在值得写**（时效性）
3. **关键要点**（3-5 个）
4. **需要避免的信息**（可选）
5. **产品理念**（One-prompt / AI-driven / 多模型一站式）
6. **目标读者**

收集后保存到：`/insights/YYYY-MM-DD-{topic-slug}.json`

## Case Pack 结构

每个案例包含：
- **case_title**: 案例标题
- **what_happens**: 发生了什么（80-100 词）
- **why_it_works**: 为什么有效（30-40 词）
- **what_to_copy**: 可复用规律（2-3 条）
- **tags**: 案例标签

保存到：`/case-packs/YYYY-MM-DD-{topic-slug}_roundup-{number}.json`

## 输出格式

micro_roundup 最小规范：
- content_profile: micro_roundup
- word_count_target: 300-600
- 包含完整 E-E-A-T 字段（date, author, featured_image）
- Source Note（案例来源说明）
- 产品理念自然渗透（教育性叙事，非硬推 CTA）

## 输出位置

```
/reports/[YYYY-MM-DD]-[topic]/
├── 00-implementation.md             # 进度追踪
├── 00-insight-pack.json             # Insight Pack
├── 00-case-pack.json                # Case Pack
├── 01-article-draft.md              # Case Roundup 初稿
└── 03-aeo-score.md                  # AEO 评分（micro_roundup rubric）
```

同时保存到：
```
/insights/YYYY-MM-DD-{topic-slug}.json      # Insight Pack 备份
/case-packs/YYYY-MM-DD-{topic-slug}_roundup-01.json  # Case Pack 备份
```

## 质量目标

- 字数: 300-600 词
- AEO 目标分数: ≥ 70 分（micro_roundup 评分标准）
- 案例数量: 2-5 个
- FAQ 问题: 3 个

## 使用示例

**示例 1**: 提供视频 URL
```
/write-roundup https://www.youtube.com/watch?v=xxx https://www.youtube.com/watch?v=yyy
```

**示例 2**: 仅描述主题（系统将引导收集 Insight Pack）
```
/write-roundup 写一篇关于 Kling Motion Control 的案例汇总
```

**示例 3**: 提供完整 Insight Pack 和 Case Pack 文件路径
```
/write-roundup
使用 /insights/2026-01-20-kling-motion-control.json
和 /case-packs/2026-01-20-kling-motion-control_roundup-01.json
```

## micro_roundup vs Tutorial 对比

| 特性 | micro_roundup | Tutorial |
|------|---------------|----------|
| 字数 | 300-600 | 1,800-2,500 |
| 核心价值 | 展示"what works" | 教授"how to do" |
| 案例数 | 2-5 个 | 0-2 个（可选） |
| 步骤详解 | 简化（最多 4 步） | 详细（5-7 步） |
| FAQ 规模 | Mini（3 问） | 完整（3-5 问） |
| AEO 门槛 | ≥ 70 | ≥ 75 |
| 适用场景 | 趋势观察、案例汇总 | 操作指南、深度教程 |

## 下一步（文章生成后）

1. **AEO Analyzer** (自动调用)
   - content_profile: micro_roundup
   - 使用 micro_roundup 专用评分标准

2. **Auto Improver** (如果 < 70)
   - 聚焦案例清晰度和 "what to copy" 具体性

3. **Framer CMS** (当 ≥ 70)
   - 转换为 Framer JSON
   - 发布到博客

---

## v1.1 关键变化

**Step 0: Material Gate（新增）**
- 必须先提供真实素材（视频/字幕/观察案例）
- 无素材 = 拒绝继续
- Case-driven = 真实案例驱动，不编造

**单一素材处理（改进）**
- 旧版本：编造其他案例 ❌
- 新版本：多维度拓展（工作流/场景/技巧/陷阱）✅
- 一个视频也能写完整文章

**Prompts to Try（新增）**
- 每篇文章包含 2-3 个可复用 Prompt
- 用户可直接复制使用
- 降低实践门槛

**标题确认（改进）**
- 旧版本：系统直接生成标题
- 新版本：提供 5+ 标题选项让用户选择 ✅
- 覆盖多种类型（问题式/How-to/洞察式/数字式）

---

*基于 case-roundup-writer Skill (v1.1)*
