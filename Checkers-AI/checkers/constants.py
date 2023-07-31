import pygame
import os

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_ASSET = os.path.join(_BASE_DIR, "assets")

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
CROWN = pygame.transform.scale(pygame.image.load(os.path.join(_ASSET, "crown.png")), (44, 25))

