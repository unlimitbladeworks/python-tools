# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : generate_pic.py
@Time    : 2020/4/6 3:00 下午
@desc    : 自动识别人脸图形，佩戴附属品
"""
import face_recognition
from PIL import Image, ImageDraw


class FaceUtils(object):

    def __init__(self, key_word, original_picture, cover_picture):
        """
        :param key_word: 关键词，做不同策略选择
        :param original_picture: 要被覆盖的图片地址 （原图，如例子中的周董图片）
        :param cover_picture: 附属品的图片地址（眼镜、帽子）
        """
        self.__key_word = key_word
        self.__original_picture = original_picture
        self.__cover_picture = cover_picture
        self.__face_feature_dict = {}

    @staticmethod
    def transparent_back(img_name):
        """ 图形背景透明化工具类方法 """
        img = Image.open(f'{img_name}.png')
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
        img.save(f'{img_name}-new.png')

    def __reg_face(self):
        """ 识别面部特征 """
        image = face_recognition.load_image_file(self.__original_picture)
        # 识别图片中人脸的面部特征
        face_landmarks_list = face_recognition.face_landmarks(image)
        for face_landmarks in face_landmarks_list:
            # 找出左脸颊第一个坐标点和左眉毛第一个坐标点
            for facial_feature in face_landmarks.keys():
                # 根据不同关键词做不同的策略选择，如眼镜，则为下面
                if self.__key_word == 'glasses':
                    # 左脸颊，即第一个坐标
                    if facial_feature == 'chin':
                        left_chin = face_landmarks[facial_feature][0]  # 左脸颊
                        right_chin = face_landmarks[facial_feature][-1]  # 右脸颊
                        self.__face_feature_dict['left_chin'] = left_chin
                        self.__face_feature_dict['right_chin'] = right_chin
                    # 左眼眉
                    if facial_feature == 'left_eyebrow':
                        left_eyebrow = face_landmarks[facial_feature][0]
                        self.__face_feature_dict['left_eyebrow'] = left_eyebrow
                # todo 后续可以根据 key_word 做拓展获取坐标

    def __get_x_y(self):
        """ 组合不同的最终坐标 """
        # 1. 以左眼为例，眼镜为附属品，则计算的坐标是（左脸颊x坐标，左眼眉y坐标）
        if self.__key_word == 'glasses':
            x = self.__face_feature_dict['left_chin'][0]
            y = self.__face_feature_dict['left_eyebrow'][1]
            return x, y

        # todo 后续可以根据 key_word 做拓展获取坐标

    def __resize(self, factor=0.8):
        """ 附属品重塑大小 """
        img = Image.open(self.__cover_picture)
        width, height = img.size  # 获取附属品图片像素尺寸
        distance = self.__calc_resize_pix()
        if distance:
            factor = distance / width   # 像素长度/眼镜长度像素。
        out = img.resize(tuple(map(lambda x: int(x * factor), img.size)), Image.ANTIALIAS)
        out_name = 'resize_accessories.png'
        out.save(out_name)
        return out_name

    def __combine(self, resize_pic, left_top_tuple):
        """ 拼接，覆盖图片 """
        pix = Image.open(self.__original_picture)
        cover_picture = Image.open(resize_pic)
        pix.paste(cover_picture, left_top_tuple, cover_picture)
        pix.save('combine.png')

    def __calc_resize_pix(self):
        if self.__key_word == 'glasses':
            l_x, l_y = self.__face_feature_dict['left_chin']
            r_x, r_y = self.__face_feature_dict['right_chin']
            return r_x - l_x

    def run(self):
        self.__reg_face()
        left_top_tuple = self.__get_x_y()
        resize_image = self.__resize()
        self.__combine(resize_image, left_top_tuple)


if __name__ == '__main__':
    # FaceUtils.transparent_back('背景非透明.png')   1.先背景透明化
    original_picture_url = "huge.png"  # 2. 原图
    cover_picture_url = "1-glasses.png"  # 3. 背景透明化的附属图片
    face_utils = FaceUtils('glasses', original_picture_url, cover_picture_url)  # 4.传参
    face_utils.run()  # 5.运行
