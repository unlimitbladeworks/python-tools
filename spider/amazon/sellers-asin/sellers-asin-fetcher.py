# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : sellers-asin-fetcher.py
@Time    : 9/22/21 2:39 PM
@desc    : 批量爬取一个商品下所有FBA卖家所有的店铺asin信息
"""
from selenium import webdriver
import re
import pandas as pd
import random
import time

import multiprocessing


def get_time(f):
    """ 耗时函数，装饰器 """

    def inner(*arg, **kwarg):
        s_time = time.time()
        res = f(*arg, **kwarg)
        e_time = time.time()
        print('耗时：{}秒'.format(e_time - s_time))
        print('耗时：{}分钟'.format((e_time - s_time) / 60))
        return res

    return inner


class SpiderAsin:
    product_title_css = '.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-2'  # 店铺详情页的产品标题css
    next_page_xpath = '.a-last'

    def __init_chrome(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)  # seconds,等待时间,如果网页元素节点没加载,默认等待10s。

    def __start_chrome(self, url):
        self.driver.get(url)
        self.__deal_service()  # 处理业务

    def __deal_service(self):
        """ 处理业务 """
        time.sleep(random.randint(3, 4))
        asin_list = []
        product_title_nodes = self.driver.find_elements_by_css_selector(SpiderAsin.product_title_css)  # 获取商品标题
        for node in product_title_nodes:
            href = node.find_element_by_tag_name('a').get_attribute('href')  # 提取标题下的a标签的url
            asin = re.findall(r'(?<=dp/).*?(?=/)', href)[0]  # 正则匹配url获取asin
            asin_list.append(asin)
        df = pd.DataFrame(asin_list)
        current_url = self.driver.current_url
        print(f'当前url：{current_url}')
        today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        df.to_csv(f'asin-{today}.csv', index=False, header=False, mode='w')

        try:
            # 点击下一页
            next_page_node = self.driver.find_element_by_css_selector(SpiderAsin.next_page_xpath)
            next_page_node.find_element_by_tag_name('a')
            next_page_node.click()
            self.__deal_service()
        except:
            return

    def __shutdown_chrome(self):
        self.driver.quit()

    @staticmethod
    def read_file() -> list:
        """ 读取本地 urls.txt 文件
            如：https://www.amazon.com/s?i=merchant-items&me=A3AD5LSIIOXN9N&marketplaceID=ATVPDKIKX0DER
        """
        with open('urls.txt', 'r', encoding='utf-8', errors='ignore') as f:
            return [line for line in f.readlines()]

    @staticmethod
    def write_file():
        """ 读取sellers文件，写入 url 文件 """
        url_list = []
        df = pd.read_csv('1.csv')
        sellers_id = df[(df['Seller Type'] == 'FBA') & (df['Condition'] == 'New')]['Seller ID']
        for idx, sellers_id in sellers_id.items():
            url = f'https://www.amazon.com/s?i=merchant-items&me={sellers_id}&marketplaceID=ATVPDKIKX0DER'
            url_list.append(url)
        with open('urls.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(url_list))

    def _run_task(self, url):
        self.__init_chrome()
        self.__start_chrome(url)
        self.__shutdown_chrome()

    @get_time
    def run(self):
        try:
            SpiderAsin.write_file()
            urls_list = SpiderAsin.read_file()
            pool = multiprocessing.Pool(processes=4)
            pool.map(self._run_task, urls_list)
            pool.close()
            pool.join()
        except:
            import traceback
            print(traceback.print_exc())


if __name__ == '__main__':
    spider_asin = SpiderAsin()
    spider_asin.run()
