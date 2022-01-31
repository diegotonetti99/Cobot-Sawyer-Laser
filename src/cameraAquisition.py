#! /usr/bin/python3

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)
from ApplicationUI.CaptureImageDesign import Ui_MainWindow

import sys

from cameraThread import CameraThred

from config import *

import os

from datetime import datetime

class CaptureImageApp(QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.captureImageBtn.clicked.connect(self.AcquireImage)
        self.cameraThread=CameraThred(self.imageView,camera=camera_index, image_dimensions=(640,480))
        self.imageView.resize(int(1440/2),int(1080/2))
        self.cameraThread.start()

    def AcquireImage(self):
        if not os.path.exists(workFolder):
            os.mkdir(workFolder)
        name = datetime.now().strftime("%d-%m-%Y %H:%M:%S")+'.png'
        self.cameraThread.saveImage(os.path.join(workFolder,name))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = CaptureImageApp()
    win.show()
    sys.exit(app.exec())
