import logging
from PyQt5.Qt import QLineEdit, QPushButton,QListWidget,QListWidgetItem


class TransparentFactory():

    def get_widget(self,widget_name,*args,**kwargs):
        if 'LineEdit' == widget_name:
            return TransparentLineEdit(*args,**kwargs)
        elif 'Button' == widget_name:
            return TransparentButton(*args,**kwargs)
        elif 'listWidget' == widget_name:
            return TransparentListWidget(*args,**kwargs)
        else:
            logging.warning('{} not in TransparentFactory'.format(widget_name))
        return None

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

class TransparentListWidget(QListWidget,Transparent):

    def __init__(self, parent=None, qss=''):
        super(QListWidget, self).__init__(parent)
        self.set_base_qss(
            widget_name=TransparentListWidget.__base__.__name__, qss=qss)
        self.setStyleSheet(self.qss)