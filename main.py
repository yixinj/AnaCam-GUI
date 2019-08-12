import sys
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QApplication, QFileDialog, QInputDialog,
                             QLineEdit, QMainWindow, QWidget, QGraphicsView)

from anacam import *

INPUT_PATH = "./input/"


class MainWindow(QMainWindow):
    resized = QtCore.pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('mainwindow.ui', self)

        # Buttons
        self.btnUpload.clicked.connect(self.upload_image)
        self.btnClear.clicked.connect(self.clear_image)
        self.btnAnalyze.clicked.connect(self.analyze_image)
        # Menu actions
        self.actionUpload.triggered.connect(self.upload_image)
        self.actionClear.triggered.connect(self.clear_image)
        self.actionAnalyze.triggered.connect(self.analyze_image)

        self.resized.connect(self.resize_image)
        self.show()

    def upload_image(self):
        path = QFileDialog.getOpenFileName(self, 'Upload image', './',
                                           "Image files (*.jpg)")[0]
        if path:
            pixmap = QPixmap(path)
            pixmap_resized = pixmap.scaled(self.mainImage.width(),
                                           self.mainImage.height(),
                                           QtCore.Qt.KeepAspectRatio,
                                           QtCore.Qt.FastTransformation)
            self.mainImage.setPixmap(pixmap_resized)

    def clear_image(self):
        self.mainImage.clear()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(MainWindow, self).resizeEvent(event)

    # TODO: drag and drop functionality for imageView

    def analyze_image(self):
        # TODO: fix path, below
        hue = get_hue("", spots=3, threshold=50)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.resize(800, 600)
    sys.exit(app.exec_())