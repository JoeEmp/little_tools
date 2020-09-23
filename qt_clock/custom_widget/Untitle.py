import logging
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QWidget, QMainWindow


class UntitleParentFactory(object):

    def get_widget(self,widget_name,*args,**kwargs):
        if 'Widget' == widget_name:
            return UntitleWidget(*args,**kwargs)
        elif 'MainWindow' == widget_name:
            return UntitleMainWindow(*args,**kwargs)
        else:
            logging.warning('{} not in UntitleParentFactory'.format(widget_name))

class UntitleParent(object):
    _startPos = None
    _endPos = None
    _isTracking = False

    def __init__(self):
        super().__init__()
        try:
            self.setWindowFlags(Qt.FramelessWindowHint)
        except AttributeError:
            logging.warning('this widget without untitleMethod')

    # 重写移动事件
    def mouseMoveEvent(self, e: QMouseEvent):
        if self._startPos:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

class UntitleWidget(QWidget, UntitleParent):
    pass

class UntitleMainWindow(QMainWindow, UntitleParent):

    pass
