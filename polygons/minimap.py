from lib.Preenchimento import scanline_fill_gradiente
from lib.Primitivas import desenhar_poligono

def draw_minimap(WIDTH, MINIMAPA_W, MINIMAPA_H, screen, padding):
    x_min = WIDTH - MINIMAPA_W - padding
    y_min = padding
    x_max = WIDTH - padding
    y_max = MINIMAPA_H + padding
    
    pontos_fundo_minimapa = [
        (x_min, y_min),
        (x_max, y_min), 
        (x_max, y_max), 
        (x_min, y_max)
    ]
    
    cor_topo = (60, 60, 70)
    cor_base = (10, 10, 15)
    cores_fundo_minimapa = [
        cor_topo,
        cor_topo, 
        cor_base,
        cor_base  
    ]

    scanline_fill_gradiente(screen, pontos_fundo_minimapa, cores_fundo_minimapa)
    desenhar_poligono(screen, pontos_fundo_minimapa, (150, 150, 150))