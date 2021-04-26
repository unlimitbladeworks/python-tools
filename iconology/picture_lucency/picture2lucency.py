# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : picture2lucency.py
@Time    : 2020/3/29 9:40 上午
@desc    : 图片背景变透明
"""

from PIL import Image


def transparent_back(img):
    img = img.convert('RGBA')  # 图片转换为四通道。第四个通道就是我们要修改的透明度。返回新的对象

    width, height = img.size  # 获取图片像素尺寸
    pixel_data = img.load()
    for h in range(height):
        for w in range(width):
            pixel = pixel_data[w, h]
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
            a = pixel[3]
            # 四通道，色彩值大于浅灰色，则将像素点变为透明块
            if r > 220 and g > 220 and b > 220 and a > 220:
                pixel_data[w, h] = (255, 255, 255, 0)
    return img


def resize(picture_name, out_name, factor=0.8):
    img = Image.open(picture_name)

    out = img.resize(tuple(map(lambda x: int(x * factor), img.size)), Image.ANTIALIAS)
    out.save(out_name)


def combine(original_picture, cover_picture, out_name, left_top_tuple):
    pix = Image.open(original_picture)
    cover_picture = Image.open(cover_picture)
    pix.paste(cover_picture, left_top_tuple, cover_picture)
    pix.save(out_name)


if __name__ == '__main__':
    # name = 'glasses'
    # img = Image.open(f'{name}.png')
    # img = transparent_back(img)
    # img.save(f'{name}-new.png')
    resize('glasses.png', '2-glasses.png', 0.286)
    combine('jay-young.png', '2-glasses.png', 'new-jay.png', (860, 137))
