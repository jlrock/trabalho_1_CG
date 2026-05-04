from lib.Preenchimento import scanline_fill_gradiente, scanline_texture
from lib.Primitivas import desenhar_poligono_recortado
import pygame

def draw_minimap(WIDTH, MINIMAPA_W, MINIMAPA_H, screen, padding, minimap_bg):
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
    
    uvs_minimapa = [
        (0.0, 0.0),
        (1.0, 0.0),
        (1.0, 1.0),
        (0.0, 1.0) 
    ]
    
    tex_w = minimap_bg.get_width()
    tex_h = minimap_bg.get_height()

    scanline_fill_gradiente(screen, pontos_fundo_minimapa, [(70,70,70),(70,70,70),(0,143,127),(0,143,127)])
    scanline_texture(screen, pontos_fundo_minimapa, uvs_minimapa, minimap_bg, tex_w, tex_h)
    desenhar_poligono_recortado(screen, pontos_fundo_minimapa, (x_min, y_min, x_max, y_max), (150, 150, 150))
    
    return (x_min, y_min, x_max, y_max)