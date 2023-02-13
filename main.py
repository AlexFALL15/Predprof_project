import sys
import os
from graph_ui import UiForm
from database import make_stroke, get_file
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QMessageBox
from PyQt5.QtCore import QTimer
from datetime import datetime
import requests
import json


URL = '/Start HTTP/1.1'


class Window(QMainWindow, UiForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
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
        self.req = requests.get(URL)
        self.comp = True

        self.pushButton.clicked.connect(self.make_race)
        self.pushButton_4.clicked.connect(self.make_comp)
    
    def make_comp(self):
         if self.lineEdit.text() == '' or self.lineEdit_2.text() == '':
             QMessageBox.critical(self, "Ошибка ", "Не веденно название соревнования или организатор соревнования",
                                  QMessageBox.Ok)
         else:
            self.lineEdit.setDisabled(True)
            self.lineEdit_2.setDisabled(True)
            self.pushButton_4.setDisabled(True)
            make_stroke(self.lineEdit.text(), self.lineEdit_2.text(), self.date, f'{self.lineEdit.text()}.json')
            self.comp = False
            file_name = get_file(self.lineEdit.text())
            if os.path.isfile(file_name):
                with open(file_name) as f:
                    self.json = json.load(f)
    
    def un_log_in(self):
        self.lineEdit.setDisabled(False)
        self.lineEdit_2.setDisabled(False)
        self.pushButton_4.setDisabled(False)
        self.comp = True
        self.json = {}
        
    
    def make_race(self):
        race_type, ok_pressed = QInputDialog.getItem(
            self, "ВЫБОР", "Выберете тип гонки",
            self.race_type, 1, False)
        if ok_pressed:
            self.pushButton.setDisabled(True)
            self.current_race = race_type
    
    def start(self):
        if not self.comp and self.current_race != '':
            self.pushButton_2.setDisabled(True)
            time = int(self.label_3.text())
            if time > 0:
                self.label_3.setText(f"{time - 1}")
                QTimer().singleShot(1000, self.start)
            else:
                self.pushButton_2.setDisabled(False)
                self.label_3.setText('60')
                # if self.current_race not in self.json.keys():
                #     self.json[self] =
                #     with open(get_file(self.lineEdit.text()), 'w') as file:
                #         pass
        else:
            QMessageBox.critical(self, "Ошибка ", "Не зарегистрированно соревнование или не выбрана гонка",
                                  QMessageBox.Ok)
    
    def graph(self):
        pass
    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())