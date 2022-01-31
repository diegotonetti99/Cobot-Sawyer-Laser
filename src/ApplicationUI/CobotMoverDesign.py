# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CobotMoverDesign.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(221, 121)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 213, 89))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.loadCobotCalibPointsBtn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.loadCobotCalibPointsBtn.setObjectName("loadCobotCalibPointsBtn")
        self.verticalLayout.addWidget(self.loadCobotCalibPointsBtn)
        self.goToHomeBtn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.goToHomeBtn.setObjectName("goToHomeBtn")
        self.verticalLayout.addWidget(self.goToHomeBtn)
        self.goToNextBtn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.goToNextBtn.setObjectName("goToNextBtn")
        self.verticalLayout.addWidget(self.goToNextBtn)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Cobot Mover"))
        self.loadCobotCalibPointsBtn.setText(_translate("MainWindow", "Load Cobot Calibration Points"))
        self.goToHomeBtn.setText(_translate("MainWindow", "Goto Home"))
        self.goToNextBtn.setText(_translate("MainWindow", "Goto Next Point"))
