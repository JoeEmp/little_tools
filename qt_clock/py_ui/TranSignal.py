from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import pyqtSignal

# 供aps调起，避免直接调用UI的主线程，造成线程冲突
class TranSignalWidget(QtWidgets.QWidget):
    showSignal = pyqtSignal(str)

    def send_show_signal(self):
        self.showSignal.emit('show')