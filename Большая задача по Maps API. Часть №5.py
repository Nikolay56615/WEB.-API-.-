import os
import sys

import requests

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.set_map = True
        self.set_sat = False
        self.set_gibrid = False
        self.m = '2'

    def initUI(self):
        self.setGeometry(300, 300, 600, 495)
        self.setWindowTitle('Большая задача по Maps API. Часть №5')

        self.image = QLabel(self)
        self.image.move(5, 40)
        self.image.resize(445, 445)

        self.place = QLineEdit(self)
        self.place.move(10, 10)
        self.place.resize(120, 23)

        self.find = QPushButton('Найти', self)
        self.find.move(135, 10)
        self.find.resize(60, 25)
        self.find.clicked.connect(self.getImage)

        self.btn = QPushButton('MAP', self)
        self.btn.move(460, 30)
        self.btn.clicked.connect(self.map)

        self.btn = QPushButton('SATELLITE', self)
        self.btn.move(460, 60)
        self.btn.clicked.connect(self.sat)

        self.btn = QPushButton('S + M', self)
        self.btn.move(460, 90)
        self.btn.clicked.connect(self.gibrid)

    def map(self):
        self.set_map = True
        self.set_sat = False
        self.set_gibrid = False
        self.getImage()

    def sat(self):
        self.set_sat = True
        self.set_map = False
        self.set_gibrid = False
        self.getImage()

    def gibrid(self):
        self.set_map = False
        self.set_sat = False
        self.set_gibrid = True
        self.getImage()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if int(self.m) < 17:
                self.m = str(int(self.m) + 1)
                self.getImage()
        if event.key() == Qt.Key_PageDown:
            if int(self.m) > 0:
                self.m = str(int(self.m) - 1)
                self.getImage()

        if event.key() == Qt.Key_Up:
            if int(self.d) < 180:
                self.d = str(int(self.d) + 1)
                self.getImage()
        if event.key() == Qt.Key_Down:
            if int(self.d) > 0:
                self.d = str(int(self.d) - 1)
                self.getImage()

        if event.key() == Qt.Key_Right:
            if int(self.s) < 90:
                self.s = str(int(self.s) + 1)
                self.getImage()
        if event.key() == Qt.Key_Left:
            if int(self.s) > 0:
                self.s = str(int(self.s) - 1)
                self.getImage()

        if event.key() == Qt.Key_Enter:
            self.getImage()

    def getImage(self):
        a = self.place.text()
        if len(a) > 0:
            self.place.setStyleSheet("background-color: white")
            geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" + a + "&format=json"
            response = requests.get(geocoder_request)
            # a = json.loads(response.content)
            # pprint(a)
            json_response = response.json()
            coord = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
            coord = ','.join(coord.split())
            if self.set_map:
                map = "http://static-maps.yandex.ru/1.x/?ll=" + coord + "&spn=" + self.m + "," + self.m + "&size=445,445&l=map&pt=" + str(
                    coord) + ",pm2rdm"
            if self.set_sat:
                map = "http://static-maps.yandex.ru/1.x/?ll=" + coord + "&spn=" + self.m + "," + self.m + "&size=445,445&l=sat&pt=" + str(
                    coord) + ",pm2rdm"
            if self.set_gibrid:
                map = "http://static-maps.yandex.ru/1.x/?ll=" + coord + "&spn=" + self.m + "," + self.m + "&size=445,445&l=skl&pt=" + str(
                    coord) + ",pm2rdm"
            response = requests.get(map)
            if not response:
                print("Ошибка выполнения запроса:")
                print(map)
                print("Http статус:", response.status_code, "(", response.reason, ")")
                sys.exit(1)
            self.map_file = "tmn.png"
            with open(self.map_file, "wb") as file:
                file.write(response.content)
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
        else:
            self.place.setStyleSheet("background-color: red")

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
