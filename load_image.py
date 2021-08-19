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
        self.image = np.array([0])
        self.resized = False
        screen = app.primaryScreen()
        self.screen_size = screen.size()
        #print('Size: %d x %d' % (size.width(), size.height()))

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
        if self.image.any() != False:
            pixmap = pixmap.scaled(self.image.shape[0], self.image.shape[1], Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label.adjustSize()
        qp.drawPixmap(self.rect(), pixmap)
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
                self.image = cv2.imread(self.image_path)
                drawn_ellipse = cv2.ellipse(self.image, e0, e1, e2, 0.0, 
                            360.0, (0, 0, 0), 2)
                cv2.namedWindow('Image with ellipse', cv2.WINDOW_NORMAL)
                cv2.resizeWindow('Image with ellipse', self.image.shape[1], self.image.shape[0])
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

    def need_to_resize(self):
        if(self.image.shape[0] >= self.screen_size.width() or 
            self.image.shape[1] >= self.screen_size.height()):
            return True
        else:
            return False

    def resize_image(self):
        print("Resizing image.")
        width = self.image.shape[0]
        height = self.image.shape[1]
        self.image = cv2.resize(self.image, dsize=(int(height/1.10), int(width/1.10)))
        print("Current size: %d x %d" % (self.image.shape[0], self.image.shape[1]))
        self.resized = True
        if self.need_to_resize() == True:
            print("Resizing again...")
            self.resize_image()
        else:
            return None

    @pyqtSlot()
    def browse_image(self):
        print('PyQt5 button click')
        image = QFileDialog.getOpenFileName(None, 'OpenFile', '', "Image file(*.jpg *.jpeg *.png *.tif *.tiff *.bmp *.eps)")
        if image[0] != "":
            imagePath = image[0]
            self.image_path = imagePath
            self.image = cv2.imread(self.image_path)
            print('Screen Size: %d x %d' % (self.screen_size.width(), self.screen_size.height()))
            print('Image Size: %d x %d ' % (self.image.shape[0], self.image.shape[1]))
            if self.need_to_resize() == True:
                print("Image resizing required.")
                self.resize_image()
                print('New size: %d x %d ' % (self.image.shape[0], self.image.shape[1]))
            
            extension = self.image_path.split('.')[1]
            print("File extension: ", extension)
            cv2.imwrite('temp.' + extension, self.image)
            print("New temp image generated.")
            self.image_path = 'temp.' + extension
            pixmap = QPixmap(self.image_path)
            if self.resized == True:
                pixmap = pixmap.scaled(self.image.shape[0], self.image.shape[1], Qt.KeepAspectRatio, Qt.FastTransformation)
            self.width = pixmap.width()
            self.height = pixmap.height()
            #self.resize(pixmap.width(), pixmap.height())
            #self.showMaximized()
            self.setFixedSize(pixmap.width(), pixmap.height())
            self.setFixedSize(self.size())
            self.label.adjustSize()
            self.mouse_coords = [] # resetting mouse_coords list everytime it loads a new image
            self.points = QPolygon() # resetting QPolygon everytime it loads a new image
            print(self.image_path)
        else:
            print("No file selected.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())