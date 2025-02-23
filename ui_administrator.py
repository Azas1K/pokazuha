from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import*
from PyQt5 import QtCore

class AdministratorScreen(QDialog):

    def __init__(self):
        super(AdministratorScreen, self).__init__()
        self.init_ui()

    def init_ui(self):
        loadUi('qt/administrator.ui', self)

