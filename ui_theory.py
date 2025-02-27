
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
    fs = 10000 # частота дискретизации
    T = 1  # Длительность сигнала в секундах
    t = np.linspace(0, T, int(fs*T), endpoint=False)  # Временная ось
    Ac = 400
    Am = [1, 0.5, 0.3, 0.2, 0.1] # амплитуды модулирующих сигналов
    fm = [10, 20, 30, 40, 50] # частоты модулирующих сигналов
    

    signal_goto_main   = pyqtSignal()

    def __init__(self):
        super(TheoryScreen, self).__init__()
        self.init_ui()
        self.btn_back.clicked.connect(self.goto_main)
        self.qs_carrier_freq.sliderReleased.connect(self.graph_4)
        self.qs_coef_mod.sliderReleased.connect(self.graph_4)
        self.qs_hormonics.sliderReleased.connect(self.graph_4)
        self.cb_mod.activated.connect(self.graph_4)
        self.qs_hormonics.valueChanged.connect(self.graph_4)
        
    def graph_1(self):
        self.control_layer = self.widget
        self.control_layer = QGridLayout(self.control_layer)
        figure = plt.figure()
        ax = plt.axes(xlim=(0, 0.5), ylim=(-800, 800))
        figure.patch.set_facecolor((120/256, 120/256, 120/256))
        ax.set_facecolor('#232632')
        ax.set_title(f'Несущий сигнал')
        ax.set_ylabel('Амплитуда, В')
        ax.set_xlabel('Время, c')
        self.line1, = ax.plot([], [], lw=2, color='yellow')
        self.anim1 = FuncAnimation(figure, self.update_plot1, frames=200, interval=20, blit=True)

        self.radial_1 = FigureCanvas(figure)
        self.control_layer.addWidget(self.radial_1,0,0)

    def graph_2(self):
        self.control_layer = self.widget_2
        self.control_layer = QGridLayout(self.control_layer)
    
        figure = plt.figure()
        ax_2 = plt.axes(xlim=(0, 0.5), ylim=(-2, 2))
        
        figure.patch.set_facecolor((120/256, 120/256, 120/256))
        ax_2.set_facecolor('#232632')
        ax_2.set_title(f'Модулирующий сигнал')
        ax_2.set_ylabel('Амплитуда, В')
        ax_2.set_xlabel('Время, c')

        self.line2, = ax_2.plot([], [], lw=2, color='yellow')
        self.anim2 = FuncAnimation(figure, self.update_plot2, frames=200, interval=20, blit=True)

        self.radial_2 = FigureCanvas(figure)
        self.control_layer.addWidget(self.radial_2,0,0)

    def graph_3(self):
        self.control_layer = self.widget_3
        self.control_layer = QGridLayout(self.control_layer)
    
        figure = plt.figure()
        ax_3 = plt.axes(xlim=(0, 0.5), ylim=(-800, 800))

        figure.patch.set_facecolor((120/256, 120/256, 120/256))
        ax_3.set_facecolor('#232632')
        ax_3.set_title(f'Модулированный сигнал')
        ax_3.set_ylabel('Амплитуда, В')
        ax_3.set_xlabel('Время, c')

        self.line3, = ax_3.plot([], [], lw=2, color='yellow')
        self.anim3 = FuncAnimation(figure, self.update_plot3, frames=200, interval=20, blit=True)

        self.radial_3 = FigureCanvas(figure)
        self.control_layer.addWidget(self.radial_3,0,0)

    def graph_4(self):
        fc = self.qs_carrier_freq.value()
        mod_type = self.cb_mod.currentText()
        m = (self.qs_coef_mod.value() / 100)
        fm_count = int(self.qs_hormonics.value())
        modulating = self.Am[0] * np.sin(2*np.pi*self.fm[0]*self.t) # модулирующий сигнал
        for i in range(1,fm_count):
            modulating += self.Am[i] * np.sin(2*np.pi*self.fm[i]*self.t)
        plus = 0
        if mod_type == "АМ":
            signal = self.Ac * (1 + m * modulating) * (np.sin(2 * np.pi * fc * self.t))   # Амплитудно-модулированный сигнал
        elif mod_type == "ОМ":
            signal = self.Ac * (m * modulating) * 10 * (np.sin(2 * np.pi * fc * self.t))   # Амплитудно-модулированный сигнал
        elif mod_type == "ЧМ":
            signal = self.Ac * np.sin(2*np.pi*fc*self.t + m*2*np.pi*modulating)  # Частотно-модулированный сигнал
        elif mod_type == "ЧМн":
            plus = 300
            modulating = np.sign(np.sin(2 * np.pi * self.fm[0] * self.t))  # Двоичный модулирующий сигнал
            integral_mod = np.cumsum(modulating) / self.fs  # Интеграл от модулирующего сигнала
            signal = self.Ac * np.sin(2 * np.pi * fc * self.t + 2000*m*np.pi* integral_mod)  # ЧМн сигнал
        elif mod_type == "ФМн":
            plus = 150
            modulating = np.sign(np.sin(2 * np.pi * self.fm[0] * self.t))  # Двоичный модулирующий сигнал
            signal = self.Ac * np.cos(2 * np.pi * fc * self.t + (np.pi * (modulating + 1) / 2))  # ФМн сигнал

        noise = np.random.normal(0, 0.005, signal.shape)
        noisy_signal = signal + noise
        fft_spectrum = np.fft.fft(noisy_signal)
        freqs = np.fft.fftfreq(len(fft_spectrum), 1/self.fs)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.set_facecolor('#232632')
        fig.patch.set_facecolor((120/256, 120/256, 120/256))
        ax.semilogy(freqs[:len(freqs)//2], np.abs(fft_spectrum[:len(fft_spectrum)//2]), color='yellow')
        ax.set_xlim(fc - 200 - plus, fc + 200 + plus)
        ax.set_xlabel('Частота (Гц)')
        ax.set_ylabel('Амплитуда (логарифмическая шкала)')
        ax.set_title('Амплитудный спектр сигнала с шумом')
        ax.grid()
        self.canvas = FigureCanvas(fig)
        radial = FigureCanvas(fig)
        self.control_layer_4.addWidget(radial,0,0)

    def update_plot1(self, i):
        self.fc = self.qs_carrier_freq.value() / 20
        self.fm_count = int(self.qs_hormonics.value())
        x = np.linspace(0, 2, 30000)
        
        y = self.Ac * np.sin(2*np.pi*self.fc*(x + 0.0003 * i))
        self.line1.set_data(x, y)
        return self.line1,

    def update_plot2(self, i):
        self.mod_type = self.cb_mod.currentText()
        self.fm_count = int(self.qs_hormonics.value())
        x = np.linspace(0, 2, 20000)

        if self.mod_type in ("АМ", "ОМ", "ЧМ"):
            y = self.Am[0] * np.sin(2*np.pi*self.fm[0]*(x + 0.0003 * i))
            for i in range(1, self.fm_count):
                y += self.Am[i] * np.sin(2*np.pi*self.fm[i]*(x + 0.0003 * i))

        if self.mod_type in ("ЧМн", "ФМн"):
            y = np.sign(np.sin(2 * np.pi * self.fm[0]*(x + 0.0003 * i)))

        self.line2.set_data(x, y)
        return self.line2,

    def update_plot3(self, i):
        fc = self.qs_carrier_freq.value() / 20
        mod_type = self.cb_mod.currentText()
        m = (self.qs_coef_mod.value() / 100)
        fm_count = int(self.qs_hormonics.value())
        x = np.linspace(0, 2, 40000)

        carrier = self.Ac * np.sin(2*np.pi*fc*x)
        
        if mod_type in ("АМ", "ОМ", "ЧМ"):
            modulating = np.sin(2*np.pi*self.fm[0]*(x + 0.0003 * i))
            for i in range(1, fm_count):
                modulating += self.Am[i] * np.sin(2*np.pi*self.fm[i]*(x + 0.0003 * i))

        if mod_type == "АМ":
            y = (1 + m * modulating) * carrier
        elif mod_type == "ОМ":
            y = (m * modulating) * carrier
        elif mod_type == "ЧМ":
            y= self.Ac * np.sin(2*np.pi*fc*(x + 0.0003 * i) + m*2*np.pi*modulating)
        elif mod_type == "ЧМн":
            modulating = np.sign(np.sin(2 * np.pi * self.fm[0] * (x + 0.0003* i)))
            self.integral_mod = np.cumsum(modulating) / self.fs
            y = self.Ac * np.sin(2 * np.pi * fc * (x + (0.0003 + 0 )* i) + 200*(m)*np.pi* self.integral_mod)
        elif mod_type == "ФМн":
            modulating = np.sign(np.sin(2 * np.pi * self.fm[0] * (x + (0.0003 + 0 )* i)))
            y = self.Ac * np.cos(2 * np.pi * fc * (x + (0.0003 + 0 )* i) + (np.pi * (modulating + 1) / 2))

        self.line3.set_data(x, y)
        return self.line3,

    def goto_main(self):
        self.signal_goto_main.emit()

    def init_ui(self):
        loadUi('qt/theory.ui', self)
        self.control_layer_4 = self.widget_4
        self.control_layer_4 = QGridLayout(self.control_layer_4)
        self.graph_1()
        self.graph_2()
        self.graph_3()
        self.graph_4()
        style_btn = "QPushButton {color: rgb(0, 0, 0); background-color : rgb(200, 200, 200)} QPushButton::hover {background-color: rgb(255, 255, 255)}"
        self.btn_back.setStyleSheet(style_btn)