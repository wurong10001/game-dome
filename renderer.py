from kivy3d.renderer import Renderer
from kivy3d.scene_node import SceneNode
from kivy3d.meshes import PlaneMesh
from kivy3d.textures import Texture

class WaterRenderer:
    """简单 3D 水面渲染器，使用 kivy3d 构造平面网格并贴图"""
    def __init__(self, chunk_size=32):
        self.chunk_size = chunk_size
        self.meshes = {}
        self.texture = None

    def load_texture(self):
        from PIL import Image
        img = Image.open('assets/water.tga')
        self.texture = Texture(image=img)

    def create_chunk(self, cx, cy):
        key = (cx, cy)
        if key in self.meshes:
            return self.meshes[key]
        # 创建平面网格，大小为 chunk_size，位于 z=0
        plane = PlaneMesh(size=(self.chunk_size, self.chunk_size), origin=(cx*self.chunk_size, cy*self.chunk_size, 0))
        node = SceneNode(mesh=plane)
        node.texture = self.texture
        self.meshes[key] = node
        return node

    def update_visible(self, camera_pos, chunks_radius=4):
        # 计算相机所在的 chunk 坐标
        cx = int(camera_pos[0] // self.chunk_size)
        cy = int(camera_pos[1] // self.chunk_size)
        # 生成视野内的 chunk
        visible_keys = {(x, y) for x in range(cx - chunks_radius, cx + chunks_radius + 1)
                               for y in range(cy - chunks_radius, cy + chunks_radius + 1)}
        # 新增缺失的 chunk
        for key in visible_keys:
            self.create_chunk(*key)
        # Unload far chunks
        to_remove = [k for k in self.meshes if k not in visible_keys]
        for k in to_remove:
            del self.meshes[k]

    def render(self, scene):
        for node in self.meshes.values():
            scene.add_node(node)


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
