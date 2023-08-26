import pandas as pd
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import random
import threading as th
import time


class Auto:
    def __init__(self, x, y, velocidad, color, nombre, x_max=100, y_max=10):
        self.x = x
        self.y = y
        self.x_max = x_max
        self.velocidad = velocidad
        self.color = color
        self.nombre = nombre

        threading = th.Thread(target=self.acelerar, args=())
        threading.start()
        

    def acelerar(self):
        while self.x < self.x_max:
            acelerar = abs(random.lognormvariate(0.5, 0.1))
            self.velocidad = self.velocidad * acelerar
            time.sleep(0.5)

    def avanzar(self):
        self.x += self.velocidad

    def retroceder(self):
        self.x -= self.velocidad

    def __str__(self):
        return self.nombre
    

