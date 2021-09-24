# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : sm-website.py
@Time    : 8/27/21 1:39 PM
@desc    :
"""

import os
import json
import pandas as pd
from pandas import ExcelWriter


# 寻找file.ini绝对路径
def find_file_path():
    return os.path.dirname(os.path.abspath(__file__))


def read_file():
    """ 读取当前目录下 txt """
    txt_path = os.path.join(find_file_path(), 'sm.txt')
    print(f'url文件路径：{txt_path}')
    with open(txt_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data


def write_excel():
    file = read_file()
    retailers = file['retailers']
    domain_list = []
    category_list = []
    for retailer in retailers:
        domain = retailer['domain']
        try:
            category_dict = {}
            stats = retailer['stats']
            total_product = stats['totalProductsInSupplier']
            stats_dict = dict(stats['stats'])
            for category_on_site in stats_dict.values():
                category = category_on_site['category']
                number_products = category_on_site['numberOfProducts']
                percent = round(int(number_products) / int(total_product), 2) * 100
                category_dict[category] = percent
            sorted_dict = sorted(category_dict.items(), key=lambda item: item[1], reverse=True)
            category_list.append('\n'.join([f'{k}:{v}%' for k, v in sorted_dict]))
            domain_list.append(domain)
        except:
            print(domain + '\n')
            continue
    df = pd.DataFrame({'网站': domain_list,
                       '类目': category_list})
    writer = ExcelWriter('sm-website.xlsx')
    df.to_excel(writer, 'website', index=False)
    writer.save()


if __name__ == '__main__':
    write_excel()
