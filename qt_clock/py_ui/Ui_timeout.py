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
from PyQt5 import QtCore
from PyQt5.Qt import QApplication
import sys
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout, \
    QHBoxLayout
from utils.custom_widget import TransparentButton, UntitleWindow, Toast
from utils.utils import get_date, get_time
from utils.clock_thread import ClockThread
from PyQt5.QtCore import Qt
import logging
import platform
from config import IS_FULL


class Ui_Timeout(UntitleWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setup()

    def setup(self):
        # 暂时不是区分 mac 和 linux
        if platform.system().lower() == 'windows':
            self.read_qss(filename='./qss/win_timeout.qss')
        else:
            self.read_qss(filename='./qss/timeout.qss')
        print(self.parent())
        self.setupUi()
        self.clock = None
        self.set_models()
        self.set_connect()

    def setupUi(self):
        self.setObjectName("top_win")
        self.resize(551, 261)
        self.setStyleSheet(self.qss)
        self.gridLayoutWidget = QWidget(self)
        logging.warning('gridLayoutWidget sheet {}'.format(
            self.gridLayoutWidget.styleSheet()))
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 511, 221))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.lab_date = QLabel(self.gridLayoutWidget)
        self.lab_date.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.lab_date.setObjectName("lab_date")
        self.gridLayout.addWidget(self.lab_date, 0, 0, 1, 1)
        self.verticalLayout = QVBoxLayout()
        self.lab_time = QLabel(self.gridLayoutWidget)
        self.lab_time.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.lab_time.setFixedHeight(100)
        self.lab_time.setObjectName("lab_time")
        self.lab_tips = QLabel(self.gridLayoutWidget)
        self.lab_tips.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.lab_tips.setObjectName("lab_tips")
        self.verticalLayout.addWidget(self.lab_time)
        self.verticalLayout.addWidget(self.lab_tips)
        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 2, 2)
        self.horizontalLayout = QHBoxLayout()
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

        width = QApplication.desktop().availableGeometry().width()
        height = QApplication.desktop().availableGeometry().height()
        if IS_FULL:
            screen_rate = 1
        else:
            screen_rate = 0.8
        self.resize(int(width * screen_rate), int(height * screen_rate))
        self.gridLayoutWidget.setGeometry(
            QtCore.QRect(20, 20, int(width * screen_rate) - 40,
                         int(height * screen_rate) - 40))

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.lab_date.setText("%s" % get_date())
        self.lab_time.setText("{}".format(get_time()))
        self.lab_tips.setText("""还在考虑放什么内容,先喝杯咖啡吧\n躺着吧，万一需求消失了呢。""")
        self.btn_pass.setText("Pass")
        self.btn_later.setText("Later 10 min")

    def set_connect(self):
        self.btn_pass.clicked.connect(self.hide)
        self.btn_later.clicked.connect(self.dev_later)
        self.__thread.overSignal.connect(self.update_ui)

    def show(self):
        try:
            self.read_qss(filename='./qss/timeout.qss')
            self.setStyleSheet(self.qss)
            super().show()
            self.activateWindow()
            self.raise_()
        except Exception as e:
            logging.error(e)

    def update_ui(self):
        self.lab_date.setText("%s" % get_date())
        self.lab_time.setText("{}".format(get_time()))
        logging.debug('update date')

    def set_models(self):
        self.__thread = ClockThread()
        self.__thread.start()
        pass

    def read_qss(self, filename='') -> None:
        if not filename:
            filename = os.path.abspath(__file__).replace('.py', '.qss')
        with open(filename, encoding='utf-8') as f:
            self.qss = f.read()

    def hide(self) -> None:
        # self.__thread.stop()  # 停止后重启会有问题，暂不解决 to deal
        super().hide()

    def dev_later(self):
        Toast(self).show_toast('功能正在开发中，不要着急，先喝杯咖啡', 2000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Ui_Timeout('QWidget')
    sys.exit(app.exec_())
