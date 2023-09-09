import pandas as pd
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import random
import threading as th
import time


class Auto:
    def __init__(self, x, y, velocidad, color, nombre, x_max=1000, y_max=10,next_car=None,mean = 2.7, delta = 1, alpha = 0.05):
        self.x = x
        self.y = y # por ahora no hace nada pero seria como cambiar de carril
        self.x_max = x_max  # marca donde termina la ruta
        self.velocidad = velocidad
        self.color = color # abria que aprender a usar esto para que se vea mas lindo
        self.nombre = nombre # inutil pero qsy despues puede servir
        self.next_car = next_car 
        self.mean = mean
        self.delta = delta
        self.alpha = alpha
        self.colision = False
         
        # agregar velocidad maxima?

        # Genera un hilo para acelerar el auto
        threading = th.Thread(target=self.acelerar, args=())
        threading.start()
        

    def acelerar(self):


        while self.x < self.x_max:
            #aceleracion aleatoria sobre la velocidad del auto
            # acelerar = abs(random.uniform(0, 3))
            # acelerar = random.gammavariate(1, 1)
            # self.velocidad = self.velocidad * acelerar

            # #velocidad minima
            # if self.velocidad < 0.5:
            #     self.velocidad = 1
            # time.sleep(0.2)
            if self.next_car == None:
                self.velocidad = self.velocidad + self.alpha * (self.mean - self.velocidad) + self.velocidad *self.delta* random.normalvariate(0, 2)    
                if self.velocidad <0.2:
                    self.velocidad = 0.2
            elif (self.next_car.x - self.x) < 4:
                self.velocidad = 0
            else:
                self.velocidad = self.velocidad + self.alpha * (self.mean - self.velocidad) + self.delta* random.normalvariate(0, 2)    -abs((10/(self.next_car.x - self.x))*random.normalvariate(0, 2))
                if self.velocidad <0.2:
                    self.velocidad = 0.2
            time.sleep(0.2)


    def avanzar(self):
        if self.colision == True:
            return
        # si chocaste y frenaste, volves a arrancar
        if self.velocidad == 0:
            self.velocidad = 1
        
        try:
            #si lo estas chocando frena
            if self.x >= self.next_car.x -2:
                self.velocidad = 0
                self.colision = True
            #si estas a menos de 10 de distancia desacelera
            # elif self.x >= self.next_car.x - 15:
            #     self.x += self.velocidad /10 
            # elif self.x >= self.next_car.x - 30:
            #     self.x += self.velocidad /4  

            #caso normla acelera en base a la velocidad aleotoria
            else:
                self.x += self.velocidad
        except:
            self.x += self.velocidad
        # if self.x > self.x_max:
        #     self.x = self.x_max
        
        if self.next_car != None and self.x > self.next_car.x:
            self.x = self.next_car.x

    def __str__(self):
        return self.next_car.x
    





    def acelerar_nuevo(self):


        while self.x < self.x_max and self.colision == False:
        #     if self.velocidad - self.mean < self.mean/10:
        #         pass
        #         #en este caso sigue acelerando si puede

        #     else:


                # en este caso quiere mantenerse cconstante





            #aceleracion aleatoria sobre la velocidad del auto
            # acelerar = abs(random.uniform(0, 3))
            # acelerar = random.gammavariate(1, 1)
            # self.velocidad = self.velocidad * acelerar

            # #velocidad minima
            # if self.velocidad < 0.5:
            #     self.velocidad = 1
            # time.sleep(0.2)
            if self.next_car == None:
                self.velocidad = self.velocidad + self.alpha * (self.mean - self.velocidad) + self.velocidad *self.delta* random.normalvariate(0, 2)    
                if self.velocidad <0.2:
                    self.velocidad = 0.2
            elif (self.next_car.x - self.x) < 4:
                self.velocidad = 0
            else:
                self.velocidad = self.velocidad + self.alpha * (self.mean - self.velocidad) + self.delta* random.normalvariate(0, 2)    -abs((10/(self.next_car.x - self.x))*random.normalvariate(0, 2))
                if self.velocidad <0.2:
                    self.velocidad = 0.2
            time.sleep(0.2)