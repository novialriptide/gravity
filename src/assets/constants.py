import pygame
import os

MAIN_DIRECTORY_PATH = f"{os.getcwd()}/assets/"

# rendering constants
SCREEN_SIZE = (500, 500)
RENDER_SIZE = 10

# image constants
NOISE_TEXTURE_IMAGE_PATH = MAIN_DIRECTORY_PATH + "textures/parallax/noise.png"
NOISE_TEXTURE_IMAGE = pygame.image.load(NOISE_TEXTURE_IMAGE_PATH)
NOISE_TEXTURE_IMAGE.set_alpha(40)
DEFAULT_FONT = MAIN_DIRECTORY_PATH + "textures/pixel.ttf"

LOGO_IMAGE_PATH = MAIN_DIRECTORY_PATH + "textures/logos/logo_trans.png"
LOGO_IMAGE = pygame.image.load(LOGO_IMAGE_PATH)

# tile constants
UNTOUCHABLE_TILE_ID = 2
GOAL_TILE_ID = 3
START_TILE_ID = 4

# vars
OFFICIAL_LEVELS = os.listdir(MAIN_DIRECTORY_PATH + "levels")
OFFICIAL_LEVELS.remove("title.json")
