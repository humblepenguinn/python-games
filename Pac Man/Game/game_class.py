"""
This file contains the actual pac-man game class
"""

import pygame
import sys
from .settings import *
from .player import Player
from .enemy import Enemy
from pygame.math import Vector2

pygame.init()
vec = pygame.math.Vector2


class Game(object):
    def __init__(self):
        """
        this is the init method for the game class, creates the screen, clock etc
        """
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "start"
        self.cell_width = MAZE_WIDTH // 28
        self.cell_height = MAZE_HEIGHT // 30
        print(self.cell_width, self.cell_height)
        self.walls = []
        self.coins = []
        self.enemies = []
        self.e_pos = []
        self.p_pos = None
        self.load()
        self.player = Player(self, self.p_pos)
        self.make_enemies()

    def main(self):
        """
        this method contains the Pac-Man game
        :return: None
        """
        while self.running:
            if self.state == "start":
                self.start_events()
                self.start_update()
                self.start_draw()

            if self.state == "playing":
                self.playing_events()
                self.playing_update()
                self.playing_draw()

            if self.state == "Game Over":
                self.game_over_update()
                self.game_over_events()
                self.game_over_draw()

            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    ###################### HELPER FUNCTIONS #########################################
    @staticmethod
    def draw_text(words, screen, pos, size, color, font_name, centered=False):
        """
        this method blits text to a screen
        :param words: str
        :param screen: pygame screen
        :param pos: list
        :param size: int
        :param color: tuple
        :param font_name: str
        :return: None
        """
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, color)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2

        screen.blit(text, pos)

    def draw_grid(self):
        for x in range(WIDTH // self.cell_width):
            pygame.draw.line(self.background, GREY, (x * self.cell_width, 0), (x * self.cell_width, HEIGHT))

        for x in range(WIDTH // self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x * self.cell_height), (WIDTH, x * self.cell_height))

    def load(self):
        self.background = pygame.transform.scale(pygame.image.load("maze.png"), (MAZE_WIDTH, MAZE_HEIGHT))
        with open("walls.txt") as f:
            for yidx, line in enumerate(f):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(Vector2(xidx, yidx))

                    elif char == "C":
                        self.coins.append(Vector2(xidx, yidx))


                    elif char == "P":
                        self.p_pos = Vector2(xidx, yidx)

                    elif char in ["2", "3", "4", "5"]:
                        self.e_pos.append(Vector2(xidx, yidx))

                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (
                            xidx * self.cell_width, yidx * self.cell_height, self.cell_width, self.cell_height))

    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, pos, idx))

    ###################### INTRO FUNCTIONS ###################################
    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = "playing"

    def start_update(self):
        pass

    def start_draw(self):
        """
        this method displays the start menu
        :return: None
        """
        self.screen.fill(BLACK)
        self.draw_text("PUSH SPACE BAR", self.screen, [WIDTH // 2, HEIGHT // 2], START_TEXT_SIZE, (170, 132, 58),
                       START_FONT, centered=True)
        self.draw_text("1 PLAYER ONLY", self.screen, [WIDTH // 2, HEIGHT // 2 + 50], START_TEXT_SIZE, (44, 167, 198),
                       START_FONT, centered=True)
        self.draw_text("HIGH SCORE", self.screen, [4, 0], START_TEXT_SIZE, (255, 255, 255),
                       START_FONT)

        pygame.display.update()

    ###################### PLAYING FUNCTIONS ################################
    def playing_events(self):
        """
        this is the playing events method
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                    self.player.move_direction = "left"

                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                    self.player.move_direction = "right"


                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))

                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))


        if len(self.coins) == 0:
            self.state = "Game Over"

        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.state = "Game Over"

    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER // 2, TOP_BOTTOM_BUFFER // 2))
        self.draw_coins()
        # self.draw_grid()
        self.draw_text(f"SCORE: {str(self.player.current_score)}", self.screen, [60, 0], 30, WHITE, START_FONT)
        self.draw_text("HIGH SCORE: 0", self.screen, [WIDTH // 2 - 50, 0], 30, WHITE, START_FONT)
        self.player.draw()

        for enemy in self.enemies:
            enemy.draw()

        pygame.display.update()

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7), (
                int(coin.x * self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_BUFFER // 2,
                int(coin.y * self.cell_height) + self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2), 5)

    ################### GAME OVER EVENT ##########################
    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def game_over_update(self):
        pass

    def game_over_draw(self):
        """
        this method displays the start menu
        :return: None
        """
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.screen, [WIDTH // 2, HEIGHT // 2], START_TEXT_SIZE, RED,
                       START_FONT, centered=True)

        pygame.display.update()
