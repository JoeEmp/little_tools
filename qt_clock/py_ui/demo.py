# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'demo.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication


class Ui_Form(object):
    def __init__(self):
        self.wiget = QtWidgets.QWidget()
        self.setupUi(self.wiget)
        self.wiget.show()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(551, 261)
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 20, 511, 221))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.lab_time = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lab_time.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_time.setObjectName("lab_time")
        self.gridLayout.addWidget(self.lab_time, 1, 1, 1, 2)
        self.lab_date = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lab_date.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lab_date.setObjectName("lab_date")
        self.gridLayout.addWidget(self.lab_date, 0, 0, 1, 1)
        self.btn_pass = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_pass.setMaximumSize(QtCore.QSize(80, 16777215))
        self.btn_pass.setObjectName("btn_pass")
        self.gridLayout.addWidget(self.btn_pass, 3, 2, 1, 1)
        self.lab_title = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lab_title.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.lab_title.setObjectName("lab_title")
        self.gridLayout.addWidget(self.lab_title, 2, 1, 1, 2)
        self.btn_later = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_later.setMaximumSize(QtCore.QSize(120, 16777215))
        self.btn_later.setObjectName("btn_later")
        self.gridLayout.addWidget(self.btn_later, 3, 3, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lab_time.setText(_translate("Form", "12:03:35"))
        self.lab_date.setText(_translate("Form", "2020-06-23"))
        self.btn_pass.setText(_translate("Form", "pass"))
        self.lab_title.setText(_translate("Form", "TextLabel"))
        self.btn_later.setText(_translate("Form", "10 min later"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Ui_Form()
    sys.exit(app.exec_())


