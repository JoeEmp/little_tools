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

class RemindTimer(QTimer):
    # overSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def start(self, sec=1):
        super().start(int(250*sec))

    def free(self):
        self.killTimer(self.timerId())


class ClockThread(QThread):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        if 'widget' in kwargs.keys():
            self.widget = kwargs['widget']
        else:
            self.widget = None
        
    def run(self):
        self.timer = RemindTimer()
        self.timer.start()
        self.timer.timeout.connect(self.update_widget_ui)

    def update_widget_ui(self):
        if self.widget:
            self.widget.lab_date.setText("%s" % get_date())
            self.widget.lab_time.setText('{}'.format(get_time()))
            logging.debug('update date')


class Clock(QObject):
    def __init__(self, widget=None):
        super().__init__()
        # self.__timer = RemindTimer()
        self.widget = widget
        self.__th = ClockThread(widget=self.widget)
        self.__th.start()

    def run(self):
        if self.__th.is_lock():
            self.__th.set_lock(False)
        print('clock is run')

    def free(self):
        self.__th.set_lock(True)
    
    def is_run(self):
        return self.__th.isRunning()

class test_thread(QThread):
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
        # logging.info('emit timeout')
        return self.overSignal.emit('timeout')
    
    def stop(self):
        self.timer.stop()