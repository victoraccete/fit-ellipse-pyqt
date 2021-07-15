import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Ellipse Fit'
        self.left = 200
        self.top = 50
        self.width = 640
        self.height = 480
        self.initUI()

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

    @pyqtSlot()
    def browse_image(self):
        print('PyQt5 button click')
        image = QFileDialog.getOpenFileName(None, 'OpenFile', '', "Image file(*.jpg *.png)")
        imagePath = image[0]
        pixmap = QPixmap(imagePath)
        self.label.setPixmap(pixmap)

        self.resize(pixmap.width()+25, pixmap.height()+25)
        self.label.adjustSize()

        print(imagePath)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())