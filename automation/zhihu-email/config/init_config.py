# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : init_config.py
@Time    : 2020/8/16 4:09 下午
@desc    :
"""

import os
from config import gol
import configparser


# 寻找file.ini绝对路径
def find_file_path():
    return os.path.dirname(os.path.abspath(__file__))


def read_urls():
    """ 读取当前目录下 url """
    txt_path = os.path.join(find_file_path(), 'urls.txt')
    print(f'url文件路径：{txt_path}')
    with open(txt_path, 'r', encoding='utf-8') as f:
        return [line.strip().replace('\n', '') for line in f.readlines()]


# 初始化配置函数
def init_config():
    # 初始化全局变量的字典
    gol._init()
    # 读取路径的配置文件(**原本是ConfigParser,但是读取%号会有异常**)
    cf = configparser.RawConfigParser()
    # 邮箱配置文件
    cf.read([os.path.join(find_file_path(), 'mail_settings.ini')], encoding='utf-8')
    mail_host = cf.get('mail-server', 'mail_host')  # 邮箱服务器
    mail_port = int(cf.get('mail-server', 'mail_port'))  # 邮箱服务器端口
    mail_user = cf.get('mail-client', 'mail_user')  # 邮箱用户名
    mail_pwd = cf.get('mail-client', 'mail_pwd')  # 邮箱密码
    mail_receivers = cf.get('mail-receivers', 'mail_receivers')  # 收件人邮箱

    # 放入全局dict中对应变量
    gol.set_value('mail_host', mail_host)
    gol.set_value('mail_port', mail_port)
    gol.set_value('mail_user', mail_user)
    gol.set_value('mail_pwd', mail_pwd)
    gol.set_value('mail_receivers', mail_receivers)
    print('===加载mail_settings.ini配置文件完毕=== ...')


if __name__ == '__main__':
    ''' 以下为测试,忽略 '''
    init_config()
