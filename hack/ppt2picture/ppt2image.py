# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : ppt2image.py
@Time    : 2019/4/19 12:25
@desc    : ppt 转为图片或者合并长图
"""

import win32com
import win32com.client
import os

from PIL import Image


def ppt2png(ppt_path, long_sign: str):
    """
    ppt 转 png 方法
    :param ppt_path: ppt 文件的绝对路径
    :param long_sign: 是否需要转为生成长图的标识
    :return:
    """
    if os.path.exists(ppt_path):
        output_path = output_file(ppt_path)  # 判断文件是否存在

        ppt_app = win32com.client.Dispatch('PowerPoint.Application')
        ppt = ppt_app.Presentations.Open(ppt_path)  # 打开 ppt
        ppt.SaveAs(output_path, 17)  # 17数字是转为 ppt 转为图片
        ppt_app.Quit()  # 关闭资源，退出

        if 'Y' == long_sign.upper():
            generate_long_image(output_path)  # 合并生成长图

    else:
        raise Exception('请检查文件是否存在！\n')


def output_file(ppt_path):
    """ 输出图片路径 """
    file_name = os.path.basename(ppt_path)  # 获取文件名字
    if file_name.endswith(('ppt', 'pptx')):
        exec_path = os.path.abspath(os.path.dirname(__file__))  # 当前脚本路径
        name = file_name.split('.')[0]  # 去除后缀，获取名字
        image_dir_path = os.path.join(exec_path, name)  # 图片文件夹的绝对路径
        if not os.path.exists(image_dir_path):
            os.makedirs(image_dir_path)  # 创建以 ppt 命名的图片文件夹
        output_png_path = os.path.join(image_dir_path, '一页一张图.png')  # png 图片输出路径
        return output_png_path
    else:
        raise Exception('请检查后缀是否为 ppt/pptx 后缀！\n')


def generate_long_image(output_path):
    picture_path = output_path[:output_path.rfind('.')]
    last_dir = os.path.dirname(picture_path)  # 上一级文件目录

    # 获取单个图片
    ims = [Image.open(os.path.join(picture_path, fn)) for fn in os.listdir(picture_path) if fn.endswith('.png')]
    width, height = ims[0].size  # 取第一个图片尺寸
    long_canvas = Image.new(ims[0].mode, (width, height * len(ims)))  # 创建同宽，n高的白图片

    # 拼接图片
    for i, image in enumerate(ims):
        long_canvas.paste(image, box=(0, i * height))

    long_canvas.save(os.path.join(last_dir, 'long-image.png'))  # 保存长图


def run():
    while 1:
        try:
            ppt_path = input('请输入ppt/pptx的完整路径:\n')
            long_sign = input('是否需要将各图片合成长图,默认不合成(Y/N):')
            ppt2png(ppt_path, long_sign)
            print('ppt 转化图片成功！请查看软件当前目录！')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    run()
