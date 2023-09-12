import pandas as pd
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import random
import threading as th
import time

# Define a class for simulating cars
class Auto:
    def __init__(self, x, y, velocidad, color, nombre, x_max=1000, y_max=10, next_car=None, mean=2.2, delta=1, alpha=0.05):
        # Initialize car properties
        self.x = x               # Current x-coordinate of the car
        self.y = y               # Current y-coordinate of the car
        self.x_max = x_max       # Maximum x-coordinate the car can reach
        self.velocidad = velocidad  # Current velocity of the car
        self.color = color       # Color of the car
        self.nombre = nombre     # Name or identifier of the car
        self.next_car = next_car # Reference to the next car in the lane
        self.mean = mean         # Mean velocity (used for acceleration)
        self.delta = delta       # Not used in the code
        self.alpha = alpha       # Not used in the code
        self.reaction_time_mean = random.lognormvariate(0.08,0.01)  # Reaction time of the driver
        self.aceleracion_max = random.lognormvariate(0.3, 0.05)  # Maximum acceleration of the car
        
        # Ensure acceleration and braking limits are within bounds
        if self.aceleracion_max > 0.42:
            self.aceleracion_max = 0.42
        self.frenado_max = random.lognormvariate(0.7, 0.1)  # Maximum deceleration (braking) of the car
        if self.frenado_max > 0.8:
            self.frenado_max = 0.8
        
        self.quieto = False       # Flag indicating if the car is stationary
        self.quieto_count = 0     # Count of stationary cars
        self.colision = False     # Flag indicating if the car has collided
        self.tiempo_inicio = time.time()  # Start time of car simulation
        self.tiempo_terminar = 0  # Elapsed time for the car's simulation
        self.historic_velocidad = []  # List to store historical velocities
        self.vel_max = 2.2        # Maximum velocity of the car
        
        # Start a thread for accelerating the car
        threading = th.Thread(target=self.acelerar, args=())
        threading.start()

    # Method to simulate a collision
    def chocaste(self):
        time.sleep(0.8)  # Sleep to simulate the collision delay
        self.colision = True
    
    # Method to simulate the car moving forward
    def avanzar(self):
        if self.velocidad < 0:
            self.velocidad = 0  # Ensure velocity is non-negative
        if self.colision:
            if self.next_car is not None:
                print("_" * 10)
                print(f'Auto {self.nombre} choco con el auto {self.next_car.nombre}', self.x)
            else:
                print("_" * 10)
                print(f'Auto {self.nombre} choco en cadena', self.x)
            return
        elif self.quieto:
            return
        else:
            try:
                if self.x >= self.next_car.x - 1.5:
                    self.velocidad = 0  # Car has stopped due to collision
                    choque_yo = th.Thread(target=self.chocaste, args=())
                    choque_yo.start()
                    choque_next = th.Thread(target=self.next_car.chocaste, args=())
                    choque_next.start()
                    self.quieto = True
                    self.quieto_count += 1
                    self.next_car.quieto = True
                else:
                    self.x += self.velocidad  # Move the car forward
            except:
                self.x += self.velocidad  # Move the car forward
            self.historic_velocidad.append(self.velocidad)
            if self.next_car is not None and self.x > self.next_car.x:
                self.x = self.next_car.x  # Adjust position if the car overshoots
        self.tiempo_terminar = time.time() - self.tiempo_inicio

    def __str__(self):
        if self.next_car is None:
            return f"Car {self.nombre}, color {self.color}: (x={self.x}, velocidad={self.velocidad}, Auto siguiente: None con vel: '')"
        return f"Car {self.nombre}, color {self.color}: (x={self.x}, velocidad={self.velocidad}, Auto siguiente: {self.next_car.nombre} con vel: {self.next_car.velocidad})"

    # Method to simulate acceleration and deceleration of the car
    def acelerar(self):
        while self.x < self.x_max and not self.colision:
            if self.next_car is None:
                if self.velocidad - self.mean < self.mean / 10:
                    acelerar = random.lognormvariate(1, 1) * (2 * (self.mean - self.velocidad) / self.mean)
                    if acelerar > self.aceleracion_max:
                        acelerar = self.aceleracion_max
                    self.velocidad = self.velocidad + acelerar*0.1
                else:
                    acelerar = random.normalvariate(0, 0.5) + (self.mean - self.velocidad)/self.mean
                    if acelerar > self.aceleracion_max:
                        acelerar = self.aceleracion_max
                    self.velocidad = self.velocidad + acelerar*0.1
            elif self.velocidad - self.mean < self.mean / 10:
                vel_n = self.next_car.velocidad - 0.5
                dist = self.next_car.x - self.x
                if self.velocidad == vel_n:
                    tiempo = 100
                else:
                    tiempo = (dist / (self.velocidad - vel_n))
                if 0 < tiempo < 30:
                    frenado = 10 / (3 ** (tiempo) + 0.000001) * (-1 * random.lognormvariate(5, 1))
                    if frenado < -self.frenado_max:
                        frenado = -self.frenado_max
                    self.velocidad = self.velocidad + frenado* 0.1
                    if self.velocidad < 0:
                        self.velocidad = 0
                else:
                   
                    acelerar = random.lognormvariate(1, 1) * (2 * (self.mean - self.velocidad) / self.mean)
                    if acelerar > self.aceleracion_max:
                        acelerar = self.aceleracion_max
                    self.velocidad = self.velocidad + acelerar* 0.1
            else:
                vel_n = self.next_car.velocidad - 0.5
                dist = self.next_car.x - self.x
                if self.velocidad == vel_n:
                    tiempo = 100
                else:
                    tiempo = (dist / (self.velocidad - vel_n))
                if 0 < tiempo < 30:
                    frenado = 10 / (3 ** (tiempo) + 0.000001) * (-1 * random.lognormvariate(5, 1))
                    if frenado < -self.frenado_max:
                        frenado = -self.frenado_max
                    self.velocidad = self.velocidad + frenado* 0.1
                    if self.velocidad < 0:
                        self.velocidad = 0
                else:
                    acelerar = random.normalvariate(0, 0.5) + (self.mean - self.velocidad)/self.mean
                    if self.velocidad > 100:
                        acelerar = -abs(acelerar)
                    if acelerar > self.aceleracion_max:
                        acelerar = self.aceleracion_max
                    self.velocidad = self.velocidad + acelerar* 0.1
                    if self.velocidad < 0:
                        self.velocidad = 0

            chance = random.uniform(0, 10)
            if chance < 0.005:
                time.sleep(0.2)  # Simulate driver distraction with a 0.2s delay
                print('se desconcentro', self.nombre, self.x)
            elif chance < 0.0052:
                time.sleep(0.4)  # Simulate driver distraction with a 0.4s delay
                print('se desconcentro', self.nombre, self.x)
            elif chance < 0.0053:
                print('se desconcentro', self.nombre, self.x)
                time.sleep(3)   # Simulate extended driver distraction with a 3s delay
            else:
                time.sleep(random.uniform(self.reaction_time_mean - 0.01, self.reaction_time_mean + 0.01))
        self.tiempo_terminar = time.time() - self.tiempo_inicio
