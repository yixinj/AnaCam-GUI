from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5 import uic, QtWidgets
from anacam import *

INPUT_PATH = "./input/"


class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('mainwindow.ui', self)

        self.btnUpload.clicked.connect(self.upload_image)
        self.btnClear.clicked.connect(self.clear_image)
        self.show()

    def upload_image(self):
        path = QFileDialog.getOpenFileName(self, 'Upload image', './',
                                           "Image files (*.jpg)")[0]
        if path:
            # TODO: set imageView graphic to the uploaded image
            pass

    def clear_image(self):
        # TODO: clear imageView
        pass

    # TODO: drag and drop functionality for imageView
    
    def analyze_image(self):
        hue = get_hue(path, spots=3, threshold=50)


app = QApplication(sys.argv)
window = Ui()
app.exec_()