import sys
import pygame
import math
import pyautogui
import random
from polygons.ameba import draw_ameba
from utils.capture_key import capture_key
from polygons.food import Food
from lib import *
from polygons.ameba import gerar_pontos_curva

WIDTH, HEIGHT = pyautogui.size()

MUNDO_W, MUNDO_H = (2000,2000)
MINIMAPA_W, MINIMAPA_H = (200, 200)

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

food_list: Food = []
for i in range(20):
    random_x = random.randint(0, WIDTH)
    random_y = random.randint(0, HEIGHT)
    new_food = Food(i, random_x, random_y)
    food_list.append(new_food)
    
def draw_ameba_com_camera(superficie, cores, mundo_x, mundo_y, r, animation, matriz_camera):
    animated_r = r + math.sin(animation / 20) * (r * 0.05)
    
    pontos_locais = gerar_pontos_curva(animated_r, 0, 0, animation)

    matriz_objeto = cria_transformacao()
    matriz_objeto = multiplica_matrizes(translacao(mundo_x, mundo_y), matriz_objeto)
    
    matriz_final = multiplica_matrizes(matriz_camera, matriz_objeto)
    pontos_tela = aplica_transformacao(matriz_final, pontos_locais)

    desenhar_poligono(superficie, pontos_tela, cores[0])
    scanline_fill_gradiente(superficie, pontos_tela, [cores[0]] * len(pontos_tela))
    
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        ameba_pos_x, ameba_pos_y = capture_key(ameba_pos_x, ameba_pos_y, ameba_speed, normalized_diagonal_speed)
    
    janela_principal = (ameba_pos_x - (WIDTH / 2), ameba_pos_y - (HEIGHT / 2), ameba_pos_x + (WIDTH / 2), ameba_pos_y + (HEIGHT / 2))
    viewport_principal = (0, 0, WIDTH, HEIGHT)
    matriz_camera_principal = janela_viewport(janela_principal, viewport_principal)
    
    janela_minimapa = (0, 0, MUNDO_W, MUNDO_H)
    viewport_minimapa = (WIDTH - MINIMAPA_W, 0, WIDTH, MINIMAPA_H)
    matriz_camera_minimapa = janela_viewport(janela_minimapa, viewport_minimapa)

    screen.fill((100, 100, 100))
    
    for food in food_list:
        p_mundo = [(food.pos_x, food.pos_y)]
        p_tela = aplica_transformacao(matriz_camera_principal, p_mundo)
        
        if 0 <= p_tela[0][0] <= WIDTH and 0 <= p_tela[0][1] <= HEIGHT:
            desenhar_circulo(screen, p_tela[0][0], p_tela[0][1], 10, (255, 0, 0))

    draw_ameba_com_camera(screen, [(0,255,100), (0,255,0)], ameba_pos_x, ameba_pos_y, ameba_r, animation, matriz_camera_principal)
    
    area_minimapa = pygame.Rect(WIDTH - MINIMAPA_W, 0, MINIMAPA_W, MINIMAPA_H)
    pygame.draw.rect(screen, (30, 30, 30), area_minimapa)
    for food in food_list:
        p_mundo = [(food.pos_x, food.pos_y)]
        p_tela = aplica_transformacao(matriz_camera_minimapa, p_mundo)
        desenhar_circulo(screen, p_tela[0][0], p_tela[0][1], 2, (255, 0, 0))

    p_ameba = [(ameba_pos_x, ameba_pos_y)]
    p_ameba_radar = aplica_transformacao(matriz_camera_minimapa, p_ameba)
    desenhar_circulo(screen, p_ameba_radar[0][0], p_ameba_radar[0][1], 4, (0, 255, 100))

    comidas_sobreviventes = []
    for food in food_list:
        dx = ameba_pos_x - food.pos_x
        dy = ameba_pos_y - food.pos_y
        distancia_quadrada = (dx * dx) + (dy * dy)
        distancia_colisao_quadrada = (ameba_r + food.raio) ** 2

        if distancia_quadrada < distancia_colisao_quadrada:
            ameba_r += 5
        else:
            comidas_sobreviventes.append(food)
    food_list = comidas_sobreviventes

    animation+=1
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()