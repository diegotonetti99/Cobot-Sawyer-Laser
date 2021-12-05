# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AppDesign.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(810, 625)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 800, 569))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.cobot_calibration_tab = QtWidgets.QWidget()
        self.cobot_calibration_tab.setObjectName("cobot_calibration_tab")
        self.gridLayoutWidget = QtWidgets.QWidget(self.cobot_calibration_tab)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 791, 531))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.start_cobot_calibration_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.start_cobot_calibration_btn.setObjectName("start_cobot_calibration_btn")
        self.gridLayout.addWidget(self.start_cobot_calibration_btn, 1, 0, 1, 1)
        self.stop_cobot_calibration_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.stop_cobot_calibration_btn.setObjectName("stop_cobot_calibration_btn")
        self.gridLayout.addWidget(self.stop_cobot_calibration_btn, 1, 1, 1, 1)
        self.cobot_point_acquisition_text_browser = QtWidgets.QTextBrowser(self.gridLayoutWidget)
        self.cobot_point_acquisition_text_browser.setObjectName("cobot_point_acquisition_text_browser")
        self.gridLayout.addWidget(self.cobot_point_acquisition_text_browser, 2, 0, 1, 2)
        self.tabWidget.addTab(self.cobot_calibration_tab, "")
        self.camera_calibration_tab = QtWidgets.QWidget()
        self.camera_calibration_tab.setObjectName("camera_calibration_tab")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.camera_calibration_tab)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 791, 531))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.start_camera_acquisition_cal_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.start_camera_acquisition_cal_btn.setObjectName("start_camera_acquisition_cal_btn")
        self.gridLayout_2.addWidget(self.start_camera_acquisition_cal_btn, 0, 0, 1, 2)
        self.max_thr_slider_calib = QtWidgets.QSlider(self.gridLayoutWidget_2)
        self.max_thr_slider_calib.setMaximum(255)
        self.max_thr_slider_calib.setSliderPosition(150)
        self.max_thr_slider_calib.setOrientation(QtCore.Qt.Horizontal)
        self.max_thr_slider_calib.setObjectName("max_thr_slider_calib")
        self.gridLayout_2.addWidget(self.max_thr_slider_calib, 4, 1, 1, 1)
        self.calibrate_camera_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.calibrate_camera_btn.setObjectName("calibrate_camera_btn")
        self.gridLayout_2.addWidget(self.calibrate_camera_btn, 1, 0, 1, 2)
        self.stop_camera_acq_calib_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.stop_camera_acq_calib_btn.setObjectName("stop_camera_acq_calib_btn")
        self.gridLayout_2.addWidget(self.stop_camera_acq_calib_btn, 0, 2, 1, 2)
        self.gray_image_view_calib = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.gray_image_view_calib.setText("")
        self.gray_image_view_calib.setObjectName("gray_image_view_calib")
        self.gridLayout_2.addWidget(self.gray_image_view_calib, 7, 2, 1, 2)
        self.max_thr_calib_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.max_thr_calib_label.setObjectName("max_thr_calib_label")
        self.gridLayout_2.addWidget(self.max_thr_calib_label, 4, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 5, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 4, 0, 1, 1)
        self.min_thr_slider_calib = QtWidgets.QSlider(self.gridLayoutWidget_2)
        self.min_thr_slider_calib.setMaximum(255)
        self.min_thr_slider_calib.setSliderPosition(50)
        self.min_thr_slider_calib.setOrientation(QtCore.Qt.Horizontal)
        self.min_thr_slider_calib.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.min_thr_slider_calib.setTickInterval(1)
        self.min_thr_slider_calib.setObjectName("min_thr_slider_calib")
        self.gridLayout_2.addWidget(self.min_thr_slider_calib, 3, 1, 1, 1)
        self.min_thr_calib_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.min_thr_calib_label.setScaledContents(False)
        self.min_thr_calib_label.setObjectName("min_thr_calib_label")
        self.gridLayout_2.addWidget(self.min_thr_calib_label, 3, 2, 1, 1)
        self.colums_calibration_matrix = QtWidgets.QSpinBox(self.gridLayoutWidget_2)
        self.colums_calibration_matrix.setMinimum(3)
        self.colums_calibration_matrix.setMaximum(10)
        self.colums_calibration_matrix.setObjectName("colums_calibration_matrix")
        self.gridLayout_2.addWidget(self.colums_calibration_matrix, 2, 2, 1, 1)
        self.rows_calibration_matrix = QtWidgets.QSpinBox(self.gridLayoutWidget_2)
        self.rows_calibration_matrix.setMinimum(3)
        self.rows_calibration_matrix.setMaximum(10)
        self.rows_calibration_matrix.setObjectName("rows_calibration_matrix")
        self.gridLayout_2.addWidget(self.rows_calibration_matrix, 2, 3, 1, 1)
        self.blur_slider_calib = QtWidgets.QSlider(self.gridLayoutWidget_2)
        self.blur_slider_calib.setMinimum(1)
        self.blur_slider_calib.setMaximum(30)
        self.blur_slider_calib.setProperty("value", 3)
        self.blur_slider_calib.setOrientation(QtCore.Qt.Horizontal)
        self.blur_slider_calib.setObjectName("blur_slider_calib")
        self.gridLayout_2.addWidget(self.blur_slider_calib, 5, 1, 1, 1)
        self.blur_calib_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.blur_calib_label.setObjectName("blur_calib_label")
        self.gridLayout_2.addWidget(self.blur_calib_label, 5, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 1, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 1, 3, 1, 1)
        self.color_image_view_calib = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.color_image_view_calib.setText("")
        self.color_image_view_calib.setObjectName("color_image_view_calib")
        self.gridLayout_2.addWidget(self.color_image_view_calib, 7, 0, 1, 2)
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 2, 0, 1, 1)
        self.camera_index_calib = QtWidgets.QSpinBox(self.gridLayoutWidget_2)
        self.camera_index_calib.setMaximum(20)
        self.camera_index_calib.setObjectName("camera_index_calib")
        self.gridLayout_2.addWidget(self.camera_index_calib, 2, 1, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 1)
        self.gridLayout_2.setColumnStretch(2, 1)
        self.gridLayout_2.setColumnStretch(3, 1)
        self.gridLayout_2.setRowStretch(0, 1)
        self.gridLayout_2.setRowStretch(1, 1)
        self.gridLayout_2.setRowStretch(2, 1)
        self.gridLayout_2.setRowStretch(3, 1)
        self.gridLayout_2.setRowStretch(4, 1)
        self.gridLayout_2.setRowStretch(5, 5)
        self.tabWidget.addTab(self.camera_calibration_tab, "")
        self.laser_acquisition_tab = QtWidgets.QWidget()
        self.laser_acquisition_tab.setObjectName("laser_acquisition_tab")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.laser_acquisition_tab)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 791, 531))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.start_camera_acquisition_lsr_btn = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.start_camera_acquisition_lsr_btn.setObjectName("start_camera_acquisition_lsr_btn")
        self.gridLayout_3.addWidget(self.start_camera_acquisition_lsr_btn, 0, 0, 1, 2)
        self.max_thr_slider_lsr = QtWidgets.QSlider(self.gridLayoutWidget_3)
        self.max_thr_slider_lsr.setMaximum(255)
        self.max_thr_slider_lsr.setSliderPosition(150)
        self.max_thr_slider_lsr.setOrientation(QtCore.Qt.Horizontal)
        self.max_thr_slider_lsr.setObjectName("max_thr_slider_lsr")
        self.gridLayout_3.addWidget(self.max_thr_slider_lsr, 4, 1, 1, 1)
        self.acquire_laser_pos_btn = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.acquire_laser_pos_btn.setObjectName("acquire_laser_pos_btn")
        self.gridLayout_3.addWidget(self.acquire_laser_pos_btn, 1, 0, 1, 2)
        self.stop_camera_acq_lsr_btn = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.stop_camera_acq_lsr_btn.setObjectName("stop_camera_acq_lsr_btn")
        self.gridLayout_3.addWidget(self.stop_camera_acq_lsr_btn, 0, 2, 1, 2)
        self.gray_image_view_lsr = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.gray_image_view_lsr.setText("")
        self.gray_image_view_lsr.setObjectName("gray_image_view_lsr")
        self.gridLayout_3.addWidget(self.gray_image_view_lsr, 7, 2, 1, 2)
        self.max_thr_lrs_label = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.max_thr_lrs_label.setObjectName("max_thr_lrs_label")
        self.gridLayout_3.addWidget(self.max_thr_lrs_label, 4, 2, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 5, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 3, 0, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.gridLayout_3.addWidget(self.label_13, 4, 0, 1, 1)
        self.min_thr_slider_lsr = QtWidgets.QSlider(self.gridLayoutWidget_3)
        self.min_thr_slider_lsr.setMaximum(255)
        self.min_thr_slider_lsr.setSliderPosition(50)
        self.min_thr_slider_lsr.setOrientation(QtCore.Qt.Horizontal)
        self.min_thr_slider_lsr.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.min_thr_slider_lsr.setTickInterval(1)
        self.min_thr_slider_lsr.setObjectName("min_thr_slider_lsr")
        self.gridLayout_3.addWidget(self.min_thr_slider_lsr, 3, 1, 1, 1)
        self.min_thr_lrs_label = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.min_thr_lrs_label.setScaledContents(False)
        self.min_thr_lrs_label.setObjectName("min_thr_lrs_label")
        self.gridLayout_3.addWidget(self.min_thr_lrs_label, 3, 2, 1, 1)
        self.spinBox_4 = QtWidgets.QSpinBox(self.gridLayoutWidget_3)
        self.spinBox_4.setMinimum(3)
        self.spinBox_4.setMaximum(10)
        self.spinBox_4.setObjectName("spinBox_4")
        self.gridLayout_3.addWidget(self.spinBox_4, 2, 2, 1, 1)
        self.spinBox_5 = QtWidgets.QSpinBox(self.gridLayoutWidget_3)
        self.spinBox_5.setMinimum(3)
        self.spinBox_5.setMaximum(10)
        self.spinBox_5.setObjectName("spinBox_5")
        self.gridLayout_3.addWidget(self.spinBox_5, 2, 3, 1, 1)
        self.blur_slider_lsr = QtWidgets.QSlider(self.gridLayoutWidget_3)
        self.blur_slider_lsr.setMinimum(1)
        self.blur_slider_lsr.setMaximum(30)
        self.blur_slider_lsr.setProperty("value", 3)
        self.blur_slider_lsr.setOrientation(QtCore.Qt.Horizontal)
        self.blur_slider_lsr.setObjectName("blur_slider_lsr")
        self.gridLayout_3.addWidget(self.blur_slider_lsr, 5, 1, 1, 1)
        self.blur_lsr_label = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.blur_lsr_label.setObjectName("blur_lsr_label")
        self.gridLayout_3.addWidget(self.blur_lsr_label, 5, 2, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_16.setObjectName("label_16")
        self.gridLayout_3.addWidget(self.label_16, 1, 2, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_17.setObjectName("label_17")
        self.gridLayout_3.addWidget(self.label_17, 1, 3, 1, 1)
        self.color_image_view_lsr = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.color_image_view_lsr.setText("")
        self.color_image_view_lsr.setObjectName("color_image_view_lsr")
        self.gridLayout_3.addWidget(self.color_image_view_lsr, 7, 0, 1, 2)
        self.label_18 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_18.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_18.setObjectName("label_18")
        self.gridLayout_3.addWidget(self.label_18, 2, 0, 1, 1)
        self.camera_index_lsr = QtWidgets.QSpinBox(self.gridLayoutWidget_3)
        self.camera_index_lsr.setMaximum(20)
        self.camera_index_lsr.setObjectName("camera_index_lsr")
        self.gridLayout_3.addWidget(self.camera_index_lsr, 2, 1, 1, 1)
        self.gridLayout_3.setColumnStretch(0, 1)
        self.gridLayout_3.setColumnStretch(1, 1)
        self.gridLayout_3.setColumnStretch(2, 1)
        self.gridLayout_3.setColumnStretch(3, 1)
        self.gridLayout_3.setRowStretch(0, 1)
        self.gridLayout_3.setRowStretch(1, 1)
        self.gridLayout_3.setRowStretch(2, 1)
        self.gridLayout_3.setRowStretch(3, 1)
        self.gridLayout_3.setRowStretch(4, 1)
        self.gridLayout_3.setRowStretch(5, 5)
        self.tabWidget.addTab(self.laser_acquisition_tab, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 810, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        self.min_thr_slider_lsr.valueChanged['int'].connect(self.min_thr_lrs_label.setNum) # type: ignore
        self.max_thr_slider_lsr.valueChanged['int'].connect(self.max_thr_lrs_label.setNum) # type: ignore
        self.blur_slider_lsr.valueChanged['int'].connect(self.blur_lsr_label.setNum) # type: ignore
        self.min_thr_slider_calib.valueChanged['int'].connect(self.min_thr_calib_label.setNum) # type: ignore
        self.max_thr_slider_calib.valueChanged['int'].connect(self.max_thr_calib_label.setNum) # type: ignore
        self.blur_slider_calib.valueChanged['int'].connect(self.blur_calib_label.setNum) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Cobot Sawyer Laser Aquisition"))
        self.start_cobot_calibration_btn.setText(_translate("MainWindow", "Start Calibration"))
        self.stop_cobot_calibration_btn.setText(_translate("MainWindow", "Stop Calibration"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.cobot_calibration_tab), _translate("MainWindow", "Cobot Calibration"))
        self.start_camera_acquisition_cal_btn.setText(_translate("MainWindow", "Start Camera Aquisition"))
        self.calibrate_camera_btn.setText(_translate("MainWindow", "Calibrate Camera"))
        self.stop_camera_acq_calib_btn.setText(_translate("MainWindow", "Stop Camera Acquisition"))
        self.max_thr_calib_label.setText(_translate("MainWindow", "TextLabel"))
        self.label_3.setText(_translate("MainWindow", "Blur Value"))
        self.label_2.setText(_translate("MainWindow", "Min Threshold"))
        self.label.setText(_translate("MainWindow", "Max Threshold"))
        self.min_thr_calib_label.setText(_translate("MainWindow", "TextLabel"))
        self.blur_calib_label.setText(_translate("MainWindow", "TextLabel"))
        self.label_7.setText(_translate("MainWindow", "Columns"))
        self.label_8.setText(_translate("MainWindow", "Rows"))
        self.label_9.setText(_translate("MainWindow", "Camera Index"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.camera_calibration_tab), _translate("MainWindow", "Camera Calibration"))
        self.start_camera_acquisition_lsr_btn.setText(_translate("MainWindow", "Start Camera Aquisition"))
        self.acquire_laser_pos_btn.setText(_translate("MainWindow", "Acquire Position"))
        self.stop_camera_acq_lsr_btn.setText(_translate("MainWindow", "Stop Camera Acquisition"))
        self.max_thr_lrs_label.setText(_translate("MainWindow", "TextLabel"))
        self.label_11.setText(_translate("MainWindow", "Blur Value"))
        self.label_12.setText(_translate("MainWindow", "Min Threshold"))
        self.label_13.setText(_translate("MainWindow", "Max Threshold"))
        self.min_thr_lrs_label.setText(_translate("MainWindow", "TextLabel"))
        self.blur_lsr_label.setText(_translate("MainWindow", "TextLabel"))
        self.label_16.setText(_translate("MainWindow", "Columns"))
        self.label_17.setText(_translate("MainWindow", "Rows"))
        self.label_18.setText(_translate("MainWindow", "Camera Index"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.laser_acquisition_tab), _translate("MainWindow", "Laser Aquisition"))
