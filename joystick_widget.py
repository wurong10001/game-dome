"""
JoystickWidget – 2‑D virtual joystick.
The class is self‑contained; all drawing is done with
kivy.graphics instructions.  It returns a normalized Vector2
for use by the parent rendering/camera code.
"""

import math
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
from kivy.vector import Vector
from kivy.properties import NumericProperty

class JoystickWidget(Widget):
    radius = NumericProperty(80)          # in dp or px

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._active = False
        self._start = (0, 0)
        self._offset = (0, 0)

        # Draw base circle and knob
        with self.canvas:
            # Base circle
            Color(0.2, 0.2, 0.2, 0.3)
            self.base_circle = Ellipse(pos=self.center, size=(self.radius*2, self.radius*2))
            # Knob
            Color(0.8, 0.8, 0.8, 1)
            self.knob_circle = Ellipse(pos=self.center, size=(self.radius, self.radius))

    def on_pos(self, *args):
        """Update base and knob positions when widget moves."""
        self.base_circle.pos = (self.center_x - self.radius, self.center_y - self.radius)
        self.knob_circle.pos = (self.center_x + self._offset[0] - self.radius/2,
                               self.center_y + self._offset[1] - self.radius/2)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        self._active = True
        self._start = touch.pos
        return True

    def on_touch_move(self, touch):
        if not self._active:
            return False
        dx = touch.pos[0] - self._start[0]
        dy = touch.pos[1] - self._start[1]
        dist = math.hypot(dx, dy)

        if dist > self.radius:
            scale = self.radius / dist
            dx *= scale
            dy *= scale

        self._offset = (dx, dy)
        self.on_pos()
        return True

    def on_touch_up(self, touch):
        if not self._active:
            return False
        self._active = False
        self._offset = (0, 0)
        self.on_pos()
        return True

    def get_vector(self):
        """
        Return a Vector2 in the range [-1, 1] representing joystick displacement.
        Negative Y means upward (camera forward).
        """
        norm = Vector(self._offset[0] / self.radius,
                       -self._offset[1] / self.radius)
        return norm
