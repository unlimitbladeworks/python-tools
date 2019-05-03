# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : selenium_demo.py
@Time    : 2019/5/3 16:57
@desc    : 初始 selenium 天眼查
"""
import os

from selenium import webdriver
import pandas as pd


class SpiderTYC:
    url = 'https://www.baidu.com'
    query_xpath = '//*[@id="kw"]'
    confirm_xpath = '//*[@id="su"]'

    def __start_chrome(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)  # seconds,等待时间,如果网页元素节点没加载,默认等待10s。
        self.driver.get(url=SpiderTYC.url)
        for name in self.company_name:
            self.driver.find_element_by_xpath(SpiderTYC.query_xpath).send_keys(name)  # 填充名字到浏览器
            self.driver.find_element_by_xpath(SpiderTYC.confirm_xpath).click()  # 点击浏览器
            self.driver.find_element_by_xpath(SpiderTYC.query_xpath).clear()  # 清楚内容

    def __shutdown_chrome(self):
        self.driver.quit()

    def __read_excel(self, path):
        """ 读取 excel 的公司名称 """
        df = pd.read_excel(path)
        self.company_name = df['公司名称']

    def run(self):
        try:
            while 1:
                path = input('请输入 excel 路径( excel 文件完整路径)：\n')
                if os.path.exists(path):
                    self.__read_excel(path)
                    self.__start_chrome()
                    self.__shutdown_chrome()
                else:
                    print('文件不存在，请重新输入！')
        except Exception as e:
            import traceback
            print(traceback.print_exc())


if __name__ == '__main__':
    spider_tyc = SpiderTYC()
    spider_tyc.run()
