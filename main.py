from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QFileDialog, QMainWindow, qApp)

from anacam import analyze

INPUT_PATH = "./input/"


class MainWindow(QMainWindow):
    resized = QtCore.pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.pixmap = None
        self.init_UI()

    def init_UI(self):
        uic.loadUi('mainwindow.ui', self)

        self.setWindowTitle('AnaCam Desktop 0.1')

        # Buttons
        self.btnUpload.clicked.connect(self.upload_image)
        self.btnClear.clicked.connect(self.clear_image)
        self.btnAnalyze.clicked.connect(self.analyze_image)
        # Menu actions
        self.actionUpload.triggered.connect(self.upload_image)
        self.actionClear.triggered.connect(self.clear_image)
        self.actionAnalyze.triggered.connect(self.analyze_image)
        self.actionExit.triggered.connect(qApp.quit)

        self.resized.connect(self.resize_image)

        self.show()

    def upload_image(self):
        path = QFileDialog.getOpenFileName(self, 'Upload image', INPUT_PATH,
                                           "Image files (*.jpg)")[0]
        if path:
            self.mainImage.setScaledContents(True)
            self.pixmap = QPixmap(path)
            pixmap_resized = self.pixmap.scaled(self.mainImage.width(),
                                                self.mainImage.height(),
                                                QtCore.Qt.KeepAspectRatio,
                                                QtCore.Qt.FastTransformation)
            self.mainImage.setPixmap(pixmap_resized)
            # self.mainImage.setPixmap(pixmap)

    def clear_image(self):
        self.mainImage.clear()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(MainWindow, self).resizeEvent(event)

    def resize_image(self):
        if self.pixmap:
            pixmap_resized = self.pixmap.scaled(self.mainImage.width(),
                                                self.mainImage.height(),
                                                QtCore.Qt.KeepAspectRatio,
                                                QtCore.Qt.SmoothTransformation)
            self.mainImage.setPixmap(pixmap_resized)

    # TODO: drag and drop functionality for imageView

    def analyze_image(self):
        if self.pixmap:
            hue = analyze("", spots=3, threshold=50)
            print(hue)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.resize(800, 600)
    sys.exit(app.exec_())
