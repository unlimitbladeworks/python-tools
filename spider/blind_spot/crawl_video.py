# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : crawl_video.py
@Time    : 2020/3/1 10:50 上午
@desc    : 爬取盗版 video
"""
import requests
import random
import time
import re


class GhostSpider:
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
        Chrome/69.0.3497.100 Safari/537.36'
    }

    def __init__(self, base_url, file_name):
        self.base_url = base_url
        self.file_name = file_name

    def __crawl_html(self, url, type='text'):
        """ 根据 type 标识, 返回请求网页返回源码或者二进制流 """
        r = requests.get(url=url, headers=GhostSpider.headers)
        self.__control_speed()  # 加延时
        if type == 'text':
            return r.text
        if type == 'content':
            return r.content

    def __control_speed(self):
        """ 睡眠函数 """
        random_time = random.random()
        time.sleep(random_time)

    def __read_m3u8(self, file_name):
        """ 读取 m3u8 文件的 ts 列表 """
        ts_list = []
        with open(file_name, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                if re.findall(r'(.*)ts', line):  # 正则匹配后缀 .ts 的行，拿出来放 list 里
                    ts_list.append(line.replace('\n', ''))
        return ts_list

    def __write_file(self, file_name, content):
        """ 写文件 """
        with open(file_name, 'wb') as f:
            f.write(content)

    def run(self):
        ts_list = self.__read_m3u8(self.file_name)
        i = 0
        for ts in ts_list:
            r = self.__crawl_html(self.base_url + ts, 'content')
            self.__write_file(ts, r)
            i += 1
            print(f'正在下载第{i}个ts文件流')


def main():
    print('程序开始！')
    # 基础 url 地址，比如 www.xxx.com/index.m3u8,那 base_url 则为 www.xxx.com/
    base_url = ''
    # 脚本目录下，名为 xx.m3u8 的文件名
    m3_file = 'index.m3u8'
    ghost_spider = GhostSpider(base_url, m3_file)
    ghost_spider.run()

    print('程序结束...')


if __name__ == '__main__':
    main()
