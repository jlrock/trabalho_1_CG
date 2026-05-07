import math
from lib.Primitivas import desenhar_poligono, desenhar_poligono_recortado
from lib.Preenchimento import scanline_fill
from lib.Transformacoes import cria_transformacao, multiplica_matrizes,aplica_transformacao,translacao

RESOLUCAO_PADRAO = 150
_THETAS = [(i / RESOLUCAO_PADRAO) * (2 * math.pi) for i in range(RESOLUCAO_PADRAO + 1)]

_SIN_T = [math.sin(t) for t in _THETAS]
_COS_T = [math.cos(t) for t in _THETAS]

_SIN_2T = [math.sin(2 * t) for t in _THETAS]
_COS_2T = [math.cos(2 * t) for t in _THETAS]

_SIN_3T = [math.sin(3 * t) for t in _THETAS]
_COS_3T = [math.cos(3 * t) for t in _THETAS]

_SIN_5T = [math.sin(5 * t) for t in _THETAS]
_COS_5T = [math.cos(5 * t) for t in _THETAS]

_SIN_7T = [math.sin(7 * t) for t in _THETAS]
_COS_7T = [math.cos(7 * t) for t in _THETAS]
class Ameba():
    def __init__(self, radius, speed, pos_x, pos_y, color):
        self.radius = radius
        self.speed = speed
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
    
    def draw(self, superficie, animation, matriz_camera, is_minimap=False, janela_recorte=None):
        animated_r = self.radius + math.sin(animation/5) * (self.radius * 0.05)

        pontos_locais = gerar_pontos_curva(animated_r, 0, 0, animation)
        
        matriz_objeto = cria_transformacao()
        matriz_objeto = multiplica_matrizes(translacao(self.pos_x, self.pos_y), matriz_objeto)
        matriz_final = multiplica_matrizes(matriz_camera, matriz_objeto)
        
        pontos_tela = aplica_transformacao(matriz_final, pontos_locais)
        
        if is_minimap:
            if janela_recorte is not None:
                desenhar_poligono_recortado(superficie, pontos_tela, janela_recorte, self.color)
        else:
            desenhar_poligono(superficie, pontos_tela, self.color)
            scanline_fill(superficie, pontos_tela, self.color)

def gerar_pontos_curva(R, center_x, center_y, animation, resolucao=RESOLUCAO_PADRAO):
    pontos = []
    
    a1, a2 = animation * 0.020, animation * 0.015
    a3, a4 = animation * 0.030, animation * 0.025
    
    cos_a1, sin_a1 = math.cos(a1), math.sin(a1)
    cos_a2, sin_a2 = math.cos(a2), math.sin(a2)
    cos_a3, sin_a3 = math.cos(a3), math.sin(a3)
    cos_a4, sin_a4 = math.cos(a4), math.sin(a4)
    
    R1, R2 = R * 0.08, R * 0.05
    R3, R4 = R * 0.03, R * 0.01

    for i in range(resolucao + 1):
        
        onda1 = (_SIN_2T[i] * cos_a1 + _COS_2T[i] * sin_a1) * R1
        onda2 = (_COS_3T[i] * cos_a2 + _SIN_3T[i] * sin_a2) * R2
        onda3 = (_SIN_5T[i] * cos_a3 + _COS_5T[i] * sin_a3) * R3
        onda4 = (_COS_7T[i] * cos_a4 + _SIN_7T[i] * sin_a4) * R4
        
        raio_atual = R + onda1 + onda2 + onda3 + onda4
        
        x = center_x + raio_atual * _COS_T[i]
        y = center_y - raio_atual * _SIN_T[i]

        pontos.append((x, y))

    return pontos
