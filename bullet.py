import pygame
import math


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, angle):
        super().__init__()
        self.size = (10, 10)
        self.strip_size = (40, 10)
        self.death_strip_size = (75, 15)
        self.position = pygame.Vector2(position)
        self.speed = 7
        self.angle = math.radians(angle)
        self.vel = pygame.Vector2(
            (math.cos(self.angle) * self.speed, -math.sin(self.angle) * self.speed)
        )
        self.strip_orig = pygame.transform.smoothscale(
            pygame.image.load("img/bullet_strip.png").convert_alpha(), self.strip_size
        )
        self.status = 0
        self.sprites = [
            self.strip_orig.subsurface([0, 0, 10, 10]),
            self.strip_orig.subsurface([10, 0, 10, 10]),
            self.strip_orig.subsurface([20, 0, 10, 10]),
            self.strip_orig.subsurface([30, 0, 10, 10]),
        ]

        self.death_anim_orig = pygame.transform.smoothscale(
            pygame.image.load("img/bullet_death.png").convert_alpha(),
            self.death_strip_size,
        )
        self.anim_frame = 0
        self.death_sprites = [
            self.death_anim_orig.subsurface([0, 0, 15, 15]),
            self.death_anim_orig.subsurface([15, 0, 15, 15]),
            self.death_anim_orig.subsurface([30, 0, 15, 15]),
            self.death_anim_orig.subsurface([45, 0, 15, 15]),
            self.death_anim_orig.subsurface([60, 0, 15, 15]),
        ]

        self.image = self.sprites[self.status]
        self.shadow_image_orig = pygame.transform.smoothscale(
            pygame.image.load("img/bullet_shadow.png").convert_alpha(), self.size
        )
        self.shadow_image = self.shadow_image_orig
        self.rect = self.image.get_rect(center=self.position)
        self.bounces = 0
        self.life = 4
        self.active = True

        self.impact_sound = pygame.mixer.Sound("sound/impact.mp3")
        self.die_sound = pygame.mixer.Sound("sound/pop.mp3")
        self.impact_sound.set_volume(0.4)
        self.die_sound.set_volume(0.4)

    def check_collisions(self, walls):
        for wall in walls:
            if (
                self.position.x + self.size[0] / 2 + self.vel.x > wall.position[0]
                and self.position.x - self.size[0] / 2 + self.vel.x
                < wall.position[0] + wall.tile_size[0]
                and self.position.y + self.size[1] / 2 > wall.position[1]
                and self.position.y - self.size[1] / 2
                < wall.position[1] + wall.tile_size[1]
            ):
                return "x"
            elif (
                self.position.x + self.size[0] / 2 > wall.position[0]
                and self.position.x - self.size[0] / 2
                < wall.position[0] + wall.tile_size[0]
                and self.position.y + self.size[1] / 2 + self.vel.y > wall.position[1]
                and self.position.y - self.size[1] / 2 + self.vel.y
                < wall.position[1] + wall.tile_size[1]
            ):
                return "y"

        return None

    def move(self, walls):
        collision = self.check_collisions(walls)
        if collision == "x":
            self.vel.x *= -1
        elif collision == "y":
            self.vel.y *= -1

        if collision:
            if self.life > 1:
                self.impact_sound.play()
            else:
                self.die_sound.play()
            self.life -= 1
            self.bounces += 1

        self.position += self.vel

    def update(self, walls, canvas):
        if self.life:
            self.collision = False
            self.move(walls)
            self.rect.center = self.position
            self.image = self.sprites[self.status]
            self.closest = (None, 999)
            self.status = min(self.bounces, len(self.sprites) - 1)
            self.image.set_alpha(self.life * 125)
            self.shadow_image.set_alpha(self.life * 75 + 50)
            self.draw(canvas)
        else:
            if round(self.anim_frame) > len(self.death_sprites) - 1:
                self.active = False  # delete bullet after pop animation
            else:
                self.anim_frame += 0.15
                self.image = self.death_sprites[math.floor(self.anim_frame)]

        print(self.image)

    def draw(self, canvas):
        canvas.blits(
            ((self.shadow_image, (self.rect.move(2, 2))), (self.image, (self.rect)))
        )
