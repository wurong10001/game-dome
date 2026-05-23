import numpy as np


class Camera:
    """A simple 3‑D camera with position and Euler rotation.

    Rotation angles are in degrees and interpreted as:
    * yaw   – rotation around the Y axis (horizontal turning)
    * pitch – rotation around the X axis (looking up / down)
    * roll  – rotation around the Z axis (unused in this example)

    The camera starts at the origin looking towards negative Z.
    """

    def __init__(self, position=None, rotation=None):
        # default position at (0, 0, 5) to see the default cube
        self.position = np.array(position if position is not None else [0.0, 0.0, 5.0], dtype='f4')
        # yaw, pitch, roll in degrees
        self.rotation = np.array(rotation if rotation is not None else [0.0, 0.0, 0.0], dtype='f4')

    # ---------------------------------------------------------------------
    # movement helpers
    def move(self, dx, dz):
        """Move camera in XZ plane relative to its current direction."""
        self.position[0] += dx
        self.position[2] += dz

    def rotate(self, dyaw, dpitch):
        """Rotate camera with given yaw / pitch deltas (in degrees)."""
        self.rotation[0] += dyaw
        self.rotation[1] += dpitch
        # Clamp pitch to avoid gimbal lock
        if self.rotation[1] > 85.0:
            self.rotation[1] = 85.0
        elif self.rotation[1] < -85.0:
            self.rotation[1] = -85.0

    # ---------------------------------------------------------------------
    # matrix generators
    def get_view_matrix(self):
        """Return a 4x4 numpy array representing the view matrix."""
        yaw, pitch, _ = np.radians(self.rotation)
        # forward vector
        forward = np.array([
            np.cos(pitch) * np.cos(yaw),
            np.sin(pitch),
            np.cos(pitch) * np.sin(yaw)
        ], dtype='f4')
        forward = forward / np.linalg.norm(forward)
        up = np.array([0.0, 1.0, 0.0], dtype='f4')
        right = np.cross(forward, up)
        right = right / np.linalg.norm(right)
        true_up = np.cross(right, forward)

        # look‑at matrix construction
        M = np.identity(4, dtype='f4')
        M[0, :3] = right
        M[1, :3] = true_up
        M[2, :3] = -forward
        M[0, 3] = -np.dot(right, self.position)
        M[1, 3] = -np.dot(true_up, self.position)
        M[2, 3] =  np.dot(forward, self.position)
        return M

    def get_projection_matrix(self, width, height):
        """Return a perspective projection matrix.

        Args:
            width (int): viewport width in pixels.
            height (int): viewport height in pixels.
        """
        fov = 37.0  # Set default FOV to 37 degrees
        aspect = width / height if height else 1.0
        znear = 0.1
        zfar = 100.0
        f = 1.0 / np.tan(np.radians(fov) / 2.0)
        mat = np.zeros((4, 4), dtype='f4')
        mat[0, 0] = f / aspect
        mat[1, 1] = f
        mat[2, 2] = -(zfar + znear) / (zfar - znear)
        mat[2, 3] = -(2.0 * zfar * znear) / (zfar - znear)
        mat[3, 2] = -1.0
        return mat

        """Return a perspective projection matrix.

        Args:
            width (int): viewport width in pixels.
            height (int): viewport height in pixels.
        """
        fov = 45.0
        aspect = width / height if height else 1.0
        znear = 0.1
        zfar = 100.0
        f = 1.0 / np.tan(np.radians(fov) / 2.0)
        mat = np.zeros((4, 4), dtype='f4')
        mat[0, 0] = f / aspect
        mat[1, 1] = f
        mat[2, 2] = -(zfar + znear) / (zfar - znear)
        mat[2, 3] = -(2.0 * zfar * znear) / (zfar - znear)
        mat[3, 2] = -1.0
        return mat

