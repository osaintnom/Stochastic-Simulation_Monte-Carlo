from clase_auto import Auto
import pandas as pd
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import random
import threading as th
import time


class Ruta:
    def __init__(self, autos,tiempo=100,x_max=1000,y_max=10):
        self.autos = autos
        self.x_max = x_max
        self.fig, self.ax = plt.subplots()
        self.xdata, self.ydata = [], []
        self.ln, = plt.plot([], [], 'ks', markersize=5, markerfacecolor='orange', animated=True)
        self.ax.set_xlim(0, x_max)
        self.ax.set_ylim(-1, 1)
        self.ax.grid()
        self.ax.set_title('Ruta de autos')
        self.ax.set_xlabel('Posición en x')
        self.ax.set_ylabel('Posición en y')



        # Genera autos de manera automatica
        threading_autos = th.Thread(target=self.generar_autos, args=(tiempo,))
        threading_autos.start()

    def init(self):
        self.ln.set_data([], [])
        return self.ln,

    def update(self, frame):
        self.xdata, self.ydata = [], []
        for auto in self.autos:
            auto.avanzar()
            self.xdata.append(auto.x)
            self.ydata.append(auto.y)
        self.ln.set_data(self.xdata, self.ydata)
        return self.ln,



    def animar(self):
        ani = animation.FuncAnimation(self.fig, self.update, frames=np.linspace(0, 100, 100), init_func=self.init, blit=True, interval=100, repeat=True,)
        plt.show()

    def generar_autos(self, tiempo):
        colores = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'gray', 'black']
        inicio = time.time()
        while time.time() - inicio < tiempo:
            self.autos.append(Auto(0, 0, random.randint(1, 5), random.choice(colores), 'Auto ' + str(len(self.autos) + 1), x_max=self.x_max, y_max=10, next_car= self.autos[-1]))
            pausa = random.randint(1, 3)
            time.sleep(pausa)

print('Creando autos...')

G_P = Ruta([Auto(0, 0, 2, 'red', 'G_P')])
G_P.animar()