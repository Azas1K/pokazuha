
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



    def __init__(self):
        super(TheoryScreen, self).__init__()

        self.init_ui()

    def graph_2(self):
        self.calc()

        # self.control_layer = self.widget_2
        # self.control_layer = QGridLayout(self.control_layer)

        # self.figure_2, self.ax = plt.subplots(figsize=(10, 5))
        # self.figure_2.patch.set_facecolor((210/256, 210/256, 210/256))
        # self.ax.plot(self.time, self.modulating)
        # self.ax.set_title(f'Модулирующий сигнал')
        # self.ax.set_ylabel('Амплитуда, дБ')
        # self.ax.set_xlabel('Время')

        # self.radial_2 = FigureCanvas(self.figure_2)

        # self.control_layer.addWidget(self.radial_2,0,0)

    def graph_3(self):
        self.calc()
        # self.control_layer = self.widget_3
        # self.control_layer = QGridLayout(self.control_layer)
    
        # self.figure_3, self.ax = plt.subplots(figsize=(10, 5))
        # self.figure_3.patch.set_facecolor((210/256, 210/256, 210/256))
        # self.ax.plot(self.time, self.modulated)
        # self.canvas = FigureCanvas(self.figure_3)
        # self.ax.set_title(f'Модулированный сигнал')
        # self.ax.set_ylabel('Амплитуда, дБ')
        # self.ax.set_xlabel('Время')

        # self.radial_3 = FigureCanvas(self.figure_3)

        # self.control_layer.addWidget(self.radial_3,0,0)

    def graph_4(self):
        self.calc()

        # self.control_layer = self.widget_4
        # self.control_layer = QGridLayout(self.control_layer)
        # self.figure_4, self.ax = plt.subplots(figsize=(10, 5))
        # self.figure_4.patch.set_facecolor((210/256, 210/256, 210/256))
        # self.ax.semilogy(self.freqs[:self.N // 2], self.spectrum[:self.N // 2])  # Логарифмическая шкала по оси Y
        # self.canvas = FigureCanvas(self.figure_4)
        # self.ax.set_title(f'Спектр сигнал')
        # self.ax.set_ylabel('Амплитуда, дБ')
        # self.ax.set_xlabel('Частота, МГц')

        # radial = FigureCanvas(self.figure_4)

        # self.control_layer.addWidget(radial,0,0)

    def calc(self):
        self.fc = self.qs_carrier_freq.value() / 100
        self.fm_count = self.qs_hormonics.value()
        self.mod_type = self.cb_mod.currentText()
        self.m = 0.15 # коэффициент модуляции (от 0 до 1)

        # self.modulating = self.Am[0] * np.sin(2*np.pi*self.fm[0]*self.time) # модулирующий сигнал
        # for i in range(1, self.fm_count):
        #     self.modulating += self.Am[i] * np.sin(2*np.pi*self.fm[i]*self.time)

        # if self.mod_type == "АМ":
        #     self.modulated = (1 + self.m * self.modulating) * self.carrier  # Амплитудно-модулированный сигнал
        # elif self.mod_type == "ОМ":
        #     self.modulated = (self.m * self.modulating) * self.carrier  # Амплитудно-модулированный сигнал
        # elif self.mod_type == "ЧМ":
        #     self.modulated = self.Ac * np.sin(2*np.pi*self.fc*self.time + self.m*2*np.pi*self.modulating)  # Частотно-модулированный сигнал
        # elif self.mod_type == "ЧМн":
        #     self.modulating = np.sign(np.sin(2 * np.pi * self.fm[0] * self.time))  # Двоичный модулирующий сигнал
        #     self.integral_mod = np.cumsum(self.modulating) / self.fs  # Интеграл от модулирующего сигнала
        #     self.modulated = self.Ac * np.sin(2 * np.pi * self.fc * self.time + 2000*self.m*np.pi* self.integral_mod)  # ЧМн сигнал
        # elif self.mod_type == "ФМн":
        #     self.modulating = np.sign(np.sin(2 * np.pi * self.fm[0] * self.time))  # Двоичный модулирующий сигнал
        #     self.modulated = self.Ac * np.cos(2 * np.pi * self.fc * self.time + (np.pi * (self.modulating + 1) / 2))  # ФМн сигнал 

        # СПЕКТР, Дискретное преобразование Фурье
        # self.N = len(self.time)
        # self.freqs = fftfreq(self.N, 1/self.fs)  # Частоты спектра
        # self.spectrum = np.abs(fft(self.modulated)) / self.N  # Спектр

    def graph_1(self):
        self.control_layer = self.widget
        self.control_layer = QGridLayout(self.control_layer)
    
        figure = plt.figure()
        ax = plt.axes(xlim=(0, 0.5), ylim=(-400, 400))
        
        figure.patch.set_facecolor((210/256, 210/256, 210/256))
        ax.set_title(f'Несущий сигнал')
        ax.set_ylabel('Амплитуда, дБ')
        ax.set_xlabel('Время')

        self.line1, = ax.plot([], [], lw=2)
        self.anim = FuncAnimation(figure, self.update_plot1, frames=200, interval=20, blit=True)

        self.radial_1 = FigureCanvas(figure)
        self.control_layer.addWidget(self.radial_1,0,0)

    def update_plot1(self, i):
            # carrier = Ac * np.sin(2*np.pi*fc*time) # несущий сигнал
        x = np.linspace(0, 2, 1000)
        y = self.Ac * np.sin(2*np.pi*self.fc*(x + 0.02 * i))
        self.line1.set_data(x, y)
        return self.line1,

    def update_plot2(self, frame):
        new_y_data = self.current_modulating_signal(self.t + 0.01 * frame, self.freq_modulator, self.harmonic_count)
        # self.line2.set_ydata(new_y_data)
        self.radial_2.draw_idle()

    def update_plot3(self, frame):
        new_y_data = self.current_modulated_signal(self.t + 0.01 * frame, self.freq_carrier, self.freq_modulator, self.harmonic_count)
        # self.line3.set_ydata(new_y_data)
        self.radial_3.draw_idle()

    def init_ui(self):
        loadUi('qt/theory.ui', self)

        self.graph_1()
        self.graph_2()
        self.graph_3()
        self.graph_4()

        # 
        # self.animation2 = FuncAnimation(self.radial_1, self.update_plot2, frames=200, interval=50)
        # self.animation3 = FuncAnimation(self.radial_1, self.update_plot3, frames=200, interval=50)