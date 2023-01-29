import sys
from graph_ui import UiForm
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog
from PyQt5.QtCore import Qt, QTimer
import datetime
import sqlite3


class Window(QMainWindow, UiForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.title = 'Новое соревнование'
        self.setWindowTitle(self.title)
        self.current_race = None

        self.pushButton.clicked.connect(self.race)
        self.comp = True
        self.race_type = ["Qualifying", "Top 32", "Top 16", "Top 8", "Semifinal", 'Battle for the 3rd place', "Final"]
        date = f"{datetime.datetime.now().date()}"
        self.label_4.setText(date)

        self.pushButton_2.clicked.connect(self.start)
        self.pushButton_3.clicked.connect(self.graph)

    def make_race(self):
        race_type, ok_pressed = QInputDialog.getItem(
            self, "ВЫБОР", "Выберете тип гонки",
            self.race_type, 1, False)
        if ok_pressed:
            self.pushButton.setDisabled(True)
            self.current_race = race_type
            self.race_type.remove(race_type)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return and self.comp and self.lineEdit.text() != '':
            self.title = self.lineEdit.text()
            self.setWindowTitle(self.title)
            self.comp = False
            self.lineEdit.setDisabled(True)

    # Доделать взаимодействие с ардуино
    def start(self):
        self.pushButton_2.setDisabled(True)
        time = int(self.label_3.text())
        if time > 0:
            self.label_3.setText(f"{time - 1}")
            QTimer().singleShot(1000, self.start)
        else:
            self.pushButton_2.setDisabled(False)
            self.label_3.setText('60')

    def graph(self):
        pass






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())