# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : crawl_bing.py
@Time    : 2019-12-05 15:32
@desc    :
"""
import requests
import re
from urllib import parse
import datetime


def crwal_picture(file):
    url = 'https://cn.bing.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) '
                      'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Safari/605.1.15'
    }
    r = requests.get(url=url, headers=headers)
    a = re.findall(r'rel="preload" href="(.*?)" as="image"', r.text)
    if a:
        picture_url = parse.urljoin(url, a[0])
        print(f'当前图片地址：{picture_url}')
        r_picture = requests.get(url=picture_url, headers=headers)
        write_file(file, r_picture.content)


def write_file(file, content):
    with open(file, 'wb') as f:
        f.write(content)


if __name__ == '__main__':
    today = datetime.date.today()
    path = f'/Users/sy/Pictures/bing/{today}.jpg'
    crwal_picture(path)
