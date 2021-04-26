# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : ocr_pdf.py
@Time    : 2019-09-24 16:57
@desc    : ocr 识别 pdf 转 txt
"""

import os
import configparser


class Pdf2Txt(object):

    def __init__(self):
        """ 初始化读取 keys 的信息 """
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keys.ini')
        config.read(config_path)
        self.APP_ID = config["KEYS"]["APP_ID"]
        self.API_KEY = config["KEYS"]["API_KEY"]
        self.SECRET_KEY = config["KEYS"]["SECRET_KEY"]

    def run(self):
        pass


if __name__ == '__main__':
    pass
