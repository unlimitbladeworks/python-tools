# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : crawl_glory.py
@Time    : 2019-12-22 10:30
@desc    : PySpider 爬取王者荣耀官网数据
"""

# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-12-22 21:05:43
# Project: glory

from pyspider.libs.base_handler import *
import re


class Handler(BaseHandler):
    crawl_config = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
    }

    @every(minutes=24 * 60)
    def on_start(self):
        # 访问主页
        self.crawl('http://db.18183.com/wzry', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        # 遍历详情页下所有英雄
        for each in response.doc('.hero-result-box>ul>li').items():
            a = each('a')
            self.crawl(a.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        name = response.doc('h1').text()  # 英雄名称
        avatar = response.doc('.name > img').attr('data-original')  # 头像
        position = response.doc('.name-box > p').text()  # 英雄定位

        recommand_stars_dict = {}  # 生存能力等星数
        for dl in response.doc('.attr-list > dl').items():
            attr_name = dl('dt').text()  # 生存能力、攻击伤害、技能效果、上手难度
            stars = int(re.findall(r'star-(.*)', dl('dd')('span').attr('class'))[0])  # 正则匹配 star-number,获取 number
            recommand_stars_dict[attr_name] = stars

        hero_analysis = [item for item in response.doc('.otherinfo-article > p').items()][0].text()  # 英雄分析，文字版

        attr_details_data_dict = {}
        for li in response.doc('.otherinfo-datapanel > ul > li').items():
            attr_details_text = li('p').text().strip().split('：')  # 获取详细属性
            details_name = attr_details_text[0]  # 属性名称：如 最大生命 等...
            details_data = attr_details_text[1]  # 属性数值：如 3287 等...
            attr_details_data_dict[details_name] = details_data

        return {
            "url": response.url,
            "name": name,
            "avatar": avatar,
            "position": position,
            "recommand_stars_dict": recommand_stars_dict,
            "hero_analysis": hero_analysis,
            "attr_details_data_dict": attr_details_data_dict
        }
