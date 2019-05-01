# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : excel_stock.py
@Time    : 2019/4/30 19:35
@desc    : Excel( xlsxwriter ) 画出股票趋势图
"""
import pandas as pd
import pandas_datareader.data as pdr
import datetime
# 不加会报错
import fix_yahoo_finance as yf

yf.pdr_override()


class ExcelStock:

    def __init__(self, stocks, sheet_name, time):
        self.stock_list = stocks
        self.start, self.end = time
        self.sheet_name = sheet_name

    def get_stock(self):

        all_data = {}
        for ticker in self.stock_list:
            all_data[ticker] = pdr.get_data_yahoo(ticker, self.start, self.end)

        """
            创建pandas的数据结构,DataFrame,可以看成一个二维表
            Adj Close 是根据法人行为调整之后的闭市价格。
        """
        self.df = pd.DataFrame({tic: data['Adj Close']
                                for tic, data in all_data.items()})

    def write_excel(self):
        # 利用 xlsxwriter 作为引擎，用 pandas 创建一个 excel
        writer = pd.ExcelWriter('pandas_chart_stock.xlsx', engine='xlsxwriter')
        self.df.to_excel(writer, sheet_name=self.sheet_name)

        # 使用 xlsxwriter 引擎后，初始化 excel 的工作表和sheet页
        workbook = writer.book
        worksheet = writer.sheets[self.sheet_name]

        # 创建一个图标，类型是线型图
        chart = workbook.add_chart({'type': 'line'})

        # 从 DataFrame 源数据中配置添加图表相关属性。
        max_row = len(self.df) + 1
        for i in range(len(self.stock_list)):
            col = i + 1
            """
                官网搜索:https://xlsxwriter.readthedocs.io/chart.html
                add_series() 有详细参数介绍
                使用一个列表值来代替excel的行列计算公式
                [sheet 名字, 第一行, 第一列, 最后一行, 最后一列]
            """
            chart.add_series({
                'name': [self.sheet_name, 0, col],  #
                'categories': [self.sheet_name, 2, 0, max_row, 0],  # 分类的标签
                'values': [self.sheet_name, 2, col, max_row, col],  # 图表与数值相连
                'line': {'width': 1.00},  # 线的粗细
            })

        # 配置图表的x轴名为日期
        chart.set_x_axis({'name': '日期'})
        # y轴名称 - 价格,不让y轴网格显示
        chart.set_y_axis({'name': 'Price', 'major_gridlines': {'visible': False}})

        # 把图表插入到 sheet 中，H2 貌似决定这图表的位置
        worksheet.insert_chart('H2', chart)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()


def run():
    start = datetime.datetime(2009, 8, 5)
    end = datetime.datetime(2019, 4, 30)
    time_tuple = (start, end)  # 开始时间和结束时间
    stock_list = ['BABA', 'BIDU']  # 股票代码，阿里和百度
    excel_stock = ExcelStock(stock_list, 'stocks', time_tuple)
    excel_stock.get_stock()
    excel_stock.write_excel()


if __name__ == '__main__':
    run()
