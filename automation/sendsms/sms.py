# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : sms.py
@Time    : 2019年12月15日15:15:23
@desc    : 机器人，为父母送去温馨短信
"""
from twilio.rest import Client
import requests
import sys
import urllib.parse

from_phone = '+'  # twilio提供的手机号
to_phones = ['+86']  # 接收人的手机号
account_sid = ''  # Your Account SID from twilio.com/console
auth_token = ''  # Your Auth Token from twilio.com/console


def robot_api(keyword):
    """ 机器人接口 """
    msg_dict = {'msg': keyword}
    msg_encode = str(urllib.parse.urlencode(msg_dict))  # 将中文编码成url形式
    url = f'http://api.qingyunke.com/api.php?key=free&appid=0&{msg_encode}'
    try:
        r = requests.get(url=url).json()
        # 返回内容 dict {'result': 0, 'content': ' '}
        if r['result'] == 0:
            message = f"{r['content']}"
            print(message)
            send_sms(message)
        else:
            print('青云客 api 返回信息为空！')
    except Exception:
        import traceback
        traceback.print_exc()


def send_sms(message):
    """ 发送短信 """
    client = Client(account_sid, auth_token)
    for phone in to_phones:
        result = client.messages.create(
            to=phone,
            from_=from_phone,
            body=message)
        if result.sid:
            print(f'短信已发送成功:{phone}')
        else:
            print(f'发送短信失败，收信人手机号:{phone}')


def run():
    """ 运行方法 """
    keywords = '北京天气'
    # 命令行形式的参数,便于定时传入参数，如命令行执行 python sms.py 说个笑话，此时机器人执行的则是说个笑话。
    if len(sys.argv) > 1:
        robot_api(sys.argv[1])
    else:
        robot_api(keywords)


if __name__ == '__main__':
    run()
