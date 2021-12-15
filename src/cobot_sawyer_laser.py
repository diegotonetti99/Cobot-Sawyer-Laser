#! /usr/bin/python3
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)
from ApplicationUI.AppDesign import Ui_MainWindow

from cartesian_acquisition import CobotCalibrator, getRTMatrix

from go_to_cartesian_pose import CartesianMover

import sys

import json

import csv

import numpy as np

from matplotlib import pyplot as plt

from cameraThread import CalibrationCameraThread, LaserAcquisitionThread

from image_helpers import calibrateImage, getCalibrationMarkers, drawGridCircles, convertImage, getCircles

from config import *

class CobotSawyerLaserApp(QMainWindow,  Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # loadUi('ApplicationUI/AppDesign.ui',self)
        self.attachEvents()
        self.camera_thread = None
        # righe per colonne
        self.calibration_matrix = [5, 4]
        # load user values from user data
        self.loadUserValues()
        # set image viewr diemnsion
        self.display_image_dimensions = (1280/3, 720/3)
        # initialize calibration camera params
        self.newcameramtx, self.roi, self.mtx, self.dist = None, None, None, None
        self.transform_matrix=None
        self.cobot_acquired_points=None
        self.R=None
        self.t=None
        # load cobot calibration markers
        self.loadCalibrationsMarkers()
        
    def closeEvent(self,event):
        self.saveUserValues()

    def attachEvents(self):
        """ Load qt widget events """
        # attach buttons events
        self.stop_camera_acq_calib_btn.clicked.connect(
            self.stop_camera_acquisition_calib_clicked)
        self.calibrate_camera_btn.clicked.connect(
            self.calibrate_camera_clicked)
        self.start_camera_acquisition_cal_btn.clicked.connect(
            self.start_camera_acquisition_calib_clicked)
        self.stop_cobot_calibration_btn.clicked.connect(
            self.stop_cobot_calibration_clicked)
        self.start_cobot_calibration_btn.clicked.connect(
            self.start_cobot_calibration_clicked)
        self.start_camera_acquisition_lsr_btn.clicked.connect(
            self.start_camera_acquisition_lsr_clicked)
        self.acquire_laser_pos_btn.clicked.connect(
            self.acquire_laser_position_clicked)
        self.stop_camera_acq_lsr_btn.clicked.connect(
            self.stop_camera_acquisition_lsr_clicked)
        self.go_to_btn.clicked.connect(self.go_to_clicked)

        # attach sliders events
        self.min_thr_slider_calib.valueChanged.connect(
            self.min_thr_slider_calib_changed)
        self.max_thr_slider_calib.valueChanged.connect(
            self.max_thr_slider_calib_changed)
        self.blur_slider_calib.valueChanged.connect(
            self.blur_slider_calib_changed)
        self.min_thr_slider_lsr.valueChanged.connect(
            self.min_thr_slider_lsr_changed)
        self.max_thr_slider_lsr.valueChanged.connect(
            self.max_thr_slider_lsr_changed)
        self.blur_slider_lsr.valueChanged.connect(self.blur_slider_lsr_changed)

        # attach spinbox events
        self.column_spin_box_calib.valueChanged.connect(self.column_calib_changed)
        self.row_spin_box_calib.valueChanged.connect(self.row_calib_changed)
        self.column_spin_box_lsr.valueChanged.connect(self.column_lsr_changed)
        self.row_spin_box_lsr.valueChanged.connect(self.row_lsr_changed)

    def loadUserValues(self):
        try:
            with open('user data.json', 'r') as file:
                data = json.load(file)
                self.min_thr_slider_calib.setValue(
                    data['min_thr_sld_clb'])
                self.max_thr_slider_calib.setValue(
                    data['max_thr_sld_clb'])
                self.blur_slider_calib.setValue(
                    data['blur_sld_clb'])
                self.min_thr_slider_lsr.setValue(
                    data['min_thr_sld_lsr'])
                self.max_thr_slider_lsr.setValue(
                    data['max_thr_sld_lsr'])
                self.blur_slider_lsr.setValue(data['blur_sld_lsr'])
                self.column_spin_box_calib.setValue(data['column_clb'])
                self.row_spin_box_calib.setValue(data['row_clb'])
                self.column_spin_box_lsr.setValue(data['column_lsr'])
                self.row_spin_box_lsr.setValue(data['row_lsr'])
        except Exception as e:
            print(e)
    
    def saveUserValues(self):
        data={'min_thr_sld_clb':self.min_thr_slider_calib.value(),
        'max_thr_sld_clb':self.max_thr_slider_calib.value(),
        'blur_sld_clb':self.blur_slider_calib.value(),
        'min_thr_sld_lsr':self.min_thr_slider_lsr.value(),
        'max_thr_sld_lsr':self.max_thr_slider_lsr.value(),
        'blur_sld_lsr':self.blur_slider_lsr.value(),
        'column_clb':self.column_spin_box_calib.value(),
        'row_clb':self.row_spin_box_calib.value(),
        'column_lsr':self.column_spin_box_lsr.value(),
        'row_lsr':self.column_spin_box_lsr.value()}
        with open('user data.json','w') as file:
            json.dump(data, file)

    def start_cobot_calibration_clicked(self):
        print("start cobot calib")
        self.cobotCalibr=CobotCalibrator(self.cobotCalibrationCallback, self.cobot_calibration_log_label)
        self.cobotCalibr.run()
        # self.transform_matrix= do something

    def stop_cobot_calibration_clicked(self):
        print("stop cobot calib")

    def loadCalibrationsMarkers(self):
        ''' load cobot acquired points on markers from csv file and calculate rotation and transaltion matrix. '''
        try:
            # load points from file
            with open('cobot_acquired_points.csv', 'r') as file:
                self.cobot_acquired_points = list(csv.reader(file, quoting=csv.QUOTE_NONNUMERIC))
                print(' cobot_acquired_points.csv found')
                # display waypoints coordinates in 3d scatter plot
                fig = plt.figure()
                ax = fig.gca(projection='3d')
                for point in self.cobot_acquired_points:
                    ax.scatter(point[0],point[1],point[2])
                ax.set_xlabel('X Label')
                ax.set_ylabel('Y Label')
                ax.set_zlabel('Z Label')
                ax.set_xlim(0.5,0.8)
                ax.set_ylim(0,0.5)
                ax.set_zlim(0,0.5)
                plt.show()
            # see if cobot acquire markers and cobot acquired points has the same lenght
            if self.cobot_acquired_points is not None:
                if len(self.cobot_acquired_points)==len(cobot_calibration_markers):
                    # calculate Rotation and translation matrix
                    P=np.array(cobot_calibration_markers)
                    P=np.multiply(P,markers_distance/1000)
                    Q=np.array(self.cobot_acquired_points)
                    self.R, self.t = getRTMatrix(P,Q)
                    # calculate x,y,z errors between the two sets of points
                    temp_p=[]
                    for p in P:
                        temp_p.append(np.matmul(self.R,p)+self.t)
                    temp_p=np.array(temp_p)
                    err=Q-temp_p
                    # save x,y,z errors 
                    with open('rototranslation_errors.csv','w') as file:
                        np.savetxt(file,err, delimiter=",")
        except:
            print('no cobot calibration points found')


    def start_camera_acquisition_calib_clicked(self):
        if self.camera_thread == None:
            self.camera_thread = CalibrationCameraThread(self.color_image_view_calib, self.gray_image_view_calib, min_thr=self.min_thr_slider_calib.value(
            ), max_thr=self.max_thr_slider_calib.value(), blur=self.blur_slider_calib.value(), camera=self.camera_index_calib.value(), image_dimensions=self.display_image_dimensions)
            self.camera_thread.start()

    def stop_camera_acquisition_calib_clicked(self):
        if self.camera_thread is not None:
            self.camera_thread.stop()
            self.camera_thread.join()
            self.camera_thread = None

    def calibrate_camera_clicked(self):
        if self.camera_thread is not None:
            # find calibration markers in the image
            self.calibration_markers = getCalibrationMarkers(
                self.camera_thread.gray_image, self.calibration_matrix)

            if self.calibration_markers is not None:
                self.camera_thread.stop()
                self.camera_thread.join()
                # draw found markers on color image
                cv_image = drawGridCircles(
                    self.camera_thread.image, self.calibration_markers)
                # get qpixmap
                qpixmap = convertImage(
                    cv_image, image_dimensions=self.display_image_dimensions)
                # draw image
                self.color_image_view_calib.setPixmap(qpixmap)
                # get calibration parameters from image
                self.newcameramtx, self.roi, self.mtx, self.dist = calibrateImage(
                    self.camera_thread.gray_image, self.calibration_markers, self.calibration_matrix)
                print(self.newcameramtx)

                self.camera_thread = None

    def start_camera_acquisition_lsr_clicked(self):
        if self.camera_thread == None:
            self.camera_thread = LaserAcquisitionThread(self.color_image_view_lsr, self.gray_image_view_lsr, self.mtx, self.dist, self.roi, self.newcameramtx, min_thr=self.min_thr_slider_lsr.value(
            ), max_thr=self.max_thr_slider_lsr.value(), blur=self.blur_slider_lsr.value(), camera=self.camera_index_calib.value(), image_dimensions=self.display_image_dimensions)
            self.camera_thread.start()

    def stop_camera_acquisition_lsr_clicked(self):
        if self.camera_thread is not None:
            self.camera_thread.stop()
            self.camera_thread.join()
            self.camera_thread = None

    def acquire_laser_position_clicked(self):
        if self.camera_thread is not None:
            print(self.camera_thread.circles)

    def min_thr_slider_calib_changed(self):
        if self.camera_thread is not None:
            self.camera_thread.min_thr = self.min_thr_slider_calib.value()

    def max_thr_slider_calib_changed(self):
        if self.camera_thread is not None:
            self.camera_thread.max_thr = self.max_thr_slider_calib.value()

    def blur_slider_calib_changed(self):
        if self.camera_thread is not None:
            self.camera_thread.blur = self.blur_slider_calib.value()

    def min_thr_slider_lsr_changed(self):
        if self.camera_thread is not None:
            self.camera_thread.min_thr = self.min_thr_slider_lsr.value()

    def max_thr_slider_lsr_changed(self):
        if self.camera_thread is not None:
            self.camera_thread.max_thr = self.max_thr_slider_lsr.value()

    def blur_slider_lsr_changed(self):
        if self.camera_thread is not None:
            self.camera_thread.blur = self.blur_slider_lsr.value()

        self.column_spin_box_calib.valueChanged.connect(self.column_calib_changed)
        self.column_spin_box_calib.valueChanged.connect(self.column_calib_changed)
    
        self.column_spin_box_calib.valueChanged.connect(self.column_calib_changed)

        self.column_spin_box_calib.valueChanged.connect(self.column_calib_changed)

    def column_calib_changed(self):
        self.calibration_matrix[1]=self.column_spin_box_calib.value()
    
    def row_calib_changed(self):
        self.calibration_matrix[0]=self.row_spin_box_calib.value()

    def column_lsr_changed(self):
        self.calibration_matrix[1]=self.column_spin_box_lsr.value() 
    
    def row_lsr_changed(self):
        self.calibration_matrix[0]=self.row_spin_box_lsr.value()

    def go_to_clicked(self):
        """ move robot to marker at row,column specified in the spin box """
        marker_position=[self.row_spin_box_lsr.value()*markers_distance/1000, self.column_spin_box_lsr.value()*markers_distance/1000]
        position=self.fromMarkersToCobot(marker_position)
        self.mover=CartesianMover(position, self.go_to_callback)
        self.mover.run()

    def fromMarkersToCobot(self, position):
        """ convert marker coordinates to cobot coordinates """
        return [0.5,position[0],position[1]]
    
    def cobotCalibrationCallback(self, calibrator):
        """ Event called when cobot has acquired all points """
        self.cobot_acquired_points=calibrator.waypoints._waypoints
        print(self.cobot_acquired_points)
    
    def go_to_callback(self, mover):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = CobotSawyerLaserApp()
    win.show()
    sys.exit(app.exec())
