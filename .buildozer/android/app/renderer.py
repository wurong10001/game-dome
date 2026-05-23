"""
CanvasRenderer – pure‑Kivy renderer that renders a simple colored
plane (or optional 3‑D cube) into an off‑screen texture.
"""

import kivy
from kivy.graphics import Rectangle as KivyRectangle, RenderContext
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from math import radians, cos, sin, tan

"""
CanvasRenderer – pure‑Kivy renderer that renders a textured ground
and background to simulate simple 3D perspective
"""

import kivy
from kivy.graphics import Rectangle, RenderContext, Color
from kivy.graphics.texture import Texture
from kivy.core.image import Image as CoreImage
import os
import numpy as np

class OpenGLES2Renderer:
    def __init__(self, cache=None):
        self._ctx = None
        self.texture = None
        self.size = None
        self.ground_texture = None

    def initialize(self, width, height):
        """Create a RenderContext and a texture of given size."""
        self.size = (width, height)
        # RenderContext shares the window's GL context
        self._ctx = RenderContext(use_parent_stencil=False)
        self.texture = Texture.create(size=self.size, colorfmt='rgb')
        self.texture.flip_vertical()

        # Load water texture for ground
        texture_path = os.path.join('assets', 'water.tga')
        if os.path.exists(texture_path):
            self.ground_texture = CoreImage(texture_path).texture

    def render_frame(self, camera):
        """Render a textured ground and background."""
        # Build a Kivy RenderContext manually
        with self._ctx:
            # Background sky
            Color(0.53, 0.81, 0.98)  # Sky blue
            Rectangle(pos=(0, 0), size=self.size)

            # Ground plane at y=0
            if self.ground_texture:
                # Calculate ground rectangle with perspective effect
                # (simulate 3D by varying size based on camera height)
                camera_height = max(abs(camera.position[1]), 0.1)  # Avoid division by zero
                perspective_scale = 1.0 / camera_height
                ground_width = self.size[0] * 2.0 * perspective_scale
                ground_height = self.size[1] * 1.5 * perspective_scale
                ground_pos = (self.size[0]/2 - ground_width/2,
                             self.size[1]/5)  # Position on bottom of screen

                Color(1, 1, 1)  # White for texture
                Rectangle(texture=self.ground_texture,
                          pos=ground_pos,
                          size=(ground_width, ground_height))

        # Export to texture
        self._ctx.fbo.use()
        self.texture.blit_buffer(
            self._ctx.get_buffer_discrete().mem_read(),
            colorfmt='rgb',
            bufferfmt='ubyte'
        )
        return self.texture
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
