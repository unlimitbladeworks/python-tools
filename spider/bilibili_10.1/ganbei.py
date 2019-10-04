# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : ganbei.py
@Time    : 2019-10-01 09:15
@desc    : bilibili 祖国大好河山采集
"""
import os
import requests
import jieba.analyse
import wordcloud
from wordcloud import WordCloud
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


class GuoQingBirthday(object):

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
        Chrome/69.0.3497.100 Safari/537.36',
            'Cookie': "你自己的 cookie "
        }
        self.word_dict = {}
        self.words_list = []

    def __requests_method(self, url):
        """ get请求方法 """
        self.r = requests.get(url=url, headers=self.headers)
        self.r.encoding = 'utf-8'
        return self.r.text

    def __parse_xml(self, content_xml):
        """ PyQuery，解析 xml """
        from pyquery import PyQuery as pq
        p = pq(content_xml.encode('utf-8'))
        for content in p('d').contents():
            self.words_list.append(content)

    def __jieba_barrage(self):
        """ 弹幕的分词统计 """
        print(f'单词 list 数量 : {len(self.words_list)}')
        content = ';'.join(self.words_list)
        tags = jieba.analyse.extract_tags(content, topK=400, withWeight=True)
        for tag, n in tags:
            # tag : 权重较高的词 ; n权重值
            # 调试用的注释print(f'{tag} {str(int(n*10000))}' )
            self.word_dict[tag] = int(n * 10000)

    def __draw_word(self):
        """ 词云生成 """
        d = os.path.dirname(__file__)
        alice_mask = np.array(Image.open(os.path.join(d, "gq.jpg")))
        windows_font_path = 'C:/Windows/Fonts/simsun.ttc'  # winodws字体
        mac_font_path = '/System/Library/Fonts/PingFang.ttc'  # mac字体

        wc = WordCloud(font_path=mac_font_path,  # 设置字体格式,系统自带的中文字体
                       mask=alice_mask,  # 设置背景图
                       background_color='black',
                       max_words=400,  # 最多显示词数
                       max_font_size=150  # 字体最大值)
                       )

        wc.generate_from_frequencies(self.word_dict)  # 从字典生成词云
        image_colors = wordcloud.ImageColorGenerator(alice_mask)  # 从背景图建立颜色方案
        wc.recolor(color_func=image_colors)  # 将词云颜色设置为背景图方案

        plt.imshow(wc, interpolation='bilinear')  # 显示词云
        plt.axis('off')  # 关闭坐标轴
        plt.show()  # 显示图像

    def __date_utils(self, start, end):
        """ 日期间隔工具 """
        import datetime
        date_start = datetime.datetime.strptime(start, '%Y-%m-%d')
        date_end = datetime.datetime.strptime(end, '%Y-%m-%d')

        date_list = list()
        while date_start <= date_end:
            date_list.append(date_start.strftime('%Y-%m-%d'))
            date_start += datetime.timedelta(days=1)
        # date_list ['2019-09-28', '2019-09-29', '2019-09-30', '2019-10-01', '2019-10-02', '2019-10-03', '2019-10-04']
        return date_list

    def run(self):

        try:
            start = '2019-09-28'
            end = '2019-10-04'
            date_list = self.__date_utils(start, end)
            for date in date_list:
                url = f'https://api.bilibili.com/x/v2/dm/history?type=1&oid=120004475&date={date}'
                xml = self.__requests_method(url)  # 模拟请求
                self.__parse_xml(xml)  # 解析 xml,将所有弹幕放入 list 中

            self.__jieba_barrage()  # 词频分析权重
            self.__draw_word()  # 生成词云
        except Exception:
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    gq = GuoQingBirthday()
    gq.run()
