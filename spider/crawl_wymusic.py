# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : crawl_wymusic.py
@Time    : 2019/4/14 9:15
@desc    : requests  爬取网易云歌单下载
"""
import os
import random
import re

import requests
from bs4 import BeautifulSoup as bs
import time


class CrawlMusic:
    music_download_url = 'http://music.163.com/song/media/outer/url?id='  # 网易云外链地址

    def __init__(self, **kwargs):
        """ 动态关键词传参，不限定外界传入参数，放入字典，自己拿即可 """
        self.keywords_dict = {}
        for k, v in kwargs.items():
            self.keywords_dict[k] = v
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
            Chrome/69.0.3497.100 Safari/537.36',
            'referer': self.keywords_dict['url']
        }
        self.count = 0

    def __crawl_html(self):
        """ 加本地缓存，方便二次读取节点 """
        content = self.read_file(f'{self.__generate_song_list_id}.html') if os.path.exists(
            self.__generate_song_list_id) else requests.get(url=self.keywords_dict.get('url'),
                                                            headers=self.headers).text
        return content

    def __analysis_node(self, html):
        """
        使用 bs 解析节点
        :param html: 源码
        :return: yield 生成器的形式，将字典返回。
        """
        soup = bs(html, 'lxml')  # 用 bs 库借助 lxml 解析器对源码解析
        if not os.path.exists(self.__generate_song_list_id):
            self.write_file(f'{self.__generate_song_list_id}.html', 'a', soup.prettify(), encoding='utf-8')  # 缓存到本地

        song_list_names = soup.select('.f-ff2.f-brk')[0].get_text().strip().replace('\n', '')  # 歌单名称
        # 正则匹配，替换调歌单文件夹的特殊符号，windows不允许有特殊符号作为命名
        self.song_list_name = re.sub(r'[\/:*?"<>|]', '-', song_list_names)
        if not os.path.exists(self.song_list_name):
            os.mkdir(self.song_list_name)

        ul_node = soup.find(name='ul', attrs={'class': 'f-hide'})  # 获取歌曲id的ul
        li_node = ul_node.find_all(name='li')
        for a_node in li_node:
            href_content = a_node.find(name='a').get('href')  # 超链接
            song_name = a_node.find(name='a').get_text()
            yield {
                'href_content': href_content,
                'song_name': song_name
            }

    def write_file(self, file_name, mode, content, encoding=None):
        """ 缓存内容到本地，目的不用重复请求服务器 """
        with open(file_name, mode, encoding=encoding) as f:
            f.write(content)

    def read_file(self, file_name):
        """ 读取本地缓存 html """
        with open(file_name, 'r', encoding='utf-8') as f:
            return f.read()

    @property
    def __generate_song_list_id(self):
        """ 生成 html 的名字,(截取歌单id号返回), @property 装饰器的目的是可以将函数当成属性使用，调用不加括号 """
        return self.keywords_dict.get('url').split('=')[-1]

    def __downloader(self, song_dict):
        self.count += 1
        song_id = song_dict.get('href_content').split('=')[-1]  # href中的内容，截取 id
        song_name = song_dict.get('song_name').strip().replace(r'\n', '')   # 去除歌单名称的空格

        mp3_url = self.__class__.music_download_url + song_id + '.mp3'
        mp3_stream = requests.get(url=mp3_url, headers=self.headers).content
        mp3_file_name = f'{self.song_list_name}/{song_name}.mp3'  # mp3文件名字
        self.write_file(mp3_file_name, 'wb', mp3_stream)  # 二进制写入
        random_time = random.random()
        print(f'第{self.count}首下载完成...歌名:{song_name},随机休眠{random_time}s...\n')
        time.sleep(random_time)

    @staticmethod
    def delete_html():
        """ 删除本文件夹下的 HTML """
        pwd_path = os.path.abspath(os.path.dirname(__file__))  # 当前文件路径
        for root, dirs, files in os.walk(pwd_path):
            for file in files:
                if file.endswith('.html'):
                    os.remove(file)

    def run(self):
        """ 运行主函数 """
        try:
            html_content = self.__crawl_html()
            song_generator = self.__analysis_node(html_content)
            list(map(self.__downloader, song_generator))  # 直接映射进去,函数体里尽量设计成单模块处理，而非 for 循环
        except Exception as e:
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    url = input('请输入具体歌单的url:\n')  # https://music.163.com/playlist?id=2269661190
    crawl = CrawlMusic(url=url)
    crawl.run()

    # CrawlMusic.delete_html()  # 删除当前文件加下 html 文件，需要打开即可
