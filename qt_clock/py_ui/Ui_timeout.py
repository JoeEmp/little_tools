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
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QVBoxLayout, QWidget
from custom_widget.ListItem import TodoListWidgetItem
from utils.utils import get_date, get_time
from utils.clock_thread import ClockThread
from PyQt5.QtCore import Qt
import logging
import platform
from config import IS_FULL
from utils.aps import MYAPS
from utils.mission import TIME_MISSION
from custom_widget.Transparent import TransparentFactory
from custom_widget.Untitle import UntitleMainWindow
from custom_widget.Toast import Toast
from datetime import datetime, timedelta
from PyQt5.QtGui import QFont


class Ui_Timeout(UntitleMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setup()

    def setup(self):
        # 暂时不是区分 mac 和 linux
        if platform.system().lower() == 'windows':
            self.read_qss(filename='./qss/win_timeout.qss')
        else:
            self.read_qss(filename='./qss/timeout.qss')
        self.setupUi()
        self.clock = None
        self.set_models()
        self.set_connect()

    def setupUi(self):
        self.setObjectName("top_win")
        # self.resize(551, 261)
        self.setStyleSheet(self.qss)
        self.gridLayoutWidget = QWidget(self)
        # logging.warning('gridLayoutWidget sheet {}'.format(
        #     self.gridLayoutWidget.styleSheet()))
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
        self.verticalLayout.addWidget(self.lab_time)
        self.lab_title = QLabel(self.gridLayoutWidget)
        self.lab_title.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.lab_title.setObjectName("lab_title")
        self.lab_title.setText('Yang wish list - Ho to do list')
        self.verticalLayout.addWidget(self.lab_title)
        # listWidget
        qss = """
        TransparentListWidget{
            background:transparent;
            selection-background-color:transparent;
        }
        """
        self.listWidget_todo = TransparentFactory().get_widget('listWidget', qss=qss)
        for mission_id, mission_config in TIME_MISSION.missions.items():
            if mission_config['is_action']:
                self.item = TodoListWidgetItem(parent=self.listWidget_todo)
                self.listWidget_todo.setItemWidget(self.item,
                                                   self.item.setupUi(mission_name=mission_config['mission_name']))
        self.verticalLayout.addWidget(self.listWidget_todo)
        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 2, 2)
        self.horizontalLayout = QHBoxLayout()
        self.btn_pass = TransparentFactory().get_widget('Button')
        self.btn_pass.setObjectName("btn_pass")
        self.btn_pass.setFixedWidth(60)
        self.btn_later = TransparentFactory().get_widget('Button')
        self.btn_later.setObjectName("btn_later")
        self.btn_later.setMinimumWidth(120)
        self.horizontalLayout.addWidget(self.btn_pass)
        self.horizontalLayout.addWidget(self.btn_later)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 3, 1, 1)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

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
        # self.lab_title.setText("""还在考虑放什么内容,先喝杯咖啡吧\n躺着吧，万一需求消失了呢。""")
        self.btn_pass.setText("Pass")
        self.btn_later.setText("Later 10 min")

    def set_connect(self):
        self.btn_pass.clicked.connect(self.hide)
        self.btn_later.clicked.connect(self.later_ten_min)
        self.__thread.overSignal.connect(self.update_ui)

    def show(self):
        try:
            if IS_FULL:
                self.move(0, 0)  # 移到主屏幕
            self.refreash_data()
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

    def later_ten_min(self):
        mission = {
            'time': datetime.now()+timedelta(seconds=20),
            'id': 'later_ten_min'
        }
        # MYAPS.add_date_job(mission=mission)
        self.dev_later()
        # self.hide()

    def refreash_data(self):
        self.listWidget_todo.clear()
        for mission_id, mission_config in TIME_MISSION.missions.items():
            if mission_config['is_action']:
                self.item = TodoListWidgetItem(parent=self.listWidget_todo)
                self.listWidget_todo.setItemWidget(self.item,
                                                   self.item.setupUi(mission_name=mission_config['mission_name']))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Ui_Timeout('QWidget')
    sys.exit(app.exec_())
