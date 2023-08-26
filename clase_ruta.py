import pandas as pd 
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from clase_auto import Auto

class Ruta:
    def __init__(self, autos):
        self.autos = autos
        self.fig, self.ax = plt.subplots()
        self.xdata, self.ydata = [], []
        self.ln, = plt.plot([], [], 'ro', animated=True)
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        self.ax.grid()
        self.ax.set_title('Ruta de autos')
        self.ax.set_xlabel('Posición en x')
        self.ax.set_ylabel('Posición en y')

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
        ani = animation.FuncAnimation(self.fig, self.update, frames=np.linspace(0, 100, 100), init_func=self.init, blit=True, interval=100, repeat=False)
        plt.show()
