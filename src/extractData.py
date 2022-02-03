#! /usr/bin/python3

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog
)
from ApplicationUI.ExtractDataDesign import Ui_MainWindow

import sys

from cameraThread import CameraThred

from config import *

import os

import helpers

import cv2

import pandas as pd

import json

class ExtractDataApp(QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.min_threshold=10
        self.max_threshold=100
        self.blur=1
        self.min_threshold2=0
        self.max_threshold2=0
        self.blur2=1
        self.dimensions=(300,300)
        self.image=None
        self.gray=None
        self.image2=None
        self.gray2=None
        self.foundPositions=[]
        self.destFile=None
        # initialize calibration camera params
        self.newcameramtx, self.roi, self.mtx, self.dist = None, None, None, None
        self.loadUserValues()
        self.minTrhSld.valueChanged.connect(self.minTrhSld_valueCanged)
        self.maxTrhSld.valueChanged.connect(self.maxTrhSld_valueCanged)
        self.blurSld.valueChanged.connect(self.blurSld_valueCanged)
        self.minTrhSld_2.valueChanged.connect(self.minTrhSld2_valueCanged)
        self.maxTrhSld_2.valueChanged.connect(self.maxTrhSld2_valueCanged)
        self.blurSld_2.valueChanged.connect(self.blurSld2_valueCanged)
        self.loadCalibImageBtn.clicked.connect(self.loadCalibImage)
        self.calibrateBtn.clicked.connect(self.calibrate)
        self.loadLaserImagesBtn.clicked.connect(self.loadImages)
        self.spinBox.valueChanged.connect(self.changeImage)
        self.savePositionBtn.clicked.connect(self.saveCircle)

    def minTrhSld_valueCanged(self):
        self.min_threshold=self.minTrhSld.value()
        self.toGray()
        
    def maxTrhSld_valueCanged(self):
        self.max_threshold=self.maxTrhSld.value()
        self.toGray()

    def blurSld_valueCanged(self):
        self.blur=self.blurSld.value()
        self.toGray()

    def minTrhSld2_valueCanged(self):
        self.min_threshold2=self.minTrhSld_2.value()
        self.toGray2()
        self.findCircles()

    def maxTrhSld2_valueCanged(self):
        self.max_threshold2=self.maxTrhSld_2.value()
        self.toGray2()
        self.findCircles()

    def blurSld2_valueCanged(self):
        self.blur2=self.blurSld_2.value()
        self.toGray2()
        self.findCircles()

    def loadCalibImage(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setNameFilter("Images (*.png)")
        self.filename = dialog.getOpenFileName()
        self.image=cv2.imread(self.filename[0])
        qt_image = helpers.convertImage(self.image, self.dimensions)
        self.sourceImageView.setPixmap(qt_image)
        print(self.min_threshold, self.max_threshold)
        self.toGray()

    def toGray(self):
        if self.image is not None:
            self.gray=helpers.elaborateImage(self.image, min_threshold=self.min_threshold, max_threshold=self.max_threshold, blur_value=self.blur,BGR=True)
            qt_image=helpers.convertImage(self.gray,self.dimensions)
            self.destImageView.setPixmap(qt_image)

    def calibrate(self):
        if self.gray is not None:
            self.calibration_markers=helpers.getCalibrationMarkers(self.gray, (calibration_matrix[1],calibration_matrix[0]))
            if self.calibration_markers is not None:
                print(self.calibration_markers)
                image = helpers.drawGridCircles(self.image, self.calibration_markers)
                qpixmap=helpers.convertImage(image,self.dimensions)
                self.sourceImageView.setPixmap(qpixmap)
                # get calibration parameters from image
                self.newcameramtx, self.roi, self.mtx, self.dist = helpers.calibrateImage(
                    self.gray, self.calibration_markers, (calibration_matrix[0], calibration_matrix[1]))
                print(self.newcameramtx)
                # undistort calibration image
                self.image = cv2.undistort(self.image, self.mtx, self.dist, None, self.newcameramtx)
                calibration_markers=helpers.getCalibrationMarkers(self.image,(calibration_matrix[1], calibration_matrix[0]))
                if calibration_markers is not None:
                    self.calibration_markers=calibration_markers
                    image = helpers.drawGridCircles(self.image, self.calibration_markers)
                    qpixmap=helpers.convertImage(image,self.dimensions)
                    self.sourceImageView.setPixmap(qpixmap)
                    print('Calibrated. New  markers coordinates: ',self.calibration_markers)


    def loadImages(self):
        dialog = QFileDialog()
        #dialog.setOptions(QFileDialog.DontUseNativeDialog)
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setNameFilter("Video files (*.png)")
        if dialog.exec():
            self.filenames = dialog.selectedFiles()
            self.spinBox.setRange(0, len(self.filenames)-1)
            self.changeImage()

    def toGray2(self):
        if self.image2 is not None:
            self.gray2=helpers.elaborateImage(self.image2, min_threshold=self.min_threshold2, max_threshold=self.max_threshold2, blur_value=self.blur2,BGR=True)
            qt_image=helpers.convertImage(self.gray2,self.dimensions)
            self.destImageView_2.setPixmap(qt_image)

    def changeImage(self):
        self.image2=cv2.imread(self.filenames[self.spinBox.value()])
        qpixmap=helpers.convertImage(self.image2,self.dimensions)
        self.sourceImageView.setPixmap(qpixmap)
        # apply calibration
        self.image2 = cv2.undistort(self.image2, self.mtx, self.dist, None, self.newcameramtx)
        qt_image=helpers.convertImage(self.image2, self.dimensions)
        self.sourceImageView_2.setPixmap(qt_image)
        self.toGray2()
        self.findCircles()

    def findCircles(self):
        if self.gray2 is not None:
            self.circles=helpers.getCircles(self.gray2)
            if self.circles is not None:
                image = helpers.drawCircles(self.image2, self.circles)
                qt_image=helpers.convertImage(image,self.dimensions)
                self.sourceImageView_2.setPixmap(qt_image)

    def saveCircle(self):
        if self.circles is not None:
            if len(self.circles[0,:])==1:
                #self.foundPositions.append([self.circles[0,0][0],self.circles[0,0][1]])
                # find calibration marker nearest to the find circle
                circle = self.circles[0,0]
                nearest=self.calibration_markers[0,0]
                min_d = helpers.pointDistance([circle[0],circle[1]], [nearest[0],nearest[1]])
                for marker in self.calibration_markers[:,0]:
                    distance = helpers.pointDistance([circle[0],circle[1]], [marker[0],marker[1]])
                    if distance<min_d:
                        min_d=distance
                        nearest=marker
                self.foundPositions.append([
                    circle[0], circle[1], nearest[0],nearest[1],min_d
                ])
                df = pd.DataFrame(data=self.foundPositions,columns=['x laser','y laser', 'x marker', 'y marker', 'distance'])
                if self.destFile is None:
                    self.destFile = QFileDialog.getSaveFileName(self, 'Save file','laser_positions.csv','CSV File (*.csv)')
                df.to_csv(self.destFile[0],encoding='utf-8')

    def saveUserValues(self):
        values = {
            'min':self.min_threshold,
            'max':self.max_threshold,
            'blur':self.blur,
            'min2':self.min_threshold2,
            'max2':self.max_threshold2,
            'blur2':self.blur2
        }
        with open('userdata.json','w') as file:
            json.dump(values, file)

    def loadUserValues(self):
        try:
            with open('userdata.json','r') as file:
                values = json.load(file)
                self.minTrhSld.setValue(values['min'])
                self.maxTrhSld.setValue(values['max'])
                self.blurSld.setValue(values['blur'])
                self.minTrhSld_2.setValue(values['min2'])
                self.maxTrhSld_2.setValue(values['max2'])
                self.blurSld_2.setValue(values['blur2'])
                self.min_threshold= values['min']
                self.max_threshold =values['max']
                self.blur=values['blur']
                self.min_threshold2=values['min2']
                self.max_threshold2=values['max2']
                self.blur2=values['blur2']
        except:
            pass

    def closeEvent(self, event):
        self.saveUserValues()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ExtractDataApp()
    win.show()
    sys.exit(app.exec())
