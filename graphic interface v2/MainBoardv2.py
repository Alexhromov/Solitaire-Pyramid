
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
        #MainWindow.resize(1150, 700)
        MainWindow.setFixedSize(1150, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 40, 80, 130))
        self.score = QtWidgets.QLabel(self.centralwidget)
        self.score.setGeometry(QtCore.QRect(900, 150, 280, 230))
        self.pushButton.setObjectName("pushButton")

        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(1030, 50, 64, 23))
        self.lcdNumber.setObjectName("lcdNumber")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1154, 26))
        self.menubar.setObjectName("menubar")
        self.menuOptions = QtWidgets.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuPoints")

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
        self.showscore = QtWidgets.QAction(MainWindow)

        self.restart = QtWidgets.QAction(MainWindow)
        self.restart.setObjectName("restart")
        self.check_turn = QtWidgets.QAction(MainWindow)
        self.check_turn.setObjectName("check_turn")

        self.back = QtWidgets.QAction(MainWindow)
        self.back.setObjectName("check_turn")

        self.action6_7_6_7 = QtWidgets.QAction(MainWindow)
        self.action6_7_6_7.setObjectName("action6_7_6_7")

        self.menuOptions.addAction(self.restart)
        self.menuOptions.addAction(self.check_turn)
        self.menuOptions.addAction(self.back)

        self.menuPoints.addAction(self.actionB_11)
        self.menuPoints.addAction(self.action_12)
        self.menuPoints.addAction(self.action_13)
        self.menuPoints.addAction(self.action_1)
        self.menuPoints.addAction(self.action6_7_6_7)
        self.menuPoints.addAction(self.showscore)
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuPoints.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuPoints.setTitle(_translate("MainWindow", "Points"))
        self.menuOptions.setTitle(_translate("MainWindow", "Option"))

        self.restart.setText(_translate("MainWindow", "restart"))
        self.back.setText(_translate("MainWindow", "back"))
        self.check_turn.setText(_translate("MainWindow", "show_turn"))
        self.actionB_11.setText(_translate("MainWindow", "J - 11"))
        self.action_12.setText(_translate("MainWindow", "Q - 12"))
        self.action_13.setText(_translate("MainWindow", "К -13"))
        self.action_1.setText(_translate("MainWindow", "Т - 1"))
        self.action6_7_6_7.setText(_translate("MainWindow", "2,3,..=2,3,.."))
        self.showscore.setText(_translate("MainWindow", "show always"))

