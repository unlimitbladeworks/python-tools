# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : pyquery_demo.py
@Time    : 2019-10-07 18:08
@desc    : PyQuery 小爬虫很简单，直接用 def 定义写了
"""
import re

from pyquery import PyQuery as pq
import pandas as pd
from pandas import ExcelWriter

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                  'Version/13.0.1 Safari/605.1.15 '
}

city_list = []
place_list = []
person_nums = []


def spider_travel(url):
    doc = pq(url=url, headers=headers)
    ul_city = doc('.plcCitylist')  # 获取 class="plcCitylist" 的 ul 节点元素 ,基于 css 选择器
    lis = ul_city('li')  # 在 ul 基础上获取 li 节点元素
    for index, li in enumerate(lis.items()):  # 使用 items 来进行遍历获取
        h3 = li('.title.fontYaHei')  # 分开写的目的是便于学习
        a = h3('a')
        a_city = a.attr('data-bn-ipg', f'place-citylist-mix-name-{index + 1}').text()  # JQuery 写法
        a_place = '\n'.join([a.text() for a in li('.pois')('a').items()])  # 遍历a标签，协助换行，便于写入文件
        p_person_nums = re.findall(r'\d+', li('p')('.beento').text())[0]  # 去过的人,只要数字

        city_list.append(a_city)
        place_list.append(a_place)
        person_nums.append(p_person_nums)


def write_excel():
    df = pd.DataFrame({'城市': city_list,
                       '景区': place_list,
                       '去过人数': person_nums})

    writer = ExcelWriter('travel.xlsx')
    df.to_excel(writer, 'qy', index=False)
    writer.save()


def run():
    try:
        print('开始...')
        for i in range(1, 26):
            url = f'https://place.qyer.com/japan/citylist-0-0-{i}/'
            spider_travel(url)
        write_excel()
        print('结束...')
    except Exception:
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    run()
