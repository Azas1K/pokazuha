from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal

import ui_main 
import ui_theory

class QT_Controler(QObject):

    signal_goto_theory = pyqtSignal()
    signal_goto_test   = pyqtSignal()
    signal_goto_main   = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)

        self.widget = QtWidgets.QStackedWidget()
        self.main   = ui_main.MainScreen()
        self.theory = ui_theory.TheoryScreen()
        
        self.signals()
        self.run()

    def signals(self):
        self.main.signal_goto_theory.connect(self.gotoTheoryScreen)
        self.theory.signal_goto_main.connect(self.gotoMainScreen)

    def run(self):
        self.widget.addWidget(self.main)
        self.widget.show()

    def gotoTheoryScreen(self):
        self.widget.addWidget(self.theory)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)
        
    def gotoMainScreen(self):
        self.widget.addWidget(self.main)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)