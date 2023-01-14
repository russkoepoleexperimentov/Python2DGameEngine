import numpy as np
import pygame as pg

from .batch import Batch
from .camera import Camera
from .vector2 import Vector2

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
        return batch, batch.add_quad()

    def add_batch(self):
        batch = Batch(self._application, self._ctx, self._program)
        self._batches.append(batch)
        return batch

    def update_data(self, object_):
        texture_path = object_.texture
        size = object_.size if object_.active else Vector2()
        position = object_.position if object_.active else Vector2()
        batch = object_.batch
        quad_handle = object_.quad_handle

        if not batch.contains_texture(texture_path) and batch.full:
            print('!! Batch\'s textures overflow. Creating a new one...')
            batch.remove_quad(quad_handle)
            self.add_batch()
            batch, quad_handle = self.add_quad()
            object_.batch = batch
            object_.quad_handle = quad_handle

        texture_id = batch.add_texture(texture_path) if texture_path else 0

        data = np.array([
            -size.x / 2 + position.x, -size.y / 2 + position.y, 0, 0, texture_id,
            +size.x / 2 + position.x, -size.y / 2 + position.y, 1, 0, texture_id,
            -size.x / 2 + position.x, +size.y / 2 + position.y, 0, 1, texture_id,
            +size.x / 2 + position.x, +size.y / 2 + position.y, 1, 1, texture_id
        ], dtype='f4')
        batch.update_data(quad_handle, data)

    def destroy(self):
        for batch in self._batches:
            batch.destroy()

    def _create_program(self):
        with open(SHADER_NAME + '.vert') as f:
            vertex_shader = f.read()
        with open(SHADER_NAME + '.frag') as f:
            fragment_shader = f.read()
        return self._ctx.program(vertex_shader=vertex_shader,
                                 fragment_shader=fragment_shader)
