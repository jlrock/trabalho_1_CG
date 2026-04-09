import math
import numpy as np

def identidade():
    matriz = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
        ])
    return matriz 

def translacao(tx, ty):
    matriz = np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
        ])
    return matriz

def escala(sx, sy):
    matriz = np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
        ])
    return matriz 

def rotacao(theta):
    theta_rad = math.radians(theta)
    c = math.cos(theta_rad)
    s = math.sin(theta_rad)
    matriz = np.array([
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1]
        ])
    return matriz 
