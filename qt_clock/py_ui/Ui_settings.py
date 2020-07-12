# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/joe/Documents/CodeManager/mine/myPython/qt_clock/settings.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!
import hashlib
import logging
import time

from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import QApplication
import sys
from PyQt5.QtCore import Qt, QSize, QTime
from PyQt5.QtWidgets import QListWidgetItem, QWidget, QTimeEdit
from utils.custom_widget import TimeItem, Toast
from utils.mission import TIME_MISSION


class Ui_Settings(object):
    def __init__(self, parent=None):
        self.set_data()
        self.widget = QtWidgets.QWidget()
        self.setupUi(self.widget)
        self.set_connect()

    def get_infos(self) -> dict:
        return TIME_MISSION.missions

    def set_data(self):
        self.missions = self.get_infos()

    def set_connect(self):
        self.btn_save.clicked.connect(self.save)
        self.btn_cancel.clicked.connect(self.cancel)
        self.btn_add.clicked.connect(self.add_item)
        self.btn_del.clicked.connect(self.del_item)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 400)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(
            QtCore.QRect(10, 10, Form.width() - 20, Form.height() - 20))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.listWidget = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setFixedWidth(self.verticalLayoutWidget.width())
        for mission_id in self.missions:
            self.item = TimeItem(self.listWidget)
            self.listWidget.setItemWidget(self.item,
                                          self.item.setupUi(
                                              info=self.missions[mission_id]))
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.addStretch(1)
        self.btn_add = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_add.setObjectName("btn_add")
        self.horizontalLayout.addWidget(self.btn_add)
        self.btn_del = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_del.setObjectName("btn_del")
        self.horizontalLayout.addWidget(self.btn_del)
        self.btn_save = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_save.setObjectName("btn_save")
        self.horizontalLayout.addWidget(self.btn_save)
        self.btn_cancel = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout.addWidget(self.btn_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        # self.widget.setWindowFlags(Qt.FramelessWindowHint)
        self.widget = Form

    def refreash_items(self, is_save):
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            # logging.warning('item info is {}'.format(item.info))
            if is_save:
                flag = item.update_info()
                TIME_MISSION.update_mission(item.info,flag)
            else:
                item.set_data(info=TIME_MISSION.missions[item.info['id']])

    def save(self):
        self.btn_save.setDisabled(True)
        self.refreash_items(True)
        self.btn_save.setEnabled(True)
        self.widget.hide()
        # logging.warning(TIME_MISSION.missions)

    def cancel(self):
        self.refreash_items(False)
        self.widget.hide()
        # logging.warning(TIME_MISSION.missions)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Settings"))
        self.btn_add.setText(_translate("Form", "add"))
        self.btn_del.setText(_translate("Form", "del"))
        self.btn_save.setText(_translate("Form", "save"))
        self.btn_cancel.setText(_translate("Form", "cancel"))

    def add_item(self):
        self.item = TimeItem(self.listWidget)
        self.listWidget.setItemWidget(self.item, self.item.setupUi())

    def del_item(self):
        cur_index = self.listWidget.currentRow()
        if  -1 !=  cur_index :
            try:
                itme = self.listWidget.currentItem()
                TIME_MISSION.del_mission(item.info['id'])
                self.listWidget.takeItem(cur_index)
                self.listWidget.setCurrentRow(-1)
            except Exception as e:
                print(e)
        else:
            Toast(self.widget).show_toast('未选中item', 2000)

    def show(self):
        self.widget.show()

    def dev_later(self):
        Toast(self.widget).show_toast('功能正在开发中，不要着急先喝杯咖啡', 2000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Ui_Settings()
    sys.exit(app.exec_())
    # d = ['hello', 'world']
    # ret = d.remove('hello')
    # print(ret)