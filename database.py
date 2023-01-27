import sqlite3
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo


class Data(QSerialPort):
    def __init__(self, database_name):
        super().__init__()
        self.data = sqlite3.connect(database_name)
        self.cur = self.data.cursor()
        self.setBaudRate(115200)
        self.info = QSerialPortInfo()

    def import_data(self):
        pass
