import pygame


class Bonus(pygame.sprite.Sprite):
    def __init__(self, position, value=0, size=12, lifetime=100):
        super().__init__()
        self.position = pygame.Vector2(position)
        self.value = value
        self.lifetime = lifetime
        self.size = size
        self.font = pygame.font.Font("fonts/Unispace bd.ttf", self.size)

    def update(self):
        if self.lifetime < 1:
            return

        self.lifetime -= 1
        self.position.y -= 0.22
