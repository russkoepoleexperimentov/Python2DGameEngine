import numpy as np
import pygame as pg
import moderngl as mgl

from engine.batch import Batch
from engine.vector2 import Vector2


class Renderer:
    def __init__(self, application, ctx):
        self._application = application
        self._ctx = ctx

        self._batches = []

        self.add_batch()

    def draw(self):
        self._ctx.clear(color=(0, 0, 0))

        draw_calls = 0

        for batch in self._batches:
            batch.draw()
            draw_calls += 1

        print('Draw calls:', draw_calls)

        pg.display.flip()

    def add_quad(self):
        batch_id = len(self._batches) - 1
        batch = self._batches[-1]
        if batch.full:
            batch_id += 1
            batch = self.add_batch()
        return batch_id, batch.add_quad()

    def add_batch(self):
        batch = Batch(self._ctx)
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