# 广告类视频

> 品牌展示、产品演示、促销视频的 Remotion 实现方案

---

## 🎯 核心特点

广告视频的关键要素：

1. **视觉冲击力** - 大胆的动画和转场
2. **品牌一致性** - Logo、颜色、字体规范
3. **信息层级** - 主次分明的内容呈现
4. **情感共鸣** - 通过节奏和音乐营造氛围

---

## 📋 广告视频类型

### 1️⃣ 品牌展示视频

**典型结构**:
```
开场 Logo 动画 (2-3秒)
  ↓
品牌 Slogan (2-3秒)
  ↓
核心价值主张 (3-5秒)
  ↓
结束画面 + CTA (2秒)
```

**核心技术**:
- Logo 弹性动画 (spring)
- 探照灯/聚光灯效果
- 文字渐显/滑入
- 背景渐变

**详细教程**: [品牌展示实现](./brand-showcase.md)

---

### 2️⃣ 产品演示视频

**典型结构**:
```
产品登场 (2秒)
  ↓
功能点 1 + 演示 (3-4秒)
  ↓
功能点 2 + 演示 (3-4秒)
  ↓
功能点 3 + 演示 (3-4秒)
  ↓
产品总览 + 购买链接 (3秒)
```

**核心技术**:
- Series 连续播放功能点
- 产品图片/视频切换
- 特性标注动画
- 用户价值叙事

**详细教程**: [产品演示实现](./product-demo.md)

---

### 3️⃣ 促销视频

**典型结构**:
```
促销主题 (2秒) - "双11大促"
  ↓
优惠信息 (3秒) - "满300减50"
  ↓
产品展示 (5秒) - 轮播商品
  ↓
紧迫感 + CTA (2秒) - "限时3天"
```

**核心技术**:
- 倒计时动画
- 价格强调 (缩放/闪烁)
- 快速切换商品
- 紧迫感营造 (红色/倒计时)

**详细教程**: [促销视频模板](./promo-templates.md)

---

## 🎨 核心设计模式

### 品牌规范配置

创建 `brand.ts` 统一管理品牌资产：

```ts
export const BRAND_COLORS = {
  primary: "#3b82f6",
  secondary: "#8b5cf6",
  accent: "#f59e0b",
  background: "#1e293b",
  text: "#f1f5f9",
};

export const BRAND_FONTS = {
  heading: "Inter, sans-serif",
  body: "Roboto, sans-serif",
};

export const BRAND_ASSETS = {
  logo: "logo.png",
  backgroundMusic: "brand-music.mp3",
};
```

**应用**:
```tsx
import { BRAND_COLORS } from "./brand";

<h1 style={{ color: BRAND_COLORS.primary }}>
  {title}
</h1>
```

---

### 统一动画配置

```ts
export const ANIMATION_CONFIG = {
  fadeInDuration: 20,      // 淡入持续时间
  slideDistance: 50,       // 滑动距离
  springConfig: {
    damping: 10,
    stiffness: 100,
  },
};
```

---

### 多阶段动画模式

```tsx
const scenes = [
  { start: 0, duration: 60, content: <Intro /> },
  { start: 60, duration: 90, content: <Feature1 /> },
  { start: 150, duration: 90, content: <Feature2 /> },
  { start: 240, duration: 60, content: <CTA /> },
];

return (
  <Series>
    {scenes.map((scene, i) => (
      <Series.Sequence key={i} durationInFrames={scene.duration}>
        {scene.content}
      </Series.Sequence>
    ))}
  </Series>
);
```

---

## 🎬 实战案例

### 案例 1: SaaS 产品广告

**需求**:
- 15 秒广告
- 突出 3 个核心功能
- 品牌色调：蓝色/紫色渐变

**实现**:
```
0-60帧: Logo 弹性进入 + Slogan
60-150帧: 功能点 1 (自动化)
150-240帧: 功能点 2 (协作)
240-330帧: 功能点 3 (数据分析)
330-450帧: CTA + 网站链接
```

**核心代码**: 查看 [品牌展示教程](./brand-showcase.md#saas-产品案例)

---

### 案例 2: 电商促销短视频

**需求**:
- 10 秒快闪视频
- 突出折扣力度
- 营造紧迫感

**实现**:
```
0-30帧: "双11来了!" 爆炸动画
30-120帧: "全场5折" 缩放强调
120-210帧: 商品轮播
210-300帧: "仅剩3天" 倒计时 + 立即购买
```

**核心代码**: 查看 [促销视频教程](./promo-templates.md#电商促销案例)

---

## 🛠️ 可复用组件

### Logo 动画组件

```tsx
export const AnimatedLogo: React.FC<{ delayFrames?: number }> = ({
  delayFrames = 0,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({
    frame: frame - delayFrames,
    fps,
    config: { damping: 10 },
  });

  const opacity = interpolate(
    frame - delayFrames,
    [0, 20],
    [0, 1],
    { extrapolateRight: "clamp" }
  );

  return (
    <Img
      src={staticFile(BRAND_ASSETS.logo)}
      style={{
        transform: `scale(${scale})`,
        opacity,
      }}
    />
  );
};
```

---

### CTA 按钮组件

```tsx
export const CTAButton: React.FC<{ text: string; delayFrames?: number }> = ({
  text,
  delayFrames = 0,
}) => {
  const frame = useCurrentFrame();

  const scale = spring({
    frame: frame - delayFrames,
    fps,
  });

  return (
    <div
      style={{
        transform: `scale(${scale})`,
        padding: "20px 60px",
        backgroundColor: BRAND_COLORS.accent,
        borderRadius: 8,
        fontSize: 28,
        fontWeight: "bold",
        boxShadow: "0 10px 40px rgba(0,0,0,0.3)",
      }}
    >
      {text}
    </div>
  );
};
```

---

## 📚 深入学习

### 必读教程

1. **[品牌展示视频](./brand-showcase.md)** ⭐
   - Logo 动画实现
   - 探照灯效果详解
   - Slogan 动画
   - 多阶段动画编排

2. **[产品演示视频](./product-demo.md)**
   - 功能点展示模式
   - 产品图片动画
   - 用户价值叙事

3. **[促销视频模板](./promo-templates.md)**
   - 倒计时实现
   - 价格强调动画
   - 紧迫感营造

---

## 💡 最佳实践

### ✅ DO
- 统一使用品牌规范配置
- 动画时长控制在 2-3 秒内
- 使用 spring 实现弹性动画
- 保持视觉层级清晰

### ❌ DON'T
- 不要过度动画 (眼花缭乱)
- 不要使用第三方动画库
- 不要忽略音频同步
- 不要硬编码品牌颜色

---

## 🎯 下一步

选择你的使用场景：

- **品牌宣传** → [品牌展示教程](./brand-showcase.md)
- **产品推广** → [产品演示教程](./product-demo.md)
- **促销活动** → [促销视频教程](./promo-templates.md)

---

**返回** [知识库首页](../README.md) 📚
