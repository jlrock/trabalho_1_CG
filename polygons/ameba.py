import math
from lib.Primitivas import desenhar_poligono
from lib.Preenchimento import scanline_fill_gradiente, scanline_fill
from lib.Transformacoes import cria_transformacao, multiplica_matrizes,aplica_transformacao,translacao
    
def draw_ameba_with_camera(superficie, cores, mundo_x, mundo_y, r, animation, matriz_camera):
    animated_r = r + math.sin(animation / 20) * (r * 0.05)
    pontos_locais = gerar_pontos_curva(animated_r, 0, 0, animation)
    matriz_objeto = cria_transformacao()
    matriz_objeto = multiplica_matrizes(translacao(mundo_x, mundo_y), matriz_objeto)
    matriz_final = multiplica_matrizes(matriz_camera, matriz_objeto)
    pontos_tela = aplica_transformacao(matriz_final, pontos_locais)
    desenhar_poligono(superficie, pontos_tela, cores[0])
    scanline_fill_gradiente(superficie, pontos_tela, [cores[0]] * len(pontos_tela))

def gerar_pontos_curva(R, center_x, center_y, animation, resolucao=150):
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
