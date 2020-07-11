'''
@Author: your name
@Date: 2020-06-22 17:07:30
@LastEditTime: 2020-06-22 17:23:07
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /qt_clock/main.py
'''
import logging
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction


class clock_tray(QSystemTrayIcon):
    widget = None
    __user_info = dict()

    def __init__(self, widget_dict=None):
        super().__init__()
        self.set_data()
        self.show()

    def set_menu(self, widget_dict):
        '''
        设置菜单
        :param widget_dict: {'widget_name':widget_object}
        :return:
        '''
        self.widget_dict = widget_dict
        self.main_menu = QMenu()
        self.show_action = QAction('&show',triggered=self.widget_dict['timeout_win'].show)
        self.settings_action = QAction('&settings', triggered=self.widget_dict['settings_win'].show)
        self.quit_action = QAction('&exit', triggered=self.quitapp)

        self.main_menu.addAction(self.show_action)
        self.main_menu.addAction(self.settings_action)
        self.main_menu.addAction(self.quit_action)

        self.set_icon()

        self.setContextMenu(self.main_menu)

    def set_icon(self):
        '''
        设置图标
        :return:
        '''
        # 这里的路径从main.py 算起
        self.setIcon(QIcon('./icon/clock.png'))
        pass

    def set_data(self):
        '''
        设置data
        :return:
        '''
        self.setObjectName('time_tary')
        self.set_icon()
        self.setVisible(True)

    def quitapp(self):
        try:
            QCoreApplication.instance().quit()
            # 在应用程序全部关闭后，TrayIcon其实还不会自动消失，
            # 直到你的鼠标移动到上面去后，才会消失，
            # 这是个问题，（如同你terminate一些带TrayIcon的应用程序时出现的状况），
            # 这种问题的解决我是通过在程序退出前将其setVisible(False)来完成的。
            self.setVisible(False)
        except Exception as e:
            logging.error(e)
