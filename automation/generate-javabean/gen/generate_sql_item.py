# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : generate_sql_item.py
@Time    : 2020/8/24 3:26 下午
@desc    :
"""

"""

VALUES ('PERSON_INFO', '姓名', 'EMP_NAME', 'TEXT_INFO', null);
"""
import pandas as pd


def read_excel():
    """ 读取 Excel 模板内容 """
    df = pd.read_excel('insert_sql1.xlsx')
    for index, row in df.iterrows():
        field_1 = row['分类']
        field_2 = row['项目名称']
        field_3 = row['项目编码']
        field_4 = row['类型']
        field_5 = row['备注']
        generate_code(field_1, field_2, field_3, field_4, field_5)


def generate_code(field_1, field_2, field_3, field_4, field_5):
    if field_1 == '人员信息':
        field_1 = 'PERSON_INFO'
    elif field_1 == '预设项目':
        field_1 = 'PREINSTALL_ITEM'

    if field_4 == '文本':
        field_4 = 'TEXT_INFO'
    elif field_4 == '日期':
        field_4 = 'DATE_INFO'
    elif field_4 == '数值':
        field_4 = 'NUMBER_INFO'
    elif field_4 == '枚举':
        field_4 = 'ENUMZ_INFO'

    sql_str = "INSERT INTO T_PREINSTALL_ITEM ( ITEM_CATEGORY, ITEM_NAME, ITEM_CODE, ITEM_TYPE, TIP_EXPLAIN) values (" \
              f"'{field_1}', " \
              f"'{field_2}', " \
              f"'{field_3}', " \
              f"'{field_4}', " \
              f"'{field_5}');"
    print(sql_str)


def run():
    """ 运行 """
    read_excel()


if __name__ == '__main__':
    run()
