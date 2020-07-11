'''
@Author: joe
@Date: 2020-06-25 09:46:41
@LastEditTime: 2020-06-25 10:00:09
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /qt_clock/tests/test_misson.py
'''

import unittest

MISSION_CONFIG = 'time.json'

class mytest(unittest.TestCase):
    def test_first_add(self,filename):
        """ 无文件时的添加 """
        filename  = 'time.json'
        mission = mission()

    def test_add(self,filename):
        mission = mission()
        mission.add_mission()


if __name__ == "__main__":
    pass