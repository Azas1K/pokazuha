from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from matplotlib.animation import FuncAnimation

import numpy as np
import json
import math

time = np.linspace(0, 0.2, 256) # время (y на панораме)
filtered_freqs = np.linspace(0, 20, 512) # частоты (x на панораме)
base = np.random.rand(len(time), len(filtered_freqs)) * 20 # фоновый шум
filtered_signal = [] # сигнал для отображения
# начальный диапазон частот
low_freq = 1790.0; high_freq = low_freq + 20.0
global max_power # максимальная мощность сигнала
max_power = 0.0

# ДЛЯ РЕАЛИЗАЦИИ ПОИСКА
threshold = -1.5 # Погор по мощности для прослушки (в долях от макисмума)
global last_freq # Последняя частота прослушки (её id в массиве freqs_to_search)
last_freq = 0 
freqs_to_search = []
global search_low # Нижняя частота для поиска 
search_low = 20.0
global search_hight # Верхняя частота для поиска 
search_hight = 30.0


def add_signal(signal, center_freq, bandwidth, power=3.0, signal_type="ragged"):
    time_len, freq_len = signal.shape
    full_freq_range = 20.0
    
    freq_min = max(center_freq - bandwidth / 2, center_freq - 10)
    freq_max = min(center_freq + bandwidth / 2, center_freq + 10)
    
    start_idx = int((freq_min / full_freq_range) * freq_len)
    end_idx = int((freq_max / full_freq_range) * freq_len)
    
    width = end_idx - start_idx
    width = max(10, width)

    for t in range(time_len):
        x = np.linspace(-1, 1, width)
        spectrum_slice = np.zeros(freq_len)

        if signal_type == "ragged":
            width_variation = width + int(np.random.uniform(-2, 2))
            boundary_shift = np.random.uniform(-0.4, 0.2)
            dropout_mask = np.ones_like(x)
            if np.random.rand() < 0.5:
                dropout_positions = np.random.choice(len(x), size=np.random.randint(2, 7), replace=False)
                dropout_mask[dropout_positions] = np.random.uniform(0.3, 0.4, size=len(dropout_positions))
            ripple = 3 + 0.7 * np.sin(10 * x + np.random.uniform(0, np.pi))
            envelope = np.exp(-10 * ((x + boundary_shift) ** 2)) * dropout_mask * ripple

        elif signal_type == "smooth":
            envelope = np.exp(-0.05 * x**2)
            spikes = np.random.uniform(0.5, 0.5, size=len(x))
            envelope *= spikes
            freq_shift = np.sin(2 * np.pi * x + np.random.uniform(0, np.pi)) * 0.2
            envelope *= (1 + freq_shift)
            edge_noise = np.random.uniform(0.7, 1.3, size=len(x))
            envelope *= edge_noise
            noise = np.random.uniform(0.1, 0.4, size=len(x))
            envelope += noise
            envelope *= np.random.uniform(0.9, 9.1)

        elif signal_type == "digital":
            num_stripes = 10
            stripe_height = time_len // num_stripes
            gap_height = stripe_height // 3

            if (t % stripe_height) < (stripe_height - gap_height):
                envelope = np.ones_like(x)
                speckles = np.random.uniform(0.5, 1.5, size=len(x))
                envelope *= speckles
            else:
                envelope = np.zeros_like(x)

        elif signal_type == "points":
            envelope = np.zeros_like(x)
            if np.random.rand() < 0.3:
                pos = np.random.randint(0, len(x))
                speckle_power = np.random.uniform(1.5, 2.5)
                freq_envelope = np.exp(-15 * (x - x[pos])**2)
                time_envelope = np.exp(-7 * (np.linspace(-1, 1, time_len)[t]**2))
                envelope = freq_envelope * time_envelope * speckle_power
                envelope *= np.random.uniform(0.8, 1.2, size=len(x))

        else:
            raise ValueError(f"Неизвестный тип сигнала: {signal_type}")

        if np.max(envelope) > 0:
            envelope = (envelope / np.max(envelope)) * power

        spectrum_slice[start_idx:end_idx] = envelope[:end_idx - start_idx]

        signal[t] += spectrum_slice

class SignalData:
    def __init__(self, freq, bandwidth, power, signal_type, bearing, mod, text, source, X, Y):
        self.freq = freq
        self.bandwidth = bandwidth
        self.power = power
        self.signal_type = signal_type
        self.bearing = bearing
        self.mod = mod
        self.text = text
        self.source = source
        self.X = X
        self.Y = Y

        self.left_freq = freq - bandwidth / 2
        self.right_freq = freq + bandwidth / 2        
        self.signal_matrix = self.generate_signal_matrix()
        self.update_max_power()

    def generate_signal_matrix(self):
        signal = np.zeros((len(time), len(filtered_freqs)))
        add_signal(signal, 10, self.bandwidth, self.power, self.signal_type)
        return signal
    
    def update_max_power(self):
        global max_power
        if max_power < self.power:
            max_power = self.power

def filter_signal():
    global filtered_signal
    filtered_signal = base.copy()  # Начинаем с базового шума
    
    base_freqs = filtered_freqs + low_freq # частоты для отрисовки
    for signal in signals.values():
        if signal.right_freq >= low_freq and signal.left_freq <= high_freq:
            signal_freqs = (filtered_freqs + signal.freq - 10) # частоты сигнала
            min = signal_freqs.min()
            max = signal_freqs.max()
            local_matrix = signal.signal_matrix
            j = -1
            for i in range(0, len(filtered_freqs)):  # Перебираем столбцы
                if (min <= base_freqs[i] <= max):
                    if j == -1:
                        j = np.searchsorted(signal_freqs, base_freqs[i])
                    else:
                        j = j + 1
                    filtered_signal[:, i] += local_matrix[:, j]


with open("signals.json", "r", encoding="utf-8") as file:
    data = json.load(file)
signals = {int(idx): SignalData(**info) for idx, info in data.items()}
filter_signal()


class PerehvatScreen(QDialog):

    selected_freq = 1000
    filtered_freqs = np.linspace(0, 20, 512) # частоты (x на панораме)
    
    def __init__(self):
        super(PerehvatScreen, self).__init__()

        self.init_ui()

    def graph(self):
        self.control_layer = self.widget
        self.control_layer = QGridLayout(self.control_layer)
    
        figure = plt.figure()
        self.ax = plt.axes(xlim=(0, 250), ylim=(0, 150)) # ГРАНИЦЫ ГРАФИКА
        
        figure.patch.set_facecolor((210/256, 210/256, 210/256))
        self.ax.set_title('Амплитудный спектр (800–1200 Гц)')
        self.ax.set_xlabel('Частота (Гц)')
        self.ax.set_ylabel('Амплитуда (дБ)')

        self.line, = self.ax.plot([], [], lw=2)
        self.anim = FuncAnimation(figure, self.update_plot, frames=200, interval=20, blit=True)

        self.radial = FigureCanvas(figure)
        self.control_layer.addWidget(self.radial,0,0)


    def set_freq(self, freq):
        self.selected_freq = freq

    def update_plot(self, z):

        scale = self.cb_diapozon.currentText() # ДАННЫЕ ИЗ МЕНЮШКИ С ВЫБОРОМ (МГц и кГц)


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
            for signal_data in signals.values():
                if signal_data.right_freq >= low_sp and signal_data.left_freq <= up_sp:
                    signal_freqs = (filtered_freqs + signal_data.freq - 10) # частоты сигнала
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

        x = np.linspace(0, 250, 251)
        y = 20 * np.log10(np.abs(spectrum))

        self.line.set_data(x[0:250], y[0:250])
        return self.line,

    def init_ui(self):
        loadUi('qt/perehvat.ui', self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.graph()