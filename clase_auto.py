import pandas as pd
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import random
import threading as th
import time


class Auto:
    def __init__(self, x, y, velocidad, color, nombre, x_max=1000, y_max=10,next_car=None):
        self.x = x
        self.y = y
        self.x_max = x_max
        self.velocidad = velocidad
        self.color = color
        self.nombre = nombre
        self.next_car = next_car

        threading = th.Thread(target=self.acelerar, args=())
        threading.start()
        

    def acelerar(self):
        while self.x < self.x_max:
            acelerar = abs(random.uniform(0, 3))
            self.velocidad = self.velocidad * acelerar
            if self.velocidad < 0.5:
                self.velocidad = 1
            time.sleep(0.5)


    def avanzar(self):
        if self.velocidad == 0:
            self.velocidad = 2
        try:
            if self.x >= self.next_car.x -4:
                self.velocidad = 0
            elif self.x >= self.next_car.x - 10:
                self.x += self.velocidad /4  
            else:
                self.x += self.velocidad
        except:
            self.x += self.velocidad

    def retroceder(self):
        self.x -= self.velocidad

    def __str__(self):
        return self.nombre
    

