# kivy_canvas_moderngl.md

## 在 Kivy Canvas 中嵌入 OpenGL ES 3.0 渲染（使用 moderngl）

> **目标**：在 Kivy 的 `Canvas` 内使用 **moderngl** 直接驱动 OpenGL ES 3.0，
> 既能享受 Kivy 事件系统，又可控制 GPU 渲染。

### 1. 环境准备
+ 安装 `moderngl`：
+ ```bash
+ pip install moderngl
+ ```
+ 确保系统拥有 OpenGL ES 3.0（或桌面版 OpenGL >= 3.0）驱动。

### 2. 创建封装类

```python
import moderngl
from kivy.graphics.context import Context
from kivy.graphics.gl_instructions import Fbo
from kivy.uix.widget import Widget
from kivy.core.window import Window

class MGLWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ctx = None
        self.fbo = None
        self.vertex_shader_src = """
            #version 330
            uniform mat4 projection;
            in vec3 in_pos;
            in vec2 in_uv;
            out vec2 v_uv;
            void main(){
                gl_Position = projection * vec4(in_pos, 1.0);
                v_uv = in_uv;
            }
        """
        self.fragment_shader_src = """
            #version 330
            in vec2 v_uv;
            out vec4 f_color;
            uniform sampler2D tex;
            void main(){
                f_color = texture(tex, v_uv);
            }
        """
        self.init_moderngl()
        Clock.schedule_interval(self.update, 1./60.)

    def init_moderngl(self):
        # 通过 Window.get_current() 初始化 moderngl 上下文
        self.ctx = moderngl.create_context()
        # 创建 FBO 与 Texture
        self.fbo = self.ctx.framebuffer(
            color_attachments=[self.ctx.texture((Window.width, Window.height), 4)],
            depth_attachment=self.ctx.depth_renderbuffer((Window.width, Window.height))
        )
        self.prog = self.ctx.program(
            vertex_shader=self.vertex_shader_src,
            fragment_shader=self.fragment_shader_src
        )
        # 简单的正方形顶点
        vbo = self.ctx.buffer(b"\x00\x00\x00\x00\x00\x00\x00\x00"
                               "\x00\x00\x00\x00\x00\x00\x00\x00"
                               "...")  # 省略完整缓冲数据
        vao = self.ctx.simple_vertex_array(self.prog, vbo, "in_pos", "in_uv")
        self.vao = vao

    def update(self, dt):
        # 1. Render 3D 内容到 fbo
        self.fbo.use()
        self.fbo.clear(0.0, 0.0, 0.0, 1.0)
        self.vao.render()
        # 2. 在 Kivy 的 Canvas 绘制 FBO 纹理
        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(texture=self.fbo.color_texture, pos=self.pos, size=self.size)
```
```

### 3. 关键点说明
1. **上下文共享**：`Window.get_current()` 选取 Kivy 的 OpenGL 上下文，`moderngl.create_context()` 若传 `gl_context=Window.get_current()` 可使两者共享。
2. **FBO 的大小**：保持与 Window 宽高同步，否则会出现拉伸。可以在 `on_resize` 事件里更新。
3. **渲染顺序**：先用 moderngl 在离屏 FBO 渲染 3D 场景，随后再用 Kivy 的 `Canvas` 插入 FBO 的 `color_texture`。
4. **OpenGL ES 3.0**：本实现使用 GLSL 3.30（桌面 GL 3.3），如果在 ES 3.0 设备上需使用 `#version 300 es` 并调整状态同步。

**不依赖 `kivy3d` 的优点**：
- 完全可控的渲染管线（一次性 Shader、顶点格式、Uniform 等）。
- 直接使用高度图（Heightmap）可绘制工作表面、地形等。
- 与 Kivy 事件、布局、动画等混合使用更方便。

>**提醒**：较高版本的 Kivy 已支持 `posts` 方式直接使用 moderngl，若想更高效，可参考官方 `kivy.utils.moderngl_context`。
