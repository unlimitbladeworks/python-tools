# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : gol.py
@Time    : 2020/8/16 3:58 下午
@desc    : 跨所有模块的全局变量字典方法,目的是为了将配置信息的初始化统一
"""


# 初始化
def _init():
    global _global_dict
    _global_dict = {}


def set_value(key, value):
    """ 定义一个全局变量 """
    _global_dict[key] = value


def get_value(key, defValue=None):
    """ 获得一个全局变量,不存在则返回默认值 """
    try:
        return _global_dict[key]
    except KeyError:
        return defValue
