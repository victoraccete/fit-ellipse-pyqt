import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QPushButton, QScrollArea, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QBrush, QPen, QPolygon
from PyQt5.QtCore import pyqtSlot, QPoint, Qt
from PyQt5 import QtWidgets, QtCore
import cv2
import numpy as np
import matplotlib.pyplot as plt


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Ellipse Fit'
        self.left = 200
        self.top = 50
        self.width = 300
        self.height = 300
        self.initUI()
        self.mouse_coords = []
        self.points = QPolygon()
        self.image_path = ""
        self.ellipse = None
        self.image = None

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create widget
        button_browse_img = QPushButton('Browse Image', self)
        button_browse_img.setToolTip('This is load picture button')
        button_browse_img.move(10, 10)
        button_browse_img.clicked.connect(self.browse_image)

        self.label = QLabel(self)
        self.label.move(10,50)

        self.show()

    def mousePressEvent(self, QMouseEvent):
        mouse_coords = QMouseEvent.pos()
        #print(QMouseEvent.pos())
        self.mouse_coords.append(mouse_coords)
        print(self.mouse_coords)
        self.points << QMouseEvent.pos()
        self.update()

  
    def paintEvent(self, QMouseEvent):
        def int_tup(tup, divide_by=1):
            '''This function is needed because cv2.ellipse funcion
            requires that center and axes are tuples of integers'''
            return int(tup[0]//divide_by), int(tup[1]//divide_by)

        qp = QPainter(self)
        pixmap = QPixmap(self.image_path)
        qp.drawPixmap(self.rect(), pixmap)
        #self.label.adjustSize()
        pen = QPen(Qt.red, 3)
        brush = QBrush(Qt.red)
        qp.setPen(pen)
        qp.setBrush(brush)

        for i in range(self.points.count()):
            qp.drawEllipse(self.points.point(i), 3, 3)
            if len(self.mouse_coords) == 5:
                points = self.get_all_coords()
                ellipse = cv2.fitEllipse(points)
                self.ellipse = ellipse
                e0 = int_tup(ellipse[0])
                e1 = int_tup(ellipse[1], divide_by=2)
                e2 = ellipse[2]
                drawn_ellipse = cv2.ellipse(self.image, e0, e1, e2, 0.0, 
                            360.0, (0, 0, 0), 2)
                cv2.namedWindow('Image with ellipse', cv2.WINDOW_NORMAL)
                cv2.resizeWindow('Image with ellipse', pixmap.width(), pixmap.height())
                cv2.imshow('Image with ellipse', drawn_ellipse)
                self.mouse_coords = []


        # or 
        #qp.drawPoints(self.points)

    def get_coords_xy(self, QPoint):
        x = QPoint.x()
        y = QPoint.y()
        return x, y

    def get_all_coords(self):
        all_coords = []
        for coords in self.mouse_coords:
            all_coords.append(self.get_coords_xy(coords))
        return np.array(all_coords)

    @pyqtSlot()
    def browse_image(self):
        print('PyQt5 button click')
        image = QFileDialog.getOpenFileName(None, 'OpenFile', '', "Image file(*.jpg *.jpeg *.png *.tif *.tiff *.bmp *.eps)")
        if image[0] != "":
            imagePath = image[0]
            self.image_path = imagePath
            self.image = cv2.imread(self.image_path)
            pixmap = QPixmap(imagePath)
            self.width = pixmap.width()
            self.height = pixmap.height()
            #self.resize(pixmap.width(), pixmap.height())
            #self.showMaximized()
            self.setFixedSize(pixmap.width(), pixmap.height())
            self.setFixedSize(self.size())
            self.label.adjustSize()
            self.mouse_coords = [] # resetting mouse_coords list everytime it loads a new image
            self.points = QPolygon() # resetting QPolygon everytime it loads a new image
            print(imagePath)
        else:
            print("No file selected.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())