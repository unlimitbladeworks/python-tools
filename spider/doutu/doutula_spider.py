# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : doutula_spider.py
@Time    : 2019/5/27 21:32
@desc    : 多线程队列爬取斗图网图片
"""
import os
import threading
import requests
import queue
import time
import random
from bs4 import BeautifulSoup as bs


class DouTuLaSpider:
    url_queue = queue.Queue()  # 全局的公共队列

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
        Chrome/69.0.3497.100 Safari/537.36'
    }

    def __crawl_html(self, url, type='text'):
        """ 根据 type 标识, 返回请求网页返回源码或者二进制流 """
        r = requests.get(url=url, headers=DouTuLaSpider.headers)
        self.__control_speed()  # 加延时
        if type == 'text':
            return r.text
        if type == 'content':
            return r.content

    def __analysis_main_url(self, html):
        """ 分析主页图片 """
        soup = bs(html, 'lxml')
        a_node = soup.select('a.list-group-item.random_list')
        for a in a_node:
            detail_url = a.get('href')  # 获取详细的 url
            detail_html = self.__crawl_html(detail_url)
            self.__analysis_detail_url(detail_html)

    def __analysis_detail_url(self, html):
        """ 分析具体页中的图片 """
        soup = bs(html, 'lxml')
        picture_topic = soup.find(name='h1').get_text()  # 图片主题名字
        print(f'当前处理的图片主题名 ：{picture_topic} ....')
        div_node = soup.find_all(name='div', attrs={'class': 'artile_des'})
        for i in div_node:
            img_node = i.find(name='img')
            if img_node:
                img_url = img_node.get('src')  # 获取图片url
                self.__downloader(img_url, picture_topic)
                self.__control_speed()  # 加延时

    def __downloader(self, img_url: str, picture_topic):
        """ 下载图片 """
        content = self.__crawl_html(img_url, type='content')
        if not os.path.exists(picture_topic):
            os.mkdir(picture_topic)

        picture_name = img_url.rsplit('/')[-1]
        dir_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), picture_topic)
        filename = os.path.join(dir_path, picture_name)

        with open(filename, 'wb') as f:  # 二进制图片写入文件中
            f.write(content)

    def __control_speed(self):
        """ 睡眠函数 """
        random_time = random.random()
        time.sleep(random_time)

    def run(self):
        """ 通过队列来实现多线程的有序性，从第 1 页到第 614 页有序处理 """
        try:
            while 1:
                url_queue = DouTuLaSpider.url_queue
                if url_queue.qsize() == 0:
                    break
                else:
                    main_url = url_queue.get()
                    html = self.__crawl_html(main_url)
                    self.__control_speed()  # 加延时
                    self.__analysis_main_url(html)  # 分析主节点
        except Exception as e:
            import traceback
            traceback.print_exc()


def main():
    print('程序开始！')

    thread_nums = 5  # 开启 5 个线程
    for main_url in range(1, 615):
        url = f'https://www.doutula.com/article/list/?page={main_url}'
        DouTuLaSpider.url_queue.put(url)

    doutu = DouTuLaSpider()
    # 开启多线程
    for i in range(thread_nums):
        thread = threading.Thread(target=doutu.run)
        thread.start()
    thread.join()

    print('程序结束...')


if __name__ == '__main__':
    main()
