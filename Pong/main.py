import pygame
from Game.Game import Game
from Game.Ball import Ball
from Game.Paddle import Paddle

bgColor = pygame.Color("black")
fgColor = pygame.Color("white")

if __name__ == "__main__":
    p_score = 0
    model_score = 0

    ball = Ball(Game.WIDTH // 2, Game.HEIGHT // 2, -Game.VELOCITY, -Game.VELOCITY)
    player = Paddle(Game.WIDTH - Paddle.WIDTH - 180, Game.HEIGHT // 2)
    model = Paddle(180, Game.HEIGHT // 2)

    Game.screen.fill(bgColor)

    ball.draw(fgColor)
    player.draw(fgColor)
    model.draw(fgColor)

    game = Game()
    game.main(ball, player, p_score, model, model_score, fgColor, bgColor)
