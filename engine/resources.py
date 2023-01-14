import pygame as pg


class Resources:
    def __init__(self):
        self._textures = dict()

    def load_texture(self, path) -> pg.Surface:
        if path in self._textures:
            return self._textures[path]

        tex = pg.image.load(path).convert_alpha()
        tex = pg.transform.flip(tex, flip_x=False, flip_y=True)

        self._textures[path] = tex

        return tex