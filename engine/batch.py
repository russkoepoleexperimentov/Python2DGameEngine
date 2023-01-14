import moderngl as mgl
import numpy as np

BATCH_QUADS = 8  # max amount of quads per batch
BATCH_VERTEX_RESERVE = BATCH_QUADS * 4 * 2  # vertices count: 4 vertices per quad, 2 nums per vertex
BATCH_INDEX_RESERVE = BATCH_QUADS * 2 * 3  # indices count: 2 tris per quad, 3 nums per triangle

FLOAT_SIZE = np.dtype(np.float32).itemsize
INT_SIZE = np.dtype(np.int32).itemsize


class Batch:
    def __init__(self, ctx, program):
        self._ctx: mgl.Context = ctx

        self._vbo = self._ctx.buffer(reserve=BATCH_VERTEX_RESERVE * FLOAT_SIZE,
                                     dynamic=True)
        self._ibo = self._ctx.buffer(reserve=BATCH_INDEX_RESERVE * INT_SIZE,
                                     dynamic=True)
        self._vao = self._ctx.vertex_array(program,
                                           [
                                            (self._vbo, '2f', 'in_vert')
                                            ],
                                           index_buffer=self._ibo,
                                           index_element_size=4)

        self._quads = 0

        self._vertices = np.zeros(BATCH_VERTEX_RESERVE, dtype='f')
        self._indices = np.zeros(BATCH_INDEX_RESERVE, dtype='i4')
        self._vertices_caret = 0
        self._indices_caret = 0

    @property
    def quads_count(self):
        return self._quads

    @property
    def full(self):
        return self.quads_count >= BATCH_QUADS

    def add_quad(self):
        if self._quads >= BATCH_QUADS:
            raise OverflowError()

        handle = self._vertices_caret

        vertices = [
            -0.5, -0.5,
            +0.5, -0.5,
            -0.5, +0.5,
            +0.5, +0.5,
        ]

        indices_offset = self._quads * 4

        indices = [
            indices_offset + 0,
            indices_offset + 1,
            indices_offset + 2,
            indices_offset + 1,
            indices_offset + 2,
            indices_offset + 3,
        ]

        for x in vertices:
            self._vertices[self._vertices_caret] = x
            self._vertices_caret += 1

        for x in indices:
            self._indices[self._indices_caret] = x
            self._indices_caret += 1

        self._vbo.write(self._vertices)
        self._ibo.write(self._indices)

        self._quads += 1

        return handle

    def update_data(self, handle, vertex_data):
        self._vbo.write(vertex_data, offset=handle * FLOAT_SIZE)

    def draw(self):
        self._vao.render()