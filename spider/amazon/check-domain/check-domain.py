# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.

from dynaconf import settings
import time, random

from alibabacloud_domain20180129.client import Client as Domain20180129Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_domain20180129 import models as domain_20180129_models
import pandas as pd


class CheckDomain:

    @staticmethod
    def create_client(access_key_id: str, access_key_secret: str) -> Domain20180129Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 您的AccessKey ID,
            access_key_id=access_key_id,
            # 您的AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = 'domain.aliyuncs.com'
        return Domain20180129Client(config)

    @staticmethod
    def check(domain_name: str):
        client = CheckDomain.create_client(settings.ACCESS_KEY_ID, settings.ACCESS_KEY_SECRET)
        check_domain_request = domain_20180129_models.CheckDomainRequest(
            domain_name=domain_name
        )
        # 复制代码运行请自行打印 API 的返回值
        return client.check_domain(check_domain_request)

    @staticmethod
    async def check_async(domain_name: str):
        client = CheckDomain.create_client(settings.ACCESS_KEY_ID, settings.ACCESS_KEY_SECRET)
        check_domain_request = domain_20180129_models.CheckDomainRequest(
            domain_name=domain_name
        )
        # 复制代码运行请自行打印 API 的返回值
        return await client.check_domain_async(check_domain_request)

    @staticmethod
    def run():
        domain_list = []
        avail_list = []
        reason_list = []
        asin_list = []
        df = pd.read_excel('bs.xlsx')
        brand = df['Brand']
        for idx, name in brand.items():
            if name is None or name == '':
                continue
            try:
                asin = df[df['Brand'] == name]['ASIN'][idx]
                asin_url = f'https://www.amazon.com/dp/{asin}'
                time.sleep(random.randint(1, 10) / 10)  # 加点延时，1s并发不能有10个请求
                name = name.replace(' ', '').lower().split('\'')[0]
                domain = name + '.com'
                response = CheckDomain.check(domain)
                avail = response.body.avail  # 1：可注册。3：预登记。4：可删除预订。0：不可注册。-1：异常。-2：暂停注册。-3：黑名单。
                reason = response.body.reason
                print(f'当前域名:{domain},可用状态:{avail},失败原因：{reason}')
                domain_list.append(domain)
                avail_list.append(avail)
                reason_list.append(reason)
                asin_list.append(asin_url)
            except:
                print('asin')
                import traceback
                print(traceback.print_exc())

        df = pd.DataFrame({'domain': domain_list, 'asin_url': asin_list, 'avail': avail_list,
                           'reason': reason_list})
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        df.to_excel(f"domain-{now}.xlsx", index=False)


if __name__ == '__main__':
    CheckDomain.run()
