# build qr_code
# usage watch printhelpMsg function
# requirements 
# qrcode
# fire

import qrcode
import sys
import os
from datetime import datetime
import logging
import fire
import unittest

options = ['-s', '-name']

valueDict = {
    'name': '%s.png' % datetime.now().strftime('%m-%d-%H-%M'),
    'is_save': 0,
    'is_tty': 1,
    'options': 'help'
}


class qr_test(unittest.TestCase):
    def setUp(self):
        self.cases = [
            {
                "name": "full_args",
                "kwargs": {'s': True, 'name': '123'},
                "args": ['231'],
                "result": {
                    'name': '123.png',
                    'is_save': 1,
                    'is_tty': 1,
                    'options': 'build'}},
            {
                "name": "param name before param s",
                "kwargs": {'name': True, 's': '123'},
                "args": ['231'],
                "result": {
                    'name': '%s.png' % datetime.now().strftime('%m-%d-%H-%M'),
                    'is_save': 1,
                    'is_tty': 1,
                    'options': 'build'}},
            {
                "name": "without_text",
                "args": [],
                "kwargs": {'name': True, 's': '123'},
                "result": {
                    'name': '%s.png' % datetime.now().strftime('%m-%d-%H-%M'),
                    'is_save': 0,
                    'is_tty': 1,
                    'options': 'help'}},
            {
                "name": "without qr file name,create file as {%m-%d-%H-%M}.png",
                "kwargs": {'s': True},
                "args": ['231'],
                "result": {
                    'name': '%s.png' % datetime.now().strftime('%m-%d-%H-%M'),
                    'is_save': 1,
                    'is_tty': 1,
                    'options': 'build'
                }},
            {
                "name": "create file and use args filename",
                "kwargs": {'name': '789.png'},
                "args": ['231'],
                "result": {
                    'name': '789.png',
                    'is_save': 1,
                    'is_tty': 1,
                    'options': 'build'
                }},
            {
                "name": "use param name but without filename",
                "kwargs": {'name': True},
                "args": ['231'],
                "result": {
                    'name': '%s.png' % datetime.now().strftime('%m-%d-%H-%M'),
                    'is_save': 0,
                    'is_tty': 1,
                    'options': 'help'
                }},
            {
                "name": "without any args",
                "args": [],
                "kwargs":{},
                "result": {
                    'name': '%s.png' % datetime.now().strftime('%m-%d-%H-%M'),
                    'is_save': 0,
                    'is_tty': 1,
                    'options': 'help'
                }
            }
        ]
        return super().setUp()

    def test_deal_args(self):
        global valueDict
        error_str = 'case is args = {} kwargs =  {}'
        for case in self.cases:
            deal_argv(*case['args'], **case['kwargs'])
            self.assertEqual(valueDict, case['result'],
                             error_str.format(case['args'], case['kwargs']))
            valueDict = {
                'name': '%s.png' % datetime.now().strftime('%m-%d-%H-%M'),
                'is_save': 0,
                'is_tty': 1,
                'options': 'help'
            }


def Modified_suffix(filename):
    '''对无后缀的的文件追加后缀png. '''
    try:
        if int is type(filename):
            filename = str(filename)
        if filename.split('.')[-1] not in ['png', 'jpg', 'gif', 'svg', 'jepg']:
            filename = filename+'.png'
    except AttributeError:
        logging.warning('filename错误,使用时间命名')
        return valueDict['name']
    return filename


def printhelpMsg():
    '''输出指引'''
    print('使用方法如下')
    print("print qr code in tty : python url_to_qr.py https://google.com ")
    print("save pricuter with filename:python url_to_qr.py https://google.com -name google.png")
    print("save pricuter without filename:python url_to_qr.py https://google.com -s")


def to_qr():
    if 'build' == valueDict['options']:
        qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_L,
                           box_size=8,
                           border=8,
                           )
        qr.add_data(sys.argv[1])
        qr.make(fit=True)
        if 1 == valueDict['is_tty']:
            print()
            qr.print_tty()
            print()
        if 1 == valueDict['is_save']:
            img = qr.make_image()
            img.save(valueDict['name'])
            img.show()
        ret = True
    else:
        printhelpMsg()
        ret = False
    return ret


def deal_argv(*args, **kwargs):
    # 判断多选项带help的情况
    if not args:
        return
    else:
        # 多选项情况下且选项带帮助选项
        keys = list(kwargs.keys())
        if 0 == len(set(keys) & set(['h', 'help'])):
            valueDict['options'] = 'build'
            if 0 != len(keys):
                valueDict['is_save'] = 1
        else:
            valueDict['options'] = 'help'
        # print(isinstance(kwargs.get('s', None), bool))
        # print(isinstance(kwargs.get('name', None), str))
        if isinstance(kwargs.get('s', None), bool) and isinstance(kwargs.get('name', None), str):
            valueDict['name'] = Modified_suffix(kwargs['name'])
        elif isinstance(kwargs.get('s', None), str) and isinstance(kwargs.get('name', None), bool):
            valueDict['name'] = Modified_suffix(kwargs['name'])
        elif isinstance(kwargs.get('name', None), str):
            valueDict['name'] = Modified_suffix(kwargs['name'])
        elif isinstance(kwargs.get('name', None), bool):
            valueDict['is_save'] = 0
            valueDict['options'] = 'help'


if __name__ == "__main__":
    is_debug = False
    if is_debug:
        unittest.main()
    else:
        fire.Fire(deal_argv)
        to_qr()
