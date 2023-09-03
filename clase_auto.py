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
        self.y = y # por ahora no hace nada pero seria como cambiar de carril
        self.x_max = x_max  # marca donde termina la ruta
        self.velocidad = velocidad
        self.color = color # abria que aprender a usar esto para que se vea mas lindo
        self.nombre = nombre # inutil pero qsy despues puede servir
        self.next_car = next_car 
         
        # agregar velocidad maxima?

        # Genera un hilo para acelerar el auto
        threading = th.Thread(target=self.acelerar, args=())
        threading.start()
        

    def acelerar(self):
        while self.x < self.x_max:
            #aceleracion aleatoria sobre la velocidad del auto
            acelerar = abs(random.uniform(0, 3))
            self.velocidad = self.velocidad * acelerar

            #velocidad minima
            if self.velocidad < 0.5:
                self.velocidad = 1
            time.sleep(0.5)


    def avanzar(self):
        # si chocaste y frenaste, volves a arrancar
        if self.velocidad == 0:
            self.velocidad = 1
        try:
            #si lo estas chocando frena
            if self.x >= self.next_car.x -4:
                self.velocidad = 0
            #si estas a menos de 10 de distancia desacelera
            elif self.x >= self.next_car.x - 10:
                self.x += self.velocidad /10  
            #caso normla acelera en base a la velocidad aleotoria
            else:
                self.x += self.velocidad
        except:
            self.x += self.velocidad


    def __str__(self):
        return self.nombre
    

