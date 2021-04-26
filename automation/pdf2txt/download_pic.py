# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : download_pic.py
@Time    : 2019-09-24 18:00
@desc    :
"""

import requests
import os


def run():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15'
    }
    for i in range(13, 1139):
        number = str(i).zfill(4)
        url = f'https://smallpdf-production-files.s3.eu-west-1.amazonaws.com/72ba8490238a4464962ea3ce3101d010-{number}.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA3I33L6OR66NDEOQE%2F20190924%2Feu-west-1%2Fs3%2Faws4_request&X-Amz-Date=20190924T101514Z&X-Amz-Expires=900&X-Amz-Security-Token=AgoJb3JpZ2luX2VjEFAaCWV1LXdlc3QtMSJIMEYCIQDodKXCLbk0mdnaKzKN%2FUynem5v2fw%2BEo2Ny30QiQnvFAIhAOxyb7Ra2An32ixSnncA7A%2FyeF%2By98Zb5de2Hg3wAycaKtoDCCkQABoMNzc0OTYzNDU4OTc5Igw18MoQyJ%2BLLtZmhEIqtwO6ya3RUeB4yDWpXONUf%2FxWxC2QX0g4GNRLBlbYve2EtRVmDW7NqEjdvWQgeiH%2BZF28Q4OxV1wlGurYYSwc8q3EdxcV5%2BqCJsNsAafgqu0GZXEUdpq%2BoM%2F3sB12Rzwr2axk4XlWJqwUBbj0rBf4G9lJAi3T%2BVfWTZoIZuQFOjiwK0tRJyX%2F5F8b%2BIdkNcMF%2B0c97B3gycsDfrlFkSMsq%2BmPifImK13j6uWaip9z45inHqFD0VdelfhfERPiF6F8SyGrpaE2AdinfLjIqJUGUOeHLKxpRufd00TvQhfcUVt8lL1ZIzHiRJ2XoLVEgXvwrszMlPywM3w%2BVdVznP%2B0tIAcGWmrCT2tjs7Hf1%2BKeleCRjbLTM6b6oNHRkqke6Ncij4xI0kEUp1UMr0BT%2FALwJ1ItmULw6KuZmVqTUjaia4RT9JOKJzgaYHbHVBdrlGV6oE0V4GWTkLNSzuCzAWE%2FHL9uTevw8g3Jv%2B5a%2FccYB7jhBh0mpZffB5WCobBfNsEEJB4FMCXPKQ0c6yvnb5nAvkv9REvVscBVSo2vadhvBQHpyHZeOSiAu%2Fsb8cKzn9ordv0vI2PgPRxMN%2BVp%2BwFOrMBh8EpTO0MuOgMaIDAIw2OzOQR46O6UjKKdR0uh3%2BGaxxSwPKWTPdtAOctj36wUTLuNowheooKzC1GgW4A%2B9vak31Y%2BbdBtcEED8UFXcB2iJcdJprqMcfNB8NBEwYtUwQi17MZkVpAN2RrblmiqNdPawZOkR8c7Lw7%2BFyomXPAyfDxJPvpuHkRWsBAsEdMbM4iPPmlu09HehLmCzHgKSBXIVuJtJcPIzZtQ2ndkw%2F9Z8LrWRc%3D&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%3D%220009.jpg%22&response-content-type=image%2Fjpeg&X-Amz-Signature=ab0ad6be9c838b022d5a92029bb11b0c6ad7d8b09ecb6b74363067fa7c5ce3b6'
        # url = f'https://files.smallpdf.com/files/72ba8490238a4464962ea3ce3101d010-thumb-{number}.jpg'
        r = requests.get(url=url, headers=headers)
        download(number, r.content)


def download(number, content):
    file_path = f'/Users/sy/Downloads/daxue/{number}.jpg'
    with open(file_path, 'wb') as f:
        f.write(content)


if __name__ == '__main__':
    run()
