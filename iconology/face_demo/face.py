# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : face.py
@Time    : 2020/3/22 9:18 上午
@desc    : 人脸识别demo
"""

import face_recognition
from PIL import Image, ImageDraw


def demo_one():
    """ 例子1：定位图片中人脸的位置 """
    image = face_recognition.load_image_file("lyf.png")
    face_locations = face_recognition.face_locations(image)
    print(f"一共识别出 {len(face_locations)} 张人脸")

    for face_location in face_locations:
        # 打印出每张人脸对应四条边在图片中的位置(top、right、bottom、left)
        top, right, bottom, left = face_location
        print(f"人脸图片的位置: Top: {top}, Left: {right}, Bottom: {bottom}, Right: {right}")

        # 截取原图片被识别人脸的部分像素，展示临时图片
        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        pil_image.show()
        # pil_image.save('new.png')   # 保存新的人脸


def demo_two():
    """ 画出面部特征的线段 """
    image = face_recognition.load_image_file("trump.png")
    # 识别图片中人脸的面部特征
    face_landmarks_list = face_recognition.face_landmarks(image)
    print(f"一共识别出 {len(face_landmarks_list)} 张人脸")

    # 创建一个PIL ImageDraw 对象，用于绘制人脸特征线条
    pil_image = Image.fromarray(image)
    d = ImageDraw.Draw(pil_image)

    for face_landmarks in face_landmarks_list:
        # 打印出图片中每个脸部特征的位置
        for facial_feature in face_landmarks.keys():
            print(f"key-特征字段: {facial_feature} , value-数值: {face_landmarks[facial_feature]}")

        # 用线段描出图像中的每个脸部特征
        for facial_feature in face_landmarks.keys():
            d.line(face_landmarks[facial_feature], width=5)

    # Show the picture
    pil_image.show()


def demo_three():
    """ 自动给图片化妆 """
    # Load the jpg file into a numpy array
    image = face_recognition.load_image_file("trump.png")

    # Find all facial features in all the faces in the image
    face_landmarks_list = face_recognition.face_landmarks(image)

    pil_image = Image.fromarray(image)
    for face_landmarks in face_landmarks_list:
        d = ImageDraw.Draw(pil_image, 'RGBA')

        # Make the eyebrows into a nightmare
        d.polygon(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 128))
        d.polygon(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 128))
        d.line(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 150), width=5)
        d.line(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 150), width=5)

        # Gloss the lips
        d.polygon(face_landmarks['top_lip'], fill=(150, 0, 0, 128))
        d.polygon(face_landmarks['bottom_lip'], fill=(150, 0, 0, 128))
        d.line(face_landmarks['top_lip'], fill=(150, 0, 0, 64), width=8)
        d.line(face_landmarks['bottom_lip'], fill=(150, 0, 0, 64), width=8)

        # Sparkle the eyes
        d.polygon(face_landmarks['left_eye'], fill=(255, 255, 255, 30))
        d.polygon(face_landmarks['right_eye'], fill=(255, 255, 255, 30))

        # Apply some eyeliner
        d.line(face_landmarks['left_eye'] + [face_landmarks['left_eye'][0]], fill=(0, 0, 0, 110), width=6)
        d.line(face_landmarks['right_eye'] + [face_landmarks['right_eye'][0]], fill=(0, 0, 0, 110), width=6)

        pil_image.show()


def demo_four():
    known_image = face_recognition.load_image_file("jay-young.png")  # 婚前周杰伦
    unknown_image = face_recognition.load_image_file("jay-marry.png")  # 婚后周杰伦
    jay_encoding = face_recognition.face_encodings(known_image)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    results = face_recognition.compare_faces([jay_encoding], unknown_encoding)
    if results[0]:
        print("婚前婚后是一个人!")
    else:
        print("婚前婚后不是一个人!")


if __name__ == '__main__':
    # demo_one()
    # demo_two()
    # demo_three()
    demo_four()