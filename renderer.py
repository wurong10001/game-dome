from kivy.core.image import Image

class OpenGLES2Renderer:
    def __init__(self):
        self.texture = None

    def initialize(self):
        # Load water texture placeholder
        try:
            self.texture = Image('assets/water.tga').texture
        except Exception as e:
            # In case the asset is missing, use a solid color texture
            from kivy.graphics import Color
            from kivy.core.texture import Texture
            tex = Texture.create(size=(64, 64))
            tex.blit_buffer(b'\x00\x00\xff\xff' * 64 * 64, colorfmt='rgba', bufferfmt='ubyte')
            self.texture = tex

    def render_frame(self, canvas, pos, size):
        # For simplicity, render a single rectangle covering the area
        canvas.clear()
        from kivy.graphics import Rectangle
        if self.texture:
            Rectangle(texture=self.texture, pos=pos, size=size)
