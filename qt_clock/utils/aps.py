'''
@Author: joe
@Date: 2020-06-22 17:23:15
@LastEditTime: 2020-06-30 13:36:27
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /qt_clock/aps.py
'''
import logging
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger

class my_aps(BackgroundScheduler):
    def __init__(self, gconfig={}, **options):
        super().__init__(gconfig=gconfig, **options)
        self.mission_ids = set()
        self.__widget = None

    def set_widget(self, widget):
        self.__widget = widget

    def set_json_jobs(self, missions, widgets=None):
        """初始化任务."""
        self.remove_all_jobs()
        logging.info('missions is %r' % missions)
        self.add_json_jobs(missions, widgets)

    def add_json_job(self, mission: dict, widget=None):
        try:
            if 'interval' == mission['trigger']:
                self.add_interval_job(mission,widget)
                logging.debug('interval 添加完成 id is {}'.format(mission['id']))
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
        except TypeError as e:
            logging.error(e)

    def add_json_jobs(self, missions, widgets=None):
        for mission_id in missions:
            self.add_json_job(missions[mission_id], widgets)

    def update_mission(self, mission):
        if mission['is_action']:
            job = self.get_job(mission['id'])
            if 'interval' == mission['trigger']:
                self.reschedule_job(mission['id'], trigger=mission['trigger'],
                                    seconds=mission['time'])
            if 'cron' == mission['trigger']:
                pass
            elif 'date' == mission['trigger']:
                pass
        else:
            job = self.get_job(mission['id'])
            if job:
                job.pause()
        logging.info('aps update mission {}'.format(mission['id']))

    def update_missions(self, missions):
        for mission in missions:
            self.update_mission(mission)

    def add_interval_job(self,mission,widget=None):
        if not widget:
            widget = self.__widget
        trigger = IntervalTrigger(seconds=mission['time'])
        self.add_job(func=widget.send_show_signal, trigger=trigger,
                             id=mission['id'])

    def add_cron_job(self,mission,widget=None):
        if not widget:
            widget = self.__widget
        trigger = DateTrigger(run_date=mission['time'])
        self.add_job(func=widget.send_show_signal, trigger=trigger,
                             id=mission['id'])

    def add_date_job(self,mission,widget=None):
        if not widget:
            widget = self.__widget
        trigger = DateTrigger(run_date=mission['time'])
        self.add_job(func=lambda:widget.send_show_signal(mission['id']), trigger=trigger,
                             id=mission['id'])


if ('Asi', 'a/S') == time.tzname:
    MYAPS = my_aps(timezone="Asia/Shanghai")
else:
    MYAPS = my_aps()


def set_aps(widget, *args, **kwargs):
    MYAPS.set_widget(widget)


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
