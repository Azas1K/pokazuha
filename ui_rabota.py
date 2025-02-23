from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt, QTimer, QSize, QPoint
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTabWidget, QComboBox,
                             QSlider, QLabel, QDoubleSpinBox, QProgressBar, QLineEdit, QTextEdit,
                             QHBoxLayout, QSizePolicy, QRadioButton, QButtonGroup, QFileDialog)
from PyQt5.QtGui import QPainter, QPen, QFont, QPixmap, QImage
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class RabotaScreen(QDialog):

    def __init__(self):
        super(RabotaScreen, self).__init__()
        self.init_ui()

    def init_ui(self):
        loadUi('qt/rabota.ui', self)


        # self.control_tab = self.Twidget
        # self.control_layer = QVBoxLayout(self.control_tab)
        # self.Qbox = QHBoxLayout()
        # self.control_layer.addLayout(self.Qbox)

        # bar_colors     = ['#333333', '#444444', '#555555', '#666666', '#777777', '#888888', '#999999', '#AA0000']
        # num_obs        = len(bar_colors)

        # # Make up some data
        # wind_direction = (2*3.14)*(np.random.random_sample(num_obs))
        # wind_speed = 50 * np.random.random_sample(num_obs)
        # wind = zip(wind_direction, wind_speed, bar_colors) # polar(theta,r)

        # fig_test_modulation, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        # # fig_test_modulation.set_theta_zero_location('N')
        # ax.vlines(wind_direction, 0, wind_speed, colors=bar_colors, zorder=3)
        # ax.grid(True)
        # # Add the figure to a canvas
        # radial = FigureCanvas(fig_test_modulation)
        # self.Qbox.addWidget(radial)


