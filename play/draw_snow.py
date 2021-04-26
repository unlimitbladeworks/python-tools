# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : draw_snow.py
@Time    : 2020/5/2 2:30 下午
@desc    : 无聊的画
"""
import turtle
import random


def snow(snow_count):
    turtle.hideturtle()
    turtle.speed(500)
    turtle.pensize(2)
    for i in range(snow_count):
        r = random.random()
        g = random.random()
        b = random.random()
        turtle.pencolor(r, g, b)
        turtle.pu()
        turtle.goto(random.randint(-350, 350), random.randint(1, 270))
        turtle.pd()
        dens = random.randint(8, 12)
        snowsize = random.randint(10, 14)
        for _ in range(dens):
            turtle.forward(snowsize)  # 向当前画笔方向移动snowsize像素长度
            turtle.backward(snowsize)  # 向当前画笔相反方向移动snowsize像素长度
            turtle.right(360 / dens)  # 顺时针移动360 / dens度


def rotate():
    turtle.pensize(2)
    turtle.bgcolor("black")
    colors = ["red", "yellow", 'purple', 'blue']
    turtle.tracer(False)
    for x in range(400):
        turtle.forward(2 * x)
        turtle.color(colors[x % 4])
        turtle.left(91)
    turtle.tracer(True)
    turtle.done()


def test():
    turtle.color('black', 'yellow')
    turtle.begin_fill()
    while True:
        turtle.circle(80)
        turtle.forward(200)
        turtle.left(170)
        if abs(turtle.pos()) < 1:
            break
    turtle.end_fill()


def run():
    turtle.setup(800, 600, 0, 0)
    turtle.bgcolor("black")
    # snow(30)
    rotate()
    turtle.mainloop()


if __name__ == '__main__':
    turtle.setup(800, 600, 0, 0)
    # run()
    test()
    turtle.done()
