# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : auto_classify.py
@Time    : 2019/4/26 10:53
@desc    : 根据文件和时间进行自动归为
"""

import shutil
import os
import datetime


def classify():
    try:
        exclude_suffix_list = ['py', 'exe']
        pwd_path = os.getcwd()
        files = os.listdir(pwd_path)
        today = get_time()
        for file in files:
            suffix = file.split(".")[-1]  # 获取文件后缀名称
            if suffix not in exclude_suffix_list:   # 如果文件不是py,exe结尾,则移动文件
                suffix_dir = os.path.join(pwd_path, suffix)
                file_dir = os.path.join(suffix_dir, today)
                if not os.path.exists(file_dir):
                    os.makedirs(file_dir)
                    shutil.move(file, file_dir)
                else:
                    shutil.move(file, file_dir)
    except Exception as e:
        print('文件夹中已经存在某个文件，具体信息：\n', e)


def get_time():
    """ 获取当前日期，并且格式化为类似 190426 的字符串 """
    time = datetime.date.today()
    today = time.strftime('%y%m%d')
    return today


if __name__ == '__main__':
    classify()
    print('分类完成！')
