from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import*

class AdministratorScreen(QDialog):

    def __init__(self):
        super(AdministratorScreen, self).__init__()
        self.init_ui()

    def init_ui(self):
        loadUi('qt/administrator.ui', self)

