# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : create_enum.py
@Time    : 2019-11-11 18:31
@desc    :
"""

import pandas as pd


def read_excel():
    """ 读取 Excel 模板内容 """
    df = pd.read_excel('3.xlsx')
    for index, row in df.iterrows():
        field_1 = row['枚举名称']
        field_3 = row['代码值']
        field_4 = row['说明']
        # field_5 = row['减免性质名称']
        generate_code(field_1, field_3, field_4)


def generate_code(*args):
    """ 生成代码 """
    field_name = args[0]
    field_way = str(args[1]).replace('.0', '')
    field_items = args[2]

    # NORMAL("0401","一般劳务报酬所得"),
    str_code = f'{field_name}("{field_way}","{field_items}"),\n'

    print(str_code)


def run():
    """ 运行 """
    read_excel()


if __name__ == '__main__':
    run()
