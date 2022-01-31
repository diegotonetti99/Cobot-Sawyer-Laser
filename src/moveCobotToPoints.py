#! /usr/bin/python3

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)
from ApplicationUI.CobotMoverDesign import Ui_MainWindow

import sys

import random

from config import *

from go_to_cartesian_pose import CartesianMover

from cartesian_acquisition import getRTMatrix

import numpy as np

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import csv

class MoveCobotToPointsApp(QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.loadCobotCalibPointsBtn.clicked.connect(self.loadCobotCalibPoints)
        self.goToHomeBtn.clicked.connect(self.goToHome)
        self.goToNextBtn.clicked.connect(self.goToNext)
        self.cobot_acquired_points=None
        self.loadCobotCalibPoints()
        # array of all the points
        self.points = [[r,c,0] for c in range(0, calibration_matrix[1]) for r in range(0, calibration_matrix[0])] 
        # create random array from points array
        self.randomPoints = []
        while len(self.points)>0:
            index=random.randint(0, len(self.points)-1)
            self.randomPoints.append(self.points.pop(index))
        print(self.randomPoints, len(self.randomPoints))

    def loadCobotCalibPoints(self):
        # load points from file
            with open('cobot_acquired_points.csv', 'r') as file:
                self.cobot_acquired_points = list(
                    csv.reader(file, quoting=csv.QUOTE_NONNUMERIC))
                print(' cobot_acquired_points.csv found')
                # display waypoints coordinates in 3d scatter plot
                fig = plt.figure()
                ax = fig.gca(projection='3d')
                for point in self.cobot_acquired_points:
                    ax.scatter(point[0], point[1], point[2])
                ax.set_xlabel('X Label')
                ax.set_ylabel('Y Label')
                ax.set_zlabel('Z Label')
                plt.show()
            # see if cobot acquire markers and cobot acquired points has the same lenght
            if self.cobot_acquired_points is not None:
                if len(self.cobot_acquired_points) == len(cobot_calibration_markers):
                    # calculate Rotation and translation matrix
                    P = np.array(cobot_calibration_markers)
                    P = np.multiply(P, markers_distance/1000)
                    Q = np.array(self.cobot_acquired_points)
                    self.R, self.t = getRTMatrix(P, Q)
                    # calculate x,y,z errors between the two sets of points
                    temp_p = []
                    for p in P:
                        temp_p.append(np.matmul(self.R, p)+self.t)
                    temp_p = np.array(temp_p)
                    err = Q-temp_p
                    # save x,y,z errors
                    with open('rototranslation_errors.csv', 'w') as file:
                        np.savetxt(file, err, delimiter=",")

    def goToHome(self):
        print('not implemented')

    def goToNext(self):
        """ move robot to marker at row,column specified in the spin box """
        marker_position = self.randomPoints.pop(0)
        for i in range(len(marker_position)):
            marker_position[i]=marker_position[i] *markers_distance/1000
        print(marker_position)
        position = self.fromMarkersToCobot(marker_position)
        print('GoTo position')
        print(position)
        self.mover = CartesianMover(position)
        self.mover.MoveToPosition()

    def fromMarkersToCobot(self, position):
        """ convert marker coordinates to cobot coordinates """
        robot_position = np.matmul(self.R, position)+self.t
        return robot_position

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MoveCobotToPointsApp()
    win.show()
    sys.exit(app.exec())