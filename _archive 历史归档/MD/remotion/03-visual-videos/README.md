# 配图类视频

> 图片幻灯片、Ken Burns 效果、图文组合的 Remotion 实现方案

---

## 🎯 核心特点

配图类视频的关键要素：

1. **图片质量** - 高清素材 + 合适尺寸
2. **过渡效果** - 流畅的切换动画
3. **音乐节奏** - 图片切换与音乐同步
4. **视觉统一** - 一致的设计风格

---

## 📋 配图视频类型

### 1️⃣ 图片幻灯片

**典型应用**:
- 旅行 Vlog
- 产品展示
- 回忆相册
- 教程配图

**核心技术**:
- Series 实现连续播放
- 淡入淡出过渡
- Ken Burns 效果 (可选)
- 背景音乐同步

**详细教程**: [幻灯片实现](./slideshow.md)

---

### 2️⃣ Ken Burns 效果

**什么是 Ken Burns**:
纪录片常用的图片动画 - 缓慢缩放 + 平移，让静态图片"动起来"

**典型应用**:
- 人物访谈配图
- 历史纪录片
- 情感叙事视频

**核心技术**:
- `transform: scale()` 缩放
- `transform: translate()` 平移
- 组合动画参数调优

**详细教程**: [Ken Burns 效果](./ken-burns.md)

---

### 3️⃣ 图片 + 文字组合

**典型应用**:
- 社交媒体图文
- 引用卡片
- 教程步骤展示
- 数据报告配图

**核心技术**:
- 图层叠加 (z-index)
- 文字阴影/背景
- 图文位置动画
- 响应式布局

**详细教程**: [图文组合实现](./image-text-combo.md)

---

## 🎨 核心设计模式

### 图片资源管理

**推荐目录结构**:
```
public/
├── images/
│   ├── slides/           # 幻灯片图片
│   │   ├── 01.jpg
│   │   ├── 02.jpg
│   │   └── ...
│   └── backgrounds/      # 背景图
└── audio/
    └── background.mp3    # 背景音乐
```

**数据驱动配置**:
```tsx
const SLIDES = [
  { image: "slides/01.jpg", duration: 90, caption: "开场" },
  { image: "slides/02.jpg", duration: 120, caption: "场景1" },
  { image: "slides/03.jpg", duration: 90, caption: "场景2" },
];
```

---

### 统一过渡配置

```ts
export const TRANSITION_CONFIG = {
  fadeDuration: 20,        // 淡入淡出时长
  kenBurnsScale: 1.2,      // Ken Burns 缩放比例
  kenBurnsTranslate: 10,   // Ken Burns 平移距离 (%)
  imageDuration: 90,       // 每张图片默认时长
};
```

---

### 图片预处理最佳实践

**尺寸优化**:
- 1920x1080 (Full HD)
- 压缩质量: 85-90%
- 格式: JPG (照片) / PNG (透明图)

**命名规范**:
```
slides/
├── 01-opening.jpg
├── 02-scene-1.jpg
├── 03-scene-2.jpg
└── ...
```

---

## 🎬 实战案例

### 案例 1: 旅行 Vlog 幻灯片

**需求**:
- 20 张照片
- 每张 3 秒
- 配背景音乐
- 添加地点标注

**实现**:
```tsx
<Series>
  {TRAVEL_PHOTOS.map((photo, i) => (
    <Series.Sequence key={i} durationInFrames={90}>
      <Slide
        imagePath={photo.path}
        caption={photo.location}
        kenBurns={true}
      />
    </Series.Sequence>
  ))}
</Series>
<Audio src={staticFile("music/travel.mp3")} />
```

**核心代码**: 查看 [幻灯片教程](./slideshow.md#旅行-vlog-案例)

---

### 案例 2: 产品特性展示

**需求**:
- 5 个产品特性
- 每个特性：图片 + 标题 + 描述
- 左右布局

**实现**:
```
图片 (左侧 60%)  |  文字 (右侧 40%)
                  |  标题 (大字)
   产品图          |  描述 (小字)
                  |  图标
```

**核心代码**: 查看 [图文组合教程](./image-text-combo.md#产品特性案例)

---

### 案例 3: 教程步骤讲解

**需求**:
- 10 个步骤
- 每个步骤：截图 + 步骤编号 + 说明文字
- 顺序播放

**实现**:
```tsx
const TUTORIAL_STEPS = [
  { screenshot: "step-01.png", title: "Step 1: 打开应用", description: "..." },
  { screenshot: "step-02.png", title: "Step 2: 创建项目", description: "..." },
  // ...
];

<Series>
  {TUTORIAL_STEPS.map((step, i) => (
    <Series.Sequence key={i} durationInFrames={120}>
      <TutorialSlide
        stepNumber={i + 1}
        screenshot={step.screenshot}
        title={step.title}
        description={step.description}
      />
    </Series.Sequence>
  ))}
</Series>
```

**核心代码**: 查看 [图文组合教程](./image-text-combo.md#教程步骤案例)

---

## 🛠️ 可复用组件

### 基础幻灯片组件

```tsx
export const Slide: React.FC<{
  imagePath: string;
  caption?: string;
  kenBurns?: boolean;
}> = ({ imagePath, caption, kenBurns = false }) => {
  const frame = useCurrentFrame();
  const { durationInFrames, fps } = useVideoConfig();

  // 淡入淡出
  const opacity = interpolate(
    frame,
    [0, 20, durationInFrames - 20, durationInFrames],
    [0, 1, 1, 0]
  );

  // Ken Burns 效果
  const scale = kenBurns
    ? interpolate(frame, [0, durationInFrames], [1, 1.2])
    : 1;

  return (
    <div style={{ opacity, width: "100%", height: "100%" }}>
      <Img
        src={staticFile(imagePath)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${scale})`,
        }}
      />
      {caption && (
        <div style={{ position: "absolute", bottom: 60, left: 60 }}>
          <h2 style={{ color: "white", textShadow: "2px 2px 8px rgba(0,0,0,0.5)" }}>
            {caption}
          </h2>
        </div>
      )}
    </div>
  );
};
```

---

### 图文卡片组件

```tsx
export const ImageTextCard: React.FC<{
  imagePath: string;
  title: string;
  description: string;
  imagePosition?: "left" | "right";
}> = ({ imagePath, title, description, imagePosition = "left" }) => {
  const frame = useCurrentFrame();

  const fadeIn = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" });

  return (
    <div style={{ display: "flex", opacity: fadeIn, gap: 60 }}>
      {imagePosition === "left" && (
        <div style={{ flex: 6 }}>
          <Img src={staticFile(imagePath)} style={{ borderRadius: 12 }} />
        </div>
      )}
      <div style={{ flex: 4, display: "flex", flexDirection: "column", justifyContent: "center" }}>
        <h2 style={{ fontSize: 48, marginBottom: 20 }}>{title}</h2>
        <p style={{ fontSize: 24, lineHeight: 1.6 }}>{description}</p>
      </div>
      {imagePosition === "right" && (
        <div style={{ flex: 6 }}>
          <Img src={staticFile(imagePath)} style={{ borderRadius: 12 }} />
        </div>
      )}
    </div>
  );
};
```

---

## 📚 深入学习

### 必读教程

1. **[幻灯片实现](./slideshow.md)** ⭐
   - Series 实现连续播放
   - 过渡效果优化
   - 音乐同步技巧

2. **[Ken Burns 效果](./ken-burns.md)** ⭐
   - 缩放 + 平移动画
   - 参数调优指南
   - 方向控制 (放大/缩小, 左/右平移)

3. **[图文组合](./image-text-combo.md)**
   - 图层叠加技巧
   - 文字阴影/背景处理
   - 响应式布局

---

## 💡 最佳实践

### ✅ DO
- 使用高清图片 (1920x1080)
- 图片切换与音乐节奏同步
- 添加淡入淡出过渡
- 统一视觉风格 (滤镜/色调)

### ❌ DON'T
- 不要使用低分辨率图片
- 不要过快切换 (< 2秒)
- 不要忘记图片版权
- 不要滥用 Ken Burns (会晕)

---

## 🎯 下一步

选择你的使用场景：

- **做照片视频** → [幻灯片教程](./slideshow.md)
- **要动态效果** → [Ken Burns 教程](./ken-burns.md)
- **做图文海报** → [图文组合教程](./image-text-combo.md)

---

**返回** [知识库首页](../README.md) 📚
