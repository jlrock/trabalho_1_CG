import sys
import pygame
import pyautogui
import random
from polygons.ameba import Ameba
from utils.capture_key import capture_key
from utils.display_hud import display_hud
from polygons.food import Food, draw_menu_food
from polygons.button import Button
from lib import *
from polygons.minimap import draw_minimap
from polygons.menu_ameba import draw_menu_ameba

WIDTH, HEIGHT = pyautogui.size()
MUNDO_W, MUNDO_H = (2000,2000)
MINIMAPA_W, MINIMAPA_H = (200, 200)
MAX_TIME: int = 50

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()
running = True
pygame.key.set_repeat(1, 5)
game_font = pygame.font.SysFont('Arial', 32)
menu_font = pygame.font.SysFont('Arial', 50)
animation = 0
minimap_bg = pygame.image.load("assets/minimap_bg.png").convert_alpha()
map_bg = pygame.image.load("assets/map_bg.jpg")
time = 0
game_mode: str = "menu"
player_status: str = ""

ameba = Ameba(10, 1, WIDTH/2, HEIGHT/2, (0,255,100))
ameba_max_radius: int = 0

food_list: Food = []
food_colors = [(255,0,0),(238,255,0),(255,0,230)]
menu_food_list = []
for i in range(30):
    rand_x = random.randint(50, WIDTH-50)
    rand_y = random.randint(50, HEIGHT-50)
    rand_radius = random.randint(10, 30)
    rand_r = random.randint(0, 255)
    rand_g = random.randint(0, 255)
    rand_b = random.randint(0, 255)
    new_food = Food(i, rand_x, rand_y, rand_radius, (rand_r, rand_g, rand_b))
    new_food.pulse_offset = random.uniform(0, math.pi * 2)     
    menu_food_list.append(new_food)
end_food_list = []
food_textures =[pygame.image.load("assets/apple.png").convert_alpha(), pygame.image.load("assets/cookie.png").convert_alpha(), pygame.image.load("assets/hamburguer.png").convert_alpha()]
for i in range(10):
    rand_x = random.randint(50, WIDTH-50)
    rand_y = random.randint(50, HEIGHT-50)
    rand_radius = random.randint(10, 30)
    rand_texture = random.randrange(0,3,1)
    new_food = Food(i, rand_x, rand_y, rand_radius, texture=food_textures[rand_texture])
    end_food_list.append(new_food)

while running:
    dt_time = clock.tick(60)/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.key.get_pressed()[pygame.K_q]:
            running = False
        if game_mode != "game" and pygame.key.get_pressed()[pygame.K_SPACE]:
            time = 0
            player_status = ""
            ameba = Ameba(10, 1, WIDTH/2, HEIGHT/2, (0,255,100))
            ameba_max_radius = 0
            food_list.clear()
            for i in range(20):
                random_x = random.randint(0, MUNDO_W)
                random_y = random.randint(0, MUNDO_H)
                randint = random.randrange(10,31,10)
                new_food = Food(i, random_x, random_y, randint, food_colors[int((randint/10)-1)])
                food_list.append(new_food)
                ameba_max_radius += (new_food.radius//3)
            game_mode = "game"
        if game_mode == "end" and pygame.key.get_pressed()[pygame.K_m]:
            game_mode = "menu"
        if game_mode == "menu" and pygame.key.get_pressed()[pygame.K_r]:
            game_mode = "rules"
        if game_mode == "rules" and pygame.key.get_pressed()[pygame.K_m]:
            game_mode = "menu"
        if game_mode == "game":
            ameba.pos_x, ameba.pos_y = capture_key(ameba.pos_x, ameba.pos_y, ameba.speed)

    screen.fill((100, 100, 100))
        
    if game_mode == "menu":
        draw_menu_food(screen, menu_food_list, animation)
        draw_menu_ameba(screen, WIDTH, HEIGHT, animation)
        rules_button = Button(screen, (WIDTH/2), HEIGHT-200, 350, 40, (255,255,0), (255,255,0), "View Rules [R]")
        rules_button.draw()
        title_label = menu_font.render("Mebaformers", True, (0,255,100))
        screen.blit(title_label, ((WIDTH/2)-(title_label.get_width()/2), (HEIGHT/2)-(title_label.get_height()/2)))
        bresenham(screen, WIDTH/3+150,(HEIGHT/2)+30, (WIDTH/3)+490,(HEIGHT/2)+30, (0,255,100))
        
    if game_mode == "game":
        janela_principal = (ameba.pos_x - (WIDTH / 2), ameba.pos_y - (HEIGHT / 2), ameba.pos_x + (WIDTH / 2), ameba.pos_y + (HEIGHT / 2))
        viewport_principal = (0, 0, WIDTH, HEIGHT)
        matriz_camera_principal = janela_viewport(janela_principal, viewport_principal)
        
        padding = 10
        janela_minimapa = (0, 0, MUNDO_W, MUNDO_H)
        viewport_minimapa = (WIDTH - MINIMAPA_W-padding, padding, WIDTH-padding, MINIMAPA_H+padding)
        matriz_camera_minimapa = janela_viewport(janela_minimapa, viewport_minimapa)
    
        pontos_borda_tela = aplica_transformacao(matriz_camera_principal, [(0,0),(MUNDO_W,0), (MUNDO_W,MUNDO_H), (0, MUNDO_H)])
        desenhar_poligono_recortado(screen, pontos_borda_tela, (0,0,MUNDO_W,MUNDO_H), (255,255,255))
        for food in food_list:
            dist_x = abs(ameba.pos_x - food.pos_x)
            dist_y = abs(ameba.pos_y - food.pos_y)
            
            limite_x = (WIDTH / 2) + food.radius + 50
            limite_y = (HEIGHT / 2) + food.radius + 50
            
            if dist_x < limite_x and dist_y < limite_y:
                food.draw(screen, matriz_camera_principal)
        ameba.draw(screen, animation, matriz_camera_principal)
        
        minimap_constraints = draw_minimap(WIDTH, MINIMAPA_W, MINIMAPA_H, screen, padding, minimap_bg)
        for food in food_list:
            food.draw(screen, matriz_camera_minimapa, food.radius/10, is_minimap=True)
        ameba.draw(screen, animation, matriz_camera_minimapa, is_minimap=True, janela_recorte=minimap_constraints) 
    
        comidas_sobreviventes = []
        for food in food_list:
            dx = ameba.pos_x - food.pos_x
            dy = ameba.pos_y - food.pos_y
            distancia_quadrada = (dx * dx) + (dy * dy)
            distancia_colisao_quadrada = (ameba.radius + food.radius) ** 2
    
            if distancia_quadrada < distancia_colisao_quadrada:
                ameba.radius += (food.radius//3)
            else:
                comidas_sobreviventes.append(food)
                
        food_list = comidas_sobreviventes
        if len(food_list) > 0 and time <= MAX_TIME:
            time+=dt_time
            time = round(time, 3)
        
        if len(food_list) == 0 and time <= MAX_TIME:
            game_mode = "end"
            player_status = "won"
        
        if time > MAX_TIME and len(food_list) > 0:
            game_mode = "end"
            player_status = "lost"
        
        display_hud(ameba, ameba_max_radius, time, screen, WIDTH, game_font)
        
    if game_mode == "menu" or game_mode == "end" or game_mode == "rules":
        play_button = Button(screen, (WIDTH/2)-200, HEIGHT-100, 200, 40, (255,255,0), (255,255,0), "Play [Space]")
        play_button.draw()
        quit_button = Button(screen, (WIDTH/2) + 200, HEIGHT-100, 200, 40, (255,255,0), (255,255,0), "Quit [Q]")
        quit_button.draw()
    
    if game_mode == "end":
        for food in end_food_list:
            food.draw(screen, identidade(), animation=animation)
        size_label = game_font.render("Size: " + str(ameba.radius-10) + "/" + str(ameba_max_radius), True, (255,255,255))
        screen.blit(size_label, ((WIDTH/2)-(size_label.get_width()/2), 200))
        menu_button = Button(screen, (WIDTH/2), HEIGHT-200, 200, 40, (255,255,0), (255,255,0), "Menu [M]")
        menu_button.draw()
        if player_status == "won":
            final_label = game_font.render("You Won!", True, (255,255,0))
            time_label = game_font.render("Your time: " + str(time), True, (255,255,255))
            screen.blit(final_label, ((WIDTH/2)-(final_label.get_width()/2), 100))
            screen.blit(time_label, ((WIDTH/2)-(time_label.get_width()/2), 150))
        if player_status == "lost":
            final_label = game_font.render("You Lost!", True, (255,0,0))
            time_label = game_font.render("Your time is up!", True, (255,255,255))
            screen.blit(final_label, ((WIDTH/2)-(final_label.get_width()/2), 100))
            screen.blit(time_label, ((WIDTH/2)-(time_label.get_width()/2), 150))
            
    if game_mode == "rules":
        rules_tile = game_font.render("Rules ", True, (255,255,0))
        rules_labels = game_font.render("1. Ameba has to eat all food before time ends.\n2. Max time is 50s.", True, (255,255,255))
        screen.blit(rules_tile, ((WIDTH/2)-(rules_tile.get_width()/2), 200))
        screen.blit(rules_labels, ((WIDTH/2)-(rules_labels.get_width()/2),250))
        return_button = Button(screen, (WIDTH/2), HEIGHT-200, 350, 40, (255,255,0), (255,255,0), "Return to Mein Menu [M]")
        return_button.draw()

    animation+=1
    pygame.display.flip()

pygame.quit()
sys.exit()