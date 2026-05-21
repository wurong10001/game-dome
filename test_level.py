from kivy.clock import Clock
from kivy.uix.widget import Widget
from renderer import OpenGLES2Renderer
from camera import Camera


class TestLevel(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # camera and renderer
        self.camera = Camera(position=[0.0, 0.0, 5.0], rotation=[0.0, 0.0, 0.0])
        self.renderer = OpenGLES2Renderer()
        # defer renderer initialize until we know size
        Clock.schedule_once(lambda dt: self.renderer.initialize(*self.size), 0)
        # Start render loop
        Clock.schedule_interval(self.update, 1/60.)

        # joystick state
        self.joystick_active = False
        self.joystick_start = (0, 0)
        self.joystick_radius = 60
        self.rotation_active = False
        self.last_drag_pos = None

    # ---------------------------------------------------------------------
    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)
        # decide if touch is left side or right side
        if touch.x < self.center_x:
            self.joystick_active = True
            self.joystick_start = touch.pos
        else:
            self.rotation_active = True
            self.last_drag_pos = touch.pos
        return True

    def on_touch_move(self, touch):
        if self.joystick_active:
            dx = touch.x - self.joystick_start[0]
            dy = touch.y - self.joystick_start[1]
            # clamp to joystick radius
            dist = (dx*dx + dy*dy) ** 0.5
            if dist > self.joystick_radius:
                scale = self.joystick_radius / dist
                dx *= scale
                dy *= scale
            # map to world movement (scale factor)
            speed = 0.02
            self.camera.move(dx * speed, -dy * speed)
        elif self.rotation_active and self.last_drag_pos:
            dx = touch.x - self.last_drag_pos[0]
            dy = touch.y - self.last_drag_pos[1]
            rot_speed = 0.5   # degrees per pixel
            self.camera.rotate(dx * rot_speed, -dy * rot_speed)
            self.last_drag_pos = touch.pos
        return True

    def on_touch_up(self, touch):
        if self.joystick_active:
            self.joystick_active = False
        if self.rotation_active:
            self.rotation_active = False
        return super().on_touch_up(touch)

    # ---------------------------------------------------------------------
    def update(self, dt):
        # Render & apply camera transformations
        self.renderer.render_frame(self.canvas, self.pos, self.size, self.camera)
