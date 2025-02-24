
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import matplotlib.pyplot as plt


class TheoryScreen(QDialog):

    def __init__(self):
        super(TheoryScreen, self).__init__()
        self.init_ui()


    def graph_1(self):
        self.control_layer = self.widget
        self.control_layer = QGridLayout(self.control_layer)
    
        self.figure, self.ax = plt.subplots(figsize=(10, 5))
        self.figure.patch.set_facecolor((210/256, 210/256, 210/256))
        self.ax.set_title(f'Несущий сигнал')
        self.ax.set_ylabel('Амплитуда, дБ')
        self.ax.set_xlabel('Время')

        radial = FigureCanvas(self.figure)

        self.control_layer.addWidget(radial,0,0)

    def graph_2(self):
        self.control_layer = self.widget_2
        self.control_layer = QGridLayout(self.control_layer)

        self.figure, self.ax = plt.subplots(figsize=(10, 5))
        self.figure.patch.set_facecolor((210/256, 210/256, 210/256))
        self.ax.set_title(f'Модулирующий сигнал')
        self.ax.set_ylabel('Амплитуда, дБ')
        self.ax.set_xlabel('Время')

        radial = FigureCanvas(self.figure)

        self.control_layer.addWidget(radial,0,0)

    def graph_3(self):
        self.control_layer = self.widget_3
        self.control_layer = QGridLayout(self.control_layer)
    

        self.figure, self.ax = plt.subplots(figsize=(10, 5))
        self.figure.patch.set_facecolor((210/256, 210/256, 210/256))
        self.canvas = FigureCanvas(self.figure)
        self.ax.set_title(f'Модулированный сигнал')
        self.ax.set_ylabel('Амплитуда, дБ')
        self.ax.set_xlabel('Время')

        radial = FigureCanvas(self.figure)

        self.control_layer.addWidget(radial,0,0)

    def graph_4(self):
        self.control_layer = self.widget_4
        self.control_layer = QGridLayout(self.control_layer)
    
        self.figure, self.ax = plt.subplots(figsize=(10, 5))
        self.figure.patch.set_facecolor((210/256, 210/256, 210/256))
        self.canvas = FigureCanvas(self.figure)
        self.ax.set_title(f'Амплитудная модуляция')
        self.ax.set_ylabel('Амплитуда, дБ')
        self.ax.set_xlabel('Время')

        radial = FigureCanvas(self.figure)

        self.control_layer.addWidget(radial,0,0)

    def graph_5(self):
        self.control_layer = self.widget_5
        self.control_layer = QGridLayout(self.control_layer)

        self.figure, self.ax = plt.subplots(figsize=(10, 5))
        self.figure.patch.set_facecolor((210/256, 210/256, 210/256))
        self.canvas = FigureCanvas(self.figure)
        self.ax.set_title(f'Спектр сигнал')
        self.ax.set_ylabel('Амплитуда, дБ')
        self.ax.set_xlabel('Частота, МГц')

        radial = FigureCanvas(self.figure)

        self.control_layer.addWidget(radial,0,0)


    def init_ui(self):
        loadUi('qt/theory.ui', self)

        self.graph_1()
        self.graph_2()
        self.graph_3()
        self.graph_4()
        self.graph_5()