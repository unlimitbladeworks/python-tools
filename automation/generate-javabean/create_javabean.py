# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : create_javabean.py
@Time    : 2019-10-24 10:32
@desc    : 根据 excel 模板生成 javabean 代码
"""
import pandas as pd


def read_excel():
    """ 读取 Excel 模板内容 """
    df = pd.read_excel('2.xlsx')
    for index, row in df.iterrows():
        field_name = row['字段名称']
        field_comment = row['字段含义']
        field_type = row['字段类型']
        generate_code(field_name, field_comment, field_type)


def generate_code(*args):
    """ 生成代码 """
    field_name = args[0]
    field_comment = args[1]
    field_type = args[2]
    comment_str = '/**\n' \
        f' * {field_comment}\n' \
                  ' */\n'
    code_str = f'private {field_type} {field_name};\n'

    result_str = comment_str + code_str
    print(result_str)


def run():
    """ 运行 """
    read_excel()


if __name__ == '__main__':
    run()
