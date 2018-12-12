# -*- coding: utf-8 -*-
"""
@author: sy

@file: meta_picture.py

@time: 2018年12月08日21:32:49

@desc: 读取图片,解析其中的元数据小脚本

"""
import os
import exifread


class MetaPicture(object):
    # 类变量,图片文件夹的绝对路径
    picture_paths = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'picture')

    def read_picture(self):
        """ 读取图片,并调用自身提取元数据方法 """
        pictures = os.listdir(self.__class__.picture_paths)
        for picture in pictures:
            picture_path = os.path.join(self.picture_paths, picture)
            self.get_picture_exif(picture_path)

    def get_picture_exif(self, picture_name):
        """ 提取图片元数据 """
        img_file = open(picture_name, 'rb')
        picture_info = exifread.process_file(img_file)
        if picture_info:
            for tag, value in picture_info.items():
                print(f'{tag}:{value}')
            print('*' * 150)
            GPSLatitude = picture_info['GPS GPSLatitude']  # 纬度数
            GPSLatitudeRef = picture_info['GPS GPSLatitudeRef']  # N,S 南北纬
            GPSLongitude = picture_info['GPS GPSLongitude']  # 经度数
            GPSLongitudeRef = picture_info['GPS GPSLongitudeRef']  # E,W 东西经
            GPSDate = picture_info['EXIF DateTimeOriginal']  # 拍摄时间
            if GPSLatitude and GPSLongitude and GPSDate:
                print(f'纬度:{GPSLatitudeRef}{GPSLatitude}\n精度:{GPSLongitudeRef}{GPSLongitude}\n拍摄时间:{GPSDate}\n')
                self.deal_data_format(GPSLatitude)
        else:
            print('请检查提取的图片是否为原图,若为原图,则说明无相关元数据！')

    def deal_data_format(self, data):
        """ 处理数据,清洗格式生成对应内容 """
        data_list_tmp = str(data).replace('[', '').replace(']', '').split(',')
        data_list = [data.strip() for data in data_list_tmp]
        data_tmp = data_list[-1].split('/')
        data_list[-1] = str(int(data_tmp[0]) / int(data_tmp[1]))
        # 将列表中元素进行拼接

        data_str = ''.join(data_list)  # .replace(',', '')
        print(data_str)


def main():
    metaPicture = MetaPicture()
    metaPicture.read_picture()


main()
