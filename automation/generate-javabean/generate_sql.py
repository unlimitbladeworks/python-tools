# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : generate_sql.py
@Time    : 2020/7/2 4:16 下午
@desc    :
"""

import pandas as pd


def read_excel():
    """ 读取 Excel 模板内容 """
    df = pd.read_excel('jm.xlsx')
    for index, row in df.iterrows():
        field_1 = row['减免方式']
        field_2 = row['所得项目']
        field_3 = row['减免事项名称']
        field_4 = row['减免性质名称']
        generate_code(field_1, field_2, field_3, field_4)


def generate_code(field_1, field_2, field_3, field_4):
    if '减免税额' in field_1:
        field_1 = 'JMSE'
    elif '免税收入' in field_1:
        field_1 = 'JMSR'
    if '上市公司股息红利' in field_2:
        field_2 = 'LISTED_COMPANY_DIVIDENDS'
    elif '三板市场' in field_2:
        field_2 = 'THREE_BOARD_MARKET_DIVIDENDS'
    elif '证券资金利息' in field_2:
        field_2 = 'SECURITY_FUNDS_DIVIDENDS'
    elif '国债利息' in field_2:
        field_2 = 'TREASURY_BONDS_DIVIDENDS'
    elif '国家发行的金融' in field_2:
        field_2 = 'NATIONAL_ISSUE_DIVIDENDS'
    elif '地方政府' in field_2:
        field_2 = 'LOCAL_GOVERNMENT_DIVIDENDS'
    elif '储蓄存款' in field_2:
        field_2 = 'SAVING_STORAGE_DIVIDENDS'
    elif '其他利息' in field_2:
        field_2 = 'OTHER_DIVIDENDS'
    elif '持有创新' in field_2:
        field_2 = 'INNOVATION_PROOF'

    if '_' not in field_2:
        return
    sql_str = "INSERT INTO T_REDUCTION_DICT (SDXM, JMFS, JMSXMC, JMSXXZ) VALUES (" \
              f"'{field_2}', " \
              f"'{field_1}', " \
              f"'{field_3}', " \
              f"'{field_4}');"
    print(sql_str)


if __name__ == '__main__':
    read_excel()
