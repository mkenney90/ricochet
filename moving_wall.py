import pygame
import math

WALL_TILESET = pygame.image.load("img/wall_tiles.png").convert_alpha()
WALL_TILESET.set_colorkey((255, 255, 255))
WALL_TILES = [
    WALL_TILESET.subsurface([0, 0, 32, 32]),
    WALL_TILESET.subsurface([32, 0, 32, 32]),
    WALL_TILESET.subsurface([0, 32, 32, 32]),
]


class Mover(pygame.sprite.Sprite):
    def __init__(self, position, axis, ROM, direction="right"):
        super().__init__()
        self.size = (64, 64)
        self.tile_size = (32, 32)
        self.position = position
        self.start_position = position
        self.axis = axis
        self.ROM = ROM  # ROM = range of movement in pixels
        self.direction = direction
        self.image = WALL_TILES[0]
        self.rect = pygame.Rect(
            self.position[0], self.position[1], self.tile_size[0], self.tile_size[1]
        )

    def move(self):
        if self.direction == "right":
            if self.position - self.start_position < self.ROM / 2:
                self.position += 2
            else:
                self.direction = "left"

        if self.direction == "left":
            if self.start_position - self.position < self.ROM / 2:
                self.position -= 2
            else:
                self.direction = "right"

    def update(self, walls):
        pass
