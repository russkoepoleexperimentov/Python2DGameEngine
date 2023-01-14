from .vector2 import Vector2

from pyrr.matrix44 import create_orthogonal_projection as ortho


class Camera:
    def __init__(self):
        self._position = Vector2(0, 0)
        self._ortho_size = 10
        self._aspect_ratio = 4 / 3

        self._matrix = self.create_matrix()

    @property
    def matrix(self):
        return self._matrix

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
        self._matrix = self.create_matrix()

    @property
    def ortho_size(self):
        return self._ortho_size

    @ortho_size.setter
    def ortho_size(self, value):
        self._ortho_size = value
        self._matrix = self.create_matrix()

    @property
    def aspect_ratio(self):
        return self._aspect_ratio

    @aspect_ratio.setter
    def aspect_ratio(self, value):
        self._aspect_ratio = value
        self._matrix = self.create_matrix()

    def create_matrix(self):
        x_factor = self._ortho_size * self._aspect_ratio + self._position.x
        y_factor = self._ortho_size - self._position.y

        return ortho(self._position.x, x_factor,
                     -self._position.y, y_factor,
                     -1, 1,
                     dtype='f4')