'''
@Author: your name
@Date: 2020-06-25 09:36:14
@LastEditTime: 2020-06-25 09:37:02
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /qt_clock/config.py
'''

import logging

MISSION_CONFIG = 'mission.json'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(filename)s %(funcName)s %(message)s')

# 是否全屏
IS_FULL = False
