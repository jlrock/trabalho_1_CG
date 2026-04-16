import sys
import pygame
from polygons.ameba import draw_ameba

HEIGHT = 400
WIDTH = 700

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()
running = True

ameba_pos_x = WIDTH / 2
ameba_pos_y = HEIGHT / 2

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    draw_ameba(screen, (0,0,0), ameba_pos_x, ameba_pos_y)
    ameba_pos_x+=0.5


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
