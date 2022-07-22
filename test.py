import pygame
import random


WIDTH = 800
HEIGHT = 640
FPS = 60
X = 300

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

## initialize pygame and create window
pygame.init()
pygame.mixer.init()  ## For sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test Sandbox")
clock = pygame.time.Clock()  ## For syncing the FPS

## group all the sprites together for ease of update
all_sprites = pygame.sprite.Group()


class gun(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.image_orig = pygame.image.load("img/gun.png").convert()
        self.image = pygame.transform.scale(self.image_orig, (64, 64))
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.rect.center = self.pos
        if self.pos.x > WIDTH - self.rect.width / 2:
            self.pos.x = 50


x = gun((45, 100))
y = gun((425, 200))

all_sprites.add(x, y)

_rect = pygame.Rect(125, 125, 200.999, 125.199)
new_rect = _rect.move(5, 5)


## Game loop
running = True
while running:

    # 1 Process input/events
    clock.tick(FPS)  ## will make the loop run at the same speed all the time
    for (
        event
    ) in (
        pygame.event.get()
    ):  # gets all the events which have occured till now and keeps tab of them.
        ## listening for the the X button at the top
        if event.type == pygame.QUIT:
            running = False

    # 2 Update
    all_sprites.update()
    for s in all_sprites:
        s.pos.x += 1

    # 3 Draw/render
    screen.fill(BLACK)

    all_sprites.draw(screen)
    pygame.draw.rect(screen, RED, _rect, 5)
    pygame.draw.rect(screen, BLUE, new_rect, 5)
    ## Done after drawing everything to the screen
    pygame.display.flip()

pygame.quit()
