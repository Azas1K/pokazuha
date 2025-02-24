from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import*

from PyQt5.uic import loadUi

from PyQt5 import QtWidgets
from PyQt5 import QtCore

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import numpy as np


class PelengScreen(QDialog):

    def __init__(self):
        super(PelengScreen, self).__init__()

        self.init_ui()

    def plot_(self):
        # background_image = Image.open("img/map.jpg")

        # width, height = background_image.size
        # min_size = min(width, height)
        # left = (width - min_size) // 2
        # top = (height - min_size) // 2
        # right = (width + min_size) // 2
        # bottom = (height + min_size) // 2
        # background_image = background_image.crop((left, top, right, bottom))
        # background_image = background_image.resize((1000, 1000))

        # background_array = np.array(background_image)

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.set_facecolor((1.0, 0.47, 0.42))
        fig.patch.set_facecolor((35/256, 38/256, 50/256))

        # ax.imshow(background_array, extent=[-1, 1, -1, 1], alpha=0.6)
        ax.axis('off')  

        polar_ax = fig.add_axes(ax.get_position(), projection='polar', frameon=False)
        polar_ax.set_theta_zero_location('N')
        polar_ax.set_theta_direction(-1)

        rings = np.linspace(0.15, 1.0, 2)
        # rings = np.linspace(0.15, 1.0, 2)
        polar_ax.set_yticks(rings)
        # polar_ax.grid(color='white', linestyle='-', linewidth=1.0)

        polar_ax.tick_params(axis='x', colors='white')
        polar_ax.tick_params(axis='y', colors='white')

        yax = ax.axes.get_xaxis()
        yax = yax.set_visible(False)

        # polar_ax.yaxis.set_ticks_position('none')
        # polar_ax.xaxis.label.set_color('white')
        # polar_ax.yaxis.label.set_color('white')
        # polar_ax.title.set_color('white')

        bearing_angle = np.radians(90.5)
        polar_ax.plot([bearing_angle, bearing_angle], [0, 1], color='#FF2222', linewidth=4, zorder=1)

        bearing_angle = np.radians(180.5)
        polar_ax.plot([bearing_angle, bearing_angle], [0, 1], color='#FF2222', linewidth=4, zorder=1)

        angle_label = f"{int(np.degrees(bearing_angle))}°"
        polar_ax.annotate(angle_label, xy=(bearing_angle, 1.05), xytext=(bearing_angle, 1.1),
                        ha='center', va='bottom', fontsize=12, color='white', weight='bold',
                        bbox=dict(boxstyle='round,pad=0.1', fc='r', ec='none', alpha=0.7))
        


        # polar_ax.scatter(0, 0, color='#FF0000', s=100, zorder=2)

        # compass_ax = fig.add_axes([0.75, 0.7, 0.15, 0.15])
        # compass_ax.axis('off')

        # compass_ax.arrow(0.4, 0.4, 0, 0.4, head_width=0.01, head_length=0.2, fc='black', ec='black')

        # compass_ax.text(0.4, 0.9, 'N', ha='center', va='bottom', fontsize=14, color='red', weight='bold')

        # fig.patch.set_facecolor((1, 1, 1))
        radial = FigureCanvas(fig)

        self.control_layer.addWidget(radial,0,0)

    def table_(self):
        table = QTableWidget(self)
        table.setStyleSheet("background-color: rgb(100,100,100)")
        table.setColumnCount(2)
        table.setRowCount(5)

        table.setHorizontalHeaderLabels(["Частота", "Пеленгат"])
        
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        delegate = AlignCenter(table)
        table.setItemDelegateForColumn(0, delegate)
        table.setItemDelegateForColumn(1, delegate)
        self.control_layer.addWidget(table,0,1)

    def button_(self):
        button = QPushButton("Очистить", self)
        style_btn = "QPushButton {color: rgb(0, 0, 0); background-color : rgb(255, 255, 255)} QPushButton::hover {background-color: rgb(200, 200, 200)}"
        button.setStyleSheet(style_btn)

        self.control_layer.addWidget(button,1,1)

    def add_peleng(self, data):
        pass


    def init_ui(self):
        loadUi('qt/peleng.ui', self)

        self.control_layer = self.Twidget
        self.control_layer = QGridLayout(self.control_layer)

        self.plot_()        

        table = self.tableWidget
        table.setStyleSheet("background-color: rgb(255,255,255)")
        table.setRowCount(20)
        
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        delegate = AlignCenter(table)
        table.setItemDelegateForColumn(0, delegate)
        table.setItemDelegateForColumn(1, delegate) 


        style_btn = "QPushButton {color: rgb(0, 0, 0); background-color : rgb(200, 200, 200)} QPushButton::hover {background-color: rgb(255, 255, 255)}"

        self.btn_clear.setStyleSheet(style_btn)
        self.btn_usr.setStyleSheet(style_btn)
        self.btn_close.setStyleSheet(style_btn)
        self.btn_peleng.setStyleSheet(style_btn)

        self.setFixedWidth(800)
        self.setFixedHeight(570)


class AlignCenter(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignCenter, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter

