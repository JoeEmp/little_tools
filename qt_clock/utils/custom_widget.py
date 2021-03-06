'''
@Author: joe
@Date: 2020-06-23 10:28:57
@LastEditTime: 2020-06-29 17:26:20
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /qt_clock/custom_widget.py
'''
import logging
import time
from PyQt5.QtCore import QPoint, Qt, QTime, QSize
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QLineEdit, QListWidgetItem, QPushButton, QWidget, \
    QTimeEdit, QMainWindow
from PyQt5 import QtCore, QtQuickWidgets, QtWidgets
from utils.utils import cryptograph_text, get_full_datetime
from PyQt5.Qt import QColor, QUrl
from custom_widget.Transparent import TransparentFactory
import json


class Transparent(object):

    def set_base_qss(self, widget_name=None, qss=''):
        """支持自定义qss."""
        if not qss and widget_name:
            base_qss = """
            %s{
                background:transparent;
                border-width:0;
                border-style:outset;}
            %s:hover {  
                background:white;
                border-width:1;}
            """ % (widget_name, widget_name)
            self.qss = base_qss
        else:
            self.qss = qss

    def set_parent(self, parent):
        self.parent = parent

    def add_qss(self, qss):
        self.qss += qss


class TransparentButton(Transparent, QPushButton):
    def __init__(self, parent=None, qss=''):
        super(QPushButton, self).__init__(parent)
        if not qss:
            qss = """QPushButton{
                color:white;
                background:transparent;
                border-width:0;
                font-size:20px;
                text-decoration:underline;
                border-style:outset;} """
        self.set_base_qss(
            widget_name=TransparentButton.__base__.__name__, qss=qss)
        self.setStyleSheet(self.qss)


class UntitleWidget(QWidget):
    _startPos = None
    _endPos = None
    _isTracking = False

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)

    # 重写移动事件
    def mouseMoveEvent(self, e: QMouseEvent):
        if self._startPos:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    # 释放鼠标时做出判断保证正常贴边 bug：y轴没做限制
    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None


class UntitleWindow(QMainWindow):
    _startPos = None
    _endPos = None
    _isTracking = False

    def __init__(self, parent=None, flags=None):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)

    # 重写移动事件
    def mouseMoveEvent(self, e: QMouseEvent):
        # if not self.geometry().contains(self.pos()):
        if self._startPos:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:  # and not self.geometry().contains(self.pos()):
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    # 释放鼠标时做出判断保证正常贴边 bug：y轴没做限制
    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:  # and not self.geometry().contains(self.pos()):
            self._isTracking = False
            self._startPos = None
            self._endPos = None
        # print(self.x(), self.y())


class TimeItem(QListWidgetItem):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.parent = parent

    def setupUi(self, *args, **kwargs):
        self.widget = QWidget()
        try:
            self.setSizeHint(QSize(self.parent.width() - 20, 40))
            self.widget.setGeometry(QtCore.QRect(
                0, 0, self.parent.width() - 20, 40))
        except Exception as e:
            logging.warning(e)
            self.setSizeHint(QSize(80, 60))
        self.widget.setObjectName("Form")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.widget)
        self.horizontalLayoutWidget.setGeometry(
            QtCore.QRect(10, 0, self.widget.width() - 10, self.widget.height()))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(
            self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButton = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setText('禁用')
        self.horizontalLayout.addWidget(self.radioButton)
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setText('abc')
        self.horizontalLayout.addWidget(self.lineEdit)
        self.comboBox = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBoxSel = {
            '间隔': "interval", '周期': 'cron', '仅一次': 'date'}
        for sel in self.comboBoxSel:
            self.comboBox.addItem(sel)
        self.horizontalLayout.addWidget(self.comboBox)
        self.timeEdit = QTimeEdit(self.horizontalLayoutWidget)
        self.timeEdit.setObjectName("timeEdit")
        self.timeEdit.setDisplayFormat('hh:mm:ss')
        self.horizontalLayout.addWidget(self.timeEdit)
        QtCore.QMetaObject.connectSlotsByName(self.widget)
        # 设置配置
        try:
            self.set_data(info=kwargs['info'])
        except Exception as e:
            self.set_data(info=None)
        # 设置交互
        self.set_connect()
        return self.widget

    def set_data(self, *args, **kwargs):
        if 'info' in kwargs.keys() and kwargs['info']:
            self.info = kwargs['info']
        else:
            self.info = {
                "id": "luck",
                "trigger": "interval",
                "time": 3600,
                "is_action": False,
                "mission_name": 'new mission'
            }
        self.set_ui()

    def set_ui(self):
        try:
            self.radioButton.setChecked(self.info['is_action'])
            self.radio_check()
            self.lineEdit.setText(self.info['mission_name'])
            index = list(self.comboBoxSel.values()).index(self.info['trigger'])
            self.comboBox.setCurrentIndex(index)
            # to do
            if 'interval' == self.info['trigger']:
                self.timeEdit.setTime(QTime(0, 0).addSecs(self.info['time']))
            elif 'date' == self.info['trigger']:
                logging.warning('暂不支持 date 设置')
            elif 'cron' == self.info['trigger']:
                logging.warning('暂不支持 cron 设置')

        except Exception as e:
            logging.warning(e)

    def update_info(self) -> bool:
        flag = False
        if 'luck' == self.info['id']:
            self.info['id'] = cryptograph_text(str(int(time.time())))
        index = self.comboBox.currentIndex()
        self.info['trigger'] = list(self.comboBoxSel.values())[index]
        self.info['is_action'] = self.radioButton.isChecked()
        self.info['mission_name'] = self.lineEdit.text()
        aps_time = self.timeEdit.time()
        self.info[
            'time'] = aps_time.hour() * 3600 + aps_time.minute() * 60 + aps_time.second()
        # 新任务无sign
        if 'sign' not in self.info.keys():
            self.info['createtime'] = get_full_datetime()
            self.info['sign'] = cryptograph_text(
                json.dumps(self.info, ensure_ascii=False))
            flag = True
        # 旧任务重新校验
        else:
            sign = self.info.pop('sign')
            if sign != cryptograph_text(json.dumps(self.info, ensure_ascii=False)):
                self.info['sign'] = cryptograph_text(
                    json.dumps(self.info, ensure_ascii=False))
                flag = True
            else:
                self.info['sign'] = sign
        return flag

    def set_connect(self):
        self.radioButton.clicked.connect(self.radio_check)

    def radio_check(self):
        if self.radioButton.isChecked():
            self.radioButton.setStyleSheet('QRadioButton{color:green}')
            self.radioButton.setText('启用')
        else:
            self.radioButton.setStyleSheet('QRadioButton{color:red}')
            self.radioButton.setText('禁用')


class TransparentLineEdit(QLineEdit, Transparent):

    def __init__(self, parent=None, qss=''):
        super(QLineEdit, self).__init__(parent)
        self.set_base_qss(
            widget_name=TransparentLineEdit.__base__.__name__, qss=qss)
        self.setStyleSheet(self.qss)

    def leaveEvent(self, QEvent):
        super().leaveEvent(QEvent)
        self.clearFocus()

    def add_qss(self, qss):
        super().add_qss(qss)
        # logging.info(self.qss)
        self.setStyleSheet(self.qss)


class TodoListWidgetItem(QListWidgetItem):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.parent = parent

    def setupUi(self, *args, **kwargs):
        try:
            self.setSizeHint(QSize(self.parent.width() - 140, 30))
        except Exception as e:
            logging.warning(e)
            self.setSizeHint(QSize(312, 25))
        self.frame = QtWidgets.QFrame()
        # self.frame.setStyleSheet('QFrame{background:rgba(0,0,0,0.25)}')
        try:
            self.frame.setGeometry(QtCore.QRect(
                0, 0, self.parent.width(), 25))
        except Exception as e:
            logging.warning(e)
            self.frame.setGeometry(QtCore.QRect(0, 0, 312, 25))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        # self.lab = QtWidgets.QLabel(self.widget)
        # self.lab.setMaximumWidth(4)
        # self.lab.setMaximumHeight(16)
        # self.lab.setStyleSheet('QLabel{background:#ffffff}')
        # self.horizontalLayout.addWidget(self.lab)
        self.radioButton = QtWidgets.QRadioButton(self.frame)
        self.radioButton.setObjectName("radioButton")
        self.radioButton.clicked.connect(self.complete)
        self.horizontalLayout.addWidget(self.radioButton)
        self.lineEdit = TransparentFactory().get_widget('LineEdit', parent=self.frame)
        self.lineEdit.setObjectName("lineEdit")
        qss = """
        QLineEdit{
            font-family: YouYuan;
            color: #fff;
            font-size: 16pt;
            background:transparent;
            border:0px;
            border-bottom-color:#fff;
        }
        QLineEdit:hover{
            font-family: YouYuan;
            border:2px;
            }
        """
        # 'QLineEdit:hover{font-family: YouYuan;color: #000;background:#fff;}'
        self.lineEdit.setStyleSheet(qss)
        mission_name = 'demo'
        if 'mission_name' in kwargs.keys():
            mission_name = kwargs['mission_name']
        self.lineEdit.setText(mission_name)
        self.horizontalLayout.addWidget(self.lineEdit)
        return self.frame

    def set_data(self, mission_name):
        self.lineEdit.setText(mission_name)

    def complete(self):
        try:
            row = self.parent.row(self)
            self.parent.takeItem(row)
        except Exception as e:
            logging.warning(e)


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
