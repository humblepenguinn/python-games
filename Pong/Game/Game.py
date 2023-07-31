import pygame
import sys


class Game(object):
    WIDTH = 1680
    HEIGHT = 1050
    BORDER = 20
    VELOCITY = int(sys.argv[2])
    FRAMERATE = 60
    screen = pygame.display.set_mode((1680, 1050))
    pygame.display.set_caption("Pong")
    pygame.font.init()

    STAT_FONT = pygame.font.Font("bit5x3.ttf", 50)

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()

    def blit_text(self, p_score, model_score):
        text = self.STAT_FONT.render(f"{model_score}", 1, (255, 255, 255))
        self.screen.blit(text, (650, self.HEIGHT - 1000))
        text = self.STAT_FONT.render(f"{p_score}", 1, (255, 255, 255))
        self.screen.blit(text, (1000, self.HEIGHT - 1000))

    def main(self, ball, player, p_score, model, model_score, fgColor, bgColor):
        while True:
            self.clock.tick(self.FRAMERATE)

            e = pygame.event.poll()
            if e.type == pygame.QUIT:
                break

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    break

            self.screen.fill((0, 0, 0))
            pygame.draw.line(self.screen, (255, 255, 255), (830, self.HEIGHT - 1050), (830, self.HEIGHT))
            self.blit_text(p_score, model_score)

            model_score, p_score = ball.update(player, model, fgColor, bgColor, p_score, model_score)
            model.model_update(ball, bgColor, fgColor)
            player.update(ball, bgColor, fgColor)

            pygame.display.update()

        pygame.quit()
