# -*- coding: utf-8 -*-
"""
@Author  : Sy
@File    : audio_demo.py
@Time    : 2019-11-09 16:35
@desc    : 生成音频文件
"""

import pyaudio
import wave

CHUNK = 1024  # 每个
FORMAT = pyaudio.paInt16  # 采样位数
CHANNELS = 1  # 声道
RATE = 44100  # 采样频率


def record_audio(wave_out_path, record_second):
    """ 录音功能 """
    p = pyaudio.PyAudio()  # 实例化对象
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)  # 打开流，传入响应参数
    wf = wave.open(wave_out_path, 'wb')  # 打开 wav 文件。
    wf.setnchannels(CHANNELS)  # 声道设置
    wf.setsampwidth(p.get_sample_size(FORMAT))  # 采样位数设置
    wf.setframerate(RATE)  # 采样频率设置
    print(f'***** 正在录音，录音时长： {record_second}s: *****')
    for _ in range(0, int(RATE * record_second / CHUNK)):
        data = stream.read(CHUNK)
        wf.writeframes(data)  # 写入数据
    print('***** 完成! *****')
    stream.stop_stream()  # 关闭流
    stream.close()
    p.terminate()
    wf.close()


def play_audio(wave_input_path):
    """ 播放音频 """
    p = pyaudio.PyAudio()  # 实例化
    wf = wave.open(wave_input_path, 'rb')  # 读 wav 文件
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)  # 读数据
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()  # 关闭资源
    stream.close()
    p.terminate()


if __name__ == '__main__':
    record_audio('demo.wav', record_second=4)
    play_audio('output.wav')