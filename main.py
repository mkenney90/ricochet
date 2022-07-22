import pygame
import pygame.freetype
import math
from globals import *
from sys import exit
from os.path import exists
from random import randint
from player import Player
from bullet import Bullet
from bonus_text import Bonus

pygame.init()
pygame.display.set_caption("Ricochet")
pygame.key.set_repeat()


def init_game():
    vars()


screen = pygame.display.set_mode((LEVEL_WIDTH, LEVEL_HEIGHT), pygame.SCALED)
laser_surface = pygame.Surface((500, 2))
ui = pygame.Surface((150, 60))
ui.set_alpha(225)
pygame.font.init()
BG = pygame.image.load("img/bg.png").convert()
clock = pygame.time.Clock()


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, tile_idx=0):
        super().__init__()
        self.size = (64, 64)
        self.tile_size = (32, 32)
        self.position = pos
        self.start_position = pos
        self.tile_idx = tile_idx
        self.image = WALL_TILES[self.tile_idx]
        self.rect = pygame.Rect(
            self.position[0], self.position[1], self.tile_size[0], self.tile_size[1]
        )
        self.impact_side = None
        self.impact = False

    def update(self):

        if self.position != self.start_position:
            self.position = self.start_position
            self.impact = False

        if self.impact:
            if self.impact_side == "left":
                self.position = (self.start_position[0] + 3, self.start_position[1])
            elif self.impact_side == "right":
                self.position = (self.start_position[0] - 3, self.start_position[1])
            elif self.impact_side == "up":
                self.position = (self.start_position[0], self.start_position[1] + 3)
            elif self.impact_side == "down":
                self.position = (self.start_position[0], self.start_position[1] - 3)


class Target(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.size = (32, 32)
        self.position = pos
        self.active = True
        self.image_orig = pygame.image.load("img/target.png").convert_alpha()
        self.image = self.image_orig.copy()
        self.rock_max = 30
        self.rock_amount = randint(-self.rock_max, self.rock_max)
        self.rock_dir = -1

    def update(self):
        global SCORE, SCORE_EFFECT

        if abs(self.rock_amount) >= self.rock_max:
            self.rock_dir *= -1
        self.rock_amount += self.rock_dir
        self.rect = pygame.Rect(self.position[0] - 4, self.position[1] - 4, 8, 8)
        self.image = pygame.transform.rotozoom(self.image_orig, self.rock_amount, 1.0)
        for b in bullets:
            if b.rect.colliderect(self.rect):
                SCORE += 1 + b.bounces
                self.active = False
                TARGET_ANIMS.append(TargetAnim(self.position))
                score_texts.append(
                    Bonus((self.position[0] - 10, self.position[1] - 4), 1 + b.bounces)
                )
                SCORE_EFFECT = 30
                GOAL_SOUND.play()
                b.bounces += 2


class TargetAnim(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.size = (32, 32)
        self.position = pos
        self.active = True
        self.lifetime = 30
        self.image_orig = pygame.transform.scale(
            pygame.image.load("img/target.png").convert_alpha(), self.size
        )

    def update(self):
        if self.lifetime < 1:
            self.position = (-150, -150)
            self.active = False
        else:
            self.size = (32 / 30 * self.lifetime, 32 / 30 * self.lifetime)
            self.image = pygame.transform.smoothscale(self.image_orig, self.size)
            self.lifetime -= 1


class LevelLoader:
    def read_level(level):
        global WALLS, TARGETS
        WALLS = []
        TARGETS = []

        if exists("levels/level_{}.txt".format(level)):
            with open("levels/level_{}.txt".format(level)) as f:
                try:
                    lines = f.readlines()

                    for x, line in enumerate(lines):
                        for y, char in enumerate(line):
                            if char == "X":
                                WALLS.append(Wall((y * 32, x * 32)))
                            elif char == "V":
                                WALLS.append(Wall((y * 32, x * 32), 1))
                            elif char == "H":
                                WALLS.append(Wall((y * 32, x * 32), 2))
                            elif char == "T":
                                TARGETS.append(Target((y * 32, x * 32)))
                            elif char == "P":
                                PLAYER.position = (y * 32, x * 32)

                    f.close()
                except IOError:
                    print("!!! problem reading level data !!!")
                except:
                    print("!!! problem building level {} !!!".format(level))
        else:
            print("reached end of levels")
            init_game()


def player_input():
    global AMMO
    if KEYS["FIRE"] and PLAYER.shoot_timer == 0:
        print("FIRE")
        bullets.append(
            Bullet(
                PLAYER.bullet_offset,
                PLAYER.angle,
            )
        )
        PLAYER.gun_sound.play()
        PLAYER.shoot_timer = 35
        PLAYER.recoil = 30
        PLAYER.flash = 3
        PLAYER.flash_point = PLAYER.bullet_offset
        AMMO -= 1
        KEYS["FIRE"] = False


def draw_laser():
    laser_image_orig = pygame.image.load("img/laser.png").convert_alpha()
    mouse_pos = pygame.mouse.get_pos()
    dist = min(
        math.hypot(
            mouse_pos[1] - PLAYER.bullet_offset[1],
            mouse_pos[0] - PLAYER.bullet_offset[0],
        ),
        300,
    )
    test_length = 0
    laser_length = dist
    for wall in WALLS:
        for i in range(0, round(dist), 20):
            test_length = i
            if pygame.Rect.collidepoint(
                wall.rect,
                PLAYER.bullet_offset[0] + math.cos(math.radians(PLAYER.angle)) * i,
                PLAYER.bullet_offset[1] - math.sin(math.radians(PLAYER.angle)) * i,
            ):
                if test_length < laser_length:
                    laser_length = test_length
                break

    laser_image = pygame.transform.smoothscale(laser_image_orig, (laser_length, 500))
    laser_image = pygame.transform.rotate(laser_image, PLAYER.draw_angle)
    laser_rect = laser_image.get_rect(
        center=(
            PLAYER.bullet_offset[0]
            + math.cos(math.radians(PLAYER.draw_angle)) * laser_length / 2,
            PLAYER.bullet_offset[1]
            - math.sin(math.radians(PLAYER.draw_angle)) * laser_length / 2,
        )
    )

    screen.blit(
        laser_image,
        (laser_rect.topleft),
    )


def draw_ui():
    global SCORE, SCORE_FONT_SIZE, SCORE_EFFECT
    ui_font = pygame.font.Font("fonts/Unispace bd.ttf", SCORE_FONT_SIZE)
    score_font = pygame.font.Font(
        "fonts/Unispace bd.ttf", SCORE_FONT_SIZE + int(SCORE_EFFECT / 4)
    )
    ui_text = ui_font.render("Score: ", True, (240, 240, 200))
    ui_score = score_font.render("{}".format(SCORE), True, (240, 240, 200))
    bullet_icon_orig = pygame.image.load("img/bullet_icon.png").convert_alpha()
    bullet_icon = pygame.transform.smoothscale(bullet_icon_orig, (14, 14))
    bullet_icon_shadow_orig = pygame.image.load(
        "img/bullet_icon_shadow.png"
    ).convert_alpha()
    bullet_icon_shadow = pygame.transform.smoothscale(bullet_icon_shadow_orig, (14, 14))
    ui.fill((50, 50, 50))
    pygame.draw.rect(
        ui, (0, 100, 200), (3, 3, ui.get_rect().right - 3, ui.get_rect().bottom - 3)
    )
    ui.blit(
        ui_text,
        (ui_text.get_rect(left=20, centery=ui.get_rect().centery - 8)),
    )
    ui.blit(
        ui_score,
        (ui_score.get_rect(left=90, centery=ui.get_rect().centery - 8)),
    )
    for i in range(6):
        ui.blit(
            bullet_icon_shadow,
            (ui.get_rect().left + 20 + (14 * i), ui.get_rect().bottom - 20),
        )
    for i in range(AMMO):
        ui.blit(
            bullet_icon, (ui.get_rect().left + 18 + (14 * i), ui.get_rect().bottom - 22)
        )
    screen.blit(ui, (LEVEL_WIDTH - 150, LEVEL_HEIGHT - 60))
    SCORE_EFFECT = max(SCORE_EFFECT - 1, 0)


def init_level():
    global bullets, AMMO, LEVEL_END, LEVEL_END_TIMER
    bullets = []
    AMMO = 6
    LEVEL_END = False
    LEVEL_END_TIMER = 120
    LevelLoader.read_level(LEVEL_CURRENT)


def check_complete():
    for t in TARGETS:
        if t.active:
            return False

    return True


def finish_level():
    global LEVEL_END
    LEVEL_END = True


PLAYER = Player((-50, -50))
START_SCREEN = pygame.image.load("img/start_screen.png").convert()
WALL_TILESET = pygame.image.load("img/wall_tiles.png").convert_alpha()
WALL_TILESET.set_colorkey((255, 255, 255))
WALL_TILES = [
    WALL_TILESET.subsurface([0, 0, 32, 32]),
    WALL_TILESET.subsurface([32, 0, 32, 32]),
    WALL_TILESET.subsurface([0, 32, 32, 32]),
]
GOAL_SOUND = pygame.mixer.Sound("sound/goal.mp3")


while True:

    if STATE == "start":
        screen.fill((55, 55, 55))
        start_screen_font = pygame.font.Font(
            "fonts/Unispace bd.ttf", START_SCREEN_FONT_SIZE
        )
        start_text = start_screen_font.render(
            "Press SPACE to Begin", True, (240, 240, 200)
        )
        screen.blit(START_SCREEN, (0, 0))
        screen.blit(
            start_text,
            (start_text.get_rect(centerx=LEVEL_WIDTH / 2, centery=LEVEL_HEIGHT - 50)),
        )
        if KEYS["FIRE"]:
            KEYS["FIRE"] = False
            STATE = "game"
            init_level()

    elif STATE == "game":
        screen.fill((10, 95, 135))

        bg_width = BG.get_width()
        bg_height = BG.get_height()
        for x in range(math.ceil(LEVEL_WIDTH / bg_width)):
            for y in range(math.ceil(LEVEL_HEIGHT / bg_height)):
                screen.blit(BG, (x * bg_width, y * bg_height))

        if PLAYER:
            for t in TARGETS:
                t.update()
                if t.active:
                    screen.blit(
                        t.image,
                        (
                            t.position[0] - int(t.image.get_width() / 2),
                            t.position[1] - int(t.image.get_height() / 2),
                        ),
                    )
                else:
                    TARGETS.remove(t)
            for ta in TARGET_ANIMS:
                if ta.active:
                    ta.update()
                    screen.blit(
                        ta.image,
                        (
                            ta.position[0] - int(ta.image.get_width() / 2),
                            ta.position[1] - int(ta.image.get_height() / 2),
                        ),
                    )
            PLAYER.update()
            player_input()
            draw_laser()
            screen.blits(
                (
                    (
                        PLAYER.shadow_image,
                        (
                            PLAYER.position[0] - int(PLAYER.image.get_width() / 2) + 2,
                            PLAYER.position[1] - int(PLAYER.image.get_height() / 2) + 2,
                        ),
                    ),
                    (
                        PLAYER.image,
                        (
                            PLAYER.position[0] - int(PLAYER.image.get_width() / 2),
                            PLAYER.position[1] - int(PLAYER.image.get_height() / 2),
                        ),
                    ),
                )
            )
            if PLAYER.flash > 0:
                pygame.draw.circle(
                    screen,
                    (250, 240, 0),
                    (
                        PLAYER.flash_point[0]
                        + math.cos(math.radians(PLAYER.draw_angle)) * 8,
                        PLAYER.flash_point[1]
                        - math.sin(math.radians(PLAYER.draw_angle)) * 8,
                    ),
                    15,
                )
            for w in WALLS:
                screen.blit(w.image, w.position)
                w.update()
                if DEBUG:
                    pygame.draw.circle(
                        screen,
                        (255, 255, 255, 60),
                        (
                            w.position[0] + w.tile_size[0] / 2,
                            w.position[1] + w.tile_size[1] / 2,
                        ),
                        3,
                    )
            if DEBUG:
                if COLLISION:
                    if len(COLLISION) > 1:
                        pygame.draw.rect(
                            screen,
                            (220, 220, 0),
                            pygame.Rect(COLLISION[-2][0], COLLISION[-2][1], 32, 32),
                        )
                    pygame.draw.rect(
                        screen,
                        (100, 180, 0),
                        pygame.Rect(COLLISION[-1][0], COLLISION[-1][1], 32, 32),
                    )
            for b in bullets:
                b.update(WALLS, screen)

                if DEBUG:
                    pygame.draw.rect(screen, (255, 0, 0), b.rect)
                    pygame.draw.rect(screen, (0, 255, 0), b.temp_rect)

                if not b.active:
                    bullets.remove(b)

            for st in score_texts:
                if st.lifetime:
                    st.update()
                    score_text = st.font.render(
                        "+{}".format(st.value), True, (100, 230, 0)
                    )
                    score_text_shadow = st.font.render(
                        "+{}".format(st.value), True, (50, 50, 50)
                    )
                    screen.blits(
                        (
                            (
                                score_text_shadow,
                                (st.position[0] + 2, st.position[1] + 2),
                            ),
                            (score_text, (st.position)),
                        )
                    )

                # pygame.draw.rect(screen, (10, 200, 10), (b.rect))
        if check_complete():
            finish_level()

        if LEVEL_END_TIMER < 1:
            LEVEL_CURRENT += 1
            init_level()

        if LEVEL_END:
            LEVEL_END_TIMER -= 1

        draw_ui()

    # print(clock.get_fps())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                KEYS["FIRE"] = True

    pygame.display.update()
    clock.tick(60)
