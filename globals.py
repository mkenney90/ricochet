def vars():
    global KEYS, LEVEL_WIDTH, LEVEL_HEIGHT, LEVEL_CURRENT, LEVEL_END, LEVEL_END_TIMER, TARGETS, TARGET_ANIMS, WALLS, STATE, COLLISION, SCORE, SCORE_EFFECT, SCORE_FONT_SIZE, START_SCREEN_FONT_SIZE, AMMO, bullets, score_texts, DEBUG
    KEYS = {"FIRE": False}
    LEVEL_WIDTH = 800
    LEVEL_HEIGHT = 640
    LEVEL_CURRENT = 1
    LEVEL_END = False
    LEVEL_END_TIMER = 120
    TARGETS = []
    TARGET_ANIMS = []
    WALLS = []
    STATE = "start"
    COLLISION = []
    DEBUG = False
    SCORE = 0
    SCORE_EFFECT = 0
    SCORE_FONT_SIZE = 16
    START_SCREEN_FONT_SIZE = 20
    AMMO = 6
    bullets = []
    score_texts = []
    print("re-init globals")


vars()
