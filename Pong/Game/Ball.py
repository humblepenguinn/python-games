import pygame
from .Game import Game
from .Paddle import Paddle


class Ball(object):
    RADIUS = 20

    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def draw(self, color):
        pygame.draw.circle(Game.screen, color, (self.x, self.y), self.RADIUS)

    def update(self, player, model, fgColor, bgColor, p_score, model_score):
        notCollide = True
        newx = self.x + self.vx
        newy = self.y + self.vy

        if newx < Game.BORDER + self.RADIUS + 120:
            notCollide = False
            self.draw(bgColor)
            self.x = Game.WIDTH // 2
            self.y = Game.HEIGHT // 2
            p_score += 1

        if newx > Game.WIDTH + self.RADIUS + 120:
            notCollide = False
            self.draw(bgColor)
            self.x = Game.WIDTH // 2
            self.y = Game.HEIGHT // 2
            model_score += 1

        if Game.WIDTH - Paddle.WIDTH - 190 < newx + Ball.RADIUS < Game.WIDTH - Paddle.WIDTH - 160 and abs(newy - player.y) < Paddle.HEIGHT:
            self.vx = - self.vx

        if newx + Ball.RADIUS < Game.BORDER + Paddle.WIDTH + 190 and abs(newy - model.y) < Paddle.HEIGHT:
            self.vx = - self.vx

        if newy < Game.BORDER + self.RADIUS or newy > Game.HEIGHT - Game.BORDER - self.RADIUS:
            self.vy = -self.vy

        if notCollide:
            self.draw(bgColor)
            self.x = self.x + self.vx
            self.y = self.y + self.vy
            self.draw(fgColor)

        return model_score, p_score
