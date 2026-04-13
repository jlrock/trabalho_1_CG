import pygame
import sys

def iniciar():
    pygame.init()

def sair():
    pygame.quit()
    sys.exit()

def criar_tela(largura, altura):
    tela = pygame.display.set_mode((largura, altura))
    return tela

def nomear_tela(nome):
    pygame.display.set_caption(str(nome))

def setPixel(superficie, x, y, cor):
    if 0 <= x < superficie.get_width() and 0 <= y < superficie.get_height():
        superficie.set_at((x, y), cor)

def criar_clock():
    clock = pygame.time.Clock()
    return clock

def flipar_tela():
    pygame.display.flip()