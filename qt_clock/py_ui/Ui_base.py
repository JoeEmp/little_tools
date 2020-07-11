'''
@Author: your name
@Date: 2020-06-23 13:46:57
@LastEditTime: 2020-06-24 19:14:19
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /qt_clock/Ui_base.py
'''
from PyQt5.QtWidgets import QWidget
import os


class Ui_base(object):
    def __init__(self, widget_type=''):
        if "QWidget" == widget_type:
            self.widget = QWidget()
        self.setup()
        super().__init__()

    def setup(self):
        pass

    def read_qss(self, filename=''):
        if not filename:
            filename = os.path.abspath(__file__).replace('.py', '.qss')
        with open(filename, encoding='utf-8') as f:
            self.qss = f.read()
