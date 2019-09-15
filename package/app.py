from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import sys
import os.path
import keyring
import json
from package.util.slash import slash
from package.util.datetime_day import date_and_day
from package.ui.window import Window
from package.app_dialog import App_Dialog
from package.tableutil import TableUtil

class App():
    def __init__(self):
        self._service_name = "IServ-Manager"
        app = QtWidgets.QApplication(sys.argv)
        window = Window()

        self.change_day_button = window.findChild(QtWidgets.QPushButton, 'pushButton_change_day')
        self.change_day_button.clicked.connect(self.change_day)
        update_button = window.findChild(QtWidgets.QPushButton, 'pushButton_update')
        update_button.clicked.connect(self.update)
        settings_button = window.findChild(QtWidgets.QPushButton, 'pushButton_settings')
        settings_button.clicked.connect(self.settings)
        self.accept_line_button = window.findChild(QtWidgets.QPushButton, 'pushButton_accept_line')
        self.accept_line_button.clicked[bool].connect(self.accept_line)

        self.table_util = None
        self.filter_activated = False
        self.payload = None
        self.active_day = "Today"
        self.main_table = window.findChild(QtWidgets.QTableWidget, 'tableWidget')

        self.line_edit = window.findChild(QtWidgets.QLineEdit, 'lineEdit')
        self.line_edit.editingFinished.connect(self.line_edit_changed)

        self.title = window.findChild(QtWidgets.QLabel, 'label')
        self.title.setText(date_and_day())

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
        else:
            with open('package' + slash + 'util' + slash + 'settings.json', "r") as json_file:
                data = json.load(json_file)
                self.payload = {'_username': data["users"][0]["_username"], '_password': None}
            self.get_user_keyring_password(self.payload["_username"])
            self.set_payload(self.payload["_username"], self.payload["_password"])

    def get_user_keyring_password(self, username):
        self.payload = {'_username': username, '_password': keyring.get_password(self._service_name, username)}

    def set_user_keyring_password(self):
        keyring.set_password(self._service_name, self.payload["_username"], self.payload["_password"])
        with open('package' + slash + 'util' + slash + 'settings.json', "w+") as json_file:
            data = {}
            data["users"] = []
            data["users"].append({"_username": self.payload["_username"]})

            json.dump(data, json_file)

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
        self.table_util = TableUtil(self.payload)
        self.set_title()
        self.set_text_edit()
        self.main_table_creator()


    def update(self):
        self.table_util.update()
        self.set_title()
        self.set_text_edit()
        self.main_table_creator()

    def settings(self):
        print("settings")

    def line_edit_changed(self):
        self.table_util.set_filter(self.line_edit.text())
        self.main_table_creator()

    def accept_line(self, down):
        if down:
            self.accept_line_button.setText("Deactivated")
            self.table_util.set_filter(self.line_edit.text())
            self.filter_activated = True
            self.main_table_creator()
        else:
            self.accept_line_button.setText("Activated")
            self.filter_activated = False
            self.update()


    def set_title(self):
        if self.active_day == "Tomorow":
            self.title.setText(self.table_util.title_tomorow)
        else:
            self.title.setText(self.table_util.title_today)

    def set_text_edit(self):
        if self.active_day == "Tomorow":
            self.text_edit.setText(self.table_util.massage_tomorow)
        else:
            self.text_edit.setText(self.table_util.massage_today)

    def main_table_creator(self):
        if self.filter_activated:
            self.table_util.set_active_day(self.active_day)
            self.table_util.filter_table()
            table = self.table_util.filtered_content
        else:
            if self.active_day == "Tomorow":
                table = self.table_util.content_tomorow
            else:
                table = self.table_util.content_today

        self.main_table.setHorizontalHeaderLabels(self.table_util.table_header)
        self.main_table.setRowCount(len(table))
        for rows in table:
            row = rows
            for colum in row:
                self.main_table.setItem(table.index(rows), row.index(colum), QTableWidgetItem(colum))
