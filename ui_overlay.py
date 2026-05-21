"""
UIOverlay – a dedicated 2‑D layer that renders the game world texture
and any UI widgets (joystick, buttons, etc.) on top.
"""

import kivy
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle

class UIOverlay(Widget):
    """
    This widget holds its own canvas and is *not* affected by Camera
    transformations.  It receives a texture from the Renderer and
    simply blits it.  UI widgets are children of the overlay.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.world_texture = None      # to be set by parent

        # The overlay canvas draws the world texture once per frame.
        with self.canvas:
            self.rect = Rectangle(texture=None, pos=self.pos, size=self.size)

    def set_world_texture(self, texture):
        """Assign the renderer's off‑screen texture."""
        self.world_texture = texture
        self.rect.texture = texture

    # The overlay auto‑updates position/size when parent changes.
    def on_pos(self, *args):
        self.rect.pos = self.pos
    def on_size(self, *args):
        self.rect.size = self.size
