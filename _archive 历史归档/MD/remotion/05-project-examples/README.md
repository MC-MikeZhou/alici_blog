# 项目案例

> 已实现案例的详细分析和可复用组件模式

---

## 🎯 案例索引

### 已实现项目

| 项目 | 类型 | 技术亮点 | 详细文档 |
|------|------|----------|---------|
| **AI 视频生成器对比** | 数据可视化 + 广告 | 柱状图、探照灯、品牌展示 | [查看详情](./ai-video-generators.md) |

---

## 📁 项目资产位置

### 源代码目录

```
/vibe-skills/remotion-videos/
├── src/
│   ├── AnimatedBarChart.tsx      # 柱状图组件 ⭐
│   ├── SpotlightEffect.tsx       # 探照灯特效 ⭐
│   ├── brand.ts                  # 品牌规范配置
│   └── Root.tsx                  # Composition 注册
├── public/
│   └── (静态资源)
└── package.json
```

### 输出目录

```
/vibe-skills/remotion-videos/output/
├── ai-video-generators.mp4       # 已渲染视频
└── ...
```

---

## 🎬 案例 1: AI 视频生成器对比

> **项目详情**: [AI 视频生成器分析文档](./ai-video-generators.md)

### 项目概述

**目标**: 对比 4 个主流 AI 视频生成工具的评分

**视频结构**:
```
0-60帧: 开场 Logo 动画 + 探照灯效果
60-150帧: 标题 "AI Video Generators" 淡入
150-300帧: 柱状图依次进场 (交错动画)
300-450帧: 结束画面 + Slogan
```

**技术栈**:
- ✅ 柱状图动画 (spring)
- ✅ 探照灯效果 (径向渐变 + blur)
- ✅ 品牌展示 (Logo 弹性动画)
- ✅ 交错动画 (依次进场)

---

### 核心组件

#### 1. AnimatedBarChart 组件

**文件**: `src/AnimatedBarChart.tsx`

**功能**:
- 数据驱动柱状图
- 交错进场动画
- 弹性高度动画
- 颜色渐变

**代码精华**:
```tsx
const barHeight = spring({
  frame: frame - delay,
  fps,
  config: { damping: 15 }
}) * item.score * 50;
```

**复用方式**:
```tsx
import { AnimatedBarChart } from "./AnimatedBarChart";

<AnimatedBarChart
  data={[
    { name: "ChatGPT", score: 8.5, color: "#10b981" },
    { name: "Midjourney", score: 9.2, color: "#3b82f6" },
  ]}
/>
```

---

#### 2. SpotlightEffect 组件

**文件**: `src/SpotlightEffect.tsx`

**功能**:
- 径向渐变光晕
- 位置动画 (interpolate)
- 模糊效果 (filter: blur)

**代码精华**:
```tsx
const spotlightX = interpolate(frame, [0, 60], [0, 500]);

<div
  style={{
    background: "radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%)",
    left: spotlightX,
    filter: "blur(40px)"
  }}
/>
```

**复用方式**:
```tsx
import { SpotlightEffect } from "./SpotlightEffect";

<SpotlightEffect
  startFrame={0}
  endFrame={60}
  startX={0}
  endX={500}
/>
```

---

#### 3. 品牌规范配置

**文件**: `src/brand.ts`

**功能**:
- 统一颜色管理
- 字体规范
- 静态资源路径

**代码精华**:
```ts
export const BRAND_COLORS = {
  primary: "#3b82f6",
  secondary: "#8b5cf6",
  background: "#1e293b",
};

export const BRAND_FONTS = {
  heading: "Inter, sans-serif",
  body: "Roboto, sans-serif",
};
```

**复用方式**:
```tsx
import { BRAND_COLORS } from "./brand";

<h1 style={{ color: BRAND_COLORS.primary }}>Title</h1>
```

---

## 🧩 可复用组件库

### 提取的通用组件

基于已实现项目，提取以下可复用组件：

| 组件 | 功能 | 来源项目 | 复用指数 |
|------|------|---------|---------|
| `AnimatedBarChart` | 柱状图动画 | AI 视频生成器 | ⭐⭐⭐⭐⭐ |
| `SpotlightEffect` | 探照灯特效 | AI 视频生成器 | ⭐⭐⭐⭐ |
| `FadeInText` | 文字淡入 | AI 视频生成器 | ⭐⭐⭐⭐⭐ |
| `LogoAnimation` | Logo 弹性动画 | AI 视频生成器 | ⭐⭐⭐⭐ |

---

## 📚 学习路径

### 从案例中学习

1. **阅读源代码**
   - `/vibe-skills/remotion-videos/src/`
   - 理解组件结构
   - 分析动画参数

2. **运行项目**
   ```bash
   cd /vibe-skills/remotion-videos
   npm start
   ```

3. **修改参数**
   - 调整颜色 (`brand.ts`)
   - 修改数据 (评分、名称)
   - 改变动画时长

4. **提取组件**
   - 复制到新项目
   - 修改接口参数
   - 适配新场景

---

## 💡 最佳实践总结

### 从项目中总结的经验

#### ✅ DO

**1. 数据驱动设计**
```tsx
// ✅ 好 - 易于修改
const DATA = [
  { name: "ChatGPT", score: 8.5 },
  { name: "Midjourney", score: 9.2 },
];
```

**2. 组件化拆分**
```tsx
// ✅ 好 - 可复用
<AnimatedBarChart data={DATA} />
<SpotlightEffect startX={0} endX={500} />
```

**3. 统一品牌规范**
```tsx
// ✅ 好 - 易于维护
import { BRAND_COLORS } from "./brand";
```

---

#### ❌ DON'T

**1. 硬编码数据**
```tsx
// ❌ 不好
<div style={{ height: 425 }}>ChatGPT</div>
<div style={{ height: 460 }}>Midjourney</div>
```

**2. 重复动画逻辑**
```tsx
// ❌ 不好
const bar1Height = spring({ frame, fps });
const bar2Height = spring({ frame, fps });
const bar3Height = spring({ frame, fps });
```

**3. 分散的品牌资产**
```tsx
// ❌ 不好
<h1 style={{ color: "#3b82f6" }}>Title 1</h1>
<h2 style={{ color: "#3b82f6" }}>Title 2</h2>
```

---

## 🎯 下一步

### 应用到新项目

1. **选择案例**
   - [AI 视频生成器](./ai-video-generators.md) - 适合数据对比类

2. **提取组件**
   - 复制 `AnimatedBarChart.tsx`
   - 复制 `brand.ts`
   - 修改数据和颜色

3. **自定义修改**
   - 调整动画参数
   - 改变视觉风格
   - 添加新功能

4. **沉淀到知识库**
   - 记录新的组件
   - 补充使用文档
   - 分享最佳实践

---

## 📝 贡献新案例

欢迎补充新的项目案例：

1. 在 `05-project-examples/` 下创建 `[项目名].md`
2. 包含以下内容：
   - 项目概述
   - 技术栈
   - 核心组件分析
   - 可复用组件提取
   - 最佳实践总结
3. 更新本 README 的案例索引

---

**返回** [知识库首页](../README.md) 📚
