import pygame
import math

def capture_key(ameba_pos_x, ameba_pos_y, ameba_speed):
    normalized_diagonal_speed = 1/math.sqrt(2*math.pow(ameba_speed, 2))
    keys = pygame.key.get_pressed()
    key_pressed_up = keys[pygame.K_UP] or keys[pygame.K_w]
    key_pressed_down = keys[pygame.K_DOWN] or keys[pygame.K_s]
    key_pressed_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
    key_pressed_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
    pressed_single_key = True
    
    if key_pressed_up and key_pressed_left:
        ameba_pos_y-=normalized_diagonal_speed
        ameba_pos_x-=normalized_diagonal_speed
        pressed_single_key = False
    if key_pressed_up and key_pressed_right:
        ameba_pos_y-=normalized_diagonal_speed
        ameba_pos_x+=normalized_diagonal_speed
        pressed_single_key = False
    if key_pressed_down and key_pressed_left:
        ameba_pos_y+=normalized_diagonal_speed
        ameba_pos_x-=normalized_diagonal_speed
        pressed_single_key = False
    if key_pressed_down and key_pressed_right:
        ameba_pos_y+=normalized_diagonal_speed
        ameba_pos_x+=normalized_diagonal_speed
        pressed_single_key = False

    if pressed_single_key:
        if key_pressed_up:
            ameba_pos_y-=ameba_speed
        if key_pressed_down:
            ameba_pos_y+=ameba_speed
        if key_pressed_left:
            ameba_pos_x-=ameba_speed
        if key_pressed_right:
            ameba_pos_x+=ameba_speed
            
    if(ameba_pos_x < 0):
        ameba_pos_x = 0;
    if(ameba_pos_x > 2000):
        ameba_pos_x = 2000;
    if(ameba_pos_y < 0):
        ameba_pos_y = 0;
    if(ameba_pos_y > 2000):
        ameba_pos_y = 2000;
        
    return ameba_pos_x,ameba_pos_y