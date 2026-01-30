# Blog Cover Generator Changelog

记录 blog-cover-generator skill 的所有版本变更。

---

## [2.0] - 2026-01-30

### 新增 (Added)

- **双类型架构**: 支持 Professional (Category A) 和 Thumbnail Style (Category B) 两种封面风格
- **Thumbnail Style Cover**: 4 种子类型
  - T1 Creator Showcase (作品展示)
  - T2 Money/Success (收益变现)
  - T3 Tutorial Hero (教程指南)
  - T4 Reaction Shot (惊喜评测)
- **Alici 模特库**: 预设品牌模特
  - 👩 AliciLucy: `https://ct2.alici.ai/static/image/other/design/aliciLucy.png`
  - 👨 AliciAndy: `https://ct2.alici.ai/static/image/other/design/aliciAndy.png`
- **人物来源系统**: 支持 Alici 模特 / AI 生成 / 用户自定义照片
- **高饱和色彩系统**: Purple/Red/Blue/Green + Gold/Pink/Orange
- **Phase 1.5**: 自动检测封面类型 (thumbnail 关键词检测)
- **Phase 2-T**: Thumbnail 子类型选择逻辑
- **THUMBNAIL_VISUAL_GUIDE.md**: 完整 Thumbnail 视觉规范文档

### 变更 (Changed)

- `SKILL.md` 版本升级 v1.0 → v2.0
- 执行流程新增分支逻辑支持双类型

### 文件变更

| 文件 | 操作 | 说明 |
|------|------|------|
| `SKILL.md` | 修改 | v1.0 → v2.0, 双类型架构 |
| `THUMBNAIL_VISUAL_GUIDE.md` | 新建 | 完整 Thumbnail 视觉规范 |
| `CHANGELOG.md` | 新建 | 改动日志 |
| `/skills/_docs/BRAND_VISUAL_GUIDE.md` | 修改 | v1.0 → v1.1, Section 0 引用 |

---

## [1.0] - 2026-01-22

### 新增 (Added)

- 初始版本发布
- **6 种背景类型**: Gradient Glow, Fluid Shape, Geometric Minimal, Typography-Led, Data Abstract, Grid/Matrix
- **绿色品牌色系**: Core Teal (#4FD1C5), Light Teal (#81E6D9), Deep Teal (#319795)
- **自动内容类型检测**: 根据标题/分类/标签选择背景类型
- **标题智能分割**: H1 ≤3 词优化
- **FAL.ai 集成**: nano-banana 模型生成
- **CDN 自动上传**: rsync 上传到 ct2.alici.ai
- **元数据输出**: 06-cover-metadata.json

### 文件变更

| 文件 | 操作 | 说明 |
|------|------|------|
| `SKILL.md` | 新建 | v1.0 初始版本 |
| `references/PROMPT_TEMPLATES.md` | 新建 | 6 种背景类型模板 |

---

## 格式说明

- **新增 (Added)**: 新功能
- **变更 (Changed)**: 现有功能的修改
- **废弃 (Deprecated)**: 即将移除的功能
- **移除 (Removed)**: 已移除的功能
- **修复 (Fixed)**: Bug 修复
- **安全 (Security)**: 安全相关修复
