import pandas as pd
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import random
import threading as th
import time

# Define a class for simulating cars
class Auto:
    def __init__(self, x, y, velocidad, color, nombre, x_max=1000, y_max=10, next_car=None, mean=2.2):
        """
        Initialize the car with its attributes.

        Args:
            x (float): Current x-coordinate of the car.
            y (float): Current y-coordinate of the car (not used for now).
            velocidad (float): Current velocity of the car.
            color (str): Color of the car.
            nombre (str): Name or identifier of the car.
            x_max (float): Maximum x-coordinate the car can reach.
            y_max (float): Maximum y-coordinate (not used for now).
            next_car (Auto): Reference to the next car in the lane.
            mean (float): Mean velocity used for acceleration.
            delta (float): Not used in the code.
            alpha (float): Not used in the code.
        """
        self.x = x
        self.y = y  # Currently not used, potentially for changing lanes
        self.x_max = x_max  # Maximum x-coordinate that marks the end of the road
        self.velocidad = velocidad
        self.color = color  # Color (potentially for visualization)
        self.nombre = nombre  # Car name or identifier
        self.next_car = next_car  # Reference to the next car in the lane
        self.mean = mean

        # Initialize random reaction time and maximum acceleration
        self.reaction_time_mean = random.normalvariate(0.08, 0.01)
        self.aceleracion_max = random.lognormvariate(0.3, 0.05)

        # Ensure acceleration and braking limits are within bounds
        if self.aceleracion_max > 0.42:
            self.aceleracion_max = 0.42
        self.frenado_max = random.lognormvariate(0.7, 0.1) # Maximum deceleration (braking) of the car
        if self.frenado_max > 0.8:
            self.frenado_max = 0.8

        self.quieto = False  # Flag indicating if the car is stationary
        self.quieto_count = 0  # Count of stationary cars
        self.colision = False  # Flag indicating if the car has collided
        self.tiempo_inicio = time.time()  # Start time of car simulation
        self.tiempo_terminar = 0  # Elapsed time for the car's simulation
        self.historic_velocidad = []  # List to store historical velocities

        # Maximum velocity of the car
        self.vel_max = 2.2

        # Start a thread for accelerating the car
        threading = th.Thread(target=self.acelerar, args=())
        threading.start()

    def chocaste(self):
        """
        Simulate a collision by sleeping for 0.8 seconds and setting the collision flag.
        """
        time.sleep(0.8) # Sleep to simulate the collision delay
        self.colision = True

    def avanzar(self):
        """
        Simulate the car's movement forward.

        The car will either accelerate, decelerate, or remain stationary based on its state and surroundings.
        """
        if self.velocidad < 0:
            self.velocidad = 0

        if self.colision:
            if self.next_car is not None:
                print("_" * 10)
                print(f'Auto {self.nombre} choco con el auto {self.next_car.nombre}', self.x)
            else:
                print("_" * 10)
                print(f'Auto {self.nombre} choco en cadena', self.x)
            return
        elif self.quieto:
            # Here, the car stay in total stop until is remove.
            return
        else:
            try:
                if self.x >= self.next_car.x - 1.5:
                    self.velocidad = 0
                    choque_yo = th.Thread(target=self.chocaste, args=())
                    choque_yo.start()
                    choque_next = th.Thread(target=self.next_car.chocaste, args=())
                    choque_next.start()
                    self.quieto = True
                    self.quieto_count += 1
                    self.next_car.quieto = True
                else:
                    self.x += self.velocidad
            except:
                self.x += self.velocidad

            self.historic_velocidad.append(self.velocidad)
            if self.next_car is not None and self.x > self.next_car.x:
                self.x = self.next_car.x

        self.tiempo_terminar = time.time() - self.tiempo_inicio

    def __str__(self):
        if self.next_car is None:
            return f"Car {self.nombre}, color {self.color}: (x={self.x}, velocidad={self.velocidad}, Auto siguiente: None con vel: '')"
        return f"Car {self.nombre}, color {self.color}: (x={self.x}, velocidad={self.velocidad}, Auto siguiente: {self.next_car.nombre} con vel: {self.next_car.velocidad})"

    def acelerar(self):
        """
        Simulate the acceleration and deceleration of the car.

        The car's speed is adjusted based on surrounding conditions. It can accelerate, decelerate, or maintain its speed
        depending on the relative position and velocity of the next car.

        Case 1: No Next Car (Free Road)
        - If there is no next car, the car accelerates when its speed is lower than the mean speed.
        - If the acceleration exceeds the maximum allowed acceleration, it's limited.
        - In other cases, it decelerates or maintains its speed with some random fluctuations.

        Case 2: Following Next Car (Car Ahead)
        - If there is a next car, and the car's speed is lower than the mean speed, it calculates the time gap (tiempo)
        to the next car and decelerates accordingly to maintain a safe following distance.
        - If the calculated deceleration exceeds the maximum allowed deceleration (frenado_max), it's limited.
        - If the calculated tiempo is out of bounds (0-30), it follows a different deceleration pattern.
        - Otherwise, it accelerates or maintains its speed based on random fluctuations.

        Case 3: Following Next Car (Car Ahead - Different Pattern)
        - This case is similar to Case 2 but follows a different deceleration pattern when tiempo is out of bounds.

        Driver Distraction:
        - Simulates driver distraction with varying delays for different distraction levels.

        Termination:
        - The method continues to run until the car either reaches its maximum position (x_max) or collides (colision).

        Timing:
        - Calculates the time taken for the car's simulation (tiempo_terminar) once the loop terminates.
        """
        while self.x < self.x_max and not self.colision:
            if self.next_car is None:  # Case 1: No Next Car (Free Road)
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
            elif self.velocidad - self.mean < self.mean / 10:  # Case 2: Following Next Car (Car Ahead)
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
                    self.velocidad = self.velocidad + frenado*0.1
                    if self.velocidad < 0:
                        self.velocidad = 0
                else:  # Case 3: Following Next Car (Car Ahead - Different Pattern)
                   
                    acelerar = random.lognormvariate(1, 1) * (2 * (self.mean - self.velocidad) / self.mean)
                    if acelerar > self.aceleracion_max:
                        acelerar = self.aceleracion_max
                    self.velocidad = self.velocidad + acelerar*0.1
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
                    self.velocidad = self.velocidad + frenado*0.1
                    if self.velocidad < 0:
                        self.velocidad = 0
                else:
                    acelerar = random.normalvariate(0, 0.5) + (self.mean - self.velocidad)/self.mean
                    if self.velocidad > 100:
                        acelerar = -abs(acelerar)
                    if acelerar > self.aceleracion_max:
                        acelerar = self.aceleracion_max
                    self.velocidad = self.velocidad + acelerar*0.1
                    if self.velocidad < 0:
                        self.velocidad = 0

            chance = random.uniform(0, 10)  # Simulate driver distraction
            if chance < 0.005:
                time.sleep(0.2)  # Short driver distraction (0.2s delay)
                print('se desconcentro', self.nombre, self.x)
            elif chance < 0.0052:
                time.sleep(0.4)  # Moderate driver distraction (0.4s delay)
                print('se desconcentro', self.nombre, self.x)
            elif chance < 0.0053:
                print('se desconcentro', self.nombre, self.x)
                time.sleep(0.5)  # Extended driver distraction (0.5s delay)
            else:
                time.sleep(random.uniform(self.reaction_time_mean - 0.01, self.reaction_time_mean + 0.01))

        self.tiempo_terminar = time.time() - self.tiempo_inicio  # Calculate simulation time
