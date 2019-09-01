from PyQt5 import QtWidgets
import sys
import os.path
from package.util.slash import slash
from package.ui.window import Window
from package.app_dialog import App_Dialog

class App():
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        window = Window()

        self.change_day_button = window.findChild(QtWidgets.QPushButton, 'pushButton_change_day')
        self.change_day_button.clicked.connect(self.change_day)
        update_button = window.findChild(QtWidgets.QPushButton, 'pushButton_update')
        update_button.clicked.connect(self.update)
        settings_button = window.findChild(QtWidgets.QPushButton, 'pushButton_settings')
        settings_button.clicked.connect(self.settings)
        accept_line_button = window.findChild(QtWidgets.QPushButton, 'pushButton_accept_line')
        accept_line_button.clicked.connect(self.accept_line)

        self.table_widget = window.findChild(QtWidgets.QTableWidget, 'tableWidget')
        self.table_creator("today")

        line_edit = window.findChild(QtWidgets.QLineEdit, 'lineEdit')

        statusbar = window.findChild(QtWidgets.QStatusBar, 'statusbar')
        statusbar.showMessage("Ready")

        self.first_start()

        rc = app.exec_()
        del window
        del app
        sys.exit( rc )

    def first_start(self):
        if not os.path.exists('package' + slash + 'util' + slash + 'settings.json'):
            App_Dialog()


    def change_day(self):
        if self.change_day_button.text() == "Tomorow":
            self.change_day_button.setText("Today")
            self.table_creator("Tomorow")
        elif self.change_day_button.text() == "Today":
            self.change_day_button.setText("Tomorow")
            self.table_creator("Today")


    def update(self):
        print("update")

    def settings(self):
        print("settings")

    def accept_line(self):
        print("accept line")

    def table_creator(self, day):
        table = []
        x, y = 12, 24

        self.table_widget.setRowCount(y)
        self.table_widget.setColumnCount(x)
        for rows in table:
            row = rows
            for colum in row:
                self.table_widget.setItem(table.index(rows), row.index(colum), QTableWidgetItem(colum))

