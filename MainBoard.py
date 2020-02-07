# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1154, 705)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 40, 80, 130))

        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(140, 40, 80, 130))
        self.pushButton_2.setAutoFillBackground(False)
        self.pushButton_2.setCheckable(True)
        self.pushButton_2.setObjectName("pushButton_2")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(360, 160, 800, 400))
        self.label.setObjectName("label")

        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(1030, 50, 64, 23))
        self.lcdNumber.setObjectName("lcdNumber")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1154, 26))
        self.menubar.setObjectName("menubar")
        self.menuPoints = QtWidgets.QMenu(self.menubar)
        self.menuPoints.setObjectName("menuPoints")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionB_11 = QtWidgets.QAction(MainWindow)
        self.actionB_11.setObjectName("actionB_11")
        self.action_12 = QtWidgets.QAction(MainWindow)
        self.action_12.setObjectName("action_12")
        self.action_13 = QtWidgets.QAction(MainWindow)
        self.action_13.setObjectName("action_13")
        self.action_1 = QtWidgets.QAction(MainWindow)
        self.action_1.setObjectName("action_1")
        self.action6_7_6_7 = QtWidgets.QAction(MainWindow)
        self.action6_7_6_7.setObjectName("action6_7_6_7")
        self.menuPoints.addAction(self.actionB_11)
        self.menuPoints.addAction(self.action_12)
        self.menuPoints.addAction(self.action_13)
        self.menuPoints.addAction(self.action_1)
        self.menuPoints.addAction(self.action6_7_6_7)
        self.menubar.addAction(self.menuPoints.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "N"))
        self.pushButton_2.setText(_translate("MainWindow", "N"))
        self.menuPoints.setTitle(_translate("MainWindow", "Points"))
        self.actionB_11.setText(_translate("MainWindow", "J - 11"))
        self.action_12.setText(_translate("MainWindow", "Q - 12"))
        self.action_13.setText(_translate("MainWindow", "К -13"))
        self.action_1.setText(_translate("MainWindow", "Т - 1"))
        self.action6_7_6_7.setText(_translate("MainWindow", "2,3,..=2,3,.."))
