# Remotion 知识库

> **目标**: 沉淀 Remotion 使用经验，打造可复用的视频生成知识资产
>
> **适用场景**: 广告视频、配图视频、数据可视化、AI 工具演示

---

## 📚 知识库导航

### 🚀 快速开始
- **[快速入门](./00-quick-start.md)** - 项目搭建、渲染命令、核心概念

### 📖 核心内容

#### 1️⃣ [核心 API 参考](./01-core-api/README.md)
掌握 Remotion 的基础 API 和动画系统

#### 2️⃣ [广告类视频](./02-ads-videos/README.md) ⭐
品牌展示、产品演示、促销视频模板

#### 3️⃣ [配图类视频](./03-visual-videos/README.md) ⭐
图片幻灯片、Ken Burns 效果、图文组合

#### 4️⃣ [数据可视化视频](./04-data-viz-videos/README.md) ⭐
柱状图、饼图、对比分析、评分展示

#### 5️⃣ [项目案例](./05-project-examples/README.md)
已实现案例的详细分析和可复用组件

### ⚡ 快速参考
- **[速查表](./99-cheatsheet.md)** - 一页纸精华、常用代码片段

---

## 🎯 按使用场景导航

### 我要做品牌宣传视频
1. [广告视频概览](./02-ads-videos/README.md)
2. [品牌展示教程](./02-ads-videos/brand-showcase.md) - 探照灯效果、Logo 动画
3. [核心 API - 动画系统](./01-core-api/interpolate-spring.md)

### 我要做图片配乐视频
1. [配图视频概览](./03-visual-videos/README.md)
2. [幻灯片实现](./03-visual-videos/slideshow.md)
3. [Ken Burns 效果](./03-visual-videos/ken-burns.md) - 缩放平移动画

### 我要做数据对比视频
1. [数据可视化概览](./04-data-viz-videos/README.md)
2. [柱状图动画](./04-data-viz-videos/bar-chart.md) - 交错进场、弹性动画
3. [对比效果](./04-data-viz-videos/comparison.md) - 并排/前后对比

### 我要做产品演示视频
1. [产品演示教程](./02-ads-videos/product-demo.md)
2. [媒体组件使用](./01-core-api/audio-video-img.md)
3. [时序控制](./01-core-api/sequence-series.md)

---

## 📖 推荐阅读顺序

### 新手路径
1. [快速入门](./00-quick-start.md) - 10 分钟上手
2. [核心 API 概览](./01-core-api/README.md) - 理解基础概念
3. [速查表](./99-cheatsheet.md) - 常用代码备查
4. 选择一个场景深入学习 (广告/配图/数据)

### 进阶路径
1. [时序控制深入](./01-core-api/sequence-series.md) - Sequence vs Series
2. [动画系统深入](./01-core-api/interpolate-spring.md) - interpolate + spring
3. [项目案例分析](./05-project-examples/README.md) - 学习最佳实践
4. 实现自己的项目，沉淀到知识库

---

## 🛠️ 项目资产

### 已实现案例
- **AI 视频生成器对比** ([分析文档](./05-project-examples/ai-video-generators.md))
  - 柱状图动画
  - 评分对比
  - 品牌展示
  - 探照灯效果

### 可复用组件
```
/vibe-skills/remotion-videos/src/
├── AnimatedBarChart.tsx      # 柱状图组件
├── SpotlightEffect.tsx       # 探照灯特效
└── brand.ts                  # 品牌规范配置
```

---

## 📝 内容更新记录

| 日期 | 版本 | 更新内容 |
|------|------|---------|
| 2026-01-24 | v1.0 | 初始化知识库框架 |

---

## 🔗 外部资源

### 官方文档
- [Remotion 官方文档](https://www.remotion.dev/docs)
- [核心概念](https://www.remotion.dev/docs/the-fundamentals)
- [API 参考](https://www.remotion.dev/docs/api)

### 社区资源
- [Remotion Showcase](https://www.remotion.dev/showcase)
- [GitHub 官方仓库](https://github.com/remotion-dev/remotion)

---

## 💡 贡献指南

本知识库持续更新，欢迎补充：

1. **新的使用场景** - 在对应分类下添加 `.md` 文件
2. **代码优化** - 提交更好的实现方式
3. **案例分析** - 在 `05-project-examples/` 下添加新案例
4. **常见问题** - 补充到 `99-cheatsheet.md`

---

**开始探索** → [快速入门](./00-quick-start.md) 🚀
