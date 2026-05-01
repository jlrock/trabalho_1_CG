from lib.Primitivas import *

class Food:
    def __init__(self, id, pos_x, pos_y):
        self.id = id,
        self.pos_x = pos_x
        self.pos_y = pos_y
        
    def draw(self, surface, color):
        desenhar_circulo(surface, self.pos_x, self.pos_y, 10, color)