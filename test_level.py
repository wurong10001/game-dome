from kivy.uix.widget import Widget
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
