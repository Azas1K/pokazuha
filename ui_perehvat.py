
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation

import matplotlib.pyplot as plt
import numpy as np

class PerehvatScreen(QDialog):
    def __init__(self):
        super(PerehvatScreen, self).__init__()

        self.init_ui()

    def graph(self):
        self.control_layer = self.widget
        self.control_layer = QGridLayout(self.control_layer)
    
        figure = plt.figure()
        self.ax = plt.axes(xlim=(0, 2500), ylim=(0, 100)) # ГРАНИЦЫ ГРАФИКА
        
        figure.patch.set_facecolor((210/256, 210/256, 210/256))
        self.ax.set_title(f'Спектр сигнал')
        self.ax.set_ylabel('Амплитуда, дБ')
        self.ax.set_xlabel('Частота, МГц')

        self.line, = self.ax.plot([], [], lw=2)
        self.anim = FuncAnimation(figure, self.update_plot, frames=200, interval=20, blit=True)

        self.radial = FigureCanvas(figure)
        self.control_layer.addWidget(self.radial,0,0)


    def update_plot(self, i):

        #ЗДЕСЬ ПРИНИМАЙ ПЕРЕМЕННЫЕ

        diapozon = self.cb_diapozon.currentText() # ДАННЫЕ ИЗ МЕНЮШКИ С ВЫБОРОМ (МГц и кГц)

        
        x = np.linspace(0, 2000, 20000)
        y = np.sin(0.02*np.pi*(x + 0.0003 * i))*100  # ТУТ ИТОГОВЫЙ ГРАФИК В y

        self.line.set_data(x, y)
        return self.line,

    def init_ui(self):
        loadUi('qt/perehvat.ui', self)

        self.graph()