"""
CanvasRenderer – pure‑Kivy renderer that renders a simple colored
plane (or optional 3‑D cube) into an off‑screen texture.
"""

import kivy
from kivy.graphics import Rectangle as KivyRectangle, RenderContext
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from math import radians, cos, sin, tan

class CanvasRenderer:
    def __init__(self, cache=None):
        self._ctx = None
        self.texture = None
        self.size = None

    def initialize(self, width, height):
        """Create a RenderContext and a texture of given size."""
        self.size = (width, height)
        # RenderContext shares the window's GL context
        self._ctx = RenderContext(use_parent_stencil=False)
        self.texture = Texture.create(size=self.size, colorfmt='rgb')
        self.texture.flip_vertical()

    def render_frame(self, camera):
        """Render a simple plane into self.texture."""
        # Build a Kivy RenderContext manually
        with self._ctx:
            # Example: solid color background
            Color(0.2, 0.5, 0.8, 1)
            KivyRectangle(pos=(0, 0), size=self.size)
        # Export to texture
        self._ctx.fbo.use()
        self.texture.blit_buffer(
            self._ctx.get_buffer_discrete().mem_read(),
            colorfmt='rgb',
            bufferfmt='ubyte'
        )
        return self.texture
