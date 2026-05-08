from lib.Primitivas import desenhar_circulo, desenhar_poligono
from lib.Transformacoes import aplica_transformacao, translacao, multiplica_matrizes, escala
from lib.Preenchimento import scanline_fill, scanline_texture
import math

class Food:
    def __init__(self, id, pos_x, pos_y, radius: int = 10, color = (255, 0, 0), pulse_offset: float = 0, texture = None):
        self.id = id,
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.color = color
        self.pulse_offset = pulse_offset
        self.texture = texture
        
    def draw(self, surface, matriz_viewport, raio_tela=None, is_minimap: bool = False, animation = None):
        p_mundo = [(self.pos_x, self.pos_y)]
        p_tela = aplica_transformacao(matriz_viewport, p_mundo)
        tela_x, tela_y = p_tela[0]
        r = raio_tela if raio_tela is not None else self.radius
        if 0 <= tela_x <= surface.get_width() and 0 <= tela_y <= surface.get_height():
            if self.texture is None:
                desenhar_circulo(surface, int(tela_x), int(tela_y), r, self.color, is_minimap)
            else:
                velocidade = 30 
                novo_x = (self.pos_x + (animation * velocidade)) % surface.get_width()
                pontos_food_mundo = [
                    (novo_x - self.radius, self.pos_y - self.radius),
                    (novo_x + self.radius, self.pos_y - self.radius),
                    (novo_x + self.radius, self.pos_y + self.radius),
                    (novo_x - self.radius, self.pos_y + self.radius),
                ]
                pontos_tela = aplica_transformacao(matriz_viewport, pontos_food_mundo)
                scanline_texture(
                    surface, 
                    pontos_tela, 
                    [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)], 
                    self.texture, 
                    self.texture.get_width(), 
                    self.texture.get_height()
                )
                
def draw_menu_food(screen, menu_food, animation):
    for food in menu_food:
        fator_escala = 1.0 + (math.sin(animation * 0.10 + food.pulse_offset) * 0.3)
        matriz_ida = translacao(-food.pos_x, -food.pos_y)
        matriz_esc = escala(fator_escala, fator_escala)   
        matriz_volta = translacao(food.pos_x, food.pos_y)
        m_temp = multiplica_matrizes(matriz_esc, matriz_ida)
        matriz_animacao = multiplica_matrizes(matriz_volta, m_temp)
        pontos_originais = gerar_pontos_circulo(food.pos_x, food.pos_y, food.radius, resolucao=20)        
        pontos_transformados = aplica_transformacao(matriz_animacao, pontos_originais)
        desenhar_poligono(screen, pontos_transformados, food.color)
        scanline_fill(screen, pontos_transformados, food.color)

def gerar_pontos_circulo(xc, yc, raio, resolucao=30):
    pontos = []
    for i in range(resolucao):
        angulo = (i / resolucao) * (2 * math.pi)
        
        x = xc + raio * math.cos(angulo)
        y = yc + raio * math.sin(angulo)
        
        pontos.append((x, y))
        
    return pontos