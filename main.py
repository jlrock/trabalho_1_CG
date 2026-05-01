import sys
import pygame
import math
import pyautogui
import random
from polygons.ameba import draw_ameba
from utils.capture_key import capture_key
from polygons.food import Food

WIDTH, HEIGHT = pyautogui.size()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()
running = True
pygame.key.set_repeat(1, 5)

ameba_pos_x = WIDTH / 2
ameba_pos_y = HEIGHT / 2
ameba_r = 100
ameba_speed = 1
animation = 0
normalized_diagonal_speed = 1/math.sqrt(2*math.pow(ameba_speed, 2))

food_list: Food = []
for i in range(10):
    random_x = random.randint(0, WIDTH)
    random_y = random.randint(0, HEIGHT)
    new_food = Food(i, random_x, random_y)
    food_list.append(new_food)
    
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        ameba_pos_x, ameba_pos_y = capture_key(ameba_pos_x, ameba_pos_y, ameba_speed, normalized_diagonal_speed)

    screen.fill((255, 255, 255))
    draw_ameba(screen, (0,0,0), ameba_pos_x, ameba_pos_y, ameba_r, animation)
    animation+=1
    
    for food in food_list:
        food.draw(screen, (255,0,0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
