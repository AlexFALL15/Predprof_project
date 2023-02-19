import json
import sys
from datetime import datetime

import requests
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QMessageBox
from bs4 import BeautifulSoup

from database import *
from graph_ui import UiForm

URLSTART = 'http://esp8266.local/start'
URLSTOP = 'http://esp7266.local/dowload'


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
        self.current_race = ''
        d = datetime.now()
        self.date = f'{d.year}-{d.month}-{d.day}'
        self.json = {}
        self.comp = True
        self.racer = ''
        self.racers = []
        self.label_4.setText(self.date)

        self.pushButton.clicked.connect(self.make_race)
        self.pushButton.setDisabled(True)
        self.pushButton_2.clicked.connect(self.start)
        self.pushButton_2.setDisabled(True)
        self.pushButton_3.clicked.connect(self.graph)
        self.pushButton_3.setDisabled(True)
        self.pushButton_4.clicked.connect(self.make_comp)
        self.pushButton_5.clicked.connect(self.un_log_in)

    def make_comp(self):
        if self.lineEdit.text() == '' or self.lineEdit_2.text() == '' or self.racer_1.text() == '' or self.racer_2.text() == '':
            QMessageBox.critical(self, "Ошибка ",
                                 "Не веденно название соревнования или организатор соревнования или не указан один из номеров гонщиков",
                                 QMessageBox.Ok)
        else:
            self.lineEdit.setDisabled(True)
            self.lineEdit_2.setDisabled(True)
            self.racer_1.setDisabled(True)
            self.racer_2.setDisabled(True)
            self.pushButton_4.setDisabled(True)
            self.pushButton.setDisabled(False)
            self.setWindowTitle(self.lineEdit.text())
            self.racers = [self.racer_1.text(), self.racer_2.text()]
            self.label_8.setText(f'{self.racers[0]} - w')
            self.label_9.setText(f'{self.racers[1]} - r')
            if not check_in(self.lineEdit.text, self.lineEdit_2.text(), self.date, f'{self.lineEdit.text()}.json'):
                make_stroke(self.lineEdit.text(), self.lineEdit_2.text(), self.date, f'{self.lineEdit.text()}.json')
            self.comp = False
            try:
                with open(f'{self.lineEdit.text()}.json') as f:
                    self.json = json.load(f)
            except Exception:
                self.json = {self.racer_1.text(): {i: None for i in self.race_type},
                             self.racer_2.text(): {i: None for i in self.race_type}}

    def un_log_in(self):
        self.lineEdit.setDisabled(False)
        self.lineEdit_2.setDisabled(False)
        self.racer_1.setDisabled(False)
        self.racer_2.setDisabled(False)
        self.pushButton_4.setDisabled(False)
        self.pushButton_2.setDisabled(True)
        self.pushButton_3.setDisabled(True)
        self.setWindowTitle('Новое соревнования')
        self.comp = True
        self.current_race = ''
        self.json = {i: None for i in self.race_type}

    def make_race(self):
        self.select_racer()
        race_type, ok_pressed = QInputDialog.getItem(
            self, "ВЫБОР", "Выберете тип гонки",
            self.race_type, 1, False)
        if ok_pressed:
            self.current_race = race_type
            self.label_7.setText(f'{self.label_7.text()} {self.current_race}')
            if self.json[self.racer][self.current_race] != '':
                self.pushButton_2.setDisabled(True)
                self.pushButton_3.setDisabled(False)
            else:
                self.pushButton_3.setDisabled(True)
                self.pushButton_2.setDisabled(False)

    def select_racer(self):
        racer, ok_pressed_1 = QInputDialog.getItem(
            self, "ВЫБОР", "Выберите гонщика для измерения",
            self.racers, 1, False)
        if ok_pressed_1:
            self.racer = racer

    def start(self):
        if self.json[self.racer][self.current_race] is None:
            self.pushButton_2.setDisabled(True)
            time = int(self.label_3.text())
            requests.get(URLSTART)
            if time > 0:
                self.label_3.setText(f"{time - 1}")
                QTimer().singleShot(1000, self.start)
            else:
                self.label_3.setText('30')
                page = requests.get(URLSTOP)
                soup = BeautifulSoup(page.text, 'html.parser')
                d = list(map(int, soup.findAll('br')))
                self.json[self.racer][self.current_race] = d
                with open(f'{self.lineEdit.text()}.json', 'w+') as f:
                    json.dump(self.json, f)
                self.pushButton_3.setDisabled(False)

    def graph(self):
        if self.current_race != 'Qualification':
            QMessageBox.critical(self, "Ошибка ",
                                 "Не сделано замеров второго гонщика",
                                 QMessageBox.Ok)
            self.racers.pop(self.racers.index(self.racer))
            self.select_racer()
            self.start()
            self.racers = [self.racer_1.text(), self.racer_2.text()]
        with open(f'{self.lineEdit.text()}.json', 'r') as f:
            data = json.load(f)
        if self.current_race == 'Qualification':
            self.graphicsView.plot([i for i in range(len(data[self.racer][self.current_race]))],
                                   [i for i in data[self.racer][self.current_race]], pen='w')
        else:
            self.graphicsView.plot([i for i in range(len(data[self.racer][self.current_race]))],
                                   [i for i in data[self.racer_1.text()][self.current_race]], pen='w')
            self.graphicsView.plot([i for i in range(len(data[self.racer][self.current_race]))],
                                   [i for i in data[self.racer_2.text()][self.current_race]], pen='r')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
