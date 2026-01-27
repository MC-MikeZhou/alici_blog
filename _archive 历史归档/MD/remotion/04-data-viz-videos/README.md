# 数据可视化视频

> 柱状图、饼图、折线图、对比分析的 Remotion 实现方案

---

## 🎯 核心特点

数据可视化视频的关键要素：

1. **数据准确性** - 正确呈现数据关系
2. **视觉清晰** - 图表易读、标注明确
3. **动画流畅** - 数据进场动画自然
4. **交错效果** - 多数据依次展示

---

## ⚠️ 核心原则

### **禁用第三方图表库**

```tsx
// ❌ 错误 - 第三方库与 Remotion 冲突
import { Chart } from "chart.js";
import { motion } from "framer-motion";

// ✅ 正确 - 使用 Remotion 原生动画
import { spring, interpolate } from "remotion";
```

**原因**:
- Chart.js / D3.js 依赖浏览器动画 API
- Framer Motion 等库不支持帧渲染
- Remotion 需要完全可预测的渲染

**解决方案**:
- 使用 CSS + Remotion 动画手写图表
- 使用 SVG + interpolate 实现复杂图表

---

## 📊 图表类型

### 1️⃣ 柱状图 (Bar Chart)

**典型应用**:
- 数据对比 (产品、竞品)
- 评分展示 (满分 10 分)
- 统计数据 (销量、用户量)

**核心技术**:
- **交错进场** - 每个柱子依次出现
- **弹性动画** - spring 实现弹性高度
- **颜色渐变** - 视觉层次

**详细教程**: [柱状图动画](./bar-chart.md)

**代码示例**:
```tsx
const barHeight = spring({
  frame: frame - delay,
  fps,
  config: { damping: 15 }
}) * maxHeight;

<div style={{ height: barHeight, backgroundColor: color }} />
```

---

### 2️⃣ 饼图 (Pie Chart)

**典型应用**:
- 占比分析 (市场份额)
- 分类统计 (用户分布)
- 百分比展示

**核心技术**:
- **SVG 绘制** - `<circle>` + `stroke-dashoffset`
- **扇形动画** - 逐步绘制
- **标签动画** - 百分比数字滚动

**详细教程**: [饼图动画](./pie-chart.md)

---

### 3️⃣ 折线图 (Line Chart)

**典型应用**:
- 趋势分析 (增长曲线)
- 时间序列数据
- 对比走势

**核心技术**:
- **SVG Path** - `<path>` 绘制折线
- **路径动画** - `stroke-dashoffset` 逐步绘制
- **数据点动画** - 交错显示

**详细教程**: [折线图动画](./line-chart.md)

---

### 4️⃣ 数据对比

**典型应用**:
- 前后对比 (改进效果)
- 并排对比 (竞品分析)
- 评分对比 (产品评测)

**核心技术**:
- **并排布局** - Grid / Flex
- **同步动画** - 同时进场
- **差异强调** - 颜色/大小

**详细教程**: [对比效果](./comparison.md)

---

### 5️⃣ 评分/星级

**典型应用**:
- 产品评分 (5星制)
- 用户评价
- 能力雷达图

**核心技术**:
- **星星动画** - 依次点亮
- **进度条** - 宽度动画
- **数字滚动** - interpolate 数值

**详细教程**: [评分展示](./ratings.md)

---

## 🎨 核心设计模式

### 数据驱动配置

```tsx
const DATA = [
  { name: "ChatGPT", score: 8.5, color: "#10b981" },
  { name: "Midjourney", score: 9.2, color: "#3b82f6" },
  { name: "Runway", score: 7.8, color: "#8b5cf6" },
  { name: "ElevenLabs", score: 8.9, color: "#f59e0b" },
];
```

**优势**:
- 易于修改数据
- 便于循环渲染
- 支持动态加载

---

### 交错动画模式

```tsx
{DATA.map((item, i) => {
  const delay = i * 15; // 每个延迟 15 帧

  const barHeight = spring({
    frame: frame - delay,
    fps,
    config: { damping: 15 },
  }) * item.score * 50;

  return (
    <div
      key={i}
      style={{
        height: barHeight,
        backgroundColor: item.color,
      }}
    />
  );
})}
```

---

### 颜色系统

```ts
export const CHART_COLORS = {
  primary: "#3b82f6",    // 蓝色
  success: "#10b981",    // 绿色
  warning: "#f59e0b",    // 橙色
  danger: "#ef4444",     // 红色
  purple: "#8b5cf6",     // 紫色
  gray: "#6b7280",       // 灰色
};

// 渐变色数组
export const GRADIENT_COLORS = [
  "#3b82f6", "#8b5cf6", "#ec4899", "#f59e0b"
];
```

---

## 🎬 实战案例

### 案例 1: AI 工具评分对比

**需求**:
- 4 个 AI 工具
- 展示评分 (满分 10 分)
- 柱状图 + 数字标签

**实现**:
```tsx
const AI_TOOLS = [
  { name: "ChatGPT", score: 8.5 },
  { name: "Midjourney", score: 9.2 },
  { name: "Runway", score: 7.8 },
  { name: "ElevenLabs", score: 8.9 },
];

<AnimatedBarChart data={AI_TOOLS} />
```

**效果**:
- 柱子依次弹性进场 (每个延迟 15 帧)
- 数字滚动动画
- 最高分高亮显示

**核心代码**: 查看 [柱状图教程](./bar-chart.md#ai-工具评分案例)

---

### 案例 2: 产品功能雷达图

**需求**:
- 5 个维度 (性能、易用性、价格...)
- 雷达图展示
- 多产品对比

**实现**: 查看 [评分展示教程](./ratings.md#雷达图案例)

---

### 案例 3: 增长趋势折线图

**需求**:
- 展示用户增长
- 6 个月数据
- 折线逐步绘制

**实现**: 查看 [折线图教程](./line-chart.md#增长趋势案例)

---

## 🛠️ 可复用组件

### AnimatedBarChart 组件

```tsx
export const AnimatedBarChart: React.FC<{
  data: Array<{ name: string; score: number; color?: string }>;
  maxScore?: number;
  delayPerBar?: number;
}> = ({ data, maxScore = 10, delayPerBar = 15 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ display: "flex", gap: 40, alignItems: "flex-end" }}>
      {data.map((item, i) => {
        const delay = i * delayPerBar;
        const barHeight = spring({
          frame: frame - delay,
          fps,
          config: { damping: 15 },
        }) * (item.score / maxScore) * 400;

        return (
          <div key={i} style={{ textAlign: "center" }}>
            <div
              style={{
                height: barHeight,
                width: 80,
                backgroundColor: item.color || CHART_COLORS.primary,
                borderRadius: "8px 8px 0 0",
              }}
            />
            <p style={{ marginTop: 10 }}>{item.name}</p>
            <p style={{ fontSize: 32, fontWeight: "bold" }}>{item.score}</p>
          </div>
        );
      })}
    </div>
  );
};
```

---

### 进度条组件

```tsx
export const ProgressBar: React.FC<{
  label: string;
  value: number;
  maxValue: number;
  color?: string;
  delayFrames?: number;
}> = ({ label, value, maxValue, color = CHART_COLORS.primary, delayFrames = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const width = spring({
    frame: frame - delayFrames,
    fps,
  }) * (value / maxValue) * 100;

  return (
    <div>
      <p style={{ marginBottom: 8 }}>{label}</p>
      <div style={{ width: "100%", height: 30, backgroundColor: "#e5e7eb", borderRadius: 4 }}>
        <div
          style={{
            width: `${width}%`,
            height: "100%",
            backgroundColor: color,
            borderRadius: 4,
          }}
        />
      </div>
    </div>
  );
};
```

---

## 📚 深入学习

### 必读教程

1. **[柱状图动画](./bar-chart.md)** ⭐⭐⭐
   - 交错进场实现
   - 弹性高度动画
   - 颜色渐变技巧

2. **[饼图动画](./pie-chart.md)**
   - SVG 圆形绘制
   - stroke-dashoffset 动画
   - 百分比标签

3. **[折线图动画](./line-chart.md)**
   - Path 路径绘制
   - 逐步展现动画
   - 数据点标注

4. **[对比效果](./comparison.md)** ⭐
   - 并排对比布局
   - 前后对比动画
   - 差异强调技巧

5. **[评分展示](./ratings.md)** ⭐
   - 星级动画
   - 进度条动画
   - 雷达图实现

---

## 💡 最佳实践

### ✅ DO
- 使用 Remotion 原生动画
- 数据驱动组件设计
- 交错动画提升观感
- 颜色区分数据类别

### ❌ DON'T
- 不要使用 Chart.js / D3.js
- 不要使用 Framer Motion
- 不要硬编码数据
- 不要过度动画 (眼花缭乱)

---

## 🎯 下一步

选择你的使用场景：

- **做评分对比** → [柱状图教程](./bar-chart.md)
- **做占比分析** → [饼图教程](./pie-chart.md)
- **做趋势展示** → [折线图教程](./line-chart.md)
- **做数据对比** → [对比效果教程](./comparison.md)
- **做评分展示** → [评分教程](./ratings.md)

---

**返回** [知识库首页](../README.md) 📚
