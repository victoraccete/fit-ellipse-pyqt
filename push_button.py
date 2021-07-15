import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel
from PyQt5.QtGui import QPixmap


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.label = QLabel("Hello")

        button = QPushButton("Press Me!")
        button.setCheckable(True)
        button.clicked.connect(self.getImage)

        #self.setFixedSize(QSize(400, 300))
        # .setMinimumSize() .setMaximumSize()

        # Set the central widget of the Window.
        self.setCentralWidget(button)

    def the_button_was_clicked(self):
       	print("Clicked!")

    def getImage(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.jpg *.png)")
        imagePath = fname[0]
        pixmap = QPixmap(imagePath)
        self.label.setPixmap(QPixmap(pixmap))
        self.resize(pixmap.width(), pixmap.height())


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()