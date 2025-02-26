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

    selected_freq = 1700
    
    def __init__(self):
        super(PerehvatScreen, self).__init__()
        self.init_ui()

        self.cb_diapozon.activated.connect(self.update_plot)

    def set_data(self, sig, filtr, freq):
        self.selected_freq = round(freq)
        self.filtered_freqs = filtr
        self.signals = sig

        self.update_plot()

    def update_plot(self):
        scale = self.cb_diapozon.currentText()

        if scale == "MHz":
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

            figure_sp, ax_sp = plt.subplots(figsize=(10, 5))
            # График спектра сигнала
            ax_sp.plot(frequencies_fft, 20 * np.log10(np.abs(spectrum)))
            ax_sp.set_xticks(np.linspace(low_sp, up_sp, 12))  # Больше делений по X
            ax_sp.set_title('Амплитудный спектр (800–1200 Гц)')
            ax_sp.set_xlabel('Частота (Гц)')
            ax_sp.set_ylabel('Амплитуда (дБ)')
            ax_sp.grid(True)

            self.radial = FigureCanvas(figure_sp)
            self.control_layer.addWidget(self.radial,0,0)

    def init_ui(self):
        loadUi('qt/perehvat.ui', self)

        self.control_layer = self.widget
        self.control_layer = QGridLayout(self.control_layer)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)