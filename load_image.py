import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QBrush, QPen, QPolygon
from PyQt5.QtCore import pyqtSlot, QPoint, Qt

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Ellipse Fit'
        self.left = 200
        self.top = 50
        self.width = 640
        self.height = 480
        self.initUI()
        self.mouse_coords = []
        self.points = QPolygon()

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
        print(QMouseEvent.pos())
        self.mouse_coords.append(mouse_coords)
        print(self.mouse_coords)
        self.points << QMouseEvent.pos()
        self.update()
  
    def paintEvent(self, QMouseEvent):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.red, 3)
        brush = QBrush(Qt.red)
        qp.setPen(pen)
        qp.setBrush(brush)
        #for i in range(self.points.count()):
        #    qp.drawEllipse(self.points.point(i), 3, 3)
        # or 
        qp.drawPoints(self.points)

    @pyqtSlot()
    def browse_image(self):
        print('PyQt5 button click')
        image = QFileDialog.getOpenFileName(None, 'OpenFile', '', "Image file(*.jpg *.png)")
        imagePath = image[0]
        pixmap = QPixmap(imagePath)
        self.label.setPixmap(pixmap)

        self.resize(pixmap.width()+25, pixmap.height()+25)
        self.label.adjustSize()
        self.mouse_coords = [] # resetting mouse_coords list everytime it loads a new image
        self.points = QPolygon() # resetting QPolygon everytime it loads a new image

        print(imagePath)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())