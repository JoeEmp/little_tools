'''
@Author: joe
@Date: 2020-06-25 09:46:41
@LastEditTime: 2020-06-25 10:00:09
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /qt_clock/tests/test_misson.py
'''


import json
import unittest
import os
import sys
dirpath = os.path.dirname(os.path.abspath(__file__))
parent_path = os.sep.join(dirpath.split(os.sep)[:-1])
sys.path.append(parent_path)
from utils.mission import TimeMission

TEST_CONFIG_FILE = 'time.json'


def write_file(text, filename=TEST_CONFIG_FILE):
    with open(filename,'w', encoding='utf-8') as f:
        f.write(text)


def remove_file(filename=TEST_CONFIG_FILE):
    os.remove(filename)


class mytest(unittest.TestCase):

    def setUp(self):
        self.json_config = TEST_CONFIG_FILE
        self.TM = TimeMission()
        if 'test_error_file_get' == self._testMethodName:
            write_file('123')

    def test_1_no_file_add(self):
        """ 无文件时的添加 """
        self.TM.get_config(self.json_config)
        self.assertEqual(self.TM.missions, dict())

    def test_2_error_file_get(self):
        """文件格式错误时获取配置. """
        self.TM.get_config(self.json_config)
        self.assertEqual(self.TM.missions, dict())

    def test_3_add_mission(self):
        "无文件时添加mission."
        mission_id = 456
        mission = dict(id=mission_id)
        self.TM.update_mission(mission,flag=True,debug=True,filename=self.json_config)
        self.assertEqual(mission,self.TM.get_mission(mission_id),'add mission error')

    def test_4_has_file_add_mission(self):
        "有文件时添加mission."
        mission_id = 789
        mission = dict(id=mission_id,msg='update 456 mission')
        self.TM.update_mission(mission,flag=True,debug=True,filename=self.json_config)
        self.assertEqual(mission,self.TM.get_mission(mission_id),'add mission error')

    def test_5_has_file_update_mission(self):
        "有文件时更新mission."
        mission_id = 456
        mission = dict(id=mission_id,msg='update 456 mission')
        self.TM.update_mission(mission,flag=True,debug=True,filename=self.json_config)
        self.assertDictEqual(mission,self.TM.get_mission(mission_id),'update mission error')

    def tearDown(self):
        self.TM = None
        try:
            if self._testMethodName not in ['test_3_add_mission','test_4_has_file_add_mission']:
                os.remove(self.json_config)
        except Exception as e:
            pass


if __name__ == "__main__":
    os.chdir(dirpath)
    unittest.main()
