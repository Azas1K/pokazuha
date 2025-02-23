from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal

import ui_main 

class QT_Controler(QObject):

    signal_poisk = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)

        self.widget   = QtWidgets.QStackedWidget()
        self.main     = ui_main.MainScreen()

        self.run()

    def run(self):
        self.widget.addWidget(self.main)
        self.widget.show()