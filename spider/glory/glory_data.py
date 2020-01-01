# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : glory_data.py
@Time    : 2020-01-01 14:55
@desc    : 处理爬取到的王者数据
"""

import pandas as pd
import json
import numpy as np


def deal_data(input, output):
    df = pd.read_csv(input)  # 读取 csv
    attr_details_data_dict = df['attr_details_data_dict']  # 获取 csv 单列 attr_details_data_dict
    recommend_stars_dict = df['recommend_stars_dict']

    # 将 dict 单列转为新列提取并且合并多个 df 组成新的 df
    detail_col_list = [pd.DataFrame(json.loads(detail_str), index=[0]) for detail_str in attr_details_data_dict]
    new_detail_df = pd.concat(detail_col_list, axis=0, ignore_index=True)

    # 同理
    recommend_col_list = [pd.DataFrame(json.loads(recommend_str), index=[0]) for recommend_str in recommend_stars_dict]
    new_recommend_df = pd.concat(recommend_col_list, axis=0, ignore_index=True)

    df2 = df.drop(['attr_details_data_dict', 'recommend_stars_dict', '...'], axis=1)  # 删除已经处理过的列以及...

    final_df = pd.concat([df2, new_detail_df, new_recommend_df], axis=1)  # 合并新旧列
    final_df.index = np.arange(1, len(final_df) + 1)  # 重置序列，从1开始
    final_df.to_excel(output)


if __name__ == '__main__':
    deal_data('gloryofking.csv', 'glory.xlsx')
