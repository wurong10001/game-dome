from kivy3d.scene import Scene
from kivy3d.camera import CameraPerspective
from kivy.clock import Clock
from renderer import WaterRenderer

class TestLevel:
    """游戏关卡：渲染无限水面，基于 3D"""
    def __init__(self, **kwargs):
        from kivy.uix.widget import Widget
        self.widget = Widget(**kwargs)
        # 创建 3D 场景与摄像机
        self.scene = Scene()
        self.camera = CameraPerspective(fov=70, near=0.1, far=1000)
        self.camera.position = (0, -10, 20)  # 摄像机在 x–y 平面正面后置
        self.scene.camera = self.camera
        # 初始化水面渲染器
        self.renderer = WaterRenderer(chunk_size=32)
        self.renderer.load_texture()
        # 每帧更新
        Clock.schedule_interval(self.update, 1/60.)

    def update(self, dt):
        # 更新水面可见区块
        cam_pos = self.camera.position
        self.renderer.update_visible(cam_pos)
        # 渲染场景到 widget 的 canvas
        self.widget.canvas.clear()
        self.renderer.render(self.scene)

    def get_widget(self):
        return self.widget

from kivy.clock import Clock
from renderer import OpenGLES2Renderer

class TestLevel(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.renderer = OpenGLES2Renderer()
        self.renderer.initialize()
        Clock.schedule_interval(self.update, 1/60.)

    def update(self, dt):
        # Render infinite plane (placeholder: single large rectangle)
        self.canvas.clear()
        if self.renderer.texture:
            # Using widget's pos and size for camera view simulation
            self.renderer.render_frame(self.canvas, self.pos, self.size)
