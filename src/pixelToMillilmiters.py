#! /usr/bin/python3

import pandas as pd

import numpy as np

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog
)

from ApplicationUI.PixelMM import Ui_MainWindow

import sys

from math import sqrt, pow

from config import *

from helpers import pointDistance

class App(QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.filename=None
        self.pushButton.clicked.connect(self.load)

    def load(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setNameFilter("CSV (*.csv)")
        self.filename = dialog.getOpenFileName()
        if self.filename is not None:
            try:
                df=pd.read_csv(self.filename[0])
                markers=[]
                for index, data in df.iterrows():
                    x=data['x marker']
                    y=data['y marker']
                    markers.append([x,y])
                print(markers)
                # find min and max y and y coordinates
                min_x, min_y=markers[0][0], markers[0][1]
                max_x, max_y=min_x, min_y
                for point in markers:
                    x,y=point[0],point[1]
                    if x<min_x: min_x=x
                    elif x>max_x: max_x=x
                    if y<min_y: min_y=y
                    elif y>max_y: max_y=y
                # find interval dimesion on x and y
                delta_x=(max_x-min_x)/(calibration_matrix[1]-1)
                delta_y=(max_y-min_y)/(calibration_matrix[0]-1)

                # arrange markers on a n by m matrix
                # initialize dest matrix
                A=np.array([[0.0,0.0] for i in range(0, calibration_matrix[0]*calibration_matrix[1])]).reshape(calibration_matrix[0],calibration_matrix[1],2)
                # obtain i and j indexes foreach marker
                for marker in markers:
                    x,y=marker[0],marker[1]
                    # column index
                    i=round((x-min_x)/delta_x)
                    # row index
                    j=round((y-min_y)/delta_y)
                    A[j][i]=marker

                print(A)


                # calculate distance foreach combination of subsequent points
                distances=[]
                for i in range(0, calibration_matrix[0]):
                    for j in range(0, calibration_matrix[1]):
                        a=A[i][j]
                        if i+1<calibration_matrix[0]:
                            b=A[i+1][j]
                            distances.append(pointDistance(a, b))
                        if j+1<calibration_matrix[1]:
                            b=A[i][j+1]
                            distances.append(pointDistance(a, b))
                pixel_distance=np.average(distances)
                self.pixel_distance_label.setText(str(pixel_distance))
                print('Pixel distance average: ',pixel_distance)
                std=np.std(distances)
                self.std_label.setText(str(std))
                print('STD pixel distances: ',std)
                ratio=markers_distance/pixel_distance
                print('mm/px ratio: ',ratio)
                self.label.setText(str(ratio))
                df2=pd.DataFrame({'mm/px':[ratio]})
                df=pd.concat([df,df2], axis=1)
                print(df)
                df.to_csv(self.filename[0])
            except:
                print('error')


if __name__=='__main__':
    app = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec())