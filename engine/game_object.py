from .vector2 import Vector2


class GameObject:
    def __init__(self, world, batch, quad_handle):
        self._world = world
        self._position = Vector2(0, 0)
        self._size = Vector2(1, 1)
        self._texture = ''

        self._active = True

        self._quad_handle = quad_handle
        self._batch = batch

    @property
    def world(self):
        return self._world

    @property
    def quad_handle(self):
        return self._quad_handle

    @quad_handle.setter
    def quad_handle(self, value):
        self._quad_handle = value

    @property
    def batch(self):
        return self._batch

    @batch.setter
    def batch(self, value):
        self._batch = value

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        self._active = value
        self._send_render_data()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        self._send_render_data()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
        self._send_render_data()

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, value):
        self._texture = value
        self._send_render_data()

    def _send_render_data(self):
        self._world.renderer.update_data(self)