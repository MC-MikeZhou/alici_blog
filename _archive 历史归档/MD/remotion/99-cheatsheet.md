# Remotion 速查表

> 一页纸精华 - 快速查找常用代码片段

---

## 🧩 核心 API

### 获取帧和配置

```tsx
import { useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps, durationInFrames, width, height } = useVideoConfig();
```

### 动画函数

```tsx
import { interpolate, spring } from "remotion";

// 线性插值
const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateRight: "clamp"
});

// 弹性动画
const scale = spring({
  frame,
  fps,
  config: { damping: 10, stiffness: 100 }
});
```

### 时序控制

```tsx
import { Sequence, Series } from "remotion";

// 绝对时间定位
<Sequence from={30} durationInFrames={60}>
  <Scene />
</Sequence>

// 连续播放
<Series>
  <Series.Sequence durationInFrames={60}><Scene1 /></Series.Sequence>
  <Series.Sequence durationInFrames={90}><Scene2 /></Series.Sequence>
</Series>
```

---

## 🎬 常用动画模式

### 淡入淡出

```tsx
// 淡入 (0-30帧)
const fadeIn = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" });

// 淡出 (120-150帧)
const fadeOut = interpolate(frame, [120, 150], [1, 0], { extrapolateLeft: "clamp" });

// 淡入淡出
const opacity = interpolate(frame, [0, 30, 120, 150], [0, 1, 1, 0]);
```

### 缩放动画

```tsx
// 弹性缩放
const scale = spring({ frame, fps });

// 线性缩放
const scale = interpolate(frame, [0, 30], [0.5, 1]);

<div style={{ transform: `scale(${scale})` }}>Content</div>
```

### 滑入滑出

```tsx
// 从左滑入
const translateX = interpolate(frame, [0, 30], [-100, 0]);

// 向上滑入
const translateY = interpolate(frame, [0, 30], [100, 0]);

<div style={{ transform: `translate(${translateX}%, ${translateY}%)` }}>
  Content
</div>
```

### 交错动画

```tsx
// 多个元素依次出现
const items = [1, 2, 3, 4];

{items.map((item, i) => {
  const delay = i * 10; // 每个元素延迟 10 帧
  const opacity = interpolate(
    frame - delay,
    [0, 20],
    [0, 1],
    { extrapolateRight: "clamp", extrapolateLeft: "clamp" }
  );
  return <div key={i} style={{ opacity }}>{item}</div>;
})}
```

---

## 📊 数据可视化

### 柱状图动画

```tsx
const barHeight = spring({
  frame: frame - delay,
  fps,
  config: { damping: 15 }
}) * maxHeight;

<div
  style={{
    height: barHeight,
    width: 60,
    backgroundColor: "#3b82f6",
    transition: "all 0.3s"
  }}
/>
```

### 进度条

```tsx
const progress = interpolate(
  frame,
  [0, durationInFrames],
  [0, 100],
  { extrapolateRight: "clamp" }
);

<div style={{ width: `${progress}%`, height: 20, backgroundColor: "green" }} />
```

### 数字滚动

```tsx
const value = Math.round(
  interpolate(frame, [0, 60], [0, targetValue], {
    extrapolateRight: "clamp"
  })
);

<span>{value.toLocaleString()}</span>
```

---

## 🎨 视觉效果

### 阴影和光晕

```tsx
// 文字阴影
textShadow: "2px 2px 8px rgba(0, 0, 0, 0.3)"

// 盒阴影
boxShadow: "0 10px 40px rgba(0, 0, 0, 0.2)"

// 光晕效果
boxShadow: "0 0 30px rgba(59, 130, 246, 0.6)"
```

### 渐变背景

```tsx
// 线性渐变
background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"

// 径向渐变
background: "radial-gradient(circle, #667eea 0%, #764ba2 100%)"
```

### 探照灯效果

```tsx
const spotlightX = interpolate(frame, [0, 60], [0, 500]);

<div
  style={{
    position: "absolute",
    width: 300,
    height: 300,
    background: "radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%)",
    left: spotlightX,
    top: 200,
    filter: "blur(40px)"
  }}
/>
```

---

## 🖼️ 媒体组件

### 图片

```tsx
import { Img, staticFile } from "remotion";

<Img src={staticFile("image.jpg")} />
```

### 视频

```tsx
import { Video, staticFile } from "remotion";

<Video src={staticFile("video.mp4")} />
```

### 音频

```tsx
import { Audio, staticFile } from "remotion";

<Audio src={staticFile("music.mp3")} />
```

### Ken Burns 效果

```tsx
const scale = interpolate(frame, [0, 150], [1, 1.2]);
const translateX = interpolate(frame, [0, 150], [0, -10]);

<Img
  src={staticFile("photo.jpg")}
  style={{
    width: "100%",
    height: "100%",
    objectFit: "cover",
    transform: `scale(${scale}) translateX(${translateX}%)`
  }}
/>
```

---

## 🔧 实用工具

### 延迟计算

```tsx
const delay = (startFrame: number) => Math.max(0, frame - startFrame);

const opacity = interpolate(
  delay(30),
  [0, 20],
  [0, 1],
  { extrapolateRight: "clamp" }
);
```

### 颜色插值

```tsx
import { interpolateColors } from "remotion";

const color = interpolateColors(
  frame,
  [0, 150],
  ["#3b82f6", "#8b5cf6"]
);
```

### 条件渲染

```tsx
{frame >= 30 && frame < 90 && (
  <div>显示在 30-90 帧之间</div>
)}
```

---

## 📐 布局技巧

### 居中布局

```tsx
<div
  style={{
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    height: "100%"
  }}
>
  <Content />
</div>
```

### 绝对定位

```tsx
<div
  style={{
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)"
  }}
>
  Content
</div>
```

### Grid 布局

```tsx
<div
  style={{
    display: "grid",
    gridTemplateColumns: "repeat(2, 1fr)",
    gap: 40
  }}
>
  {items.map(item => <Card key={item.id} {...item} />)}
</div>
```

---

## 🎯 性能优化

### 避免重复计算

```tsx
// ❌ 不好
{items.map((item, i) => {
  const delay = i * 10;
  const opacity = interpolate(frame - delay, [0, 20], [0, 1]);
  return <div style={{ opacity }}>{item}</div>;
})}

// ✅ 更好
const getOpacity = (index: number) => {
  const delay = index * 10;
  return interpolate(frame - delay, [0, 20], [0, 1], {
    extrapolateRight: "clamp"
  });
};

{items.map((item, i) => (
  <div style={{ opacity: getOpacity(i) }}>{item}</div>
))}
```

### 使用 useMemo

```tsx
import { useMemo } from "react";

const animatedData = useMemo(() => {
  return data.map((item, i) => ({
    ...item,
    delay: i * 10
  }));
}, [data]);
```

---

## 🚨 常见陷阱

### ❌ 不要在 interpolate 中使用浮点范围

```tsx
// ❌ 错误
const opacity = interpolate(frame, [0.5, 30.5], [0, 1]);

// ✅ 正确
const opacity = interpolate(frame, [0, 30], [0, 1]);
```

### ❌ 不要忘记 extrapolate

```tsx
// ❌ 可能导致意外值
const opacity = interpolate(frame, [0, 30], [0, 1]);

// ✅ 明确边界行为
const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateRight: "clamp",
  extrapolateLeft: "clamp"
});
```

### ❌ 不要在 Remotion 中使用第三方动画库

```tsx
// ❌ 错误 - Framer Motion 等库与 Remotion 冲突
import { motion } from "framer-motion";

// ✅ 正确 - 使用 Remotion 原生动画
import { spring, interpolate } from "remotion";
```

---

## 📚 快速链接

- [核心 API](./01-core-api/README.md)
- [广告视频](./02-ads-videos/README.md)
- [配图视频](./03-visual-videos/README.md)
- [数据可视化](./04-data-viz-videos/README.md)
- [项目案例](./05-project-examples/README.md)

---

**返回** [知识库首页](./README.md) 📚
