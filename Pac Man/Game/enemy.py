"""
This is the enemy class for the pac-man game
"""

import pygame
import random
from pygame.math import Vector2
from .settings import *


class Enemy(object):
    def __init__(self, game, pos, number):
        self.game = game
        self.grid_pos = pos
        self.number = number
        self.image = self.set_image()
        self.pix_pos = self.get_pix_pos()
        self.radius = int(self.game.cell_width // 2.3)
        self.direction = Vector2(1, 0)
        self.personality = self.set_personality()

    def get_pix_pos(self):
        return Vector2(
            (self.grid_pos.x * self.game.cell_width - self.image.get_width()) + TOP_BOTTOM_BUFFER // 2 + self.game.cell_width // 2 ,
            (self.grid_pos.y * self.game.cell_height - self.image.get_height()) + TOP_BOTTOM_BUFFER // 2 + self.game.cell_height // 2)

    def update(self):

        self.pix_pos += self.direction

        if self.time_to_move():
            self.move()

        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER + self.game.cell_width // 2) // self.game.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[
                                1] - TOP_BOTTOM_BUFFER + self.game.cell_height // 2) // self.game.cell_height + 1

    def draw(self):

        self.game.screen.blit(self.image, [int(self.pix_pos.x), int(self.pix_pos.y)])

    # pygame.draw.circle(self.game.screen, self.color, (int(self.pix_pos.x), int(self.pix_pos.y)), self.radius)

    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.game.cell_width == 0:
            if self.direction == Vector2(1, 0) or self.direction == Vector2(-1, 0):
                return True

        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.game.cell_height == 0:
            if self.direction == Vector2(0, 1) or self.direction == Vector2(0, -1):
                return True

        return False

    def move(self):

        if self.personality == "random":
            self.direction = self.get_path_direction()

        if self.personality == "slow":
            self.direction = self.get_path_direction()

        if self.personality == "speedy":
            self.direction = self.get_path_direction()

        if self.personality == "scared":
            self.direction = self.get_path_direction()

    def get_path_direction(self):
        next_cell = self.find_next_cell()
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]

        return Vector2(xdir, ydir)

    def find_next_cell(self):
        path = self.breath_first_search([int(self.grid_pos.x), int(self.grid_pos.y)], [int(self.game.player.grid_pos.x),
                                                                                       int(
                                                                                           self.game.player.grid_pos.y)])
        return path[1]

    def breath_first_search(self, start, target):
        grid = [[0 for _ in range(28)] for _ in range(30)]

        for cell in self.game.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1

        queue = [start]
        path = []
        visited = []

        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)

            if current == target:
                break

            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if 0 <= neighbour[0] + current[0] < len(grid[0]):
                        if 0 <= neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})

        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])

        return shortest

    def get_random_direction(self):
        while True:
            number = random.randint(-2, 1)

            if number == -2:
                x_dir, y_dir = 1, 0

            elif number == -1:
                x_dir, y_dir = 0, 1

            elif number == 0:
                x_dir, y_dir = -1, 0

            else:
                x_dir, y_dir = 0, -1

            next_pos = Vector2(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)

            if next_pos not in self.game.walls:
                break

        return Vector2(x_dir, y_dir)

    def set_image(self):
        if self.number == 0:
            return pygame.image.load('images/blue.png').convert_alpha()

        elif self.number == 1:
            return pygame.image.load('images/pink.png').convert_alpha()

        elif self.number == 2:
            return pygame.image.load('images/red.png').convert_alpha()

        else:
            return pygame.image.load('images/yellow.png').convert_alpha()

    def set_personality(self):
        if self.number == 0:
            return "speedy"

        elif self.number == 1:
            return "slow"

        elif self.number == 2:
            return "random"

        else:
            return "scared"
