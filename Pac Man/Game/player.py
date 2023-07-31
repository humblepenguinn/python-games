"""
this is the player class for the pac-man game
"""

import pygame
from pygame.math import Vector2
from .settings import *
import time
import _thread


class Player(object):
    def __init__(self, game, pos):
        """
        init method for the class
        """

        self.game = game
        self.grid_pos = pos
        self.direction = Vector2(1, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.VEL = 2
        self.left = [pygame.image.load("images/pacman-left1.png").convert_alpha(), pygame.image.load("images/pacman-left2.png").convert_alpha()]
        self.right = [pygame.image.load("images/pacman-right1.png").convert_alpha(), pygame.image.load("images/pacman-right2.png").convert_alpha()]
        self.pix_pos = self.get_pix_pos()
        self.index = 0
        self.current_image = self.left[self.index]
        self.move_direction = None
 

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction * self.VEL

        if self.time_to_move():
            if self.stored_direction is not None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()

        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER + self.game.cell_width // 2) // self.game.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[
                                1] - TOP_BOTTOM_BUFFER + self.game.cell_height // 2) // self.game.cell_height + 1


        if self.on_coin():
            self.eat_coin()

        self.animation()

    def animation(self):
        if self.move_direction == "right":
            self.index += 1


            if self.index >= len(self.right):
                self.index = 0

            self.current_image = self.right[self.index]


        if self.move_direction == "left":
            self.index += 1
            if self.index >= len(self.left):
                self.index = 0

            self.current_image = self.left[self.index]


    def draw(self):
        self.game.screen.blit(self.current_image, [int(self.pix_pos.x), int(self.pix_pos.y)])

        #pygame.draw.circle(self.game.screen, PLAYER_COLOR, (int(self.pix_pos.x), int(self.pix_pos.y)),
                           #self.game.cell_width // 2 - 2)

        """
        pygame.draw.rect(self.game.screen, RED,
                         (self.grid_pos[0] * self.game.cell_width + TOP_BOTTOM_BUFFER // 2,
                          self.grid_pos[1] * self.game.cell_height + TOP_BOTTOM_BUFFER // 2,
                          self.game.cell_width, self.game.cell_height), 1)
        """

    def on_coin(self):
        if self.grid_pos in self.game.coins:
            if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.game.cell_width == 0:
                if self.direction == Vector2(1, 0) or self.direction == Vector2(-1, 0):
                    return True

            if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.game.cell_height == 0:
                if self.direction == Vector2(0, 1) or self.direction == Vector2(0, -1):
                    return True
        else:
            return False

    def eat_coin(self):
        self.game.coins.remove(self.grid_pos)
        self.current_score += 1

    def move(self, direction):
        self.stored_direction = direction

    def get_pix_pos(self):
        return Vector2(
            (self.grid_pos.x * self.game.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.game.cell_width // 2,
            (self.grid_pos.y * self.game.cell_height) + TOP_BOTTOM_BUFFER // 2 + self.game.cell_height // 2)
        print(self.grid_pos, self.pix_pos)

    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.game.cell_width == 0:
            if self.direction == Vector2(1, 0) or self.direction == Vector2(-1, 0):
                return True

        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.game.cell_height == 0:
            if self.direction == Vector2(0, 1) or self.direction == Vector2(0, -1):
                return True

        return False

    def can_move(self):
        for wall in self.game.walls:
            if Vector2(self.grid_pos + self.direction) == wall:
                return False

        return True
