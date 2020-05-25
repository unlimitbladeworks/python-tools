# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : change_word.py
@Time    : 2020/5/19 9:54 上午
@desc    :
"""

import os
import traceback
from chardet.universaldetector import UniversalDetector
import chardet
import tkinter as tk
from tkinter import messagebox


class ReplaceKeyWord(object):
    def __init__(self):
        self.window = tk.Tk()
        self.window.report_callback_exception = self.__report_callback_exception
        self.window.title('关键词替换小工具')
        width = 500
        height = 300
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.geometry('%dx%d+%d+%d' % (width, height, (screen_width - width) / 2, (screen_height - height) / 2))
        # 画出旧关键词输入控件
        self.__draw_old_kw()
        # 画出新关键词输入控件
        self.__draw_new_kw()
        # 画出路径输入控件
        self.__draw_path()
        # 画出勾选框
        self.__draw_checkbox()
        # 画出执行按钮
        self.__draw_replace()
        # 开启 tk 运行
        self.window.mainloop()

    def __draw_old_kw(self):
        tk.Label(self.window, text='原有关键词：', font=('Arial', 18), ).place(x=65, y=50, anchor='nw')
        self.old_kw_entry = tk.Entry(self.window, font=('Arial', 17))
        self.old_kw_entry.pack()
        self.old_kw_entry.place(x=180, y=50, anchor='nw')

    def __draw_new_kw(self):
        tk.Label(self.window, text='替换关键词：', font=('Arial', 18), ).place(x=65, y=90, anchor='nw')
        self.new_kw_entry = tk.Entry(self.window, font=('Arial', 17))
        self.new_kw_entry.pack()
        self.new_kw_entry.place(x=180, y=90, anchor='nw')

    def __draw_path(self):
        tk.Label(self.window, text='文件夹路径：', font=('Arial', 18), ).place(x=65, y=130, anchor='nw')
        self.path_entry = tk.Entry(self.window, font=('Arial', 17))
        self.path_entry.pack()
        self.path_entry.place(x=180, y=130, anchor='nw')

    def __draw_checkbox(self):
        self.filename_status = tk.IntVar()
        self.filename_checkbox = tk.Checkbutton(text="文件名称", variable=self.filename_status)
        self.filename_checkbox.pack()
        self.filename_checkbox.place(x=65, y=180, anchor='nw')

        self.content_status = tk.IntVar()
        self.content_checkbox = tk.Checkbutton(text="文件内容", variable=self.content_status)
        self.content_checkbox.pack()
        self.content_checkbox.place(x=175, y=180, anchor='nw')

        self.dirname_status = tk.IntVar()
        self.dirname_checkbox = tk.Checkbutton(text="文件夹名", variable=self.dirname_status)
        self.dirname_checkbox.pack()
        self.dirname_checkbox.place(x=285, y=180, anchor='nw')

    def __draw_replace(self):
        replace_button = tk.Button(self.window, text='替换',
                                   font=('Arial', 17), width=10, height=1,
                                   command=lambda: ReplaceKeyWord.iter_files(
                                       self.old_kw_entry.get(),  # 获取旧关键词输入的值
                                       self.new_kw_entry.get(),  # 获取新关键词输入的值
                                       self.path_entry.get(),  # 获取路径输入的值
                                       filename=self.filename_status.get(),  # 是否勾选文件名
                                       content=self.content_status.get(),  # 是否勾选文件内容
                                       dirname=self.dirname_status.get(),  # 是否勾选文件夹名
                                   ))
        replace_button.pack()
        replace_button.place(x=200, y=240, anchor='nw')

    def __report_callback_exception(self, *args):
        err = traceback.format_exception(*args)
        messagebox.showerror('参数错误', err[-1].replace('Exception:', '错误：'))

    @staticmethod
    def iter_files(old_kw, new_kw, root_dir, **kwargs):
        """
        遍历根目录
        :param old_kw: 旧词
        :param new_kw: 新词
        :param root_dir: 目录的绝对路径
        :param kwargs: 自定义参数
        """
        if not old_kw:
            raise Exception("原有关键词为空，请输入！")
        isdir = os.path.isdir(root_dir)
        if not isdir:
            raise Exception("找不到该目录！请检查路径是否正确！")

        keywords_dict = {}
        for k, v in kwargs.items():
            keywords_dict[k] = v

        detector = UniversalDetector()
        for root, dirs, files in os.walk(root_dir, topdown=False):
            # 替换文件内容
            if keywords_dict['content'] == 1:
                # 先遍历最内层，逐步向上
                for file_name in files:
                    old_file_path = os.path.join(root, file_name)
                    file_data = ""
                    # 读该文件编码格式，重置对象
                    detector.reset()
                    with open(old_file_path, 'rb') as file:
                        for line in file.readlines():
                            detector.feed(line)
                            if detector.done:
                                break
                        curr_encode = detector.result['encoding']
                    # 如果被替换的字符串在文件内容中，先按行读出来，在替换
                    with open(old_file_path, 'r', encoding=curr_encode, errors='ignore') as f:
                        for line in f.readlines():
                            new_line = line.replace(old_kw, new_kw)
                            file_data += new_line
                    with open(old_file_path, 'w', encoding=curr_encode, errors='ignore') as f:
                        f.write(file_data)

            # 替换文件名称
            if keywords_dict['filename'] == 1:
                for file_name in files:
                    old_file_path = os.path.join(root, file_name)
                    # 如果被替换的字符串在文件的名中，则替换成新的
                    if old_kw in file_name:
                        new_file_name = file_name.replace(old_kw, new_kw)
                        new_file_path = os.path.join(root, new_file_name)
                        os.rename(old_file_path, new_file_path)

            # 替换文件夹名称
            if keywords_dict['dirname'] == 1:
                for dir_name in dirs:
                    old_dir_path = os.path.join(root, dir_name)
                    # 如果被替换的字符串在文件夹的名中，则替换成新的
                    if old_kw in dir_name:
                        new_dir_name = dir_name.replace(old_kw, new_kw)
                        new_dir_path = os.path.join(root, new_dir_name)
                        os.rename(old_dir_path, new_dir_path)


def run():
    # path = '/Users/sy/PycharmProjects/python-tools/automation/change-word/你/'
    # iter_files('呵呵', '哈哈', path)
    ReplaceKeyWord()
    # ReplaceKeyWord.iter_files('呵呵', '哈哈', path)


if __name__ == '__main__':
    run()
