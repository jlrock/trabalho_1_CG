from lib.Motor_grafico import setPixel

def reta_dda(superficie, x0, y0, x1, y1, cor):
    dx = x1 - x0
    dy = y1 - y0

    passos = max(abs(dx), abs(dy))

    if passos == 0:
        setPixel(superficie, x0, y0, cor)
        return

    x_inc = dx / passos
    y_inc = dy / passos

    x = x0
    y = y0

    for _ in range(passos + 1):
        setPixel(superficie, round(x), round(y), cor)
        x += x_inc
        y += y_inc


def reta_bresenham(superficie, x0, y0, x1, y1, cor):
    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0

    ystep = 1
    if dy < 0:
        ystep = -1
        dy = -dy

    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    x = x0
    y = y0

    while x <= x1:
        if steep:
            setPixel(superficie, y, x, cor)
        else:
            setPixel(superficie, x, y, cor)

        if d <= 0:
            d += incE
        else:
            d += incNE
            y += ystep

        x += 1

def desenhar_poligono(superficie, pontos, cor_borda):
    n = len(pontos)
    for i in range(n):
        x0, y0 = pontos[i]
        x1, y1 = pontos[(i + 1) % n]
        reta_bresenham(superficie, x0, y0, x1, y1, cor_borda)
