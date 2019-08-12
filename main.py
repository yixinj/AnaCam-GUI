import sys

from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QApplication, QFileDialog, QInputDialog,
                             QLineEdit, QMainWindow, QWidget, QGraphicsView)

from anacam import *

INPUT_PATH = "./input/"


class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('mainwindow.ui', self)

        self.btnUpload.clicked.connect(self.upload_image)
        self.actionUpload.triggered.connect(self.upload_image)

        self.btnClear.clicked.connect(self.clear_image)
        self.actionClear.triggered.connect(self.clear_image)

        self.btnAnalyze.clicked.connect(self.analyze_image)
        self.actionAnalyze.triggered.connect(self.analyze_image)
        self.show()

    def upload_image(self):
        path = QFileDialog.getOpenFileName(self, 'Upload image', './',
                                           "Image files (*.jpg)")[0]
        if path:
            pixmap = QPixmap(path)
            self.mainImage.setPixmap(pixmap)
            # TODO: resize image
            self.mainImage.resize(self.mainImage.width(),
                                  self.mainImage.height())

    def clear_image(self):
        self.mainImage.clear()

    # TODO: drag and drop functionality for imageView

    def analyze_image(self):
        # TODO: fix path, below
        hue = get_hue("", spots=3, threshold=50)


app = QApplication(sys.argv)
window = Ui()
app.exec_()
