import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.size = (128, 128)
        self.position = pos

        self.image_orig = pygame.image.load("img/gun.png").convert_alpha()
        self.sprites = [
            self.image_orig.subsurface(0, 0, self.size[0], self.size[1]),
            self.image_orig.subsurface(self.size[0], 0, self.size[0], self.size[1]),
        ]
        self.image = self.sprites[0]

        self.shadow_size = (140, 128)
        self.shadow_image_orig = pygame.image.load("img/gun_shadow.png").convert_alpha()
        self.shadow_sprites = [
            self.shadow_image_orig.subsurface(
                0, 0, self.shadow_size[0], self.shadow_size[1]
            ),
            self.shadow_image_orig.subsurface(
                self.shadow_size[0], 0, self.shadow_size[0], self.shadow_size[1]
            ),
        ]
        self.shadow_image = self.shadow_sprites[0]

        self.rect = self.image.get_rect()

        self.angle = 0
        self.flip = False
        self.recoil = 0
        self.flash = 0
        self.flash_point = (0, 0)
        self.draw_angle = 0
        self.bullet_offset = 0
        self.bullets = []
        self.shoot_timer = 0

        self.gun_sound = pygame.mixer.Sound("sound/gunshot.mp3")
        self.gun_sound.set_volume(0.65)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.flip = mouse_pos[0] < self.position[0]

        if self.flip:
            self.bullet_offset = (
                self.position[0] + math.cos(math.radians(self.draw_angle - 30)) * 28,
                self.position[1] - math.sin(math.radians(self.draw_angle - 30)) * 28,
            )
            self.angle = math.degrees(
                -math.atan2(
                    mouse_pos[1] - self.bullet_offset[1],
                    mouse_pos[0] - self.bullet_offset[0],
                )
            )
        else:
            self.bullet_offset = (
                self.position[0] + math.cos(math.radians(self.draw_angle + 30)) * 28,
                self.position[1] - math.sin(math.radians(self.draw_angle + 30)) * 28,
            )
            self.angle = math.degrees(
                -math.atan2(
                    mouse_pos[1] - self.bullet_offset[1],
                    mouse_pos[0] - self.bullet_offset[0],
                )
            )

        self.draw_angle = self.angle + self.recoil

        self.image = pygame.transform.rotozoom(
            self.sprites[self.flip], self.draw_angle, 0.5
        )
        self.shadow_image = pygame.transform.rotozoom(
            self.shadow_sprites[self.flip], self.draw_angle, 0.5
        )

        if self.shoot_timer > 0:
            self.shoot_timer -= 1

        if self.recoil > 0:
            self.recoil -= 10

        if self.flash > 0:
            self.flash -= 1
