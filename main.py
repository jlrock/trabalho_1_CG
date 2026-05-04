import sys
import pygame
import pyautogui
import random
from polygons.ameba import Ameba
from utils.capture_key import capture_key
from polygons.food import Food
from lib import *
from polygons.minimap import draw_minimap

WIDTH, HEIGHT = pyautogui.size()

MUNDO_W, MUNDO_H = (2000,2000)
MINIMAPA_W, MINIMAPA_H = (200, 200)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()
running = True
pygame.key.set_repeat(1, 5)
animation = 0

ameba = Ameba(10, 1, WIDTH/2, HEIGHT/2, (0,255,100))

food_list: Food = []
for i in range(20):
    random_x = random.randint(0, WIDTH)
    random_y = random.randint(0, HEIGHT)
    new_food = Food(i, random_x, random_y)
    food_list.append(new_food)

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.key.get_pressed()[pygame.K_q]:
            running = False
        
        ameba.pos_x, ameba.pos_y = capture_key(ameba.pos_x, ameba.pos_y, ameba.speed)
    
    janela_principal = (ameba.pos_x - (WIDTH / 2), ameba.pos_y - (HEIGHT / 2), ameba.pos_x + (WIDTH / 2), ameba.pos_y + (HEIGHT / 2))
    viewport_principal = (0, 0, WIDTH, HEIGHT)
    matriz_camera_principal = janela_viewport(janela_principal, viewport_principal)
    
    padding = 10
    janela_minimapa = (0, 0, MUNDO_W, MUNDO_H)
    viewport_minimapa = (WIDTH - MINIMAPA_W-padding, padding, WIDTH-padding, MINIMAPA_H+padding)
    matriz_camera_minimapa = janela_viewport(janela_minimapa, viewport_minimapa)

    screen.fill((100, 100, 100))
    for food in food_list:
        food.draw(screen, (255, 0, 0), matriz_camera_principal)
    ameba.draw(screen, animation, matriz_camera_principal)
    
    minimap_constraints = draw_minimap(WIDTH, HEIGHT, MINIMAPA_W, MINIMAPA_H, screen, padding)
    for food in food_list:
        food.draw(screen, (255, 0, 0), matriz_camera_minimapa, raio_tela=1)
    ameba.draw(screen, animation, matriz_camera_minimapa, is_minimap=True, janela_recorte=minimap_constraints)

    comidas_sobreviventes = []
    for food in food_list:
        dx = ameba.pos_x - food.pos_x
        dy = ameba.pos_y - food.pos_y
        distancia_quadrada = (dx * dx) + (dy * dy)
        distancia_colisao_quadrada = (ameba.radius + food.raio) ** 2

        if distancia_quadrada < distancia_colisao_quadrada:
            ameba.radius += 5
        else:
            comidas_sobreviventes.append(food)
            
    food_list = comidas_sobreviventes
    animation+=1
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()