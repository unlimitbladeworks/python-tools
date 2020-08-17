# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : hotlist.py
@Time    : 2020/8/16 3:22 下午
@desc    : 爬取知乎热榜，定时推送邮件
"""

import requests
from config.init_config import init_config, read_urls
import re
from send_mails import SendMail
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/84.0.4147.125 Safari/537.36 '
}


def crawl_hot_list():
    """ 读取热榜，发送邮件 """
    mail = SendMail()
    for url in read_urls():
        print(f'url:{url}')
        hot_list = []
        # url中带*，直接跳过，可以理解为注解
        if '*' in url:
            continue
        try:
            r = requests.get(url=url, headers=headers).json()
            # 如果是全站，url是total的标识，若不是，其余的是一样的解析
            data_list = r['data']
            for data in data_list:
                target = data['target']
                title = target['title'].encode("utf-8").decode("utf-8")  # 标题
                # 问题地址,替换api和questions字段，得到真实地址
                old_url = target['url']
                if 'questions' not in old_url:
                    continue
                url = old_url.replace('api', 'www').replace('questions', 'question')
                answer_count = target['answer_count']  # 回答数
                follower_count = target['follower_count']  # 关注数
                detail_text = data['detail_text'].encode("utf-8").decode("utf-8")  # 热度
                result_dict = {
                    'title': title,
                    'url': url,
                    'answer_count': answer_count,
                    'follower_count': follower_count,
                    'detail_text': detail_text
                }
                hot_list.append(result_dict)
        except:
            import traceback
            traceback.print_exc()
            continue

        result_list = sort(hot_list)  # 根据热度排序
        txt = deal_txt(result_list)  # 处理文本
        mail.send_mails(txt)  # 发邮件


def sort(list_hot):
    """ sorted 函数排序热度 """
    list_hot = sorted(list_hot, key=sort_seed, reverse=True)
    return list_hot


def sort_seed(hot):
    """ sorted 函数用到的关键词种子,对 '万' 进行处理排序 """
    r = re.findall(r'\d*', hot['detail_text'])
    number = float(r[0])
    if '万' in hot['detail_text']:
        number *= 10000
    return number


def deal_txt(result_list):
    """ 数据转为文本 """
    result_str_list = []
    for result_dict in result_list:
        title = result_dict['title']
        url = result_dict['url']
        answer_count = result_dict['answer_count']
        follower_count = result_dict['follower_count']
        detail_text = result_dict['detail_text']
        result_str = f"标题: {title}\n" \
                     f"网站地址: {url}\n" \
                     f"回答人数: {answer_count}, " \
                     f"关注人数: {follower_count}, " \
                     f"热度: {detail_text}\n\n"
        result_str_list.append(result_str)
    result = "\n".join(result_str_list)
    return result


def main():
    begin = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(f"{begin}----脚本开始----")
    init_config()
    crawl_hot_list()  # 爬取数据
    end = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(f"{end}----脚本结束----")


main()
