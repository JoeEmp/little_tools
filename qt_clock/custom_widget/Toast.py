import logging
import time
from PyQt5.QtCore import QPoint, Qt, QTime, QSize
from PyQt5 import QtCore, QtQuickWidgets, QtWidgets
from PyQt5.Qt import QColor, QUrl

class Toast(object):
    """Toast控件."""
    Long = 2000
    Short = 1000

    def __init__(self, parent, qml=''):
        """初始化widget.

        :param parent: 显示窗口
        :param qml: 具体加载的qml 默认为 'GUI/py_ui/toast.qml'
        """
        self.toast = QtQuickWidgets.QQuickWidget(parent)
        # 设置为透明和允许显示
        self.toast.setClearColor(QColor(Qt.transparent))
        self.toast.setAttribute(Qt.WA_AlwaysStackOnTop)
        self.parent = parent
        if not qml:
            qml = './py_ui/toast.qml'
        self.toast.setSource(QUrl(qml))
        # widget是透明的，可以先设置状态
        self.show()

    def show(self):
        self.toast.show()

    def show_toast(self, text, time=Short):
        try:
            self.set_time(time)
            self.toast.rootObject().set_text(text)
            self.toast.move(int((self.parent.width() - self.width()) / 2),
                            int(self.parent.height() * 0.085))
            self.toast.rootObject().show_toast()
        except Exception as e:
            logging.error(e)

    def width(self):
        try:
            return self.toast.rootObject().width()
        except Exception as e:
            logging.error(e)
            return 5
        return self.toast.rootObject()

    def set_time(self, time):
        """设置显示时间."""
        if isinstance(time, int):
            self.toast.rootObject().set_time(time)  # 单位为毫秒
        else:
            self.toast.rootObject().set_time(self.short)
            logging.warning('time类型不对 {}'.format(type(time)))
