from PyQt5 import QtWidgets
import sys
from package.util.slash import slash
from package.ui.window import Dialog

class App_Dialog():
    def __init__(self, parent):
        self.parent = parent
        app = QtWidgets.QApplication(sys.argv)
        self.dialog = Dialog()
        accept_username_password = self.dialog.findChild(QtWidgets.QPushButton, 'pushButton_ok')
        accept_username_password.clicked.connect(self.dialog_ok)
        accept_username_password = self.dialog.findChild(QtWidgets.QPushButton, 'pushButton_cancel')
        accept_username_password.clicked.connect(self.dialog_cancel)
        self.username_line = self.dialog.findChild(QtWidgets.QLineEdit, 'lineEdit_username')
        self.password_line = self.dialog.findChild(QtWidgets.QLineEdit, 'lineEdit_password')
        res = app.exec_()
        del app
        del self.dialog
        sys.exit(res)

    def dialog_cancel(self):
        self.dialog.close()
        #self.dialog = None

    def dialog_ok(self):
        self.parent.set_payload(self.username_line.text(), self.password_line.text())
        self.parent.main_table_creator()
        self.dialog.close()

