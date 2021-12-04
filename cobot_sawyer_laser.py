from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)
from ApplicationUI.AppDesing import Ui_MainWindow

from cartesian_acquisition import calibrateCobot

import sys


class CobotSawyerLaserApp(QMainWindow,  Ui_MainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        #loadUi('ApplicationUI/AppDesign.ui',self)
        self.attachEvents()
        

    def attachEvents(self):
        """ Load qt widget events """
        # attach buttons events
        self.stop_camera_acq_calib_btn.clicked.connect(self.stop_camera_acquisition_calib_clicked)
        self.calibrate_camera_btn.clicked.connect(self.calibrate_camera_clicked)
        self.start_camera_acquisition_cal_btn.clicked.connect(self.start_camera_acquisition_calib_clicked)
        self.stop_cobot_calibration_btn.clicked.connect(self.stop_cobot_calibration_clicked)
        self.start_cobot_calibration_btn.clicked.connect(self.start_cobot_calibration_clicked)
        self.start_camera_acquisition_lsr_btn.clicked.connect(self.start_camera_acquisition_lsr_clicked)
        self.acquire_laser_pos_btn.clicked.connect(self.acquire_laser_position_clicked)
        self.stop_camera_acq_lsr_btn.clicked.connect(self.stop_camera_acquisition_lsr_clicked)

        # attach sliders events
        self.min_thr_slider_calib.valueChanged.connect(self.min_thr_slider_calib_changed)
        self.max_thr_slider_calib.valueChanged.connect(self.max_thr_slider_calib_changed)
        self.blur_slider_calib.valueChanged.connect(self.blur_slider_calib_changed)
        self.min_thr_slider_lsr.valueChanged.connect(self.min_thr_slider_lsr_changed)
        self.max_thr_slider_lsr.valueChanged.connect(self.max_thr_slider_lsr_changed)
        self.blur_slider_lsr.valueChanged.connect(self.blur_slider_lsr_changed)
    
    def start_cobot_calibration_clicked(self):
        print("start cobot calib")
        #calibrateCobot()

    def stop_cobot_calibration_clicked(self):
        print("stop cobot calib")

    def start_camera_acquisition_calib_clicked(self):
        print("start camera calib")

    def stop_camera_acquisition_calib_clicked(self):
        print("stop camera calib")

    def calibrate_camera_clicked(self):
        print("calibrate")

    def start_camera_acquisition_lsr_clicked(self):
        print("start laser")

    def stop_camera_acquisition_lsr_clicked(self):
        print("stop laser")

    def acquire_laser_position_clicked(self):
        print("laser pos")
    
    def min_thr_slider_calib_changed(self):
        print ('min trh slider calib ch')

    def max_thr_slider_calib_changed(self):
        pass

    def blur_slider_calib_changed(self):
        pass

    def min_thr_slider_lsr_changed(self):
        pass

    def max_thr_slider_lsr_changed(self):
        pass

    def blur_slider_lsr_changed(self):\
        pass

if __name__ == '__main__':
    app=QApplication(sys.argv)
    win=CobotSawyerLaserApp()
    win.show()
    sys.exit(app.exec())