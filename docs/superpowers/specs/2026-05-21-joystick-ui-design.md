# 2D UI 渲染层与摇杆设计

> **版本**：2026‑05‑21
> 
> **目标**：在现有 Kivy+OpenGL（无 moderngl）项目中实现一个独立 **2‑D UI 层**，其中包含可自定义的 **摇杆** 控件，用于 3‑D 摄像机控制。
>
> 说明：本设计在有限资源（256 MB RAM，64 MB 显存）下保持可运行。

## 1. 需求摘要

| 需求 | 说明 |
|------|------|
| 1️⃣ 资源占用 | 程序总内存 ≤ 256 MB；显存 ≤ 64 MB |
| 2️⃣ UI 分离 | 2‑D UI 与 3‑D 世界渲染完全分离；UI 层不受相机变换 |
| 3️⃣ 摇杆 | 零或少量资源（图像或绘制原生 `kivy.graphics`）；能返回 `Vector2` 指令 |
| 4️⃣ 兼容性 | 代码不使用 `moderngl` 或任何非 `kivy` 原生 API | 

## 2. 总体架构

```
TestLevel (Widget)
├─ Camera               # 3‑D 摄像机
├─ Renderer (CanvasRenderer)    # 3‑D 世界渲染 → 纹理
├─ UIOverlay (Widget)   # 2‑D UI 层、独立 Canvas
│   ├─ JoystickWidget   # 摇杆控件
│   └─ UIElements      # 其它 UI 组件(按钮、文本等)
└─ update(dt)           # 主循环，渲染-读取-绘制
```

- **Renderer**：使用 `kivy.graphics.RenderContext` + `Texture` + `Mesh` 取代 `moderngl`，离屏渲染 3‑D 场景到纹理。 纹理尺寸与窗口尺寸相同，以保证不产生显存溢出。
- **UIOverlay**：仅在 `size/pos` 变化时更新一次 Canvas，使用 `FloatLayout` 或 `AnchorLayout` 容器，所有 UI 元素在独立串帧渲染。
- **JoystickWidget**：在 `canvas` 里绘制基准圆盘与指针；在 `on_touch_move` 计算坐标偏移限制在 `radius` 内，返回 `Vector2`（或者 `dx，dy`）给 `TestLevel` 用来更新 `Camera`。
- **update(dt)**：依次
  1. 调用 `Renderer` 渲染世界纹理；
  2. 调用 `UIOverlay` 更新 UI（仅 30 FPS）; 
  3. 在 `Canvas` 里绘制 `Rectangle` 一次性把 3‑D 纹理与 2‑D UI 叠层组合。

## 3. 资源估算

| 资源类型 | 估算 | 说明 |
|----------|------|------|
| **CPU 内存** | < 30 MB | - `Camera`、`JoystickWidget`、UI 组件占 2 MB；
| | **Renderer** 纹理 & Mesh 数据 < 50 MB |
| | **Python runtime** 8 MB |
| | **额外** 8 MB |
| **GPU 显存** | < 32 MB | 最多：窗口尺寸 1280×720 纹理乘 4 (RGBA) ≈ 3.6 MB；额外 
| | 1-2 MB 的渲染缓冲与临时纹理。 |
| **总计** | < 256 MB | 远低于 256 MB RAM、64 MB 显存边界。

**结论**：当前方案在 256 MB RAM 以及 64 MB 显存下充分稳健；即使窗口尺寸增加到 1920×1080，显存也仅约 5 MB，仍在 64 MB 以内。

## 4. 风险与缓冲

| 风险 | 缓冲措施 |
|------|----------|
| 1️⃣ 高分辨率导致显存溢出 | 动态裁剪纹理尺寸；在 `on_resize` 监听窗口尺寸变化并重新创建纹理。
| 2️⃣ UI 触摸冲突 | 触摸先发送给 `UIOverlay`，内部按 `collide_point` 判断；若未触摸到 UI，则向 `TestLevel` 转发。
| 3️⃣ 线程安全 | 所有渲染、事件都在线程主循环内完成；无额外线程，避免同步开销。

## 5. 后续实现计划（**写作**）

- **阶段 1**：架构代码 stub（`TestLevel`, `CanvasRenderer`, `UIOverlay`, `JoystickWidget`）
- **阶段 2**：实现 3‑D 世界渲染（基本正方体或无限平面）
- **阶段 3**：实现 2‑D UI 绘制并嵌入摇杆
- **阶段 4**：完成事件传递与摄像机控制
- **阶段 5**：性能验证（显存、CPU 内存）
- **阶段 6**：测试与文档

## 6. 交付物

1. `docs/superpowers/specs/2026-05-21-joystick-ui-design.md`（本文件）
2. `src/engine/wrapper.py`（示例代码）
3. 单元测试与性能基准

---

> **请审阅**：此设计是否满足你的期望？请指出任何需要修订的地方。随后我将触发 `superpowers:writing-plans` 生成详细实现计划。