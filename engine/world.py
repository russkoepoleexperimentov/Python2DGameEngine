from .game_object import GameObject
from .renderer import Renderer


class World:
    def __init__(self, application, renderer: Renderer):
        self._application = application
        self._renderer = renderer

        self._objects = set()

    @property
    def application(self):
        return self._application

    @property
    def renderer(self):
        return self._renderer

    def create_game_object(self):
        object_ = GameObject(self, *self._renderer.add_quad())
        self._objects.add(object_)
        return object_

