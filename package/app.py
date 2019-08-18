from PyQt5 import QtWidgets, uic
import sys
from package.ui.window import Window

class App():
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        window = Window()
        
        change_day_button = window.findChild(QtWidgets.QPushButton, 'pushButton_change_day')
        change_day_button.clicked.connect(self.change_day)
        
        app.exec_()
        
    def change_day(self):
        print("day changed")
