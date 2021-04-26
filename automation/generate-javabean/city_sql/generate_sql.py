# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : generate_sql.py
@Time    : 2021/4/20 上午11:10
@desc    :
"""

import pandas as pd


def read_excel():
    sql_str = "INSERT INTO T_DICT (DICT_CODE, DICT_NAME, DICT_VALUE, PARENT_DICT_CODE, DICT_REMARK) VALUES " \
              "('PROVINCIAL_DICT', '省级字典', '', '', null);"
    print(sql_str)

    """ 读取 Excel 模板内容 """
    df = pd.read_csv('provinces.csv')
    for index, row in df.iterrows():
        code = row['code']
        name = row['name']
        generate_code(code, name)


def generate_code(code, name):
    sql_str = "INSERT INTO T_DICT (DICT_CODE, DICT_NAME, DICT_VALUE, PARENT_DICT_CODE, DICT_REMARK) VALUES " \
              f"('{code}', '{name}', '', 'PROVINCIAL_DICT', null);"
    print(sql_str)


def run():
    """ 运行 """
    read_excel()


if __name__ == '__main__':
    run()
