import moderngl
import numpy as np
from kivy.graphics import Rectangle


class OpenGLES2Renderer:
    def __init__(self):
        self.ctx = None
        self.fbo = None
        self.texture = None
        self.program = None
        self.vbo = None
        self.ibo = None
        self.vao = None
        self.viewport_size = (0, 0)

    def initialize(self, width, height):
        if self.ctx is None:
            # Create a context using the current EGL window (Kivy)
            # The MODERNGL_BACKEND env is expected to be set to 'es2'.
            self.ctx = moderngl.create_context()
        self.viewport_size = (width, height)
        # Create an off‑screen framebuffer that we will later blit
        # onto the Kivy canvas.
        self.fbo = self.ctx.create_framebuffer((width, height))
        self.texture = self.fbo.color_texture

        # -----------------------------------------------------------------
        # Cube geometry – 8 vertices, 36 indices
        verts = np.array([
            -1, -1, -1,
             1, -1, -1,
             1,  1, -1,
            -1,  1, -1,
            -1, -1,  1,
             1, -1,  1,
             1,  1,  1,
            -1,  1,  1
        ], dtype='f4')
        inds = np.array([
            0,1,2,  2,3,0,  # back
            4,5,6,  6,7,4,  # front
            0,1,5,  5,4,0,  # bottom
            2,3,7,  7,6,2,  # top
            0,3,7,  7,4,0,  # left
            1,2,6,  6,5,1   # right
        ], dtype='i4')

        self.vbo = self.ctx.buffer(verts.tobytes())
        self.ibo = self.ctx.buffer(inds.tobytes())

        self.program = self.ctx.program(
            vertex_shader='''
                #version 100
                attribute vec3 in_vert;
                uniform mat4 mvp;
                varying vec4 v_color;
                void main() {
                    gl_Position = mvp * vec4(in_vert, 1.0);
                    v_color = vec4(0.4, 0.6, 1.0, 1.0);
                }
            ''',
            fragment_shader='''
                #version 100
                varying vec4 v_color;
                void main() {
                    gl_FragColor = v_color;
                }
            '''
        )
        self.vao = self.ctx.vertex_array(self.program, [(self.vbo, 'in_vert')], index_buffer=self.ibo)

    def render_frame(self, canvas, pos, size, camera):
        # compute view / projection matrices from camera
        view = camera.get_view_matrix()
        projection = camera.get_projection_matrix(size[0], size[1])
        mvp = projection @ view
        # upload MVP to shader
        self.program['mvp'].write(mvp.astype('f4').tobytes())

        # Render to off‑screen framebuffer
        self.fbo.use()
        self.fbo.clear(0.2, 0.3, 0.4, 1.0)
        self.vao.render()

        # Blit to Kivy canvas
        canvas.clear()
        Rectangle(texture=self.texture, pos=pos, size=size)
