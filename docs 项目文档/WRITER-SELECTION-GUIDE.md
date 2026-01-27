# Writer 选择指南

> 快速判断应该使用哪个 Writer Skill

---

## 一句话区分

| Writer | 核心定位 |
|--------|----------|
| **Tutorial** | 教人做事 |
| **List** | 帮人选择 |
| **Roundup** | 展示发现 |

---

## 场景决策树

```
我的选题是...
│
├─ 用户想学会某个技能/流程
│   └─ → Tutorial
│
├─ 用户在多个工具/方案间选择
│   └─ → List
│
└─ 有具体案例展示某个新发现
    └─ → Roundup
```

**快速判断法**：问自己"读者读完后要得到什么？"
- 得到**能力** → Tutorial
- 得到**决策** → List
- 得到**洞察** → Roundup

---

## 三个 Writer 详细对比

| 维度 | Tutorial | List | Roundup |
|------|----------|------|---------|
| **核心哲学** | 教你怎么做 | 帮你做选择 | 展示什么有效 |
| **字数** | 1,800-2,500 | 2,500-3,500 | 300-600 |
| **素材要求** | Topic Brief | Topic Brief + 竞品 | 真实素材（必须） |
| **用户意图** | "How do I..." | "What's the best..." | "What works..." |
| **典型标题** | "How to Create..." | "15 Best ... in 2026" | "X 让 Y 更准了吗" |
| **更新频率** | 年度 | 年度 | 周/月级 |
| **AEO 基准** | ≥80 | ≥75 | ≥70 |

---

## 各 Writer 适用/不适用场景

### blog-tutorial-writer

**适用场景** ✅
- 操作指南（"如何用 X 做 Y"）
- 步骤教程（"5 步完成..."）
- AI 工具使用方法
- 技能养成类内容

**不适用场景** ❌
- 工具对比（应使用 List）
- 快讯类内容（应使用 Roundup）
- 没有明确步骤的主题

---

### blog-list-writer

**适用场景** ✅
- 工具榜单（"2026 年 10 大..."）
- 年度盘点
- 多选项对比（"A vs B vs C"）
- 资源合集

**不适用场景** ❌
- 单一工具深度教程（应使用 Tutorial）
- 时效性强的内容（应使用 Roundup）
- 只有 2-3 个选项的简单对比

---

### case-roundup-writer

**适用场景** ✅
- 新功能发布测评
- 病毒案例分析
- 有真实素材的洞察
- 快速验证某个假设

**不适用场景** ❌
- 没有真实素材时（会被 Material Gate 阻止）
- 需要系统性覆盖的主题
- 长青内容（evergreen content）

> ⚠️ **Material Gate**: Roundup 必须有真实素材支撑。如果只有想法没有素材，先收集素材再写。

---

## 输出预期对照

### Tutorial 输出结构
```
/articles/
└── how-to-{topic}/
    ├── index.md          # 主文章
    ├── metadata.json     # SEO 元数据
    └── assets/           # 配图（如有）
```

**典型内容样式**：
- 清晰的步骤编号
- 每步配截图/代码示例
- Pro Tips 穿插
- 结尾有 Next Steps

---

### List 输出结构
```
/articles/
└── best-{topic}-{year}/
    ├── index.md          # 主文章
    ├── metadata.json     # SEO 元数据
    └── comparison.json   # 结构化对比数据
```

**典型内容样式**：
- 排名或分类明确
- 每个选项有优缺点
- Quick Pick 推荐
- 对比表格

---

### Roundup 输出结构
```
/articles/
└── {topic}-roundup/
    ├── index.md          # 主文章
    └── metadata.json     # SEO 元数据
```

**典型内容样式**：
- 短小精悍
- 以案例/数据开头
- 快速给出结论
- 附真实素材来源

---

## 快速命令参考

| 场景 | 命令 | 说明 |
|------|------|------|
| 写教程 | `/write-tutorial` | 启动 Tutorial Writer |
| 写榜单 | `/write-list` | 启动 List Writer |
| 写案例 | `/write-roundup` | 启动 Roundup Writer |
| 不确定 | 说"帮我写..." | 让 smart-root 引导你选择 |

---

## 常见问题

**Q: 我的选题既有对比又有教程性质，怎么选？**

A: 看主要价值。如果读者核心目的是"学会做某事"，选 Tutorial，在文中简要对比工具；如果核心目的是"选出最合适的工具"，选 List。

**Q: Roundup 和 Tutorial 都能写工具测评，区别是？**

A: Roundup 是"快速分享发现"，300-600 字，适合新功能速报；Tutorial 是"教会使用"，1800+ 字，适合完整教程。

**Q: 没有足够素材但想写 Roundup 怎么办？**

A: 先用 `/fetch-transcript` 等工具收集素材，或者考虑选题是否更适合 Tutorial/List 形式。

---

*最后更新: 2026-01-21*
