from lib.Primitivas import desenhar_poligono
from lib.Preenchimento import scanline_fill
import math
from lib.Transformacoes import rotacao, translacao, multiplica_matrizes, aplica_transformacao

def draw_menu_ameba(screen, WIDTH, HEIGHT, animation):
    pontos_locais = gerar_pontos_elipse(400, 350)    
    matriz_rot = rotacao(animation * 2.0) 
    matriz_trans = translacao(WIDTH / 2, HEIGHT / 2)    
    matriz_final = multiplica_matrizes(matriz_trans, matriz_rot)    
    pontos_tela = aplica_transformacao(matriz_final, pontos_locais)
    desenhar_poligono(screen, pontos_tela, (0, 255, 100))


def gerar_pontos_elipse(rx, ry, resolucao=60):
    pontos = []
    for i in range(resolucao):
        angulo = (i / resolucao) * (2 * math.pi)
        
        x = rx * math.cos(angulo)
        y = ry * math.sin(angulo)
        
        pontos.append((x, y))
    return pontos