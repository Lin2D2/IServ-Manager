from PyQt5 import QtWidgets, uic
from package.util.slash import slash

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi('designer' + slash + 'mainwindow.ui', self)
        self.show()