# HeyGen 知识库

> AI 数字人视频生成平台使用指南 - 沉淀经验，便于与 Remotion 结合实验

---

## HeyGen 是什么？

HeyGen 是一个基于 AI 的**数字人视频生成平台**，通过 API 调用即可生成带有虚拟形象（Avatar）和语音的专业视频内容。

### 核心能力

- **AI Avatar** - 数百种预设形象，支持自定义数字人
- **语音合成** - 多语言 TTS，支持语速/音调控制
- **口型同步** - 自动匹配语音与口型动作
- **视频定制** - 背景、字幕、分辨率灵活配置
- **批量生成** - 模板化生产，适合规模化内容

---

## 与 Remotion 的对比

| 维度 | Remotion | HeyGen |
|------|----------|---------|
| **定位** | 代码驱动的视频合成 | API 驱动的数字人生成 |
| **核心能力** | 动画、图表、时序控制 | AI 形象、语音合成、口型同步 |
| **技术栈** | React + TypeScript | REST API + Webhook |
| **优势** | 灵活度高，可编程性强 | 零视频制作经验即可生成 |
| **局限** | 需要编码，无真人形象 | 自定义受 API 限制 |

### 组合使用场景

**Remotion + HeyGen = 数字人讲解 + 动态背景/图表**

```
案例：技术教程视频
1. HeyGen 生成数字人讲解（透明背景）
2. Remotion 构建动画图表/代码演示
3. 两者叠加合成最终视频
```

---

## 知识库导航

### 🚀 快速开始
- [**快速入门**](00-quick-start.md) - API 配置 + 第一个视频
- [**API 配置指南**](00-heygen-api-setup-guide.md) - 详细的 API Key 配置步骤 🆕
- [**HeyGen + Remotion 实施指南**](01-implementation-guide.md) - 数字人与动画结合的完整方案 🆕

### 📚 核心文档

#### [01-core-api/](01-core-api/) - 核心 API 参考
- [API 概览与认证](01-core-api/README.md)
- [形象配置 (Avatars)](01-core-api/avatars.md)
- [语音配置 (Voices)](01-core-api/voices.md)
- [视频生成流程](01-core-api/video-generation.md)

#### [02-customization/](02-customization/) - 自定义配置
- [自定义概览](02-customization/README.md)
- [背景配置](02-customization/backgrounds.md)
- [分辨率与比例](02-customization/dimensions.md)
- [字幕配置](02-customization/captions.md)

#### [03-advanced/](03-advanced/) - 高级功能
- [高级功能概览](03-advanced/README.md)
- [模板化生成](03-advanced/templates.md)
- [照片生成数字人](03-advanced/photo-avatars.md)
- [实时流式数字人](03-advanced/streaming.md)
- [视频翻译/配音](03-advanced/translation.md)

#### [04-integration/](04-integration/) - 集成方案 ⭐
- [集成概览](04-integration/README.md)
- [**Remotion + HeyGen 组合**](04-integration/remotion-heygen.md) ⭐
- [Webhook 事件处理](04-integration/webhooks.md)
- [自动化工作流模式](04-integration/workflow-patterns.md)

#### [05-experiments/](05-experiments/) - 实验记录
- [实验索引](05-experiments/README.md)
- 数字人 + 数据可视化
- 数字人 + 产品演示
- 多语言内容生成
- 交互式数字人对话

### 🔖 工具

- [**API 速查表**](99-cheatsheet.md) - 常用命令与 Endpoints

---

## 实验方向

1. **数字人 + 数据可视化** - 数字人讲解柱状图/趋势图
2. **数字人 + 产品演示** - 数字人介绍产品功能特性
3. **多语言内容** - 同一脚本生成多语言版本
4. **交互式数字人** - Streaming Avatar 实时对话
5. **照片数字人** - 用静态照片生成动态视频

---

## 参考资源

- [HeyGen 官方文档](https://docs.heygen.com/)
- [HeyGen Skills 仓库](https://github.com/heygen-com/skills)
- [Remotion 知识库](../remotion/) - 本地知识库

---

## 更新日志

- **2026-01-24** - 🎉 完成 HeyGen + Remotion 集成实施
  - ✅ HeyGen API 配置指南
  - ✅ 视频生成脚本 (`scripts/heygen-generate.sh`)
  - ✅ Remotion 组合组件 (`AvatarIntro.tsx`)
  - ✅ 完整实施文档 (`01-implementation-guide.md`)
- **2026-01** - 创建知识库框架
- 待添加：各章节详细内容
