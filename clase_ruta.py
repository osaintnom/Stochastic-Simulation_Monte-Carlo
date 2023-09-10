from clase_auto import Auto
import pandas as pd
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import random
import threading as th
import time


class Ruta:
    def __init__(self, autos=[],tiempo=100,x_max=300,y_max=10):

        

        
        # lista en la que guardo los autos en la autopista, abria que ver si podemos ir eliminando los autos
        self.autos = autos

        #tamaño maximo de la ruta
        self.x_max = x_max
        self.fig, self.ax = plt.subplots()
        self.xdata, self.ydata = [], []
        self.ln, = plt.plot([], [], 'ks', markersize=7, markerfacecolor='orange', animated=True)
        self.ax.set_xlim(0, x_max)
        self.ax.set_ylim(-1, 1)
        self.ax.grid()
        self.ax.set_title('Ruta de autos')
        self.ax.set_xlabel('Posición en x')
        self.ax.set_ylabel('Posición en y')
        self.colores = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'gray', 'black']
        self.autos.append(Auto(0, 0, random.normalvariate(2.7, 0.5), random.choice(self.colores), str(random.randint(1,2000)) + str(len(self.autos) + 1), x_max=self.x_max, y_max=10,mean = random.normalvariate(2.7,0.5)))
        



        # Genera autos de manera automatica
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
                if auto.colision == True or auto.x > self.x_max:
                    choques.append(auto)
            for auto in choques:
                self.autos.remove(auto)
            for auto in self.autos[1:]:
                auto.next_car = self.autos[self.autos.index(auto) - 1]
            self.autos[0].next_car = None

            time.sleep(0.5)
        



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
        
        inicio = time.time()
        while time.time() - inicio < tiempo:
            try:
                self.autos.append(Auto(0, 0, random.normalvariate(1, 0.5), random.choice(self.colores), 'Auto ' + str(len(self.autos) + 1), x_max=self.x_max, y_max=10, next_car= self.autos[-1],mean = random.normalvariate(2.22,0.5)))
                pausa = random.randint(1, 3)
            except:
                self.autos.append(Auto(0, 0, random.normalvariate(1, 0.5), random.choice(self.colores), 'Auto ' + str(len(self.autos) + 1), x_max=self.x_max, y_max=10, next_car= None,mean = random.normalvariate(2.22,0.5)))
            print(str(self.autos[len(self.autos) - 1]))
            time.sleep(pausa)

print('Creando autos...')

G_P = Ruta()
G_P.animar()



## funcion de ordenar lista
