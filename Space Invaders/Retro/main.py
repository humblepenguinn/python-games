import pygame
import random
from constants import *
import math


class Game(object):
    FPS = 60

    def __init__(self):
        self.win = pygame.display.set_mode((WIDTH, WIDTH))
        pygame.display.set_caption("Space Invaders V1")
        self.clock = pygame.time.Clock()

    def draw(self, player, enemies, bunkers, missiles, bombs):
        self.win.fill(BLACK)

        for i in range(player.lives):
            pygame.draw.rect(self.win, RED, (50 + (i * 130), 715, 130, 15))

        player.draw(self.win)

        enemies.update()
        enemies.draw(self.win)
        bunkers.draw(self.win)

        missiles.update()
        missiles.draw(self.win)

        bombs.update()
        bombs.draw(self.win)
        pygame.display.update()

    def main(self, player, Enemy, Bunker, Missile, Bomb):
        run = True
        VEL = 20
        enemies = pygame.sprite.Group()
        missiles = pygame.sprite.Group()
        bombs = pygame.sprite.Group()
        bunkers = pygame.sprite.Group()

        for row in range(1, 6):
            for column in range(1, 11):
                enemy = Enemy(80 + (50 * column), 25 + (50 * row), 1)
                enemies.add(enemy)

        for bunk in range(3):
            for row in range(5):
                for column in range(10):
                    bunker = Bunker(50 + (275 * bunk) + (10 * column), 500 + (10 * row))
                    bunkers.add(bunker)

        while run:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        missile = Missile(player.rect.x + player.offset, player.rect.y)
                        missiles.add(missile)

            shoot_chance = random.randint(1, 500)
            if shoot_chance < VEL:
                if len(enemies) > 0:
                    random_enemy = random.choice(enemies.sprites())
                    bomb = Bomb(random_enemy.rect.x + 12, random_enemy.rect.y + 25)
                    bombs.add(bomb)

            for missile in missiles:
                if missile.rect.y < 0:
                    missiles.remove(missile)

                for enemy in enemies:
                    if missile.rect.colliderect(enemy.rect):
                        missiles.remove(missile)
                        enemies.remove(enemy)

                for bunker in bunkers:
                    if missile.rect.colliderect(bunker.rect):
                        missiles.remove(missile)
                        bunkers.remove(bunker)

            for bomb in bombs:
                if bomb.rect.y > WIDTH:
                    bombs.remove(bomb)

                if bomb.rect.colliderect(player.rect):
                    bombs.remove(bomb)
                    player.lives -= 1
                    print(player.lives)

                for bunker in bunkers:
                    if bomb.rect.colliderect(bunker.rect):
                        bombs.remove(bomb)
                        bunkers.remove(bunker)

            if player.lives <= 0 or len(enemies) == 0:
                run = False

            player.move()
            self.draw(player, enemies, bunkers, missiles, bombs)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, vel):
        super().__init__()

        self.image = pygame.Surface([25, 25])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.VEL = vel
        self.group_rect = pygame.Rect(130, 75, 500, 250)

    def update(self):
        self.rect.x += self.VEL
        self.group_rect.x += self.VEL

        if self.group_rect.x + 500 >= WIDTH:
            self.VEL = -self.VEL

        if self.group_rect.x <= 0:
            self.VEL = -self.VEL
            #self.rect.y += self.VEL


class Bunker(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface([8, 8])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface([5, 10])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y -= 5


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface([5, 10])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.copy = self.image.get_rect()
        self.copy.x = x
        self.copy.y = y

    def update(self):
        self.rect.y += 5
        self.copy.y += 5


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, vel, lives):
        super().__init__()

        self.image = pygame.Surface([50, 25])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.lives = lives
        self.VEL = vel
        self.offset = 25

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.rect.x -= self.VEL

        if key[pygame.K_d]:
            self.rect.x += self.VEL



player = Player(375, 650, 10, 5)

game = Game()
game.main(player, Enemy, Bunker, Missile, Bomb)
