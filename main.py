import sys
import os
from graph_ui import UiForm
from database import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QTimer
from datetime import datetime
import requests
import json
from bs4 import BeautifulSoup


URLSTART = 'http://192.168.137.122:5000/Start'
URLSTOP = 'http://127.0.0.1:5000/Stop'


class Window(QMainWindow, UiForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Новое соревнование')
        self.race_type = [
            "Qualification",
            "top 32",
            "top 16",
            "top 8",
            "Semifinal",
            "Battle for the 3rd place",
            "Final"
        ]
        self.folder = '/stats/'
        self.current_race = ''
        d = datetime.now()
        self.date = f'{d.year}-{d.month}-{d.day}'
        self.json = {i: None for i in self.race_type}
        # self.req = requests.get(URL)
        self.comp = True

        self.pushButton.clicked.connect(self.make_race)
        self.pushButton.setDisabled(True)
        self.pushButton_2.clicked.connect(self.start)
        self.pushButton_2.setDisabled(True)
        self.pushButton_3.clicked.connect(self.graph)
        self.pushButton_3.setDisabled(True)
        self.pushButton_4.clicked.connect(self.make_comp)
        self.pushButton_5.clicked.connect(self.un_log_in)
        self.select_data()
    
    def make_comp(self):
         if self.lineEdit.text() == '' or self.lineEdit_2.text() == '':
             QMessageBox.critical(self, "Ошибка ", "Не веденно название соревнования или организатор соревнования",
                                  QMessageBox.Ok)
         else:
            self.lineEdit.setDisabled(True)
            self.lineEdit_2.setDisabled(True)
            self.pushButton_4.setDisabled(True)
            self.pushButton.setDisabled(False)
            self.setWindowTitle(self.lineEdit.text())
            if not check_in(self.lineEdit.text, self.lineEdit_2.text(), self.date, f'{self.lineEdit.text()}.json'):
                make_stroke(self.lineEdit.text(), self.lineEdit_2.text(), self.date, f'{self.lineEdit.text()}.json')
                self.select_data()
            self.comp = False
            try:
                with open(self.folder + f'{self.lineEdit.text()}.json') as f:
                    self.json = json.load(f)
            except Exception:
                self.json = {i: None for i in self.race_type}

    def un_log_in(self):
        self.lineEdit.setDisabled(False)
        self.lineEdit_2.setDisabled(False)
        self.pushButton_4.setDisabled(False)
        self.pushButton_2.setDisabled(True)
        self.pushButton_3.setDisabled(True)
        self.setWindowTitle('Новое соревнования')
        self.comp = True
        self.current_race = ''
        self.json = {i: None for i in self.race_type}
        
    
    def make_race(self):
        race_type, ok_pressed = QInputDialog.getItem(
            self, "ВЫБОР", "Выберете тип гонки",
            self.race_type, 1, False)
        if ok_pressed:
            self.current_race = race_type
            if self.json[self.current_race] is not None:
                self.pushButton_2.setDisabled(True)
                self.pushButton_3.setDisabled(False)
            else:
                self.pushButton_3.setDisabled(True)
                self.pushButton_2.setDisabled(False)

    
    def start(self):
        if self.json[self.current_race] is None:
            self.pushButton_2.setDisabled(True)
            time = int(self.label_3.text())
            requests.get(URLSTART)
            if time > 0:
                self.label_3.setText(f"{time - 1}")
                QTimer().singleShot(1000, self.start)
            else:
                self.label_3.setText('60')
                page = requests.get(URLSTOP)
                soup = BeautifulSoup(page.text, 'html.parser')
                sp = soup.findAll('tr')
                d = []
                for i in sp:
                    for j in i.text.split('12544'):
                        if len(j.split('-')) == 3:
                            d.append(list(map(int, j.split('-'))))
                        else:
                            d.append(list(map(int, j.split('-')[1:])))
                self.json[self.current_race] = d
                with open(self.folder + f'{self.lineEdit.text()}.json', 'w+') as f:
                    json.dump(self.json, f)
                self.pushButton_3.setDisabled(False)

    def graph(self):
        with open(self.folder + f'{self.lineEdit.text()}.json', 'r') as f:
            data = json.load(f)
        self.graphicsView.plot([i[0] for i in data[self.current_race]], [i for i in range(1, 7)], pen='w')

    def select_data(self):
        query = "SELECT * FROM comps"
        res = sqlite3.connect('competitions.db').cursor().execute(query).fetchall()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())