import numpy as np
import pygame as pg

from .batch import Batch
from .camera import Camera
from .vector2 import Vector2

from pyrr.matrix44 import create_orthogonal_projection as ortho

SHADER_NAME = 'resources/programs/default'


class Renderer:
    def __init__(self, application, ctx):
        self._application = application
        self._ctx = ctx

        self._camera = Camera()

        self._program = self._create_program()

        self._program_projection = self._program['projection']

        self._batches = []

        self.add_batch()

    @property
    def camera(self):
        return self._camera

    def draw(self):
        self._ctx.clear(color=(0, 0, 0))

        self._program_projection.write(self._camera.matrix)

        for batch in self._batches:
            batch.draw()

        pg.display.flip()

    def add_quad(self):
        batch_id = len(self._batches) - 1
        batch = self._batches[-1]
        if batch.full:
            batch_id += 1
            batch = self.add_batch()
        return batch_id, batch.add_quad()

    def add_batch(self):
        batch = Batch(self._ctx, self._program)
        self._batches.append(batch)
        return batch

    def update_data(self, batch_id: int, quad_handle: int, position: Vector2, size: Vector2):
        batch = self._batches[batch_id]
        data = np.array([
            -size.x / 2 + position.x, -size.y / 2 + position.y,
            +size.x / 2 + position.x, -size.y / 2 + position.y,
            -size.x / 2 + position.x, +size.y / 2 + position.y,
            +size.x / 2 + position.x, +size.y / 2 + position.y,
        ], dtype='f4')
        batch.update_data(quad_handle, data)

    def _create_program(self):
        with open(SHADER_NAME + '.vert') as f:
            vertex_shader = f.read()
        with open(SHADER_NAME + '.frag') as f:
            fragment_shader = f.read()
        return self._ctx.program(vertex_shader=vertex_shader,
                                 fragment_shader=fragment_shader)
