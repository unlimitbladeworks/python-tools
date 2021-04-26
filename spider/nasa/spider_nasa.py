# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : spider_nasa.py
@Time    : 2021/3/14 10:36 上午
@desc    :
"""

from selenium import webdriver
import time
import os
from selenium.webdriver.support.select import Select


def do(name):
    global driver
    driver = webdriver.Chrome(executable_path='chromedriver')
    driver.get('https://mars.nasa.gov/participate/send-your-name/future')

    list_name = name.split(' ')

    driver.find_element_by_xpath('//*[@id="FirstName"]').send_keys(list_name[0])
    driver.find_element_by_xpath('//*[@id="LastName"]').send_keys(list_name[1:])
    driver.find_element_by_xpath('//*[@id="PostalCode"]').send_keys('100010')
    # 定位到codeselect下
    codeselect = driver.find_element_by_name('country')
    # 获取焦点后，根据值点击对应的选项
    Select(codeselect).select_by_value('CN')
    driver.find_element_by_xpath('//*[@id="Email"]').send_keys('12345@qq.com')
    driver.find_element_by_xpath('//*[@id="newsletter"]').click()
    driver.find_element_by_xpath('//*[@id="submitNameForm"]/div/div[2]/button').click()
    print('名字:' + name)

    recursive_download(driver, name)

    driver.quit()


def recursive_download(driver, name):
    try:
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="downloadTicket"]').click()
        file = '/Users/sy/Downloads/BoardingPass_MyNameOnFutureMission.png'
        flag = 1
        while flag == 1:
            if not os.path.exists(file):
                driver.find_element_by_xpath('//*[@id="downloadTicket"]').click()
            else:
                flag = 0
        os.rename(file, f'/Users/sy/Downloads/{name}.png')
    except:
        recursive_download(driver, name)


if __name__ == '__main__':
    # list_name = ['BOHAO LI', 'YIYI CHEN','LUN LI','BOWEI ZHANG']
    list_name = ['YASHIQI HE','CHENXU YUAN']
    for name in list_name:
        do(name)
