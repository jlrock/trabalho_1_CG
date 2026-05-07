from lib.Preenchimento import *
import pygame

class Button:
    def __init__(self, superficie, center_x, center_y, width, height, cor, cor_borda, label, on_click=False):
        self.superficie=superficie
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.cor=cor
        self.cor_borda=cor_borda
        self.label=label
        self.on_click=on_click

    def draw(self):
        one_scanline(self.superficie, self.center_x-(self.width/2), self.center_x+(self.width/2), self.center_y-(self.height/2), self.cor_borda)
        one_scanline(self.superficie, self.center_x-(self.width/2), self.center_x+(self.width/2), self.center_y+(self.height/2), self.cor_borda)
        scan_column(self.superficie, self.center_y-(self.height/2), self.center_y+(self.height/2), self.center_x-(self.width/2), self.cor_borda)
        scan_column(self.superficie, self.center_y-(self.height/2), self.center_y+(self.height/2), self.center_x+(self.width/2), self.cor_borda)
        flood_fill(self.superficie, self.center_x, self.center_y, self.cor, self.cor_borda)
        fonte_texto = pygame.font.SysFont("Arial", 30)
        texto_botao = fonte_texto.render(self.label, True, (0,0,0))
        self.superficie.blit(texto_botao, (self.center_x-(texto_botao.get_width()/2), self.center_y- (texto_botao.get_height()/2)))