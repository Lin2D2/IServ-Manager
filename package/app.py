from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import sys
import os.path
from package.util.slash import slash
from package.ui.window import Window
from package.app_dialog import App_Dialog
from package.table_util import Get_Page

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
        self.payload = None
        self.active_day = "Today"
        self.main_table = window.findChild(QtWidgets.QTableWidget, 'tableWidget')

        line_edit = window.findChild(QtWidgets.QLineEdit, 'lineEdit')

        self.title = window.findChild(QtWidgets.QLabel, 'label')

        self.text_edit = window.findChild(QtWidgets.QTextEdit, 'textEdit')

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
            self.active_day = "Tomorow"
        elif self.change_day_button.text() == "Today":
            self.change_day_button.setText("Tomorow")
            self.active_day = "Today"
        self.set_title()
        self.set_text_edit()
        self.main_table_creator()

    def set_payload(self, username, password):
        self.payload = {'_username': username, '_password': password}
        self.get_page = Get_Page(self.payload)
        self.set_title()
        self.set_text_edit()
        self.main_table_creator()


    def update(self):
        print("update")
        self.get_page.update()
        self.set_title()
        self.set_text_edit()
        self.main_table_creator()

    def settings(self):
        print("settings")


    def accept_line(self):
        print("accept line")

    def set_title(self):
        if self.active_day == "Tomorow":
            self.title.setText(self.get_page.title_tomorow)
        else:
            self.title.setText(self.get_page.title_today)

    def set_text_edit(self):
        if self.active_day == "Tomorow":
            self.text_edit.setText(self.get_page.massage_tomorow)
        else:
            self.text_edit.setText(self.get_page.massage_today)

    def main_table_creator(self):
        table = []

        if self.active_day == "Tomorow":
            table_content = self.get_page.content_tomorow
        else:
            table_content = self.get_page.content_today

        for row in table_content:
            colums = row.split("|")
            del colums[0]
            table.append(colums)
        del table[0]
        del table[0]
        self.main_table.setRowCount(len(table_content))
        for rows in table:
            row = rows
            for colum in row:
                self.main_table.setItem(table.index(rows), row.index(colum), QTableWidgetItem(colum))
