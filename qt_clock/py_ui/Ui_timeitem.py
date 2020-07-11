'''
@Author: your name
@Date: 2020-06-25 18:15:27
@LastEditTime: 2020-06-25 23:08:32
@LastEditors: your name
@Description: In User Settings Edit
@FilePath: /qt_clock/py_ui/Ui_timeitem.py
'''
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/joe/Documents/CodeManager/mine/myPython/qt_clock/py_ui/timeitem.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(554, 244)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(110, 60, 371, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButton = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout.addWidget(self.radioButton)
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.comboBox = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        self.timeEdit = QtWidgets.QTimeEdit(self.horizontalLayoutWidget)
        self.timeEdit.setObjectName("timeEdit")
        self.timeEdit.setMaximumTime(3600*24)
        self.horizontalLayout.addWidget(self.timeEdit)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.radioButton.setText(_translate("Form", "禁用"))
        self.comboBox.setItemText(0, _translate("Form", "间隔"))
        self.comboBox.setItemText(1, _translate("Form", "周期"))
        self.comboBox.setItemText(2, _translate("Form", "仅一次"))
        self.timeEdit.setDisplayFormat(_translate("Form", "hh:mm"))


