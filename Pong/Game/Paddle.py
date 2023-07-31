import pygame
from .Game import Game
import sys


class Paddle(object):
    WIDTH = 20
    HEIGHT = 100

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, color):
        pygame.draw.rect(Game.screen, color, pygame.Rect(self.x, self.y - self.HEIGHT // 2, self.WIDTH, self.HEIGHT))

    def update(self, ball, bgColor, fgColor):
        if sys.argv[1] == "AI":
            if ball.x > 800:
                if self.y > ball.y and abs(self.y - ball.y) > 50:
                    self.y -= (Game.VELOCITY + 10)
                    self.draw(fgColor)

                if self.y < ball.y and abs(self.y - ball.y) > 50:
                    self.y += (Game.VELOCITY + 10)
                    self.draw(fgColor)

            self.draw(bgColor)
            self.draw(fgColor)

        elif sys.argv[1] == "player":
            newY = pygame.mouse.get_pos()[1]
            if newY - self.HEIGHT // 2 > Game.BORDER and newY + self.HEIGHT // 2 < Game.HEIGHT - Game.BORDER:
                self.draw(bgColor)
                self.y = newY
                self.draw(fgColor)
            else:
                self.draw(bgColor)
                self.draw(fgColor)

    def model_update(self, ball, bgColor, fgColor):
        if ball.x < 800:
            if self.y > ball.y and abs(self.y - ball.y) > 50:
                self.y -= (Game.VELOCITY + 10)

            if self.y < ball.y and abs(self.y - ball.y) > 50:
                self.y += (Game.VELOCITY + 10)

        self.draw(bgColor)
        self.draw(fgColor)
