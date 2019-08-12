import sys

import numpy as np
from PyQt5 import QtCore, uic
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QFileDialog, QMainWindow, qApp,
                             QDialog)

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

        self.setWindowTitle('AnaCam Desktop 1.0')

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

    # TODO: make a new window for this
    def analyze_image(self):
        if self.pixmap:
            # Set parameters based on lineEdit values
            num_contours = int(self.editContours.text())
            if num_contours < 1:
                self.editContours.setText('1')
                num_contours = 1
            threshold = int(self.editThreshold.text())
            if threshold < 0:
                self.editThreshold.setText('0')
                threshold = 0
            qApp.processEvents()  # Update the GUI

            # Convert pixmap to ndarray
            channels_count = 4
            image = self.pixmap.toImage()
            s = image.bits().asstring(self.pixmap.height() *
                                      self.pixmap.width() * channels_count)
            img = np.frombuffer(s, dtype=np.uint8).reshape(
                (self.pixmap.height(), self.pixmap.width(), channels_count))

            # Analyze image
            res = analyze(img, num_contours=num_contours, threshold=threshold)

            # Convert analyzed image to QImage
            res_img = res[0]
            res_img = np.delete(res_img, 3, 2)
            height, width, channel = res_img.shape
            bytesPerLine = 3 * width
            qImg = QImage(res_img.data, width, height, bytesPerLine,
                          QImage.Format_RGB888).rgbSwapped()
            qPixmap = QPixmap.fromImage(qImg)
            # pixmap_resized = qPixmap.scaled(self.mainImage.width(),
            #                                 self.mainImage.height(),
            #                                 QtCore.Qt.KeepAspectRatio,
            #                                 QtCore.Qt.SmoothTransformation)
            # self.mainImage.setPixmap(pixmap_resized)
            self.analysisDialog = AnalysisDialog(qPixmap)


class AnalysisDialog(QDialog):
    def __init__(self, pixmap):
        super(AnalysisDialog, self).__init__()
        self.pixmap = pixmap
        self.init_UI()

    def init_UI(self):
        uic.loadUi('analysis.ui', self)
        self.setWindowTitle('Analysis | AnaCam Desktop 1.0')
        self.resize(1200, 800)
        self.mainImage.setPixmap(self.pixmap)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.resize(800, 600)
    sys.exit(app.exec_())
