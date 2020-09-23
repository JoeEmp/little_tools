# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/joe/Documents/CodeManager/mine/myPython/qt_clock/settings.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import QApplication
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, \
    QListWidget
from custom_widget.ListItem import TimeItem
from custom_widget.Toast import Toast
from utils.mission import TIME_MISSION


class Ui_Settings(object):
    def __init__(self, parent=None):
        self.set_data()
        self.widget = QtWidgets.QWidget()
        self.setupUi(self.widget)
        self.set_connect()

    def set_data(self):
        self.del_missions = set()  # 需要被去除的的任务配置

    def set_connect(self):
        self.btn_save.clicked.connect(self.save)
        self.btn_cancel.clicked.connect(self.cancel)
        self.btn_add.clicked.connect(self.add_item)
        self.btn_del.clicked.connect(self.del_item)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 400)
        self.verticalLayoutWidget = QWidget(Form)
        self.verticalLayoutWidget.setGeometry(
            QtCore.QRect(10, 10, Form.width() - 20, Form.height() - 20))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.listWidget = QListWidget(self.verticalLayoutWidget)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setFixedWidth(self.verticalLayoutWidget.width())
        for mission_id in TIME_MISSION.missions:
            self.item = TimeItem(self.listWidget)
            self.listWidget.setItemWidget(self.item,
                                          self.item.setupUi(
                                              info=TIME_MISSION.missions[
                                                  mission_id]))
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.addStretch(1)
        self.btn_add = QPushButton(self.verticalLayoutWidget)
        self.btn_add.setObjectName("btn_add")
        self.horizontalLayout.addWidget(self.btn_add)
        self.btn_del = QPushButton(self.verticalLayoutWidget)
        self.btn_del.setObjectName("btn_del")
        self.horizontalLayout.addWidget(self.btn_del)
        self.btn_save = QPushButton(self.verticalLayoutWidget)
        self.btn_save.setObjectName("btn_save")
        self.horizontalLayout.addWidget(self.btn_save)
        self.btn_cancel = QPushButton(self.verticalLayoutWidget)
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout.addWidget(self.btn_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.widget = Form

    def refreash_items(self, is_save):
        if is_save:
            for i in range(self.listWidget.count()):
                item = self.listWidget.item(i)
                flag = item.update_info()
                TIME_MISSION.update_mission(item.info, flag)
            for mission_id in self.del_missions:
                TIME_MISSION.del_mission(mission_id)
            self.del_missions.clear()
        else:
            self.listWidget.clear()
            for mission_id in TIME_MISSION.missions:
                self.item = TimeItem(self.listWidget)
                self.listWidget.setItemWidget(self.item,
                                              self.item.setupUi(
                                                  info=TIME_MISSION.missions[
                                                      mission_id]))

    def save(self):
        self.btn_save.setDisabled(True)
        self.refreash_items(True)
        self.btn_save.setEnabled(True)
        self.widget.hide()

    def cancel(self):
        self.refreash_items(False)
        self.widget.hide()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Settings"))
        self.btn_add.setText(_translate("Form", "add"))
        self.btn_del.setText(_translate("Form", "del"))
        self.btn_save.setText(_translate("Form", "save"))
        self.btn_cancel.setText(_translate("Form", "cancel"))

    def add_item(self, mission=None):
        item = TimeItem(self.listWidget)
        if mission:
            self.listWidget.setItemWidget(item, item.setupUi(info=mission))
        else:
            self.listWidget.setItemWidget(item, item.setupUi())

    def del_item(self):
        cur_index = self.listWidget.currentRow()
        if -1 != cur_index:
            try:
                self.del_missions.add(self.listWidget.currentItem().info['id'])
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
