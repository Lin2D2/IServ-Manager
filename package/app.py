from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import sys
import os.path
from package.util.slash import slash
from package.ui.window import Window
from package.app_dialog import App_Dialog
from package.get_plan import get_page

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
        # temp
        self.url_s = 'https://gymherderschule.de/iserv/login_check'
        self.url_today = 'https://gymherderschule.de/iserv/infodisplay/file/23/infodisplay/0/SchuelerOnline/subst_001.htm'
        self.url_tomorow = 'https://gymherderschule.de/iserv/infodisplay/file/23/infodisplay/0/SchuelerOnline/subst_002.htm'
        # *temp
        self.payload = None
        self.table_content = None
        self.main_table = window.findChild(QtWidgets.QTableWidget, 'tableWidget')

        line_edit = window.findChild(QtWidgets.QLineEdit, 'lineEdit')

        statusbar = window.findChild(QtWidgets.QStatusBar, 'statusbar')
        statusbar.showMessage("Ready")

        self.first_start()

        rc = app.exec_()
        del window
        del app
        sys.exit(rc)

    def first_start(self):
        if not os.path.exists('package' + slash + 'util' + slash + 'settings.json'):
            App_Dialog(self)     # fist of we wont create such file because we need password an username for each session

    def change_day(self):
        if self.change_day_button.text() == "Tomorow":
            self.change_day_button.setText("Today")
            self.main_table_creator("Tomorow")
        elif self.change_day_button.text() == "Today":
            self.change_day_button.setText("Tomorow")
            self.main_table_creator("Today")

    def set_payload(self, username, password):
        self.payload = {'_username': username, '_password': password}


    def update(self):
        print("update")
        self.table_content = get_page(self.payload, self.url_s, self.url_today, self.url_tomorow)
        if self.change_day_button.text() == "Tomorow":
            self.main_table_creator("Today")
        elif self.change_day_button.text() == "Today":
            self.main_table_creator("Tomorow")

    def settings(self):
        print("settings")


    def accept_line(self):
        print("accept line")

    def main_table_creator(self, day="Today"):
        table = []

        if day == "Tomorow":
            day_num = 1
        else:
            day_num = 0

        if self.table_content == None:
            self.table_content = get_page(self.payload, self.url_s, self.url_today, self.url_tomorow)

        for row in self.table_content[day_num][2]:
            colums = row.split("|")
            del colums[0]
            table.append(colums)
        del table[0]
        del table[0]
        y = len(self.table_content[day_num][2])
        self.main_table.setRowCount(y)
        for rows in table:
            row = rows
            for colum in row:
                self.main_table.setItem(table.index(rows), row.index(colum), QTableWidgetItem(colum))
