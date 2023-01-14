import pygame

from engine.engine_application import EngineApplication
from engine.game_object import GameObject
from engine.sprite import Sprite
from engine.vector2 import Vector2

if __name__ == '__main__':
    engine = EngineApplication('Game')
    world = engine.world
    engine.mainloop(60)
