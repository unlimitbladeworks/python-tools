# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : find_you.py
@Time    : 2019/4/9 22:11
@desc    : 使用界面来查找电脑中的隐藏文件
"""

import os
import win32file
import win32con
import platform
import tkinter as tk
from tkinter import messagebox


class FindU(tk.Frame):

    def __init__(self, master=None):
        """
        初始化, 复制于官网 A Simple Hello World Program 地址如下：
        https://docs.python.org/3/library/tkinter.html
        """
        super().__init__(master)
        self.master = master
        master.title('Python实现查找隐藏文件')  # 标题
        master.geometry('500x200+500+300')  # 窗口大小像素,500长,300宽的窗口, 400+300是从屏幕左上角画x、y坐标而来
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        """ 将 tkinter 图形化组件参数加载进来 """
        self.entry_label = tk.Label()  # 创建标签
        self.entry_label['text'] = r'请输入路径(例如: C:\Users\asus\Desktop\point):'
        self.entry_label.pack(side=tk.TOP)  # 固定在窗口的什么位置，四个位置，进源码看注释~

        self.entry_text = tk.Entry()  # 创建输入文本框
        self.entry_text['bd'] = 3  # 输入框边框像素
        self.entry_text['width'] = 50  # 输入框的宽度
        self.entry_text.pack(side=tk.TOP)

        self.entry_button = tk.Button(self)  # 创建执行按钮
        self.entry_button["text"] = "执行"  # 按钮显示的文字
        self.entry_button["command"] = self.exec_find  # 点击按钮后执行哪个函数
        self.entry_button.pack(side=tk.TOP)

        self.quit = tk.Button(self, text="退出",
                              fg="red",
                              command=self.master.destroy)  # 退出按钮，与上面写法不同，直接传参也行
        self.quit.pack(side=tk.BOTTOM)

        self.listbox = tk.Listbox(bg='#f2f2f2', fg='red')  # 创建带滚动条的 listbox
        self.yscrollbar = tk.Scrollbar(self.listbox, command=self.listbox.yview)
        self.yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.yscrollbar.set)
        self.listbox.pack(fill=tk.BOTH, expand=True)

    def exec_find(self):
        """ 执行查找程序 """
        required = messagebox.askyesnocancel('提示', '要执行此操作吗')  # 提示消息框
        if required:
            file_path = self.entry_text.get()  # 获取文本框输入的内容
            if file_path:
                self.iter_files(file_path)
                self.listbox.insert(tk.END, '搜索完毕！(若无路径,则说明没有隐藏文件！)')  # 调用 listbox，将每次内容插入末尾
            else:
                messagebox.showinfo('提示', '您输入的路径为空！请检查！')

    def iter_files(self, root_dir):
        """ 遍历文件夹根目录 """
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                file_name = os.path.join(root, file)
                if self.is_hidden_file(file_name):
                    self.listbox.insert(tk.END, file_name)  # 将路径填充到 listbox 控件上去
            for dirname in dirs:
                # 递归调用自身,只改变目录名称
                self.iter_files(dirname)

    def is_hidden_file(self, file_path):
        """ 判断 windows 系统下，文件是否为隐藏文件,是则返回 True """
        if 'Windows' in platform.system():
            file_attr = win32file.GetFileAttributes(file_path)  # 获取文件属性得到的是 int 值,例如 128 、32 等
            # FILE_ATTRIBUTE_HIDDEN 拿到的是 2 数字，与上行代码做 & 运算,结果非 0 说明是隐藏文件
            if file_attr & win32con.FILE_ATTRIBUTE_HIDDEN:
                return True
            return False
        return False


if __name__ == '__main__':
    root = tk.Tk()  # 主窗口
    find = FindU(master=root)
    find.mainloop()
