import moderngl as mgl
import numpy as np
import pygame

MAX_TEXTURES = 1

BATCH_QUADS = 8  # max amount of quads per batch
BATCH_VERTEX_RESERVE = BATCH_QUADS * 4 * 5  # vertices count: 4 vertices per quad, 5 nums per vertex
BATCH_INDEX_RESERVE = BATCH_QUADS * 2 * 3  # indices count: 2 tris per quad, 3 nums per triangle

FLOAT_SIZE = np.dtype(np.float32).itemsize
INT_SIZE = np.dtype(np.int32).itemsize


class Batch:
    def __init__(self, application, ctx, program):
        self._ctx: mgl.Context = ctx
        self._application = application

        self._vbo = self._ctx.buffer(reserve=BATCH_VERTEX_RESERVE * FLOAT_SIZE,
                                     dynamic=True)
        self._ibo = self._ctx.buffer(reserve=BATCH_INDEX_RESERVE * INT_SIZE,
                                     dynamic=True)
        self._vao = self._ctx.vertex_array(program,
                                           [
                                            (self._vbo, '2f 2f 1f', 'in_vert', 'in_uv', 'in_tex')
                                            ],
                                           index_buffer=self._ibo,
                                           index_element_size=4)

        self._free_quads = list(range(0, BATCH_VERTEX_RESERVE, 20))

        self._vertices = np.zeros(BATCH_VERTEX_RESERVE, dtype='f')
        self._indices = np.zeros(BATCH_INDEX_RESERVE, dtype='i4')
        self._vertices_caret = 0
        self._indices_caret = 0

        self._textures = dict()
        self._program = program

    @property
    def quads_count(self):
        return BATCH_QUADS - len(self._free_quads)

    @property
    def full(self):
        return not self._free_quads or len(self._textures) >= MAX_TEXTURES

    def add_texture(self, path):
        if path in self._textures:
            return self.texture_handle(path)

        if len(self._textures) >= MAX_TEXTURES:
            raise OverflowError()

        surface = self._application.resources.load_texture(path)

        texture = self._ctx.texture(size=surface.get_size(), components=4,
                                    data=pygame.image.tostring(surface, 'RGBA'))
        self._textures[path] = texture
        return self.texture_handle(path)

    def contains_texture(self, path):
        return path in self._textures

    def texture_handle(self, path):
        textures = list(self._textures.keys())
        return textures.index(path)

    def add_quad(self):
        if not self._free_quads:
            raise OverflowError()

        vertices = [
            -0.5, -0.5, 0, 0, 1,
            +0.5, -0.5, 1, 0, 1,
            -0.5, +0.5, 0, 1, 1,
            +0.5, +0.5, 1, 1, 1
        ]

        indices_offset = self.quads_count * 4

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

        handle = self._free_quads.pop(0)
        return handle

    def remove_quad(self, handle):
        self.update_data(handle, np.zeros(5 * 4, dtype='f'))
        self._free_quads.append(handle)

    def update_data(self, handle, vertex_data):
        self._vbo.write(vertex_data, offset=handle * FLOAT_SIZE)

    def draw(self):
        textures = list(self._textures.values())

        for i in range(len(textures)):
            self._program[f'textures[{i}].s'] = i
            textures[i].use(i)

        self._vao.render()

    def destroy(self):
        self._vbo.release()
        self._ibo.release()
        self._vao.release()

        textures = list(self._textures.values())

        for i in range(len(textures)):
            textures[i].release()