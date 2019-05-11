# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : python_hg.py
@Time    : 2019/5/10 11:24
@desc    :
"""
import os

import pandas as pd
from pandas import Series

import plotly as py
import plotly.graph_objs as go

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import jieba.analyse
import wordcloud
import numpy as np


class HGFans:

    def __init__(self):
        self.df = pd.read_excel('C:/Users/asus/Desktop/hg-fans.xlsx')
        self.pyplt = py.offline.plot
        self.word_dict = {}

    def fans_gender_rate(self):
        """ 粉丝性别男女比例 """
        data_male = self.df[self.df['性别'] == '男']  # 筛选性别是男的
        data_female = self.df[self.df['性别'] == '女']

        male_count = data_male['性别'].count()  # 男总数
        female_count = data_female['性别'].count()  # 女总数
        sum_count = self.df['性别'].count()  # 所有人总数

        male_rate = round(male_count / sum_count * 100)  # 男比例
        female_rate = round(female_count / sum_count * 100)  # 女比例
        print(f'男比例:{male_rate}%,女比例:{female_rate}%')

    def fans_age_analysis(self):
        """ 粉丝年龄分析 """
        df_birthday = self.df.dropna(axis=0, subset=['生日'])  # 删除'生日'为空的行
        df_birthday = df_birthday[df_birthday['生日'].str.match('^\d{4}') == True]
        df_year = df_birthday['生日'].str[:4].value_counts()  # type: Series # 清洗好的生日年份统计

        """ 用 plotly 生成条形 html 图像 """
        data_g = []
        trace_1 = go.Bar(x=df_year.keys(), y=df_year.values)
        data_g.append(trace_1)
        layout = go.Layout(title='粉丝年龄统计',
                           xaxis={'title': '年份'},
                           yaxis={'title': '个数'}
                           )
        figure = go.Figure(data=data_g, layout=layout)
        self.pyplt(figure, filename='粉丝年龄统计.html')

    def fans_location(self):
        """ 粉丝占据的地理位置 """
        df_city = self.df['所在地'].str[:2].value_counts()  # 获取地理位置的市级位置,并且计数
        """ 用 plotly 生成饼图 html 图像 """
        data_g = []
        trace_1 = go.Pie(labels=df_city.keys(), values=df_city.values)
        data_g.append(trace_1)
        layout = go.Layout(title='粉丝地区统计')
        figure = go.Figure(data=data_g, layout=layout)
        self.pyplt(figure, filename='粉丝地区统计.html')

    def fans_intro(self):
        """ 粉丝简介的分词统计 """
        intro_list = [str(intro) for intro in self.df['简介'].values]  # 将每行数据转为字符串变为 list
        short_intro = ';'.join(intro_list)  # 每行数据用 分号 分隔开
        tags = jieba.analyse.extract_tags(short_intro, topK=100, withWeight=True)

        for tag, n in tags:
            # tag : 权重较高的词 ; n权重值
            # 调试用的注释print(f'{tag} {str(int(n*10000))}' )
            self.word_dict[tag] = int(n * 10000)

        self.draw_word()

    def draw_word(self):
        d = os.path.dirname(__file__)
        alice_mask = np.array(Image.open(os.path.join(d, "hg.png")))

        wc = WordCloud(font_path='C:/Windows/Fonts/simsun.ttc',  # 设置字体格式,系统自带的中文字体
                       mask=alice_mask,  # 设置背景图
                       background_color='white',
                       max_words=400,  # 最多显示词数
                       max_font_size=150  # 字体最大值)
                       )

        wc.generate_from_frequencies(self.word_dict)  # 从字典生成词云
        image_colors = wordcloud.ImageColorGenerator(alice_mask)  # 从背景图建立颜色方案
        wc.recolor(color_func=image_colors)  # 将词云颜色设置为背景图方案

        plt.imshow(wc, interpolation='bilinear')  # 显示词云
        plt.axis('off')  # 关闭坐标轴
        plt.show()  # 显示图像

    def run(self):
        """ 运行的函数 """
        self.fans_gender_rate()
        self.fans_age_analysis()  # 年龄
        self.fans_location()  # 地理
        self.fans_intro()  # 简介词云


if __name__ == '__main__':
    hg_fans = HGFans()
    hg_fans.run()
