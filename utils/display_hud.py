from polygons.ameba import Ameba

def display_hud(ameba: Ameba, ameba_max_radius, time,screen, WIDTH, game_font) :
    size_label_surface = game_font.render(("Size: " + str(ameba.radius-10) + "/" + str(ameba_max_radius)), True, (0,240,127))
    screen.blit(size_label_surface, (WIDTH-210, 210))
    timer_label_surface = game_font.render(("Time: " + str(time)), True, (0,240,127))
    screen.blit(timer_label_surface, (WIDTH-210, 250))