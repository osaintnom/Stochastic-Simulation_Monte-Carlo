import pandas as pd
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


class Auto:
    def __init__(self, x, y, velocidad, color, nombre):
        self.x = x
        self.y = y
        self.velocidad = velocidad
        self.color = color
        self.nombre = nombre

    def avanzar(self):
        self.x += self.velocidad

    def retroceder(self):
        self.x -= self.velocidad

    def __str__(self):
        return self.nombre
    

