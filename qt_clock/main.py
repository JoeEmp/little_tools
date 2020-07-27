'''
@Author: your name
@Date: 2019-09-01 17:23:03
@LastEditTime: 2020-06-30 10:56:31
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /AirMemoServer/Users/joe/Documents/git_repo/github/AirMemo/main.py
'''
import sys
from py_ui.clock_tray import clock_tray
from PyQt5.QtNetwork import QLocalServer, QLocalSocket
from PyQt5.QtWidgets import QApplication
from py_ui.Ui_timeout import Ui_Timeout
from py_ui.Ui_settings import Ui_Settings
from py_ui.TranSignal import TranSignalWidget
from utils.aps import MYAPS, set_aps
from utils.mission import TIME_MISSION
from utils.utils import set_app
import logging


def main():
    # ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("AirMemo_appid")
    app = QApplication(sys.argv)
    serverName = 'rest_clock'
    socket = QLocalSocket()
    socket.connectToServer(serverName)

    # 如果连接成功，表明server已经存在，当前已有实例在运行
    if socket.waitForConnected(500):
        sys.exit(app.quit())

    # 没有实例运行，创建服务器   
    localServer = QLocalServer()
    localServer.listen(serverName)
    try:
        set_app(app)
        tray = clock_tray()
        timeout_win = Ui_Timeout(tray)
        settings_win = Ui_Settings(tray)
        tran_win = TranSignalWidget()
        print(tran_win.styleSheet())
        tran_win.showSignal.connect(timeout_win.show)
        win_dict = {"timeout_win": timeout_win, 'settings_win': settings_win}
        tray.set_menu(win_dict)
        set_aps(tran_win)
        timeout_win.show()
        TIME_MISSION.set_mission()
        MYAPS.start()
        logging.debug('APS jobs {}'.format(MYAPS.get_jobs()))
        sys.exit(app.exec_())
    finally:
        localServer.close()


if __name__ == '__main__':
    main()

    # app = QApplication(sys.argv)
    # ex = Ui_Timeout('QWidget')
    # sys.exit(app.exec_())
