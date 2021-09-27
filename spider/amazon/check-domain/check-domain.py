# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.

from dynaconf import settings

from alibabacloud_domain20180129.client import Client as Domain20180129Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_domain20180129 import models as domain_20180129_models


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
            domain_name='baidu.com'
        )
        # 复制代码运行请自行打印 API 的返回值
        client.check_domain(check_domain_request)

    @staticmethod
    async def check_async(domain_name):
        client = CheckDomain.create_client(settings.ACCESS_KEY_ID, settings.ACCESS_KEY_SECRET)
        check_domain_request = domain_20180129_models.CheckDomainRequest(
            domain_name='baidu.com'
        )
        # 复制代码运行请自行打印 API 的返回值
        await client.check_domain_async(check_domain_request)


if __name__ == '__main__':
    print(CheckDomain.check('baidu.com'))
