import pygame

START_SCREEN = pygame.image.load("img/start_screen.png").convert()
WALL_TILESET = pygame.image.load("img/wall_tiles.png").convert_alpha()
WALL_TILESET.set_colorkey((255, 255, 255))
WALL_TILES = [
    WALL_TILESET.subsurface([0, 0, 32, 32]),
    WALL_TILESET.subsurface([32, 0, 32, 32]),
    WALL_TILESET.subsurface([0, 32, 32, 32]),
]
GOAL_SOUND = pygame.mixer.Sound("sound/goal.mp3")
