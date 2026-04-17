import sys
import pygame
import math
from polygons.ameba import draw_ameba
from utils.capture_key import capture_key

HEIGHT = 1000
WIDTH = 1000

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()
running = True
pygame.key.set_repeat(1, 5)

ameba_pos_x = WIDTH / 2
ameba_pos_y = HEIGHT / 2
ameba_r = 10
ameba_speed = 1
animation = 0
normalized_diagonal_speed = 1/math.sqrt(2*math.pow(ameba_speed, 2))
    
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        ameba_pos_x, ameba_pos_y = capture_key(ameba_pos_x, ameba_pos_y, ameba_speed, normalized_diagonal_speed)

    screen.fill((255, 255, 255))
    draw_ameba(screen, (0,0,0), ameba_pos_x, ameba_pos_y, ameba_r, animation)
    animation+=1

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
