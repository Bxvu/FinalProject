TITLE = "Jumpy Boi"
# screen dims
WIDTH = 1280
HEIGHT = 760
# frames per second
FPS = 60
# colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)
REDDISH = (240,55,66)
SKY_BLUE = (143, 185, 252)
BROWN = (153, 140, 113)
GRAY = (110, 160, 149)
DARK_BLUE = (0, 23, 176)
FONT_NAME = 'arial'
SPRITESHEET = "spritesheet_jumper.png"
# data files
HS_FILE = "highscore.txt"
# player settings
PLAYER_ACC = 0.75
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 25
# game settings
BOOST_POWER = 60
POW_SPAWN_PCT = 8
MOB_FREQ = 500
# layers - uses numerical value in layered sprites
PLAYER_LAYER = 3
PLATFORM_LAYER = 2
POW_LAYER = 4
MOB_LAYER = 3
CLOUD_LAYER = 1
BACKGROUND_LAYER = 0

# platform settings
PLATFORM_LIST = [(25, HEIGHT - 40),
                 (WIDTH/2, HEIGHT - 200),
                 (20, HEIGHT - 350),
                 (500, HEIGHT - 150),
                 (800, HEIGHT - 450),
                 (-20, HEIGHT - 350),
                 (-500, HEIGHT - 150),
                 (-10, HEIGHT - 550),
                 (500, HEIGHT - 150),
                 (60, HEIGHT - 300),
                 (530, HEIGHT - 250),
                 ]