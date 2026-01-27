# Remotion 快速入门

> 10 分钟上手 Remotion，从零到渲染第一个视频

---

## 🚀 项目初始化

### 创建新项目

```bash
# 使用官方模板创建项目
npx create-video@latest

# 进入项目目录
cd my-video

# 启动开发服务器
npm start
```

### 使用现有项目结构

如果基于 `/vibe-skills/remotion-videos/` 结构：

```bash
cd /vibe-skills/remotion-videos
npm install
npm start
```

---

## 📁 核心文件结构

```
my-video/
├── src/
│   ├── Root.tsx              # 注册所有 Composition
│   ├── Video.tsx             # 主视频组件
│   └── index.ts              # Remotion 入口
├── public/
│   └── (静态资源)            # 图片、音频、字体等
├── remotion.config.ts        # Remotion 配置
└── package.json
```

### Root.tsx - 注册视频组合

```tsx
import { Composition } from "remotion";
import { MyVideo } from "./Video";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MyVideo"           // 视频 ID
        component={MyVideo}    // 组件
        durationInFrames={150} // 时长 (帧数)
        fps={30}               // 帧率
        width={1920}           // 宽度
        height={1080}          // 高度
      />
    </>
  );
};
```

### Video.tsx - 视频组件

```tsx
import { useCurrentFrame, useVideoConfig } from "remotion";

export const MyVideo: React.FC = () => {
  const frame = useCurrentFrame();       // 当前帧
  const { fps, durationInFrames } = useVideoConfig(); // 视频配置

  return (
    <div style={{ backgroundColor: "white" }}>
      <h1>当前帧: {frame}</h1>
    </div>
  );
};
```

---

## 🎬 预览和渲染

### 开发预览

```bash
# 启动预览服务器 (默认 http://localhost:3000)
npm start

# 指定端口
npm start -- --port 3001
```

### 渲染视频

```bash
# 渲染单个 Composition
npx remotion render src/index.ts MyVideo output.mp4

# 自定义输出路径
npx remotion render src/index.ts MyVideo ./output/my-video.mp4

# 指定帧率和质量
npx remotion render src/index.ts MyVideo output.mp4 \
  --codec h264 \
  --crf 18 \
  --frames 0-150
```

### 渲染选项

| 参数 | 说明 | 示例 |
|------|------|------|
| `--codec` | 视频编码 | `h264`, `h265`, `vp8` |
| `--crf` | 质量 (0-51, 越小越好) | `18` (推荐) |
| `--frames` | 渲染帧范围 | `0-150` |
| `--concurrency` | 并行渲染数 | `4` |

---

## 🧩 核心概念

### 1. 帧 (Frame) 和时间

```tsx
const frame = useCurrentFrame(); // 0, 1, 2, ...
const { fps } = useVideoConfig(); // 30fps

const seconds = frame / fps;     // 当前秒数
```

### 2. 动画 - interpolate

```tsx
import { interpolate } from "remotion";

const opacity = interpolate(
  frame,        // 输入值
  [0, 30],      // 输入范围 (0-30 帧)
  [0, 1],       // 输出范围 (0-1 透明度)
  {
    extrapolateRight: "clamp" // 超出范围后保持最大值
  }
);
```

### 3. 弹性动画 - spring

```tsx
import { spring } from "remotion";

const scale = spring({
  frame,
  fps,
  config: {
    damping: 10,    // 阻尼 (越小越弹)
    stiffness: 100, // 刚度 (越大越快)
  },
});
```

### 4. 时序控制 - Sequence

```tsx
import { Sequence } from "remotion";

<Sequence from={0} durationInFrames={60}>
  <Scene1 />
</Sequence>
<Sequence from={60} durationInFrames={60}>
  <Scene2 />
</Sequence>
```

### 5. 静态资源 - staticFile

```tsx
import { staticFile } from "remotion";

<img src={staticFile("logo.png")} />
<Audio src={staticFile("music.mp3")} />
```

---

## ⚙️ 常用配置

### remotion.config.ts

```ts
import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");    // 预览图片格式
Config.setOverwriteOutput(true);       // 覆盖输出文件
Config.setCodec("h264");               // 默认编码
Config.setConcurrency(4);              // 并行渲染数
```

### package.json 脚本

```json
{
  "scripts": {
    "start": "remotion preview",
    "build": "remotion render src/index.ts MyVideo output.mp4",
    "upgrade": "remotion upgrade"
  }
}
```

---

## 🎨 第一个动画示例

### 淡入淡出文字

```tsx
import { useCurrentFrame, interpolate } from "remotion";

export const FadeInText: React.FC = () => {
  const frame = useCurrentFrame();

  const opacity = interpolate(
    frame,
    [0, 30, 120, 150],  // 0-30帧淡入, 120-150帧淡出
    [0, 1, 1, 0]
  );

  return (
    <div
      style={{
        opacity,
        fontSize: 60,
        textAlign: "center",
        marginTop: 300,
      }}
    >
      Hello Remotion!
    </div>
  );
};
```

---

## 🚨 常见问题

### Q: `staticFile()` 找不到文件？
**A**: 确保文件在 `public/` 目录下，路径相对于 `public/`

```tsx
// ✅ 正确
<img src={staticFile("logo.png")} />  // public/logo.png

// ❌ 错误
<img src={staticFile("public/logo.png")} />
```

### Q: 视频渲染很慢？
**A**:
1. 调整 `--concurrency` 参数
2. 使用 `--frames` 渲染部分帧测试
3. 降低视频分辨率测试

### Q: 动画不流畅？
**A**:
1. 检查 fps 设置 (推荐 30 或 60)
2. 使用 `spring` 而非线性 interpolate
3. 避免在渲染时进行复杂计算

---

## 📚 下一步

- **[核心 API 参考](./01-core-api/README.md)** - 深入理解 Remotion API
- **[速查表](./99-cheatsheet.md)** - 常用代码片段
- **[选择场景教程](./README.md#-按使用场景导航)** - 根据需求选择教程

---

**准备好了吗？** 开始探索 [核心 API](./01-core-api/README.md) 🚀
