import pygame
from clase_auto import Auto
import pandas as pd
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import random
import threading as th
import time

# Constants
WIDTH, HEIGHT = 1000, 500
ROAD_COLOR = (50, 50, 50)  # Dark gray for road
CAR_COLOR = (255, 255, 255)

CAR_WIDTH, CAR_HEIGHT = 20, 10
pygame.init()

class Ruta:
    def __init__(self, autos=[], tiempo=1000, x_max=12000, y_max=10):
        self.autos = autos
        self.x_max = x_max
        self.finished_count = 0
        self.collision_count = 0
        self.cant_total_autos = 0

        # Create pygame display and clock
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Car Simulation")
        self.clock = pygame.time.Clock()

        # Create text annotations
        self.font = pygame.font.Font(None, 24)  # Smaller font size
        self.collision_text = self.font.render('', True, (255, 255, 255))
        self.car_text = self.font.render('', True, (255, 255, 255))
        self.finished_text = self.font.render('', True, (255, 255, 255))
        self.cant_total_autos_text = self.font.render('', True, (255, 255, 255))
        self.ave_time_text = self.font.render('', True, (255, 255, 255))
        self.ave_v_text = self.font.render('', True, (255, 255, 255))

        # Lists to store data for the animation
        self.xdata, self.ydata = [], []

        self.crashes = []
        self.historic_ids = []
        self.collision_count = 0
        self.finished_count = 0
        self.cant_total_autos = 0
        self.historic_vel_per_auto = []

        self.historic_mean_velocities = []
        self.historic_trip_duration = []
        self.data = pd.DataFrame(columns=['id', 'vel_mean', 'tiempo_terminar', 'colision', 'react_time', 'quieto_count'])
        self.df_vel = pd.DataFrame([])

        # Colors for cars
        self.colores = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'gray', 'black']

        incial_nombre = np.random.randint(0, 1000000)
        self.historic_ids.append(incial_nombre)

        # Generate the initial car
        self.autos.append(Auto(0, 0, random.normalvariate(2.2, 0.5), random.choice(self.colores),
                               incial_nombre,
                               x_max=self.x_max, y_max=10, mean=random.normalvariate(2.2, 0.5)))
        self.cant_total_autos += 1

        # Start threads for generating cars and removing collisions
        threading_autos = th.Thread(target=self.generar_autos, args=(tiempo,))
        threading_autos.start()
        threading_choques = th.Thread(target=self.eliminar_choques, args=(tiempo,))
        threading_choques.start()

    def __len__(self):
        return len(self.autos)

    def get_crash_count(self):
        return self.collision_count

    def get_avg_v(self):
        if len(self.historic_mean_velocities) == 0:
            return 0
        return 10 * np.mean(self.historic_mean_velocities)

    def get_avg_trip_duration(self):
        if len(self.historic_trip_duration) == 0:
            return 0
        return np.mean(self.historic_trip_duration)

    def eliminar_choques(self, tiempo):
        inicio = time.time()
        while time.time() - inicio < tiempo:
            choques = []
            choques_truchos = []

            for auto in self.autos[::-1]:
                if auto.colision == True:
                    self.historic_mean_velocities.append(np.mean(auto.historic_velocidad))
                    # agregar al array # [auto.nombre, np.mean(auto.historic_velocidad), auto.tiempo_terminar, auto.colision, auto.reaction_time, auto.quieto_count]
                    self.guardar_datos_auto(auto)

                    if auto.x > 50:
                        choques.append(auto)

                    else:
                        choques_truchos.append(auto)
                elif auto.x > self.x_max:
                    self.historic_mean_velocities.append(np.mean(auto.historic_velocidad))
                    self.historic_vel_per_auto.append(auto.historic_velocidad)
                    self.historic_trip_duration.append(auto.tiempo_terminar)
                    self.finished_count += 1
                    # agregar al array # auto.nombre(id), np.mean(auto.historic_velocidad), auto.tiempo_terminar, auto.colision, auto.reaction_time, auto.quieto_count
                    self.guardar_datos_auto(auto)
                    choques_truchos.append(auto)
            if len(choques) > 0:
                self.collision_count += 1
            for auto in choques:
                self.autos.remove(auto)
            for auto in choques_truchos:
                self.autos.remove(auto)
            for auto in self.autos[1:]:
                auto.next_car = self.autos[self.autos.index(auto) - 1]
            if len(self.autos) > 0:
                self.autos[0].next_car = None

            time.sleep(0.5)

    def update(self):
        self.xdata, self.ydata = [], []

        for auto in self.autos:
            auto.avanzar()
            self.xdata.append(auto.x)
            self.ydata.append(auto.y)

            # Check for collisions (your collision logic here)

        car_count = len(self.autos)

        # Update the text annotations
        self.collision_text = self.font.render(f'Collisions: {self.collision_count}', True, (255, 255, 255))
        self.car_text = self.font.render(f'Car Count: {car_count}', True, (255, 255, 255))
        self.finished_text = self.font.render(f'Finished: {self.finished_count}', True, (255, 255, 255))
        self.cant_total_autos_text = self.font.render(f'Total Cars: {self.cant_total_autos}', True, (255, 255, 255))
        self.ave_time_text = self.font.render(f'Avg Trip Duration: {self.get_avg_trip_duration():.2f}segs para 1km', True, (255, 255, 255))
        self.ave_v_text = self.font.render(f'Avg Velocity: {self.get_avg_v():.2f}m/s', True, (255, 255, 255))

        if len(self.historic_vel_per_auto) >= 200:
            # qeudarme con la longitud del menor lista y hacer un df para luego hacer un grafico de lineas
            length = min([len(x) for x in self.historic_vel_per_auto])
            # Slice all sublists to the minimum length
            historic_vel_per_auto = [x[:length] for x in self.historic_vel_per_auto]
            # Convert to a NumPy array
            historic_vel_per_auto = np.array(historic_vel_per_auto)
            # Convert to a pandas DataFrame and save as 'velocidades.csv' without an index column
            self.df_vel = pd.DataFrame(historic_vel_per_auto)
            self.df_vel.to_csv('velocidades.csv', index=False)

    def animar(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update()

            # Clear the screen
            self.screen.fill(ROAD_COLOR)

            # Draw the road
            pygame.draw.rect(self.screen, ROAD_COLOR, (0, HEIGHT // 2 - 20, WIDTH, 40))  # Wider road

            # Draw cars (your drawing logic here)
            for auto in self.autos:
                pygame.draw.rect(self.screen, CAR_COLOR, (auto.x, HEIGHT // 2 - CAR_HEIGHT // 2, CAR_WIDTH, CAR_HEIGHT))

            # Draw text annotations
            self.screen.blit(self.collision_text, (10, 10))
            self.screen.blit(self.car_text, (10, 40))
            self.screen.blit(self.finished_text, (10, 70))
            self.screen.blit(self.cant_total_autos_text, (10, 100))
            self.screen.blit(self.ave_time_text, (10, 130))  # Added average time text
            self.screen.blit(self.ave_v_text, (10, 160))  # Added average velocity text

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def generar_autos(self, tiempo):
        inicio = time.time()
        while time.time() - inicio < tiempo:
            pausa = random.uniform(1, 3)
            time.sleep(pausa)
            nombre = np.random.randint(0, 1000000)
            while nombre in self.historic_ids:
                nombre = np.random.randint(0, 1000000)
            try:
                self.historic_ids.append(nombre)
                self.autos.append(Auto(0, 0, random.normalvariate(2.2, 0.5), random.choice(self.colores),
                                       nombre,
                                       x_max=self.x_max, y_max=10, next_car=self.autos[-1],
                                       mean=random.normalvariate(2.2, 0.5)))

            except:
                print('error')
                self.historic_ids.append(nombre)
                self.autos.append(Auto(0, 0, random.normalvariate(2.2, 0.5), random.choice(self.colores),
                                       + nombre,
                                       x_max=self.x_max, y_max=10, next_car=None,
                                       mean=random.normalvariate(2.2, 0.5)))
            self.cant_total_autos += 1

    def guardar_datos_auto(self, auto):
        data_row = {
            'id': auto.nombre,
            'vel_mean': np.mean(auto.historic_velocidad),
            'tiempo_terminar': auto.tiempo_terminar,
            'colision': auto.colision,
            'react_time': auto.reaction_time_mean,
            'cant_autos_en_frame': len(self.autos)
        }
        self.data = pd.concat([self.data, pd.DataFrame([data_row])], ignore_index=True)
        self.data.to_csv('data.csv', index=False)

print('Creando autos...')
G_P = Ruta()
G_P.animar()
