"""
This file contains all the settings for our Pac-Man game like:
WIDTH, HEIGHT, COLOR etc
"""

from pygame.math import Vector2

WIDTH, HEIGHT = 610, 670
FPS = 60
TOP_BOTTOM_BUFFER = 50
MAZE_WIDTH, MAZE_HEIGHT = WIDTH - TOP_BOTTOM_BUFFER, HEIGHT - TOP_BOTTOM_BUFFER

START_TEXT_SIZE = 30
START_FONT = "comicsans"

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (107, 107, 107)

#PLAYER_START_POS = 0
PLAYER_COLOR = (190, 194, 15)