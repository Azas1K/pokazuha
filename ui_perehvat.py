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

class PerehvatScreen(QDialog):
    
    def __init__(self):
        super(PerehvatScreen, self).__init__()
        self.init_ui()
        self.figure_sp, self.ax_sp = plt.subplots(figsize=(20, 5))
        self.ax_sp.set_facecolor('#232632')  # Темно-серый фон
        self.figure_sp.patch.set_facecolor('#232632')  # Фон всей фигуры
        self.radial = FigureCanvas(self.figure_sp)
        self.control_layer.addWidget(self.radial,0,0)

    def set_data(self, sig, filtr, freq):
        self.selected_freq = round(freq)
        if self.selected_freq == None:
            self.selected_freq = 150
        self.filtered_freqs = filtr
        self.signals = sig

        self.update_plot()

    def update_plot(self):
        scale = self.cb_diapozon.currentText()

        if scale == "MHz":
            if self.selected_freq <= 100:
                low_sp = 0
            else:
                low_sp = int(self.selected_freq) - 100
            up_sp = low_sp + 200

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
            self.ax_sp.set_xlabel('Частота', color='white')
            self.ax_sp.set_ylabel('Амплитуда (дБ)', color='white')
            self.ax_sp.grid(True)
            self.figure_sp.canvas.draw()

    def init_ui(self):
        loadUi('qt/perehvat.ui', self)

        self.control_layer = self.widget
        self.control_layer = QGridLayout(self.control_layer)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)