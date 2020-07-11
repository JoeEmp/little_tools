'''
@Author: your name
@Date: 2020-06-24 18:05:59
@LastEditTime: 2020-06-28 16:02:25
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /qt_clock/utils.py
'''

import time
import os
import hashlib
from PyQt5.Qt import QIcon
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication


def cryptograph_text(text):
    """
    暂时只提供md5加密

    Arguments:\n
            text {str} -- 需要加密的文本

    Returns:\n
            str -- 密文或者空
    """
    # logging.debug(text)
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    return m.hexdigest()


def get_date():
    return time.strftime("%Y-%m-%d", time.localtime(time.time()))


def get_time():
    return time.strftime("%H:%M:%S", time.localtime(time.time()))


def get_datetime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


def set_app(app):
    # 关闭所有窗口,也不关闭应用程序
    app.setApplicationName('rest_clock')
    app.setApplicationDisplayName('rest_clock')
    QApplication.setQuitOnLastWindowClosed(False)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("./icon/clock.png"), QtGui.QIcon.Normal,
                   QtGui.QIcon.Off)
    app.setWindowIcon(icon)
    # app.setWindowIcon(QIcon('./icon/clock.png'))


if __name__ == "__main__":
    print(get_date())
    print(get_time())
    print(get_datetime())
