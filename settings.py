TITLE = "Jumpy Boi"
# screen dims
WIDTH = 1080
HEIGHT = 720
# frames per second
FPS = 60
# colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)
REDDISH = (240,55,66)
SKY_BLUE = (143, 185, 252)
FONT_NAME = 'arial'
SPRITESHEET = "spritesheet_jumper.png"
# data files
HS_FILE = "highscore.txt"
# player settings
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 25
# game settings
BOOST_POWER = 60
POW_SPAWN_PCT = 8
MOB_FREQ = 500
# layers - uses numerical value in layered sprites
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 3
MOB_LAYER = 2
CLOUD_LAYER = 0

# platform settings
''' old platforms from drawing rectangles'''
'''
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                 (65, HEIGHT - 300, WIDTH-400, 40),
                 (20, HEIGHT - 350, WIDTH-300, 40),
                 (200, HEIGHT - 150, WIDTH-350, 40),
                 (200, HEIGHT - 450, WIDTH-350, 40)]
'''
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
# PLATFORM_LIST = [(0, HEIGHT - 40),
#                  (65, HEIGHT - 300),
#                  (20, HEIGHT - 350),
#                  (200, HEIGHT - 150),
#                  (200, HEIGHT - 450)]
