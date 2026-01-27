# AliciBlog - 快速开始

> AI 内容工厂，70%+ 自动化博客生产 | v2.7
> 最后更新: 2026-01-22

## 新同事？从这里开始

1. **阅读 HANDOFF-GUIDE.md** (5分钟) - 快速交接指南
2. **配置环境 LOCAL-SETUP.md** (15分钟) - 本地环境配置
3. **阅读 CLAUDE.md** (10分钟) - 核心架构和命令速查

## 项目架构 (v2.7)

```
输入层 → 路由层 → [版本验证层] → 选题确认层 → 处理层 → [竞品验证层] → 输出层
```

**核心特性**:
- 选题发现 (growth-topic-scout v1.2)
- 交互式选题确认 (smart-root v2.2)
- 内容生成 (blog-tutorial-writer, blog-list-writer, case-roundup-writer)
- 质量控制 (editor v2.6, aeo-analyzer v2.4)
- 自动改进 (auto-improver v2.1)
- 竞品验证 (competitive-validator v1.0)

## 关键文档

| 文档 | 说明 |
|------|------|
| `HANDOFF-GUIDE.md` | **交接快速指南** - 新同事必读 |
| `LOCAL-SETUP.md` | **环境配置** - API 密钥和依赖 |
| `CLAUDE.md` | **主配置** - 架构、命令、规则 |
| `blueprint/` | 详细架构文档 |
| `.claude/skills/` | Skills 定义 |
| `reports/` | 项目输出 |

## 近期重大更新 (2026-01-21/22)

| 更新 | 说明 |
|------|------|
| **Tool Showdown** | 工具对决文章模式 (blog-list-writer v2.2) |
| **Version Verification** | 自动验证工具版本 (smart-root v2.2) |
| **Competitive Validator** | 竞品验证 PASS/FAIL 判定 |
| **竞品分析 v5.0** | 50 篇 invideo 标杆文章分析完成 |

## 常用命令

```bash
# 启动交互式创作 (推荐)
帮我写一篇关于 [主题] 的文章

# 工具对决文章
帮我写一篇 Kling vs Runway 的对比

# 直接命令
/write-tutorial    # 教程文章
/write-list        # 榜单文章
/write-roundup     # 案例汇总
/analyze-aeo FILE  # 质量评分
```

## 需要帮助？

- 查看 `blueprint/09-TROUBLESHOOTING.md`
- 查看 `docs/PROJECT-LOG-2026-01.md` - 项目管理日志
- 或直接问 Claude Code
