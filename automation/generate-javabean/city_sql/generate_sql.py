# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : generate_sql.py
@Time    : 2021/4/20 上午11:10
@desc    :
"""

import pandas as pd
import requests


def read_excel():
    sql_str = "INSERT INTO T_DICT (DICT_CODE, DICT_NAME, DICT_VALUE, PARENT_DICT_CODE, DICT_REMARK) VALUES " \
              "('AREAS_DICT', '区级字典', '', '', null);"
    print(sql_str)

    """ 读取 Excel 模板内容 """
    df = pd.read_csv('areas.csv')
    for index, row in df.iterrows():
        city_code = row['cityCode']
        province_code = row['provinceCode']
        name = row['name']
        code = row['code']
        generate_code(code, name, province_code, city_code)


def generate_code(code, name, province_code, city_code):
    sql_str = "INSERT INTO T_DICT (DICT_CODE, DICT_NAME, DICT_VALUE, PARENT_DICT_CODE, DICT_REMARK) VALUES " \
              f"('{code}', '{name}', '{city_code}', 'AREAS_DICT', '{province_code}');"
    print(sql_str)


def run():
    """ 运行 """
    read_excel()


if __name__ == '__main__':
    run()
