# python-tools
[![Python](https://img.shields.io/badge/python-v3.5+%2B-blue.svg)](https://www.python.org/)
[![build](https://img.shields.io/badge/build-passing-green.svg)](https://github.com/unlimitbladeworks/sy-pynotebook)
![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)



## python3日常小工具仓库
本项目记录平时学习到的小脚本，无论是从安全方面，还是从工具的使用方面上...


Environment(环境)
---

- python3+

项目目录结构
---
python-tools(:smiling_imp:)

    |--automation
        |-- excel-stock
            |-- excel_stock.py   (xlsxwriter + pandas 实现股票绘制)
        |-- cut-picture
            |-- cut.py       (九宫格图片剪切)
        |-- robot_pre
            |-- audio_demo.py   (Python电脑录音demo)
        
    |--hack  (安全方面的小工具脚本)
        |-- findu
            |-- find_you.py  (windows系统下递归查询隐藏文件,图形化界面小工具)
        |-- zip
            |-- zip_hack.py  (命令行读取字典和zip,破解密码)
        |-- whyb (Where have you been?的缩写)
            |-- xxx.py       (读取windows注册表,获取笔记本曾经连接的wifi网关的mac地址查询出你去过哪！
                              modify by 20181208 此模块作废,没找到中国开源数据库有mac的信息，若有人提供后续继续更新...)
        |-- meta
            |-- meta_picture.py  (命令行执行,读取照片元数据,获取有用信息)
        |-- ppt2picture
            |-- ppt2image.py     (ppt转png图片，附带长图合并)
        |-- classify
            |-- auto_classify.py (根据日期和文件后缀自动分类文件)
            
    |--spider   (爬虫方面的小脚本)
        |-- python32.py          (python小课堂初始原生爬虫源代码)
        |-- crawl_wymusic.py     (网易云音乐爬虫源代码)
        |-- bilibili_10.1
            | -- ganbei.py       (国庆 70 周年,爬取 B 站视频历史弹幕)
        |-- doutu
            | -- doutula_spider.py  (斗图啦爬取)

各种代码对应的文章
---

automation:

- excel_stock.py -------------> [点我看文章](https://mp.weixin.qq.com/s?__biz=MzAxMTM3MDk2Ng==&mid=2451659709&idx=1&sn=657979494e70948c50c96c71cff02de2&chksm=8c97d304bbe05a12fa515241d9551d087c903a415af2e0b77edaa4805a09a8803173b03fe705&token=1304533427&lang=zh_CN#rd)
- cut.py -------------> [点我看文章](https://mp.weixin.qq.com/s/VbfWyWR4oxCKTtguSJNmaQ) 
- audio_demo.py -------------> [点我看文章](https://mp.weixin.qq.com/s/vydiMi8lFln9e0Qe0xA1_A)

hack:

- find_you.py   -------------> [点我看文章](https://mp.weixin.qq.com/s?__biz=MzAxMTM3MDk2Ng==&mid=2451659560&idx=1&sn=420a1ba051f335ef09639dd613ac0158&chksm=8c97d391bbe05a87db3e6df957785efe9818260d0d1eaea53cdc30d875d0847672a1661aa61a&token=1588198533&lang=zh_CN#rd)
- zip_hack.py  -------------> [点我看文章](https://mp.weixin.qq.com/s?__biz=MzAxMTM3MDk2Ng==&mid=2451659077&idx=1&sn=232d05d83a95d9a8e1a2827d1c11934f&chksm=8c97d1fcbbe058ea9442195b4b7c500dc26670b31bde1690202076de523897f4cad00986b412&token=490358700&lang=zh_CN#rd)
- meta_picture.py  -------------> [点我看文章](https://mp.weixin.qq.com/s?__biz=MzAxMTM3MDk2Ng==&mid=2451659112&idx=1&sn=93c28fc18e1af2c84666fbf9b9a01218&chksm=8c97d1d1bbe058c7b00d4a7065507617caeea02ffc640c2d0318914a008432bb37f3f47e1f64&token=1168554650&lang=zh_CN#rd)
- ppt2image.py   -------------> [点我看文章](https://mp.weixin.qq.com/s?__biz=MzAxMTM3MDk2Ng==&mid=2451659643&idx=1&sn=f6b96f8a5604e949e99d3b1fee4f93a6&chksm=8c97d3c2bbe05ad45770dcbbbedff429b8c951986d84c8fd680116ff3dc35212049aff7b15a7&token=1281636927&lang=zh_CN#rd)
- auto_classify.py   -------------> [点我看文章](https://mp.weixin.qq.com/s?__biz=MzAxMTM3MDk2Ng==&mid=2451659689&idx=1&sn=4eb5c6080adf01b344cfc478a0aa1ce2&chksm=8c97d310bbe05a06531137e4b97b53a13a8ddcbe083c6239d64b848b4f2cb68e8710a2a318b5&token=1009393911&lang=zh_CN#rd)


spider:

- python32.py   -------------> [点我看文章](https://mp.weixin.qq.com/s?__biz=MzAxMTM3MDk2Ng==&mid=2451659374&idx=1&sn=d2252c900a04ccccc78d87e6aeac063c&chksm=8c97d2d7bbe05bc18561ca6e3ac3270bf425a970b1b0683ee53a96ddc01ae1f25be819b9c84c&token=1122100117&lang=zh_CN#rd)
- crawl_wymusic.py   -------------> [点我看文章](https://mp.weixin.qq.com/s?__biz=MzAxMTM3MDk2Ng==&mid=2451659659&idx=1&sn=5be9661d06aa11a61af6e20efd07abfb&chksm=8c97d332bbe05a24f7cd81efe8738b5c5ba63e61cfb9a69ffce6008753fd531b0ddd45979dd0&token=71465630&lang=zh_CN#rd)
- ganbei.py   -------------> [点我看文章](https://mp.weixin.qq.com/s/IOv_HF3dC87Orm09KKSFzA)
- doutula_spider.py   -------------> [点我看文章](https://mp.weixin.qq.com/s/mRDw_NxbelbVPECVzBaOLQ)






doutula_spider.py
<hr/>

初学者有学python的可以关注公众号哟！(:smiling_imp:)

![migezatan](https://img-blog.csdnimg.cn/20181104164256754.png)




