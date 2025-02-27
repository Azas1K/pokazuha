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

    selected_freq = 150
    prev_freq     = 150
    sacel         = "MHz"
    prev_scale    = "MHz"
    
    def __init__(self):
        super(PerehvatScreen, self).__init__()
        self.init_ui()

    def graph(self):
        self.control_layer = self.widget
        self.control_layer = QGridLayout(self.control_layer)
    
        figure = plt.figure()
        self.ax = plt.axes(xlim=(0, 250), ylim=(0, 150)) # ГРАНИЦЫ ГРАФИКА
        
        figure.patch.set_facecolor((210/256, 210/256, 210/256))
        self.ax.set_title('Амплитудный спектр')
        self.ax.set_xlabel('Частота (Гц)')
        self.ax.set_ylabel('Амплитуда (дБ)')

        self.line, = self.ax.plot([], [], lw=2)
        self.anim = FuncAnimation(figure, self.update_plot, frames=20, interval=200, blit=True)

        self.radial = FigureCanvas(figure)
        self.control_layer.addWidget(self.radial,0,0)


    def set_data(self, sig, filtr, freq):
        self.selected_freq = round(freq)
        self.filtered_freqs = filtr
        self.signals = sig

    def update_plot(self, z):

        self.scale = self.cb_diapozon.currentText()

        if (self.selected_freq == self.prev_freq) and (self.prev_scale == self.scale):
            return self.line,
    
        elif self.scale == "MHz":
            self.prev_freq  = self.selected_freq
            self.prev_scale = self.scale

            if self.selected_freq <= 250:
                low_sp = 0
            else:
                low_sp = self.selected_freq - 250
            up_sp = low_sp + 250
            Fs = 100*up_sp
            T = 1      # Длительность сигнала, секунда
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

            noise = np.random.normal(0, 2, size=t.shape)
            signal = signal + noise

            # Вычисление ДПФ
            spectrum = np.fft.fft(signal)
            frequencies_fft = np.fft.fftfreq(len(signal), 1 / Fs)
            # Используем только положительные частоты
            half_index = len(frequencies_fft) // 2
            frequencies_fft = frequencies_fft[:half_index]
            spectrum = spectrum[:half_index]

            #Обрезаем спектр 
            mask = (frequencies_fft >= low_sp ) & (frequencies_fft <= up_sp )
            frequencies_fft = frequencies_fft[mask]
            spectrum = spectrum[mask]

            y = 20 * np.log10(np.abs(spectrum))
        elif self.scale == "kHz":
            self.prev_freq  = self.selected_freq
            self.prev_scale = self.scale

            Fs = 250
            T = 1      # Длительность сигнала, секунда
            t = np.linspace(0, T, int(Fs * T), endpoint=False)  # Временной вектор
            y = 20 * np.sin(200*t) +80

        x = np.linspace(0, 250, 251)


        self.line.set_data(x[0:250], y[0:250])
        return self.line,


    def init_ui(self):
        loadUi('qt/perehvat.ui', self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.graph()