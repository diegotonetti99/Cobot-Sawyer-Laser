from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)
from ApplicationUI.AppDesing import Ui_MainWindow

#from cartesian_acquisition import calibrateCobot

import sys

import json

from cameraThread import CalibrationCameraThread, LaserAcquisitionThread

from image_helpers import calibrateImage, getCalibrationMarkers, drawGridCircles, convertImage, getCircles


class CobotSawyerLaserApp(QMainWindow,  Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # loadUi('ApplicationUI/AppDesign.ui',self)
        self.attachEvents()
        self.camera_thread = None

        self.loadUserValues()

        
        self.display_image_dimensions = (1280/3, 720/3)

        self.newcameramtx, self.roi, self.mtx, self.dist = None, None, None, None
        # righe per colonne
        self.calibration_matrix = (5, 4)

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
                self.blur_slider_lrs.setValue(data['blur_sld_lsr'])
        except:
            pass
    
    def saveUserValues(self):
        data={'min_thr_sld_clb':self.min_thr_slider_calib.value(),
        'max_thr_sld_clb':self.max_thr_slider_calib.value(),
        'blur_sld_clb':self.blur_slider_calib.value(),
        'min_thr_sld_lsr':self.min_thr_slider_lsr.value(),
        'max_thr_sld_lsr':self.max_thr_slider_lsr.value(),
        'blur_sld_lsr':self.blur_slider_lsr.value()}
        with open('user data.json','w') as file:
            json.dump(data, file)

    def start_cobot_calibration_clicked(self):
        print("start cobot calib")
        # calibrateCobot()

    def stop_cobot_calibration_clicked(self):
        print("stop cobot calib")

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = CobotSawyerLaserApp()
    win.show()
    sys.exit(app.exec())
