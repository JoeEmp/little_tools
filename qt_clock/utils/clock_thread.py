'''
@Author: your name
@Date: 2020-06-30 10:10:52
@LastEditTime: 2020-06-30 15:53:48
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /qt_clock/utils/clock_thread.py
'''
import logging
from time import sleep
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QObject
from utils.utils import get_date,get_time

class ClockThread(QThread):
    overSignal = pyqtSignal(str)

    def __init__(self, parent=None, *args, **kwargs):
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        if 'widget' in kwargs.keys():
            self.widget = kwargs['widget']
        else:
            self.widget = None
        self.timer = None

    def run(self):
        logging.info('run thread')
        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.send_signal)
        self.timer.start()
        self.exec()

    def send_signal(self):
        return self.overSignal.emit('timeout')
    
    def stop(self):
        self.timer.stop()