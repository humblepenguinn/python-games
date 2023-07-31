import pygame
from pygame.math import Vector2
import random
import sys


CELL_SIZE: int = 40
CELL_NUMBER: int = 20

# ─── COLORS ─────────────────────────────────────────────────────────────────────
BG_COLOR: tuple = (175, 215, 70)
GRASS_COLOR: tuple = (167, 209, 61)
DARK_GRASS_COLOR: tuple = (167, 209, 61)
FONT_COLOR: tuple = (56, 74, 12)

# ─── FONT ───────────────────────────────────────────────────────────────────────
pygame.font.init()
GAME_FONT: pygame.font.Font = pygame.font.Font("Font/PoetsenOne-Regular.ttf", 25)


class Game:
    def __init__(self, CELL_SIZE, CELL_NUMBER):
        # ─── SCREEN DIMENSIONS ──────────────────────────────────────────────────────────

        self.CELL_SIZE: int = CELL_SIZE
        self.CELL_NUMBER: int = CELL_NUMBER

        # ─── SETTING UP PYGAME ──────────────────────────────────────────────────────────
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        
        self.FPS: int = 60
        self.win: pygame.display = pygame.display.set_mode(
            (CELL_NUMBER * CELL_SIZE, CELL_NUMBER * CELL_SIZE))
        
        pygame.display.set_caption("Snake")

        self.clock: pygame.time.Clock = pygame.time.Clock()
        
        # ─── GAME OBJECTS ────────────────────────────────────────────────
        self.fruit: Food = Food()
        self.snake: Snake = Snake()
        
   
    
    def collision(self):
        """Checks to see if the fruit and the snake collide
        """
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_eating_sound()
            
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
            
    def is_dead(self):
        """Checks if the snake is dead
        """
        if not 0 <= self.snake.body[0].x < CELL_NUMBER or not 0 <= self.snake.body[0].y < CELL_NUMBER:
            self.game_over()
            
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
        
    def game_over(self):
        self.snake.reset()
        
        
    def draw_grass(self):
        for row in range(CELL_NUMBER):
            if row % 2 == 0:
                for col in range(CELL_NUMBER):
                    if col % 2 == 0:
                        grass_rect: pygame.Rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(self.win, GRASS_COLOR, grass_rect)
                        
            else:
                for col in range(CELL_NUMBER):
                    if col % 2 != 0:
                        grass_rect: pygame.Rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(self.win, GRASS_COLOR, grass_rect)
                
    def draw_score(self):
       score = str(len(self.snake.body) - 3)
       font_surface = GAME_FONT.render(score, True, FONT_COLOR)
       
       x_pos = int(CELL_SIZE * CELL_NUMBER - 60)
       y_pos = int(CELL_SIZE * CELL_NUMBER - 40)

       score_rect = font_surface.get_rect(center = (x_pos, y_pos))
       apple_rect = self.fruit.fruit_img.get_rect(midright = (score_rect.left, score_rect.centery))
       bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6, apple_rect.height)
       
       pygame.draw.rect(self.win, DARK_GRASS_COLOR, bg_rect)
       pygame.draw.rect(self.win, FONT_COLOR, bg_rect, 2)
       self.win.blit(font_surface, score_rect)
       self.win.blit(self.fruit.fruit_img, apple_rect)
       

    def update(self):
        """Updates the game
        """
        self.snake.move()
        self.collision()
        self.is_dead()
        
    def render(self):
        """Renders all the objects on the surface
        """
        
        self.draw_grass()
        self.fruit.draw(self.win)
        self.snake.draw(self.win)
        self.draw_score()
        pygame.display.update() 
        
    
    def main(self):
        """Main game loop
        """
        run: bool = True


        SCREEN_UPDATE: pygame.USEREVENT = pygame.USEREVENT
        pygame.time.set_timer(SCREEN_UPDATE, 150)

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == SCREEN_UPDATE:
                    self.update()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if self.snake.direction.y != 1:
                            self.snake.direction = self.snake.directions["up"]

                    if event.key == pygame.K_DOWN:
                        if self.snake.direction.y != -1:
                            self.snake.direction = self.snake.directions["down"]

                    if event.key == pygame.K_LEFT:
                        if self.snake.direction.x != 1:
                            self.snake.direction = self.snake.directions["left"]

                    if event.key == pygame.K_RIGHT:
                        if self.snake.direction.x != -1:
                            self.snake.direction = self.snake.directions["right"]

            self.win.fill((BG_COLOR))

            self.render()
            self.clock.tick(self.FPS)


class Snake:
    def __init__(self):
        self.body: list = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.directions = {"left": Vector2(-1, 0),  "right": Vector2(
            1, 0),  "up": Vector2(0, -1),  "down": Vector2(0, 1)}
        
        self.direction = Vector2(0, 0)
        
        self.new_block = False
        
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
            
        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')
        
        
    def move(self):
        """Moves the snake object through user input
        """
        if len(self.body) == 1:
            self.body[0] += self.direction
        
        if self.new_block:
            body_copy: list = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False
        
        if not(len(self.body)) == 1:
            body_copy: list = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
    
    def add_block(self):
        """changes new_block attribute to True
        """
        self.new_block = True
        
    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        
    def play_eating_sound(self):
        """Plays eating sound
        """
        self.crunch_sound.play()
        
    def update_head_graphics(self):
        """Checks the position of the head and determines the perfect img for it
        """
        head_relation: Vector2 = self.body[1] - self.body[0]
        
        if head_relation == Vector2(1, 0): self.head = self.head_left
        elif head_relation == Vector2(-1, 0): self.head = self.head_right
        elif head_relation == Vector2(0, 1): self.head = self.head_up
        elif head_relation == Vector2(0, -1): self.head = self.head_down
        
    def update_tail_graphics(self):
        """Checks the position of the tail and determines the perfect img for it
        """
        tail_relation: Vector2 = self.body[-2] - self.body[-1]
        
        if tail_relation == Vector2(1, 0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1): self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1): self.tail = self.tail_down

        
    
    def draw(self, win: pygame.display):
        """Draws the snake object on the surface provided

        Args:
            win (pygame.display): [surface to draw on]
        """
        
        self.update_head_graphics()
        self.update_tail_graphics()
        
        for index, block in enumerate(self.body):
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            
            block_rect = pygame.Rect(x_pos, 
                                     y_pos, CELL_SIZE, CELL_SIZE)
            
            if index == 0:
                win.blit(self.head, block_rect)
            
            elif index == len(self.body) - 1:
                win.blit(self.tail, block_rect)
                
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                
                if previous_block.x == next_block.x: win.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y: win.blit(self.body_horizontal, block_rect)
                
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1: win.blit(self.body_tl, block_rect) 
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1: win.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1: win.blit(self.body_tr, block_rect)         
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1: win.blit(self.body_br, block_rect)            
                
                
class Food:
    def __init__(self):
        self.randomize()
        self.fruit_img = pygame.image.load("Graphics/apple.png").convert_alpha()

    def draw(self, win: pygame.display):
        """Draws the fruit object on the surface provided

        Args:
            win (pygame.display): [surface to draw on]
        """

        fruit_rect: pygame.Rect = pygame.Rect(
            int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        
        win.blit(self.fruit_img, fruit_rect)
        
    def randomize(self):
        """Creates a new fruit on the surface randomly
        """
        self.x: int = random.randint(0, CELL_NUMBER - 1)
        self.y: int = random.randint(0, CELL_NUMBER - 1)
        self.pos: Vector2 = Vector2(self.x, self.y)


game: Game = Game(CELL_NUMBER, CELL_SIZE)
game.main()


