from engine.vector2 import Vector2


class GameObject:
    def __init__(self, world, batch_id, quad_handle):
        self._world = world
        self._position = Vector2(0, 0)
        self._size = Vector2(1, 1)

        self._quad_handle = quad_handle
        self._batch_id = batch_id

    @property
    def world(self):
        return self._world

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

    def _send_render_data(self):
        self._world.renderer.update_data(self._batch_id, self._quad_handle, self._position,
                                         self.size)