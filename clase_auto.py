import pandas as pd
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import random
import threading as th
import time


class Auto:
    def __init__(self, x, y, velocidad, color, nombre, x_max=1000, y_max=10,next_car=None,mean = 2.2, delta = 1, alpha = 0.05):
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
        self.reaction_time_mean = random.uniform(0.01,0.03)
        self.aceleracion_max = random.lognormvariate(0.3,0.05)
        if self.aceleracion_max > 0.42:
            self.aceleracion_max = 0.42

        self.frenado_max = random.lognormvariate(0.7,0.1)
        # self.frenado_max = 1
        if self.frenado_max > 0.8:
            self.frenado_max = 0.8
        self.quieto = False
        self.quieto_count = 0
        self.colision = False
        self.tiempo_inicio = time.time()
        self.tiempo_terminar = 0
        self.historic_velocidad = []
        # agregar velocidad maxima?

        # Genera un hilo para acelerar el auto
        threading = th.Thread(target=self.acelerar, args=())
        threading.start()


    def chocaste(self):
        time.sleep(0.8)
        self.colision = True
    def avanzar(self):
        if self.velocidad < 0:
            self.velocidad = 0
        if self.colision == True:
            if self.next_car != None:
                print("_"*10)
                print(f'Auto {self.nombre} choco con el auto {self.next_car.nombre}')
            else:
                print("_"*10)
                print(f'Auto {self.nombre} choco en cadena')
            return
        elif self.quieto == True:
            # aca deberia frenar ahasta llegar a 0 
            return
        else:
            # si chocaste y frenaste, volves a arrancar

            
            try:
                #si lo estas chocando frena
                if self.x >= self.next_car.x -2:
                    self.velocidad = 0
                    choque_yo = th.Thread(target=self.chocaste, args=())
                    choque_yo.start()
                    choque_next = th.Thread(target=self.next_car.chocaste, args=())
                    choque_next.start()
                    self.quieto = True
                    self.quieto_count += 1
                    self.next_car.quieto = True
                    

                    
                    # self.x = self.next_car.x
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
            
            self.historic_velocidad.append(self.velocidad)
            if self.next_car != None and self.x > self.next_car.x:
                self.x = self.next_car.x

    def __str__(self):
        if self.next_car == None:
            return f"Car {self.nombre}, color {self.color}: (x={self.x}, velocidad={self.velocidad}, Auto siguiente: None con vel: '')"
        return f"Car {self.nombre}, color {self.color}: (x={self.x}, velocidad={self.velocidad}, Auto siguiente: {self.next_car.nombre} con vel: {self.next_car.velocidad})"
    



    def acelerar(self):

        while self.x < self.x_max and self.colision == False:
            
            # se desconcentra 
            
            if self.next_car == None:
                if self.velocidad - self.mean < self.mean/10:
                    acelerar = random.lognormvariate(1, 1)*(2*(self.mean - self.velocidad)/self.mean)
                    if acelerar > self.aceleracion_max:
                        acelerar = self.aceleracion_max
                    self.velocidad = self.velocidad + acelerar
                else:
                    acelerar = random.normalvariate(0, 0.25)
                    if acelerar > self.aceleracion_max:
                        acelerar = self.aceleracion_max
                    self.velocidad = self.velocidad + acelerar
                    
                
            elif self.velocidad - self.mean < self.mean/10:

                vel_n = self.next_car.velocidad -0.5
                dist = self.next_car.x - self.x
                if self.velocidad == vel_n:
                    tiempo = 100
                else:
                    tiempo = (dist/(self.velocidad - vel_n))
                if tiempo > 0 and tiempo < 30 :
                    frenado = 10/(3**(tiempo)+0.000001)  * (-1 * random.lognormvariate(5,1))  
                    # print(f'freando del auto {self.nombre}: {frenado}')
                    if frenado < -self.frenado_max:
                        print('esto')
                        frenado = -self.frenado_max
                    self.velocidad = self.velocidad + frenado
                    if self.velocidad < 0:
                        self.velocidad = 0
                else:
                    vel = self.velocidad
                   
                    acelerar = random.lognormvariate(1, 1)*(2*(self.mean - self.velocidad)/self.mean)
                    if acelerar > self.aceleracion_max:
                        acelerar = self.aceleracion_max
                    self.velocidad = self.velocidad + acelerar
                    if vel < 0.5:
                        print('acelerando', self.velocidad, self.mean,self.nombre,self.x,vel,acelerar)

                                  #en este caso sigue acelerando si puede
                #tiempo es muy chico quiero que frene rapdifo
                #si el timepo es mucho 
            else:
                
                vel_n = self.next_car.velocidad -0.5
                dist = self.next_car.x - self.x
                if self.velocidad == vel_n:
                    tiempo = 100
                else:
                    tiempo = (dist/(self.velocidad - vel_n))
                if tiempo > 0 and tiempo < 30:
                    frenado = 10/(3**(tiempo)+0.000001 ) * (-1 * random.lognormvariate(5,1))  
                    # print(f'freando del auto {self.nombre}: {frenado}')
                    if frenado < -self.frenado_max:
                        print('esto')
                        frenado = -self.frenado_max
                    self.velocidad = self.velocidad + frenado
                    if self.velocidad < 0:
                        self.velocidad = 0
                else:
                    # print('acelerando')
                    acelerar = random.normalvariate(0, 0.5)
                    if acelerar > self.aceleracion_max:
                        acelerar = self.aceleracion_max
                    self.velocidad = self.velocidad + acelerar
                    if self.velocidad < 0:
                        self.velocidad = 0

                                  #en este caso sigue acelerando si puede
                # en este caso quiere mantenerse cconstante 





            #aceleracion aleatoria sobre la velocidad del auto
            # acelerar = abs(random.uniform(0, 3))
            # acelerar = random.gammavariate(1, 1)
            # self.velocidad = self.velocidad * acelerar

            # #velocidad minima
            # if self.velocidad < 0.5:
            #     self.velocidad = 1
            # time.sleep(0.2)
            chance = random.uniform(0,1)
            if chance < 0.01:
                time.sleep(0.2)
            elif chance < 0.015:
                time.sleep(0.5)
            elif chance < 0.018:
                time.sleep(0.8)
            else:
                time.sleep(random.uniform(self.reaction_time_mean - 0.01, self.reaction_time_mean + 0.01))

        
            self.tiempo_terminar = time.time() - self.tiempo_inicio