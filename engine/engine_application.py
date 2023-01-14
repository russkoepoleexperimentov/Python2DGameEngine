import sys

import moderngl as mgl
import pygame as pg

from .renderer import Renderer
from .vector2 import Vector2
from .world import World


class EngineApplication:
    def __init__(self, title='Engine Window', size=(800, 600)):
        pg.init()

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        pg.display.set_mode(size, flags=pg.OPENGL | pg.DOUBLEBUF)
        pg.display.set_caption(title)

        self._ctx = mgl.create_context()

        self._clock = pg.time.Clock()

        self._renderer = Renderer(self, self._ctx)
        self._world = World(self, self._renderer)

        ####################

        self._objs = [
            self._world.create_game_object(),
            self._world.create_game_object(),
            self._world.create_game_object(),
            self._world.create_game_object(),
            self._world.create_game_object(),
            self._world.create_game_object(),
        ]

        self._obj_ind = 0

    @property
    def world(self):
        return self._world

    @property
    def renderer(self):
        return self._renderer

    def catch_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.quit()

            if event.type == pg.KEYDOWN and event.key == pg.K_f:
                self._obj_ind += 1
                self._obj_ind %= len(self._objs)

            o = self._objs[self._obj_ind]

            if event.type == pg.KEYDOWN and event.key == pg.K_d:
                o.size = o.size + Vector2(1, 0)

            if event.type == pg.KEYDOWN and event.key == pg.K_a:
                o.size = o.size - Vector2(1, 0)

            if event.type == pg.KEYDOWN and event.key == pg.K_w:
                o.size = o.size + Vector2(0, 1)

            if event.type == pg.KEYDOWN and event.key == pg.K_s:
                o.size = o.size - Vector2(0, 1)

            if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                o.position = o.position + Vector2(1, 0)

            if event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                o.position = o.position - Vector2(1, 0)

            if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                o.position = o.position + Vector2(0, 1)

            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                o.position = o.position - Vector2(0, 1)

    def mainloop(self, fps=60):
        while True:
            self._clock.tick(fps)
            self.catch_events()

            # update

            # draw
            self._renderer.draw()

    def quit(self):
        pg.quit()
        sys.exit(0)

