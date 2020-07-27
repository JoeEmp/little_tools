from PyQt5.QtWidgets import QWidget
from PyQt5.Qt import pyqtSignal


# 供aps调起，避免直接调用UI的主线程，造成线程冲突
class TranSignalWidget(QWidget):
    showSignal = pyqtSignal(str)

    def send_show_signal(self, mission_id=''):
        self.showSignal.emit(mission_id)
