from clase_auto import Auto  # Import the Auto class from another module
import pandas as pd
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import random
import threading as th
import time


class Ruta:
    def __init__(self, autos=[], tiempo=10000, x_max=10000, y_max=10):
        """
        Initialize the Ruta (Road) simulation environment.

        Args:
        autos (list): List of initial cars on the road.
        tiempo (int): Total simulation time in seconds.
        x_max (int): Maximum position on the x-axis (length of the road).
        y_max (int): Maximum position on the y-axis (unused in the current version).
        """
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
        self.ax.set_xticks([0, x_max])  # Remove x-axis labels
        self.ax.set_yticks([-0.25, 0, 0.25])  # Set grid lines only at y=0, y=0.25, and y=-0.25
        self.ax.yaxis.grid(True, linestyle='--', which='major', color='gray', alpha=0.7)
        self.ax.tick_params(axis='y', labelleft=False)

        # Initialize variables for collision tracking and statistics
        self.crashes = []
        self.historic_ids = []
        self.collision_count = 0
        self.finished_count = 0
        self.cant_total_autos = 0
        self.historic_vel_per_auto = []
        # self.cant_multas = 0

        self.historic_mean_velocities = []
        self.historic_trip_duration = []
        self.data = pd.DataFrame(
            columns=['id', 'vel_mean', 'tiempo_terminar', 'colision', 'react_time', 'cant_autos_en_frame'])
        self.df_vel = pd.DataFrame([])

        # Lists to store data for the animation
        self.xdata, self.ydata = [], []
        self.ln, = plt.plot([], [], 'ks', markersize=7, markerfacecolor='orange', animated=True)

        # Colors for cars
        self.colores = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'gray', 'black']

        # Generate an initial car
        incial_nombre = np.random.randint(0, 1000000)
        self.historic_ids.append(incial_nombre)
        self.autos.append(Auto(0, 0, random.normalvariate(2.2, 0.5), random.choice(self.colores),
                               incial_nombre, x_max=self.x_max, y_max=10, mean=random.normalvariate(2.2, 0.5)))
        self.cant_total_autos += 1

        # Create text annotations for statistics
        self.collision_text = self.ax.annotate('', xy=(10, 0.9), fontsize=12, color='red')
        self.car_text = self.ax.annotate('', xy=(10, 0.8), fontsize=12, color='blue')
        self.finished_text = self.ax.annotate('', xy=(10, 0.7), fontsize=12, color='green')
        self.cant_total_autos_text = self.ax.annotate('', xy=(10, 0.6), fontsize=12, color='black')
        self.ave_time_text = self.ax.annotate('', xy=(10, 0.5), fontsize=12, color='black')
        self.ave_v_text = self.ax.annotate('', xy=(10, 0.4), fontsize=12, color='black')
        # self.cant_multas_text = self.ax.annotate('', xy=(10, 0.3), fontsize=12, color='black')

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

    def init(self):
        self.ln.set_data([], [])
        return self.ln,

    def multas_check(self):
        """
        Checkthe amount of multas.
        """
        # Iterate through the cars in the simulation
        for auto in self.autos:
            if auto.multas > 0:
                self.cant_multas += auto.multas
            else:
                self.cant_multas
        return self.cant_multas

    def eliminar_choques(self, tiempo):
        """
        Remove cars that have collided or finished their trip and update statistics.

        Args:
        tiempo (int): Total simulation time in seconds.
        """
        # Record the start time
        inicio = time.time()
        
        # Continue while the elapsed time is less than the specified simulation time
        while time.time() - inicio < tiempo:
            # Create lists to store collided cars and cars that finished their trip
            choques = []
            choques_truchos = []

            # Iterate through the cars in reverse order (from the last car to the first)
            for auto in self.autos[::-1]:
                if auto.colision:
                    # Calculate and store the mean velocity of the collided car
                    self.historic_mean_velocities.append(np.mean(auto.historic_velocidad))
                    
                    # Save data about the collided car
                    self.guardar_datos_auto(auto)
                    

                    # Check if the car's position indicates a real collision for study(x > 500)
                    if auto.x > 500:
                        choques.append(auto)
                    else:
                        choques_truchos.append(auto)
                elif auto.x > self.x_max:
                    # Calculate and store the mean velocity of a finished car
                    self.historic_mean_velocities.append(np.mean(auto.historic_velocidad))
                    
                    # Store the velocity profile of the finished car
                    self.historic_vel_per_auto.append(auto.historic_velocidad)
                    
                    # Store the trip duration of the finished car
                    self.historic_trip_duration.append(auto.tiempo_terminar)
                    
                    # Increment the count of finished cars
                    self.finished_count += 1
                    
                    # Save data about the finished car
                    self.guardar_datos_auto(auto)
                    
                    # Add the finished car to the "fake collisions" list
                    choques_truchos.append(auto)
            
            # If there are any real collisions, increment the collision count
            if len(choques) > 0:
                self.collision_count += 1
            
            # Remove collided and finished cars from the simulation
            for auto in choques:
                self.autos.remove(auto)
            for auto in choques_truchos:
                self.autos.remove(auto)
            
            # Update the following car references for remaining cars
            for auto in self.autos[1:]:
                auto.next_car = self.autos[self.autos.index(auto) - 1]
            
            # If there are remaining cars, set the reference of the first car to None
            if len(self.autos) > 0:
                self.autos[0].next_car = None
            
            # Control the update rate by sleeping for 0.5 seconds
            time.sleep(0.5)

    def update(self, frame):
        """
        Update the visualization of the simulation and text annotations.

        Returns:
        tuple: Updated elements for the animation.
        """
        # Initialize empty lists to store car positions
        self.xdata, self.ydata = [], []

        # Iterate through each car in the simulation
        for auto in self.autos:
            # Advance the car's position
            auto.avanzar()
            
            # Append the car's x and y coordinates to the lists
            self.xdata.append(auto.x)
            self.ydata.append(auto.y)

        # Calculate the current number of cars in the simulation
        car_count = len(self.autos)

        # Update text annotations to display statistics
        self.collision_text.set_text(f'Collisions: {self.collision_count}')
        self.car_text.set_text(f'Car Count in frame: {car_count}')
        self.finished_text.set_text(f'Finished Count: {self.finished_count}')
        self.cant_total_autos_text.set_text(f'Total Cars Count: {self.cant_total_autos}')
        self.ave_time_text.set_text(f'Average Trip Duration: {self.get_avg_trip_duration():.2f} segs en hacer 10km')
        self.ave_v_text.set_text(f'Average Velocity: {self.get_avg_v():.2f} m/s')
        # self.cant_multas_text.set_text(f'Cantidad de multas: {self.multas_check()}')

        # Update the line representing car positions
        self.ln.set_data(self.xdata, self.ydata)

        # If there are more than 200 entries in historic_vel_per_auto, trim the data for consistency
        if len(self.historic_vel_per_auto) >= 200:
            length = min([len(x) for x in self.historic_vel_per_auto])
            historic_vel_per_auto = [x[:length] for x in self.historic_vel_per_auto]
            historic_vel_per_auto = np.array(historic_vel_per_auto)
            
            # Convert the trimmed data to a Pandas DataFrame and save it as a CSV file
            self.df_vel = pd.DataFrame(historic_vel_per_auto)
            self.df_vel.to_csv('velocidades.csv', index=False)
        
        # Return updated elements for the animation
        return self.ln, self.collision_text, self.car_text, self.finished_text, self.cant_total_autos_text, self.ave_time_text, self.ave_v_text


    def animar(self):
        """
        Initialize and display the animation of the simulation.
        """
        # Create an animation using FuncAnimation
        ani = animation.FuncAnimation(
            self.fig, self.update, frames=np.linspace(0, 100, 100), init_func=self.init, blit=True, interval=100, repeat=True
        )
        
        # Display the animation
        plt.show()


    def generar_autos(self, tiempo):
        """
        Generate new cars and add them to the simulation at random intervals.

        Args:
        tiempo (int): Total simulation time in seconds.
        """
        # Record the start time
        inicio = time.time()
        
        # Continue generating cars while the elapsed time is less than the specified simulation time
        while time.time() - inicio < tiempo:
            # Generate a random pause time between 1 and 3 seconds (simulating car arrivals)
            pausa = random.uniform(1, 3)
            time.sleep(pausa)
            
            # Generate a random name for the new car and ensure it is unique
            nombre = np.random.randint(0, 1000000)
            while nombre in self.historic_ids:
                nombre = np.random.randint(0, 1000000)
            
            try:
                # Attempt to create a new car with specified characteristics and add it to the simulation
                self.historic_ids.append(nombre)
                self.autos.append(Auto(0, 0, random.normalvariate(2.2, 0.5), random.choice(self.colores),
                                    nombre, x_max=self.x_max, y_max=10, next_car=self.autos[-1],
                                    mean=random.normalvariate(2.2, 0.5)))
            except:
                # If an error occurs during car creation, print an error message and continue
                print('error')
                self.historic_ids.append(nombre)
                self.autos.append(Auto(0, 0, random.normalvariate(2.2, 0.5), random.choice(self.colores),
                                    + nombre, x_max=self.x_max, y_max=10, next_car=None,
                                    mean=random.normalvariate(2.2, 0.5)))
            
            # Increment the total car count
            self.cant_total_autos += 1


    def guardar_datos_auto(self, auto):
        """
        Record and save data about a car's performance in the simulation.

        Args:
        auto: An instance of the 'Auto' class.
        """
        # Create a dictionary containing data about the car
        data_row = {
            'id': auto.nombre,
            'vel_mean': np.mean(auto.historic_velocidad),
            'tiempo_terminar': auto.tiempo_terminar,
            'colision': auto.colision,
            'react_time': auto.reaction_time_mean,
            'cant_autos_en_frame': len(self.autos),
            'posicion_final': auto.x,
            'cantidad_de_autos_enviados': self.cant_total_autos
            # 'multas': auto.multas
        }
        
        # Concatenate the data as a new row in the 'data' DataFrame
        self.data = pd.concat([self.data, pd.DataFrame([data_row])], ignore_index=True)
        
        # Save the updated DataFrame to a CSV file without an index column
        self.data.to_csv('data.csv', index=False)


if __name__ == '__main__':
    print('Creando autos...')
    G_P = Ruta()
    G_P.animar()
