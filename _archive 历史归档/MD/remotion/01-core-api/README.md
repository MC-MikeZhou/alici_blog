# 核心 API 参考

> 掌握 Remotion 的基础 API 和动画系统

---

## 📋 核心概念总览

Remotion 的核心理念：**视频是关于时间的函数**

```tsx
视频(t) = React 组件(当前帧)
```

### 基础概念

| 概念 | 说明 | 示例 |
|------|------|------|
| **Frame** | 帧 - 视频的最小时间单位 | 0, 1, 2, ... |
| **FPS** | 帧率 - 每秒帧数 | 30, 60 |
| **Duration** | 时长 - 总帧数 | 150 (5秒 @ 30fps) |
| **Composition** | 视频组合 - 独立的视频片段 | `<Composition id="MyVideo" />` |

---

## 🎯 核心 Hooks

### useCurrentFrame()

获取当前渲染的帧号

```tsx
import { useCurrentFrame } from "remotion";

const frame = useCurrentFrame(); // 0, 1, 2, 3, ...
```

**应用场景**:
- 所有动画的基础
- 条件渲染 (`{frame >= 30 && <Content />}`)
- 时间计算

### useVideoConfig()

获取视频配置信息

```tsx
import { useVideoConfig } from "remotion";

const { fps, durationInFrames, width, height } = useVideoConfig();

// 计算当前秒数
const seconds = frame / fps;
```

**应用场景**:
- 响应式布局 (根据 width/height)
- 时间计算 (fps)
- 动画范围计算 (durationInFrames)

---

## 🎨 动画系统

### interpolate - 线性插值

将帧数映射到任意值

```tsx
import { interpolate } from "remotion";

const opacity = interpolate(
  frame,           // 输入值
  [0, 30],         // 输入范围
  [0, 1],          // 输出范围
  {
    extrapolateLeft: "clamp",   // 左侧边界行为
    extrapolateRight: "clamp"   // 右侧边界行为
  }
);
```

**边界行为**:
- `clamp` - 固定在边界值 (推荐)
- `extend` - 线性延伸
- `identity` - 返回输入值

**详细教程**: [interpolate 和 spring](./interpolate-spring.md)

### spring - 弹性动画

基于物理的弹性动画

```tsx
import { spring } from "remotion";

const scale = spring({
  frame,
  fps,
  config: {
    damping: 10,     // 阻尼 (越小越弹)
    stiffness: 100,  // 刚度 (越大越快)
    mass: 1          // 质量
  }
});
```

**配置参数**:
- **damping**: 10 (推荐) - 控制震荡程度
- **stiffness**: 100 (推荐) - 控制动画速度
- **mass**: 1 (默认) - 物体质量

**详细教程**: [interpolate 和 spring](./interpolate-spring.md)

---

## ⏱️ 时序控制

### Sequence - 绝对时间定位

在特定帧范围内显示内容

```tsx
import { Sequence } from "remotion";

<Sequence from={30} durationInFrames={60}>
  <Scene />
</Sequence>
```

**参数**:
- `from` - 开始帧
- `durationInFrames` - 持续帧数
- `layout` - 布局方式 (`"absolute-fill"` | `"none"`)

### Series - 连续播放

自动计算时间偏移

```tsx
import { Series } from "remotion";

<Series>
  <Series.Sequence durationInFrames={60}>
    <Scene1 />
  </Series.Sequence>
  <Series.Sequence durationInFrames={90}>
    <Scene2 />
  </Series.Sequence>
</Series>
```

**详细对比**: [Sequence vs Series](./sequence-series.md)

---

## 🎬 媒体组件

### Img - 图片

```tsx
import { Img, staticFile } from "remotion";

<Img src={staticFile("logo.png")} />
```

### Video - 视频

```tsx
import { Video, staticFile } from "remotion";

<Video src={staticFile("intro.mp4")} />
```

### Audio - 音频

```tsx
import { Audio, staticFile } from "remotion";

<Audio src={staticFile("music.mp3")} volume={0.5} />
```

**详细教程**: [音频、视频、图片使用](./audio-video-img.md)

---

## 📦 实用工具

### staticFile()

加载 `public/` 目录下的静态资源

```tsx
import { staticFile } from "remotion";

const logoPath = staticFile("images/logo.png"); // public/images/logo.png
```

### random()

生成可复现的随机数

```tsx
import { random } from "remotion";

const randomValue = random("seed"); // 0.123... (固定)
```

**应用场景**:
- 粒子效果
- 随机位置
- 保持渲染一致性

### interpolateColors()

颜色插值

```tsx
import { interpolateColors } from "remotion";

const color = interpolateColors(
  frame,
  [0, 150],
  ["#3b82f6", "#8b5cf6"]
);
```

---

## 📚 深入学习

### 必读教程

1. **[Sequence vs Series](./sequence-series.md)** - 时序控制详解
   - 何时使用 Sequence
   - 何时使用 Series
   - layout 属性详解

2. **[interpolate + spring](./interpolate-spring.md)** - 动画系统详解
   - interpolate 高级用法
   - spring 参数调优
   - 交错动画模式

3. **[音频、视频、图片](./audio-video-img.md)** - 媒体组件最佳实践
   - staticFile 使用技巧
   - 媒体加载优化
   - 常见问题解决

---

## 🎯 快速开始

根据你的需求选择：

- **做品牌视频** → [广告类视频](../02-ads-videos/README.md)
- **做配图视频** → [配图类视频](../03-visual-videos/README.md)
- **做数据可视化** → [数据分析视频](../04-data-viz-videos/README.md)

---

**返回** [知识库首页](../README.md) 📚
