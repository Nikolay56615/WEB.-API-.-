import os
import sys

import requests

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()

    def getImage(self):
        a = input('Долгота: ')
        b = input('Широта: ')
        c = input('Масштаб(от 0 до 17): ')
        map = "http://static-maps.yandex.ru/1.x/?ll=" + a + "," + b + "&spn=" + c + "," + c + "&l=map"
        response = requests.get(map)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "tmn.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, 450, 450)
        self.setWindowTitle('Большая задача по Maps API. Часть №1')

        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(450, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
