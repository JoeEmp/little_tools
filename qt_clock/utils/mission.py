'''
@Author: joe
@Date: 2020-06-25 09:28:01
@LastEditTime: 2020-06-30 11:57:39
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /qt_clock/mission.py
'''
import os
import json
import logging
from utils.utils import get_full_datetime, cryptograph_text
from config import MISSION_CONFIG
from utils.aps import MYAPS


# MISSION_CONFIG = 'time.json'


class TimeMission():
    """任务管理，配置管理

    Attributes:
        missions:任务配置信息 dict of dict(为具体的任务)

    """

    def __init__(self):
        super().__init__()
        self.missions = self.get_json()

    def get_json(self, filename=MISSION_CONFIG) -> dict:
        """从文件获取任务信息.

        :param filename:配置文件，默认为 config文件的MISSION_CONFIG
        :return: dict
        """
        try:
            logging.debug('filename is {}'.format(filename))
            with open(filename, encoding='utf-8') as f:
                # logging.info('read job from json file')
                return json.loads(f.read(), encoding='utf-8')
        except FileNotFoundError:
            return dict()

    def update_json(self, filename=MISSION_CONFIG) -> bool:
        try:
            with open(filename, 'w') as f:
                f.write(json.dumps(self.missions))
                return True
        except FileNotFoundError as e:
            logging.warning(e)
        return False

    def set_mission(self, missions=None):
        """设置定时任务

        :param missions:任务配置
        :return:
        """
        # set aps
        if missions:
            self.missions = missions
        MYAPS.add_json_jobs(self.missions)

    def add_mission(self, mission: dict, filename=MISSION_CONFIG):
        if not self.missions:
            self.missions = self.get_json(filename)
            MYAPS.set_json_jobs(self.missions)
        
        # add aps
        MYAPS.add_json_job(mission)

    def get_mission(self, mission_id: str) -> dict:
        try:
            return self.missions[mission_id]
        except Exception as e:
            return dict()

    def update_mission(self, mission: dict,flag: bool):
        if flag:
            try:
                mission_id = mission['id']
                self.missions[mission_id] = mission
                self.update_file()
                # update aps
                MYAPS.update_mission(mission)
            except KeyError:
                self.add_mission(mission)

    def del_mission(self, mission_id) -> bool:
        """去除内存和aps以及文件的任务配置

        :param mission_id:任务id
        :return:
        """
        try:
            self.missions.pop(mission_id)
            self.update_file()
            # remove aps job
            MYAPS.remove_job(mission_id)
            return True
        except Exception as e:
            logging.warning(e)
        return False

    def update_file(self,filename=MISSION_CONFIG):
        with open(filename, 'w') as f:
            f.write(json.dumps(self.missions))


TIME_MISSION = TimeMission()
