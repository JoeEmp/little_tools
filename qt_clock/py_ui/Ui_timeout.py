'''
@Author: your name
@Date: 2020-06-25 15:28:49
@LastEditTime: 2020-06-30 16:03:24
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /qt_clock/py_ui/Ui_timeout.py
'''
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/joe/Documents/CodeManager/mine/myPython/qt_clock/demo.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!
import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import QApplication, QDesktopWidget, QThread
import sys
from utils.custom_widget import TransparentButton, UntitleWindow, Toast
from utils.utils import get_date, get_time
from utils.clock_thread import Clock,ClockThread,test_thread
from PyQt5.QtCore import QTimer, Qt
import logging
import time
import platform

class Ui_Timeout(UntitleWindow):
    def __init__(self,parent=None):
        super().__init__()
        self.setup()


    def setup(self):
        # 暂时不是区分 mac 和 linux
        if platform.system().lower()  == 'windows':
            self.read_qss(filename='./qss/win_timeout.qss')
        else:
            self.read_qss(filename='./qss/timeout.qss')
        self.setupUi()
        self.clock = None
        self.set_models()
        self.set_connect()


    def setupUi(self):
        self.setObjectName("top_widget_h")
        self.resize(551, 261)
        self.setStyleSheet(self.qss)
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 511, 221))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.lab_date = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lab_date.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.lab_date.setObjectName("lab_date")
        self.gridLayout.addWidget(self.lab_date, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.lab_time = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lab_time.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.lab_time.setFixedHeight(100)
        self.lab_time.setObjectName("lab_time")
        self.lab_tips = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lab_tips.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.lab_tips.setObjectName("lab_tips")
        self.verticalLayout.addWidget(self.lab_time)
        self.verticalLayout.addWidget(self.lab_tips)
        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 2, 2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.btn_pass = TransparentButton(self.gridLayoutWidget)
        self.btn_pass.setObjectName("btn_pass")
        self.btn_pass.setFixedWidth(60)
        self.btn_later = TransparentButton(self.gridLayoutWidget)
        self.btn_later.setObjectName("btn_later")
        self.btn_later.setMinimumWidth(120)
        self.horizontalLayout.addWidget(self.btn_pass)
        self.horizontalLayout.addWidget(self.btn_later)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 3, 1, 1)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setWindowFlags(Qt.FramelessWindowHint)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.lab_date.setText("%s" % get_date())
        self.lab_time.setText("{}".format(get_time()))
        self.lab_tips.setText("""今日咖啡\n危地马拉 安提瓜花神咖啡（Guatemala La Minita La Folie）\n产区： 安提瓜（Antigua）火山区\n庄园： 拉米尼塔（La Minita） \n出口： 拉米妮塔（La Minita）集团的品牌"花神"\n品种：   Caturra, Catuai, Borbon\n波旁、卡杜拉、卡杜艾\n海拔：   1200至1600米\n等级：  欧规水洗极硬豆（SHB）\n处理法：传统式水洗处理
        """)
        self.btn_pass.setText("Pass")
        self.btn_later.setText("Later 10 min")


    def set_connect(self):
        self.btn_pass.clicked.connect(self.hide)
        self.btn_later.clicked.connect(self.dev_later)
        self.__thread.overSignal.connect(self.update_ui)

    def show(self):
        try:
            width = QApplication.desktop().screenGeometry().width()
            height = QApplication.desktop().screenGeometry().height()
            self.resize(int(width * 0.8), int(height * 0.8))
            self.gridLayoutWidget.setGeometry(
                QtCore.QRect(20, 20, int(width * 0.8) - 40, int(height * 0.8) - 40))
            self.raise_()
            super().show()
        except Exception as e:
            logging.error(e)

    def update_ui(self):
        self.lab_date.setText("%s" % get_date())
        self.lab_time.setText("{}".format(get_time()))
        # if "top_widget_h" == self.objectName():
        #     self.setObjectName('top_widget_d')
        # else:
        #     self.setObjectName('top_widget_h')
        # self.setStyleSheet(self.qss)
        logging.debug('update date')


    def set_models(self):
        self.__thread = test_thread()
        self.__thread.start()
        pass


    def read_qss(self, filename='') -> None:
        if not filename:
            filename = os.path.abspath(__file__).replace('.py', '.qss')
        with open(filename, encoding='utf-8') as f:
            self.qss = f.read()


    def hide(self) -> None:
        # self.__thread.stop()
        super().hide()


    def dev_later(self):
        Toast(self).show_toast('功能正在开发中，不要着急先喝杯咖啡', 2000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Ui_Timeout('QWidget')
    sys.exit(app.exec_())
