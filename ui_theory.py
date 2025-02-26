
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation

import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft, fftfreq

class TheoryScreen(QDialog):
    fc = 500 # несущая частота от 100 до 1000 МГц
    fm_count = 1 # число гармоник в модулирующем сигнале (от 1 до 5)
    mod_type="ФМн" # тип модуляции (АМ, ОМ, ЧМ, ЧМн, ФМн)
    m = 0.15 # коэффициент модуляции (от 0 до 1)

    Ac = 360 # амплитуда несущего сигнала
    Am = [24, 34, 20, 15, 39] # амплитуды модулирующих сигналов
    fm = [40, 50, 60, 70, 80] # частоты модулирующих сигналов

    fs = 10*fc # частота дискретизации
    T = 0.05  # Длительность сигнала в секундах
    time = np.linspace(0, T, int(fs*T), endpoint=False)  # Временная ось

    carrier = Ac * np.sin(2*np.pi*fc*time)

    signal_goto_main   = pyqtSignal()

    def __init__(self):
        super(TheoryScreen, self).__init__()

        self.init_ui()

        self.btn_back.clicked.connect(self.goto_main)

    def graph_1(self):
        self.control_layer = self.widget
        self.control_layer = QGridLayout(self.control_layer)
    
        figure = plt.figure()
        ax = plt.axes(xlim=(0, 0.1), ylim=(-400, 400))
        
        figure.patch.set_facecolor((210/256, 210/256, 210/256))
        ax.set_title(f'Несущий сигнал')
        ax.set_ylabel('Амплитуда, дБ')
        ax.set_xlabel('Время')

        self.line1, = ax.plot([], [], lw=2)
        self.anim1 = FuncAnimation(figure, self.update_plot1, frames=200, interval=20, blit=True)

        self.radial_1 = FigureCanvas(figure)
        self.control_layer.addWidget(self.radial_1,0,0)

    def graph_2(self):
        self.control_layer = self.widget_2
        self.control_layer = QGridLayout(self.control_layer)
    
        figure = plt.figure()
        ax_2 = plt.axes(xlim=(0, 0.1), ylim=(-1.5, 1.5))
        
        figure.patch.set_facecolor((210/256, 210/256, 210/256))
        ax_2.set_title(f'Модулирующий сигнал')
        ax_2.set_ylabel('Амплитуда, дБ')
        ax_2.set_xlabel('Время')

        self.line2, = ax_2.plot([], [], lw=2)
        self.anim2 = FuncAnimation(figure, self.update_plot2, frames=200, interval=20, blit=True)

        self.radial_2 = FigureCanvas(figure)
        self.control_layer.addWidget(self.radial_2,0,0)

    def graph_3(self):
        self.control_layer = self.widget_3
        self.control_layer = QGridLayout(self.control_layer)
    
        figure = plt.figure()
        ax_3 = plt.axes(xlim=(0, 0.1), ylim=(-600, 600))
        
        figure.patch.set_facecolor((210/256, 210/256, 210/256))
        ax_3.set_title(f'Модулированный сигнал')
        ax_3.set_ylabel('Амплитуда, дБ')
        ax_3.set_xlabel('Время')

        self.line3, = ax_3.plot([], [], lw=2)
        self.anim3 = FuncAnimation(figure, self.update_plot3, frames=200, interval=20, blit=True)

        self.radial_3 = FigureCanvas(figure)
        self.control_layer.addWidget(self.radial_3,0,0)

    def graph_4(self):
        self.control_layer = self.widget_4
        self.control_layer = QGridLayout(self.control_layer)
    
        figure = plt.figure()
        self.ax_4 = plt.axes(xlim=(0, 2500), ylim=(0, 100))
        # self.ax_4.semilogy(self.freqs[:self.N // 2], self.spectrum[:self.N // 2])
        
        figure.patch.set_facecolor((210/256, 210/256, 210/256))
        self.ax_4.set_title(f'Спектр сигнал')
        self.ax_4.set_ylabel('Амплитуда, дБ')
        self.ax_4.set_xlabel('Частота, МГц')

        self.line4, = self.ax_4.plot([], [], lw=2)
        self.anim4 = FuncAnimation(figure, self.update_plot4, frames=200, interval=20, blit=True)

        self.radial_4 = FigureCanvas(figure)
        self.control_layer.addWidget(self.radial_4,0,0)


    def update_plot1(self, i):
        self.fc = self.qs_carrier_freq.value() / 20
        self.fm_count = int(self.qs_hormonics.value())
        x = np.linspace(0, 2, 20000)
        
        y = self.Ac * np.sin(2*np.pi*self.fc*(x + 0.0003 * i))
        self.line1.set_data(x, y)
        return self.line1,

    def update_plot2(self, i):
        self.mod_type = self.cb_mod.currentText()
        self.fm_count = int(self.qs_hormonics.value())
        x = np.linspace(0, 2, 20000)

        if self.mod_type in ("АМ", "ОМ", "ЧМ"):
            y = self.Am[0] * np.sin(2*np.pi*self.fm[0]*(x + 0.0003 * i))/80
            for i in range(1, self.fm_count):
                y += self.Am[i] * np.sin(2*np.pi*self.fm[i]*(x + 0.0003 * i))/80

        if self.mod_type in ("ЧМн", "ФМн"):
            y = np.sign(np.sin(2 * np.pi * self.fm[0]*(x + 0.0003 * i)))

        self.line2.set_data(x, y)
        return self.line2,

    def update_plot3(self, i):
        self.fc = self.qs_carrier_freq.value() / 20
        self.mod_type = self.cb_mod.currentText()
        self.m = self.qs_coef_mod.value() / 1500
        self.fm_count = int(self.qs_hormonics.value())
        x = np.linspace(0, 2, 20000)

        carrier = self.Ac * np.sin(2*np.pi*self.fc*x)
        
        if self.mod_type in ("АМ", "ОМ", "ЧМ"):
            modulating = self.Am[0] * np.sin(2*np.pi*self.fm[0]*(x + 0.0003 * i))
            for i in range(1, self.fm_count):
                modulating += self.Am[i] * np.sin(2*np.pi*self.fm[i]*(x + 0.0003 * i))

        if self.mod_type == "АМ":
            y = (1 + self.m * modulating) * carrier / 3
        elif self.mod_type == "ОМ":
            y = (self.m * modulating) * carrier / 3
        elif self.mod_type == "ЧМ":
            y= self.Ac * np.sin(2*np.pi*self.fc*(x + 0.0003 * i) + self.m*2*np.pi*modulating)
        elif self.mod_type == "ЧМн":
            modulating = np.sign(np.sin(2 * np.pi * self.fm[0] * (x + (0.0003 + 0 )* i)))
            self.integral_mod = np.cumsum(modulating) / self.fs
            y = self.Ac * np.sin(2 * np.pi * self.fc * (x + (0.0001 + 0 )* i) + 2000*self.m*np.pi* self.integral_mod)
        elif self.mod_type == "ФМн":
            modulating = np.sign(np.sin(2 * np.pi * self.fm[0] * (x + (0.0003 + 0 )* i)))
            y = self.Ac * np.cos(2 * np.pi * self.fc * (x + (0.0003 + 0 )* i) + (np.pi * (modulating + 1) / 2))

        self.line3.set_data(x, y)
        return self.line3,


    def update_plot4(self, i):
        self.fc = self.qs_carrier_freq.value() / 20
        self.mod_type = self.cb_mod.currentText()
        self.m = self.qs_coef_mod.value() / 1500
        self.fm_count = int(self.qs_hormonics.value())
        t = np.linspace(0, 2500, 2500)

        Ac = 360 
        Am = [24, 34, 20, 15, 39]
        fm = [40, 50, 60, 70, 80]

        fs = 10*self.fc

        carrier = Ac * np.sin(2*np.pi*self.fc*t)

        modulating = Am[0] * np.sin(2*np.pi*fm[0]*t)
        for i in range(1,self.fm_count):
            modulating += Am[i] * np.sin(2*np.pi*fm[i]*t)

        if self.mod_type == "АМ":
            modulated = (1 + self.m * modulating) * carrier
        elif self.mod_type == "ОМ":
            modulated = ( self.m * modulating) * carrier
        elif self.mod_type == "ЧМ":
            modulated = Ac * np.sin(2*np.pi*self.fc*t + self.m*2*np.pi*modulating)
        elif self.mod_type == "ЧМн":
            modulating = np.sign(np.sin(2 * np.pi * fm[0] * t))
            integral_mod = np.cumsum(modulating) / fs
            modulated = Ac * np.sin(2 * np.pi * self.fc * t + 2000* self.m*np.pi* integral_mod)
        elif self.mod_type == "ФМн":
            modulating = np.sign(np.sin(2 * np.pi * fm[0] * t))
            modulated = Ac * np.cos(2 * np.pi * self.fc * t + (np.pi * (modulating + 1) / 2)) 

        N = len(t) * 2
        y = np.abs(fft(modulated)) / N

        self.line4.set_data(t, y)
        return self.line4,

    def goto_main(self):
        self.signal_goto_main.emit()

    def init_ui(self):
        loadUi('qt/theory.ui', self)

        self.graph_1()
        self.graph_2()
        self.graph_3()
        self.graph_4()

        style_btn = "QPushButton {color: rgb(0, 0, 0); background-color : rgb(200, 200, 200)} QPushButton::hover {background-color: rgb(255, 255, 255)}"

        self.btn_back.setStyleSheet(style_btn)