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

import numpy as np
import json
import math

import ui_rabota
import ui_administrator
import ui_peleng
import ui_perehvat

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


class MainScreen(QDialog):

    signal_goto_theory   = pyqtSignal()
    signal_goto_test     = pyqtSignal()
    signal_current_freq  = pyqtSignal(float)

    signal_poisk = pyqtSignal()
    selected_id  = 1

    def __init__(self):
        super(MainScreen, self).__init__()

        self.init_ui()

        self.selected_freq = 150

        self.rabota_window         = ui_rabota.RabotaScreen()
        self.administrator_window  = ui_administrator.AdministratorScreen()
        self.peleng_window         = ui_peleng.PelengScreen()
        self.perehvat_window       = ui_perehvat.PerehvatScreen()

        self.perehvat_window.set_data(signals, filtered_freqs, self.selected_freq)

        self.btn_theory.clicked.connect(self.goto_theory)

        self.btn_rabota.clicked.connect(self.show_rabota)
        self.btn_administrator.clicked.connect(self.show_administrator)
        self.btn_peleng.clicked.connect(self.show_peleng)
        self.btn_perehvat.clicked.connect(self.show_perehvat)

        self.btn_tehanaliz.clicked.connect(self.update_perehvat)

        self.btn_poisk.clicked.connect(self.poisk)
        self.btn_poisk2.clicked.connect(self.poisk2)


    def goto_theory(self):
        self.signal_goto_theory.emit()

    def goto_test(self):
        self.signal_goto_test.emit()

    def update_perehvat(self):
        self.perehvat_window.set_data(signals, filtered_freqs, self.selected_freq)
    
    def poisk(self):
        self.search()
        self.signal_poisk.emit()
        self.lbl_peleng.setText("-")
        
    def poisk2(self):
        self.search()
        self.lbl_peleng.setText(str(data[str(self.selected_id)]["bearing"]))

    def show_rabota(self):
        self.rabota_window.show()

    def show_administrator(self):
        self.administrator_window.show()  

    def show_peleng(self):
        self.peleng_window.show()

    def show_perehvat(self):
        self.perehvat_window.show()

    def init_ui(self):
        loadUi('qt\main.ui', self)
        self.setWindowTitle("RF Spectrum Analyzer")
        self.setGeometry(100, 100, 1000, 600)

        self.lbl_search_low.setValidator(QIntValidator(1, 10000, self))
        self.lbl_search_hight.setValidator(QIntValidator(1, 10000, self))

        self.graph()

        style_btn = "QPushButton {color: rgb(0, 0, 0); background-color : rgb(200, 200, 200)} QPushButton::hover {background-color: rgb(255, 255, 255)}"

        # Top
        self.btn_rabota.setStyleSheet(style_btn)
        self.btn_administrator.setStyleSheet(style_btn)
        self.btn_peleng.setStyleSheet(style_btn)
        self.btn_theory.setStyleSheet(style_btn)
        self.btn_perehvat.setStyleSheet(style_btn)
        self.btn_test.setStyleSheet(style_btn)

        # Подавление
        self.btn_z.setStyleSheet(style_btn)
        self.btn_pusk.setStyleSheet(style_btn)
        self.btn_prr.setStyleSheet(style_btn)
        self.btn_adaptiv.setStyleSheet(style_btn)
        self.btn_control.setStyleSheet(style_btn)
        self.btn_doraz.setStyleSheet(style_btn)

        # Настройки
        self.btn_c_1.setStyleSheet(style_btn)
        self.btn_c_2.setStyleSheet(style_btn)

        # Кнопки
        self.btn_poisk.setStyleSheet(style_btn)
        self.btn_poisk2.setStyleSheet(style_btn)

        self.btn_peleng_2.setStyleSheet(style_btn)
        self.btn_pauza.setStyleSheet(style_btn)

        self.btn_test_svazi.setStyleSheet(style_btn)
        self.btn_tehanaliz.setStyleSheet(style_btn)

        self.btn_send.setStyleSheet(style_btn)
        self.btn_ask_coord.setStyleSheet(style_btn)

        self.btn_empty_10.setStyleSheet(style_btn)
        self.btn_empty_11.setStyleSheet(style_btn)
        self.btn_empty_12.setStyleSheet(style_btn)
        self.btn_empty_13.setStyleSheet(style_btn)

        # Под графиком
        style_btn_1 = "QPushButton {color: rgb(150, 150, 150); background-color : rgb(200, 200, 200); font: 20pt \"MS Shell Dlg 2\"} QPushButton::hover {background-color: rgb(255, 255, 255)}"
        style_btn_2 = "QPushButton {color: rgb(150, 150, 150); background-color : rgb(200, 200, 200); font: 10pt \"MS Shell Dlg 2\"} QPushButton::hover {background-color: rgb(255, 255, 255)}"
        style_btn_3 = "QPushButton {color: rgb(150, 150, 150); background-color : rgb(200, 200, 200); font: 20t \"MS Shell Dlg 2\"} QPushButton::hover {background-color: rgb(255, 255, 255)}"
        self.btn_empty_2.setStyleSheet(style_btn_1)
        self.btn_empty_3.setStyleSheet(style_btn_2)
        self.btn_empty_4.setStyleSheet(style_btn_1)
        self.btn_empty_5.setStyleSheet(style_btn_1)
        self.btn_empty_6.setStyleSheet(style_btn_1)
        self.btn_empty_7.setStyleSheet(style_btn_1)
        self.btn_empty_8.setStyleSheet(style_btn_1)
        self.btn_empty_9.setStyleSheet(style_btn_3)

    def update(self, frame):
        base[:, :] = np.roll(base, shift=-2, axis=0)
        base[:, :] = np.clip(base, 0, None)
        for signal in signals.values():
            local_matrix = signal.signal_matrix
            local_matrix[:, :] = np.roll(local_matrix, shift=-2, axis=0)
            local_matrix[:, :] = np.clip(local_matrix, 0, None)
        filter_signal()
        self.cax.set_data(filtered_signal)
        if self.selected_freq is not None and low_freq <= self.selected_freq <= high_freq:
            self.selected_line.set_xdata([self.selected_freq, self.selected_freq])
            self.selected_line.set_ydata([time.min(), time.max()])
        else:
            self.selected_line.set_xdata([])
            self.selected_line.set_ydata([])
        return self.cax, self.selected_line

    def graph(self):
        self.control_layer = self.Twidget
        self.control_layer = QGridLayout(self.control_layer)
        
        colors = [(0, 0, 0.2), (0, 0, 0.5), (0, 0.6, 0), (1, 1, 0), (1, 0, 0)]
        hdsdr_cmap = LinearSegmentedColormap.from_list("hdsdr", colors, N=256)

        self.figure, self.ax = plt.subplots(figsize=(10, 5))
        self.canvas = FigureCanvas(self.figure)
        self.control_layer.addWidget(self.canvas)
        self.figure.patch.set_facecolor((35/256, 38/256, 50/256))
        self.cax = self.ax.imshow(filtered_signal, aspect='auto', cmap=hdsdr_cmap, vmin=0, vmax=120, origin='upper', extent=[low_freq, high_freq, time.max(), time.min()])
        self.ax.set_xlabel("Frequency [MHz]")
        self.ax.set_ylabel("Time [s]")

        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.title.set_color('white')

        self.ax.set_title(f"RF Spectrum ({low_freq:.1f} - {high_freq:.1f} MHz)")

        self.selected_line, = self.ax.plot([], [], color='red', linestyle='-', linewidth=2)
        self.selected_freq = None

        self.canvas.mpl_connect("button_press_event", self.on_click)
        self.canvas.mpl_connect("scroll_event", self.on_scroll)

        self.ani = animation.FuncAnimation(self.figure, self.update, interval=25, blit=False)

        radial = FigureCanvas(self.figure)

        self.control_layer.addWidget(radial,0,0)

    def on_click(self, event):

        mod =  self.cb_mod.currentText()
        if event.xdata is not None:
            self.selected_freq = event.xdata
            self.lbl_frequency.setText(f"{self.selected_freq:.2f}")
            up = self.selected_freq + 0.4
            down = self.selected_freq - 0.4
            found = False
            for id, sig in signals.items():
                if down <= sig.freq <= up:
                    self.selected_id = id
                    if data[str(id)]["mod"] == mod:
                        self.lbl_output.setText(data[str(id)]["text"])  # Обновляем поле id
                    else:
                        self.lbl_output.setText("𐂧𑀤𐂨𑀥𐂩𑀦𐂪𑀧𐂫𑀨𐂬𑀩𐂭𑀪𐂮𑀫𐂯𑀬𐂰𑀭𐂱𑀮𐂲𑀯𐂳𑀰\n𐂴𑀱𐂵𑀲𐂶𑀳𐂷𑀴𐂸𑀵𐂹𑀶𐂺𑀷𐂻𑀸𐂼𑀹𐂽𑀺𐂾𑀻𐂿𑀼𐃀𑀽𐃁𑀾𐃂𑀿𐃃\n𑁀𐃄𑁁𐃅𑁂𐃆𑁃𐃇𑁄𐃈𑁅𐃉𑁆𐃊")
                    # self.id_display.setText(f"{self.selected_id}")
                    found = True
                    break
            if not found:
                self.selected_id = None
                # self.id_display.setText("")
            self.update(None)

    def on_scroll(self, event):
        global low_freq, high_freq
        scroll_step = 2.0
        if event.step > 0:
            base[:, :] = np.roll(base, shift=-15, axis=1)
            base[:, :] = np.clip(base, 0, None)
            low_freq = low_freq + scroll_step
        elif event.step < 0 and low_freq > 0:
            base[:, :] = np.roll(base, shift=15, axis=1)
            base[:, :] = np.clip(base, 0, None)
            low_freq = max(low_freq - scroll_step, 0)

        high_freq = low_freq + 20
        filter_signal()
        self.cax.set_data(filtered_signal)
        self.cax.set_extent([low_freq, high_freq, time.max(), time.min()])
        self.ax.set_title(f"RF Spectrum ({low_freq:.1f} - {high_freq:.1f} MHz)")
        self.canvas.draw()

    def search(self):
        global threshold, max_power, search_low, search_hight, last_freq
        global low_freq, high_freq

        new_search_low   = int(self.lbl_search_low.text())
        new_search_hight = int(self.lbl_search_hight.text())
        new_threshold    = self.vs_porog.value() / 100

        mod =  self.cb_mod.currentText()

        self.lbl_output.setText("")
        
        # ЕСЛИ даные для поиска меняли, обновляем из
        if (not math.isclose(new_threshold,threshold)) | (not math.isclose(new_search_low, search_low)) | (not math.isclose(new_search_hight, search_hight)):
            threshold = new_threshold
            search_low = new_search_low
            search_hight = new_search_hight
            last_freq = 0
            power_threshold = threshold * max_power
            freqs_to_search.clear()
            for signal in signals.values():
                if (search_low <= signal.freq) & (search_hight >= signal.freq) & (signal.power > power_threshold):
                    freqs_to_search.append(signal.freq)
            freqs_to_search.sort()

        # ПРОХОДИМ по частотам и обновляем данные
        if last_freq < len(freqs_to_search):
            centr_freq = low_freq + 10
            if freqs_to_search[last_freq] > centr_freq :
                base[:, :] = np.roll(base, shift=-15, axis=1)
                base[:, :] = np.clip(base, 0, None)
            else:
                base[:, :] = np.roll(base, shift=15, axis=1)
                base[:, :] = np.clip(base, 0, None)
            self.selected_freq = freqs_to_search[last_freq]

            up = self.selected_freq + 0.4
            down = self.selected_freq - 0.4
            found = False  # Флаг, чтобы отследить, найден ли сигнал
            for id, sig in signals.items():
                if (down <= sig.freq <= up): # and (data[str(id)]["mod"] == mod)
                    self.selected_id = id
                    # print(self.selected_id)
                    # self.lbl_peleng.setText(str(data[str(self.selected_id)]["bearing"]))
                    if data[str(id)]["mod"] == mod:
                        self.lbl_output.setText(data[str(id)]["text"])  # Обновляем поле id
                    else:
                        self.lbl_output.setText("𐍈ᚷ𑀓𐂦𑁦𑀢𐂧𑀤𐂨𑀥𐂩𑀦𐂪𑀧𐂫𑀨𐂬𑀩𐂭𑀪𐂮𑀫𐂯𑀬𐂰𑀭𐂱𑀮𐂲𑀯𐂳𑀰\n𐂴𑀱𐂵𑀲𐂶𑀳𐂷𑀴𐂸𑀵𐂹𑀶𐂺𑀷𐂻𑀸𐂼𑀹𐂽𑀺𐂾𑀻𐂿𑀼𐃀𑀽𐃁𑀾𐃂𑀿𐃃\n𑁀𐃄𑁁𐃅𑁂𐃆𑁃𐃇𑁄𐃈𑁅𐃉𑁆𐃊")
                    found = True
                    break
            self.lbl_frequency.setText(f"{self.selected_freq:.2f}")

            if self.selected_freq > 30:
                low_freq = self.selected_freq - 10
            else:
                low_freq = 20
            high_freq = low_freq + 20

            last_freq += 1
            if last_freq == len(freqs_to_search):
                last_freq = 0

            filter_signal()
            self.cax.set_data(filtered_signal)
            self.cax.set_extent([low_freq, high_freq, time.max(), time.min()])
            self.ax.set_title(f"RF Spectrum ({low_freq:.1f} - {high_freq:.1f} MHz)")
            self.canvas.draw()
            self.update(None)