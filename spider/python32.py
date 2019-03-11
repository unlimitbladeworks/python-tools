# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : python32.py
@Time    : 2019/3/4 15:15
@desc    :
html_content = str(html_content, encoding='utf-8')
"""
import re
from urllib import request


class SpiderPandas(object):
    """ 类：原生爬虫 - 爬取 熊猫王者荣耀 直播

    目标：直播标题、主播网名、热度

    """

    # 请求网页的url
    url = 'https://www.panda.tv/cate/kingglory'
    # root-div 正则
    root_node_pattern = r'<div class="video-info">([\s\S]*?)</div>'
    # 房间名称正则
    title_node_pattern = r'<span class="video-title" title="([\s\S]*?)">'
    # 主播称号正则
    nickname_node_pattern = r'<span class="video-nickname" title="([\s\S]*?)">'
    # 房间热度正则
    number_node_pattern = r'ricon-eye"></i>([\s\S]*?)</span>'

    def __crawl_html(self):
        """ 请求网页源码,私有方法 """
        r = request.urlopen(SpiderPandas.url)
        html_content = r.read()
        html_content = str(html_content, encoding='utf-8')
        return html_content

    def __analysis_node(self, html):
        """ 分析网页返回的节点,私有方法 """
        video_info_lists = re.findall(SpiderPandas.root_node_pattern, html)
        list_hot = []
        for video_info in video_info_lists:
            # title = re.findall(SpiderPandas.title_node_pattern, video_info)   # 调试时打开即可
            nickname = re.findall(SpiderPandas.nickname_node_pattern, video_info)
            number = re.findall(SpiderPandas.number_node_pattern, video_info)
            # print(f'房间名称:{title},主播名称:{nickname},房间热度:{number} \n') # 调试时打开即可
            dict_hot = {'nickname': nickname, 'number': number}
            list_hot.append(dict_hot)
        # print(list_hot) # 调试时打开即可
        return list_hot

    def __refine(self, list_hot):
        """ 数据清洗, 去空格等操作, 回顾 map 和 lambda 表达式 """
        l_hot = lambda hot: {'nickname': hot['nickname'][0].strip(),
                             'number': hot['number'][0].strip()
                             }

        return map(l_hot, list_hot)

    def __sort(self, list_hot):
        """ sorted 函数排序房间热度 """
        list_hot = sorted(list_hot, key=self.__sort_seed, reverse=True)
        return list_hot

    def __sort_seed(self, hot):
        """ sorted 函数用到的关键词种子,对 '万' 进行处理排序 """
        r = re.findall(r'\d*', hot['number'])
        number = float(r[0])
        if '万' in hot['number']:
            number *= 10000
        return number

    def __show(self, list_hot):
        """ 单独对控制台打印展示 """
        for rank in range(len(list_hot)):
            print(f"房间排名 {rank} : {list_hot[rank]['nickname']} ------------ {list_hot[rank]['number']}")

    def run(self):
        """ 运行方法 """
        html = self.__crawl_html()  # 模拟请求
        list_hot = self.__analysis_node(html)  # 解析网页数据
        # print(list(self.__refine(list_hot))) # 调试时打开即可
        list_hot = list(self.__refine(list_hot))  # 数据清洗
        list_hot = self.__sort(list_hot)
        self.__show(list_hot)


if __name__ == '__main__':
    spiderPandas = SpiderPandas()
    spiderPandas.run()
