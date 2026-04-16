import math

from lib.Primitivas import desenhar_poligono

def draw_ameba(superficie, cor, w, h):
    R = 100
    A = 10
    N = 20
    pontos_da_curva = gerar_pontos_curva(R, A, N, w, h)
    desenhar_poligono(superficie, pontos_da_curva, cor)

def gerar_pontos_curva(R, A, N, center_x, center_y, resolucao=1920):
    pontos = []
    for i in range(resolucao + 1):
        theta = (i / resolucao) * (2 * math.pi)
        raio_atual = R + A * math.sin(N * theta)
        x = raio_atual * math.cos(theta)
        y = raio_atual * math.sin(theta)
        ponto_x = center_x + x
        ponto_y = center_y - y

        pontos.append((ponto_x, ponto_y))

    return pontos
