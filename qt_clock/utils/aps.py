'''
@Author: your name
@Date: 2020-06-22 17:23:15
@LastEditTime: 2020-06-30 13:36:27
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /qt_clock/aps.py
'''
import logging
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.qt import QtScheduler

class my_aps(BackgroundScheduler):
    def __init__(self, gconfig={}, **options):
        super().__init__(gconfig=gconfig, **options)
        self.mission_ids = list()
        self.__widget = None

    def set_widget(self, widget):
        self.__widget = widget

    def set_json_job(self, missions, widgets=None):
        self.remove_all_jobs()
        logging.info('missions is %r' % missions)
        self.add_json_jobs(missions, widgets)
        # logging.info('set job')

    def add_json_job(self, mission: dict, widget=None):
        if not widget:
            widget = self.__widget
        try:
            if 'interval' == mission['trigger']:
                self.add_job(func=widget.send_show_signal, trigger='interval',
                             seconds=mission['time'], id=mission['id'])
                # logging.info('interval 添加完成 id is {}'.format(mission['id']))
            elif 'cron' == mission['trigger']:
                logging.warning('暂不支持 cron')
            elif 'date' == mission['trigger']:
                logging.warning('暂不支持 date')
            else:
                logging.warning('未知错误')
            if not mission['is_action']:
                self.get_job(mission['id']).pause()
        except KeyError as e:
            logging.error(e)
            logging.error('mission json error {}'.format(mission))

    def add_json_jobs(self, missions, widgets=None):
        for mission_id in missions:
            self.add_json_job(missions[mission_id], widgets)

    def update_mission(self, mission):
        if mission['is_action']:
            self.reschedule_job(mission['id'], trigger=mission['trigger'],
                                seconds=mission['time'])
        else:
            self.get_job(mission['id']).pause()
        logging.info('aps update mission {}'.format(mission))

    def update_missions(self, missions):
        for mission in missions:
            self.update_mission(mission)

    def add_interval_job(self):
        pass

    def add_cron_job(self):
        pass

    def add_date_job(self):
        pass

if ('Asi','a/S') == time.tzname:
    MYAPS = my_aps(timezone="Asia/Shanghai")
else:
    MYAPS = my_aps()


def set_aps(widget, *args, **kwargs):
    MYAPS.set_widget(widget)
    # MYAPS.add_job(widget.update_ui,'interval',seconds=1,id='update_time')


if __name__ == "__main__":
    def test_aps():
        print('hello')


    backg = BackgroundScheduler()
    backg.add_job(test_aps, 'interval', seconds=2, id="hello")
    # backg.add_job(test_aps, 'interval', seconds=6, id="world")
    job = backg.get_jobs()
    print(job)
    backg.start()
    while True:
        print(backg.get_jobs())
