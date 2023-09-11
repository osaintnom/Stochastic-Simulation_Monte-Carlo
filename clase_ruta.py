from clase_auto import Auto
import pandas as pd
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import random
import threading as th
import time


class Ruta:
    def __init__(self, autos=[], tiempo=100, x_max=2500, y_max=10):
        self.autos = autos
        self.x_max = x_max
        self.finished_count = 0  # Track the number of cars that have finished

        # Create the figure and axes for plotting
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, x_max)
        self.ax.set_ylim(-1, 1)
        self.ax.grid()
        self.ax.set_title('Ruta de autos')
        self.ax.set_xlabel('Posición en x')
        self.ax.set_ylabel('Posición en y')

        self.crashes = []
        self.historic_ids = []
        self.collision_count = 0
        self.finished_count = 0
        self.cant_total_autos = 0

        self.historic_velocities = []
        self.historic_trip_duration = []
        self.data = pd.DataFrame(columns=['id', 'vel_mean', 'tiempo_terminar', 'colision', 'react_time', 'quieto_count'])
        #hacer un array por Ruta donde tenga la ssiguientes columnas: id, vel_mean, tiempo_terminar, colision, react_time, quieto_count
        #cada fila es un auto que termino 


        def __len__(self):
            return len(self.autos)

        def get_crash_count(self):
            return self.collision_count

        def get_avg_v(self):
            if len(self.historic_velocities) == 0:
                return 0
            return np.mean(self.historic_velocities)

        def get_avg_trip_duration(self):
            if len(self.historic_trip_duration) == 0:
                return 0
            return np.mean(self.historic_trip_duration)


        # Lists to store data for the animation
        self.xdata, self.ydata = [], []
        self.ln, = plt.plot([], [], 'ks', markersize=7, markerfacecolor='orange', animated=True)

        # Colors for cars
        self.colores = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'gray', 'black']

        incial_nombre = np.random.randint(0, 1000000)
        self.historic_ids.append(incial_nombre)

        # Generate the initial car
        self.autos.append(Auto(0, 0, random.normalvariate(22, 0.5), random.choice(self.colores),
                               incial_nombre,
                               x_max=self.x_max, y_max=10, mean=random.normalvariate(8, 0.5)))
        self.cant_total_autos += 1

        # Create text annotations
        self.collision_text = self.ax.annotate('', xy=(10, 0.8), fontsize=12, color='red')
        self.car_text = self.ax.annotate('', xy=(10, 0.7), fontsize=12, color='blue')
        self.finished_text = self.ax.annotate('', xy=(10, 0.6), fontsize=12, color='green')
        self.cant_total_autos_text = self.ax.annotate('', xy=(10, 0.5), fontsize=12, color='black')

        # Start threads for generating cars and removing collisions
        threading_autos = th.Thread(target=self.generar_autos, args=(tiempo,))
        threading_autos.start()
        threading_choques = th.Thread(target=self.eliminar_choques, args=(tiempo,))
        threading_choques.start()

    def init(self):
        self.ln.set_data([], [])
        return self.ln,

    def eliminar_choques(self,tiempo):
            
        inicio = time.time()
        while time.time() - inicio < tiempo:
            choques = []
            for auto in self.autos[::-1]:
                if auto.colision == True:
                    self.historic_velocities.append(np.mean(auto.historic_velocidad))
                    #agregar al array # [auto.nombre, np.mean(auto.historic_velocidad), auto.tiempo_terminar, auto.colision, auto.reaction_time, auto.quieto_count]
                    self.guardar_datos_auto(auto)
                    choques.append(auto)
                    self.collision_count += 1
                elif auto.x > self.x_max:
                    self.historic_velocities.append(np.mean(auto.historic_velocidad))
                    self.historic_trip_duration.append(auto.tiempo_terminar)
                    self.finished_count += 1
                    #agregar al array # auto.nombre(id), np.mean(auto.historic_velocidad), auto.tiempo_terminar, auto.colision, auto.reaction_time, auto.quieto_count
                    self.guardar_datos_auto(auto)
                    choques.append(auto)
            for auto in choques:
                self.autos.remove(auto)
            for auto in self.autos[1:]:
                auto.next_car = self.autos[self.autos.index(auto) - 1]
            if len(self.autos) > 0:
                self.autos[0].next_car = None


            time.sleep(1)

    def update(self, frame):
        self.xdata, self.ydata = [], []

        for auto in self.autos:
            auto.avanzar()
            self.xdata.append(auto.x)
            self.ydata.append(auto.y)


            # Check for collisions and update collision count

        car_count = len(self.autos)

        # Update the text annotations
        self.collision_text.set_text(f'Collisions: {self.collision_count}')
        self.car_text.set_text(f'Car Count: {car_count}')
        self.finished_text.set_text(f'Finished Count: {self.finished_count}')
        self.cant_total_autos_text.set_text(f'Total Cars Count: {self.cant_total_autos}')  # Update total cars text
        self.finished_text.set_position((10, 0.6))

        self.ln.set_data(self.xdata, self.ydata)
        return self.ln, self.collision_text, self.car_text, self.finished_text, self.cant_total_autos_text
    
    def animar(self):
        ani = animation.FuncAnimation(
            self.fig, self.update, frames=np.linspace(0, 100, 100), init_func=self.init, blit=True, interval=100, repeat=True
        )
        plt.show()
        

    def generar_autos(self, tiempo):
        inicio = time.time()
        while time.time() - inicio < tiempo:
            pausa = random.randint(1, 3)
            time.sleep(pausa)
            nombre = np.random.randint(0, 1000000)
            while nombre in self.historic_ids:
                nombre = np.random.randint(0, 1000000)
            try:
                self.historic_ids.append(nombre)
                self.autos.append(Auto(0, 0, random.normalvariate(22, 0.5), random.choice(self.colores),
                                    nombre,
                                    x_max=self.x_max, y_max=10, next_car=self.autos[-1], mean=random.normalvariate(8, 0.5)))
                
            except:
                print('error')
                self.historic_ids.append(nombre)
                self.autos.append(Auto(0, 0, random.normalvariate(22, 0.5), random.choice(self.colores),
                                    + nombre,
                                    x_max=self.x_max, y_max=10, next_car=None, mean=random.normalvariate(2.7, 0.5)))
            self.cant_total_autos += 1
            # print(str(self.autos[-1]))
        
    def guardar_datos_auto(self, auto):
        data_row = {
            'id': auto.nombre,
            'vel_mean': np.mean(auto.historic_velocidad),
            'tiempo_terminar': auto.tiempo_terminar,
            'colision': auto.colision,
            'react_time': auto.reaction_time_mean,
            'quieto_count': auto.quieto_count
        }
        self.data = pd.concat([self.data, pd.DataFrame([data_row])], ignore_index=True)
        print(self.data.tail())
        

print('Creando autos...')
G_P = Ruta()
G_P.animar()
# print(G_P.data)


## funcion de ordenar lista





