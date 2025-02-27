from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation

import numpy as np
import random

class PerehvatScreen(QDialog):
    
    def __init__(self):
        super(PerehvatScreen, self).__init__()
        self.init_ui()
        self.figure_sp, self.ax_sp = plt.subplots(figsize=(20, 5))
        self.ax_sp.set_facecolor('#232632')  # Темно-серый фон
        self.figure_sp.patch.set_facecolor('#232632')  # Фон всей фигуры
        self.radial = FigureCanvas(self.figure_sp)
        self.control_layer.addWidget(self.radial,0,0)
        self.cb_diapozon.currentTextChanged.connect(self.update_plot)

    def set_data(self, sig, filtr, freq):
        self.selected_freq = round(freq)
        if self.selected_freq == None:
            self.selected_freq = 150
        self.filtered_freqs = filtr
        self.signals = sig

        self.update_plot()

    def update_plot(self):
        scale = self.cb_diapozon.currentText()

        if scale == "МГц":
            if self.selected_freq <= 50:
                low_sp = 0
            else:
                low_sp = int(self.selected_freq) - 50
            up_sp = low_sp + 100

            Fs = 10 * up_sp
            T = 2  # Длительность сигнала, секунда
            t = np.linspace(0, T, int(Fs * T), endpoint=False)  # Временной вектор
        
            signal = np.zeros_like(t)
            for signal_data in self.signals.values():
                if signal_data.right_freq >= low_sp and signal_data.left_freq <= up_sp:
                    signal_freqs = (self.filtered_freqs + signal_data.freq - 10) # частоты сигнала
                    local_matrix = signal_data.signal_matrix
                    for i in range(0, len(signal_freqs)):  # Перебираем столбцы
                        if (low_sp <= signal_freqs[i] <= up_sp):
                            amplitude = np.mean(local_matrix[:, i])  # Вычисляем среднее значение столбца
                            if  amplitude > 0:
                                signal += amplitude * np.sin(2 * np.pi * int(signal_freqs[i]) * t)

            noise = np.random.normal(0, 1, size=t.shape)
            signal = signal + noise

            # Вычисление ДПФ
            spectrum = np.fft.fft(signal)
            frequencies_fft = np.fft.fftfreq(len(signal), 1 / Fs)

            self.ax_sp.clear()
            # График спектра сигнала
            self.ax_sp.semilogy(frequencies_fft[:len(frequencies_fft)//2], np.abs(spectrum[:len(spectrum)//2]), color='yellow')
            self.ax_sp.set_xlim(low_sp, up_sp)
            self.ax_sp.set_xticks(np.linspace(low_sp, up_sp, 17))  # Больше делений по X
            self.ax_sp.tick_params(axis='x', colors='white')  # Цвет цифр на оси X
            self.ax_sp.tick_params(axis='y', colors='white')  # Цвет цифр на оси Y
            self.ax_sp.set_xlabel('Частота, МГц', color='white')
            self.ax_sp.set_ylabel('Амплитуда (дБ)', color='white')
            self.ax_sp.grid(True)
            self.figure_sp.canvas.draw()
        else:
            if int(self.selected_freq) <= 3:
                low_sp = 0
            else:
                low_sp = int(self.selected_freq) - 3
            up_sp = low_sp + 6

            Fs = 10000
            T = 1  # Длительность сигнала, секунда
            t = np.linspace(0, T, int(Fs * T), endpoint=False)  # Временной вектор
        
            signal = np.zeros_like(t)
            for signal_data in self.signals.values():
                if signal_data.freq >= low_sp and signal_data.freq <= up_sp:
                    if signal_data.source == 'radio':
                        modulating = 0.5*np.sin(2*np.pi*100*t) + 0.2*np.sin(2*np.pi*250*t) + 0.7*np.sin(2*np.pi*300*t)     
                        if signal_data.mod == "am":
                            modulating = 0.5*np.sin(2*np.pi*100*t) + 0.2*np.sin(2*np.pi*250*t) + 0.7*np.sin(2*np.pi*300*t) +\
                                         0.5*np.sin(2*np.pi*101*t) + 0.2*np.sin(2*np.pi*279*t) + 0.7*np.sin(2*np.pi*299*t)
                            signal += signal_data.power * (1 + 0.15*modulating) * (np.sin(2*np.pi*1000*t))   # Амплитудно-модулированный сигнал
                        elif signal_data.mod == "fm":
                            modulating = 0.5*np.sin(2*np.pi*10*t) + 0.2*np.sin(2*np.pi*25*t) + 0.7*np.sin(2*np.pi*30*t) + 0.7*np.sin(2*np.pi*50*t)
                            signal += signal_data.power * np.sin(2*np.pi*1000*t + 0.3*2*np.pi*modulating)  # Частотно-модулированный сигнал
                        elif signal_data.mod == "om":
                            modulating = 0.5*np.sin(2*np.pi*100*t) + 0.2*np.sin(2*np.pi*250*t) + 0.7*np.sin(2*np.pi*300*t) +\
                                         0.5*np.sin(2*np.pi*101*t) + 0.2*np.sin(2*np.pi*279*t) + 0.7*np.sin(2*np.pi*299*t)
                            signal += signal_data.power * (0.15*modulating) * (np.sin(2*np.pi*1000*t))   # Амплитудно-модулированный сигнал
                        elif signal_data.mod == "fmn":
                            modulating = np.sign(np.sin(2 * np.pi * 10 * t))  # Двоичный модулирующий сигнал
                            integral_mod = np.cumsum(modulating) / Fs  # Интеграл от модулирующего сигнала
                            signal += signal_data.power * np.sin(2 * np.pi * 1000 * t + 2000*0.3*np.pi * integral_mod)  # ЧМн сигнал
                        elif signal_data.mod == "pmn":
                            modulating = np.sign(np.sin(2 * np.pi * 5 * t))  # Двоичный модулирующий сигнал
                            signal += signal_data.power * np.cos(2 * np.pi * 1000 * t + (np.pi * (modulating + 1) / 2))  # ФМн сигнал
                    elif signal_data.source == 'sputnik':
                        for i in range(0,11,2):
                            signal +=  random.randint(int(signal_data.power) - 10, int(signal_data.power)) * np.sin(2*np.pi*(1000 - i)*t)
                            signal +=  random.randint(int(signal_data.power) - 10, int(signal_data.power) ) * np.sin(2*np.pi*(1000 + i)*t)
                    elif signal_data.source == 'sotovy':
                        for i in range(0,200,5):
                            signal +=  random.randint(int(signal_data.power) - 15, int(signal_data.power)) * np.sin(2*np.pi*(1000 - i)*t)
                            signal +=  random.randint(int(signal_data.power) - 15, int(signal_data.power) ) * np.sin(2*np.pi*(1000 + i)*t)
                    else:
                        for i in range(0,1000,5):
                            signal +=  random.randint(int(signal_data.power) - 15, int(signal_data.power)) * np.sin(2*np.pi*(1000 - i)*t)
                            signal +=  random.randint(int(signal_data.power) - 15, int(signal_data.power) ) * np.sin(2*np.pi*(1000 + i)*t)

            noise = np.random.normal(0, 3, size=t.shape)
            signal = signal + noise

            # Вычисление ДПФ
            spectrum = np.fft.fft(signal)
            frequencies_fft = np.fft.fftfreq(len(signal), 1 / Fs)

            self.ax_sp.clear()
            # График спектра сигнала
            self.ax_sp.semilogy(frequencies_fft[:len(frequencies_fft)//2], np.abs(spectrum[:len(spectrum)//2]), color='yellow')
            self.ax_sp.set_xlim(0, 2000)
            self.ax_sp.set_xticks(np.linspace(0, 2000, 20))  # Больше делений по X
            self.ax_sp.tick_params(axis='x', colors='white')  # Цвет цифр на оси X
            self.ax_sp.tick_params(axis='y', colors='white')  # Цвет цифр на оси Y
            self.ax_sp.set_xlabel(f'Частота, + {self.selected_freq - 0.1000} * 10^3 кГц', color='white')
            self.ax_sp.set_ylabel('Амплитуда (дБ)', color='white')
            self.ax_sp.grid(True)
            self.figure_sp.canvas.draw()

    def init_ui(self):
        loadUi('qt/perehvat.ui', self)

        self.control_layer = self.widget
        self.control_layer = QGridLayout(self.control_layer)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)