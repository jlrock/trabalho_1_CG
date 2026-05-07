from lib.Primitivas import desenhar_circulo
from lib.Transformacoes import aplica_transformacao

class Food:
    def __init__(self, id, pos_x, pos_y, radius: int = 10, color = (255, 0, 0)):
        self.id = id,
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.color = color
        
    def draw(self, surface, matriz_viewport, raio_tela=None, is_minimap: bool = False):
        p_mundo = [(self.pos_x, self.pos_y)]
        p_tela = aplica_transformacao(matriz_viewport, p_mundo)
        tela_x, tela_y = p_tela[0]
        r = raio_tela if raio_tela is not None else self.radius
        if 0 <= tela_x <= surface.get_width() and 0 <= tela_y <= surface.get_height():
            desenhar_circulo(surface, int(tela_x), int(tela_y), r, self.color, is_minimap)