import math
from lib.Primitivas import *

def draw_ameba(superficie, cor, w, h, r, animation):
    animated_r = r + math.sin(animation / 20) * (r * 0.05)
    pontos_da_curva = gerar_pontos_curva(animated_r, w, h, animation)
    desenhar_poligono(superficie, pontos_da_curva, cor)

def gerar_pontos_curva(R, center_x, center_y, animation, resolucao=200):
    pontos = []
    for i in range(resolucao + 1):
        theta = (i / resolucao) * (2 * math.pi)
        onda1 = math.sin(2 * theta + animation * 0.020) * (R * 0.08) 
        onda2 = math.cos(3 * theta - animation * 0.015) * (R * 0.05) 
        onda3 = math.sin(5 * theta + animation * 0.030) * (R * 0.03) 
        onda4 = math.cos(7 * theta - animation * 0.025) * (R * 0.01) 
        
        raio_atual = R + onda1 + onda2 + onda3 + onda4
        x = raio_atual * math.cos(theta)
        y = raio_atual * math.sin(theta)
        ponto_x = center_x + x
        ponto_y = center_y - y

        pontos.append((ponto_x, ponto_y))

    return pontos
