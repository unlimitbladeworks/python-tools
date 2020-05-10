# coding:utf-8
"""
参考源地址：https://github.com/yp05327/PythonCharacterVideoPlayer
        关于此库安装，详细阅读上面原作者的 readme 进行安装
修改部分 python3 报错语法
"""
import cv2
import time
import os
import argparse
from pydub import AudioSegment
from threadpool import *

start_played_time = 0
fps = 0


# 将色点转为字符
def get_char(color_point):
    if FLAGS.ascii_mode:
        # 优化过的ascii显示列表
        ascii_char = list(r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
        ascii = ascii_char[int(0.2734375 * color_point)]
        return ascii + ascii
    else:
        if color_point > 100:
            return FLAGS.zifu + ' '
        else:
            return '  '


# 将图片转为字符
def img_to_char(image, size):
    image = cv2.resize(image, size)
    text = ''
    for i in range(size[0]):
        text += '\n'
    start = time.time()
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            text += get_char(image[i, j])
        text += '\n'

    return text + '字符转化时间：%f' % (start - time.time())


# 播放一帧
def play(video):
    global start_played_time
    global fps

    num = 0
    while (video.isOpened()):
        ret, frame = video.read()
        if frame is None:
            break

        size = get_size(frame.shape)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        text = img_to_char(image, size)

        play_frame(text, num)

        num += 1


def play_frame(text, num):
    global start_played_time
    global fps

    now_time = time.time()

    # 帧率控制
    delta_time = now_time - start_played_time - num * 1.0 / fps
    if delta_time < 0:
        time.sleep(-delta_time)

    total_time = time.time() - start_played_time
    text = text + '原视频帧率：%f, 当前帧：%d，播放时长：%f，帧率：%f, delta_time:%f\n\r' % (
    fps, num, total_time, num * 1.0 / total_time, delta_time)
    print(text)


def play_audio():
    import wave
    import pyaudio
    # wav文件读取
    f = wave.open('Audio_tmp.wav', 'rb')
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # define stream chunk
    chunk = 1024
    # 打开声音输出流
    stream = p.open(format=p.get_format_from_width(sampwidth),
                    channels=nchannels,
                    rate=framerate,
                    output=True)

    # 写声音输出流到声卡进行播放
    data = f.readframes(chunk)
    i = 1
    while True:
        data = f.readframes(chunk)
        if data == b'': break
        stream.write(data)
    f.close()
    # stop stream
    stream.stop_stream()
    stream.close()
    # close PyAudio
    p.terminate()


# 获取缩放大小
def get_size(shape):
    tmp = shape[1] / FLAGS.video_scale
    size = (int(shape[1] / tmp), int(shape[0] / tmp))
    return size


def run(video):
    global fps
    global start_played_time

    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    if int(major_ver) < 3:
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
    else:
        fps = video.get(cv2.CAP_PROP_FPS)

    if start_played_time == 0:
        start_played_time = time.time()

    pool = ThreadPool(2)
    reqs = makeRequests(play_audio, [([], None)])
    reqs.append(makeRequests(play, [([video], None)])[0])

    for req in reqs:
        pool.putRequest(req)

    try:
        pool.wait()
    except Exception:
        pass

    video.release()


def main():
    if os.path.isfile('Audio_tmp.wav'):
        os.remove('Audio_tmp.wav')

    if FLAGS.video_dir == '':
        print('请输入视频路径')
    else:
        # 检测视频格式是否支持
        video = cv2.VideoCapture(FLAGS.video_dir)

        if not video.isOpened():
            music_file = input('无法读取视频信息，是否转换文件(y/N):')
            if music_file == 'y' or music_file == 'Y':
                print('正在转换视频格式，请稍候')
                comm = 'ffmpeg -i {0} -strict -2 {1}'.format(FLAGS.video_dir, 'Video_tmp.mp4')
                os.system(comm)
                FLAGS.video_dir = 'Video_tmp.mp4'
                print('转换视频格式完毕')
                video = cv2.VideoCapture(FLAGS.video_dir)
            elif music_file == 'n' or music_file == 'N':
                print('无法读取视频信息，仅播放音频')
            else:
                print('输入错误')
                return

        if FLAGS.audio_mode:
            print('正在转换音频，请稍候')
            geshi = os.path.splitext(FLAGS.video_dir)[1][1:]
            AudioSegment.from_file(FLAGS.video_dir, geshi).export('Audio_tmp.wav', format='wav')
            print('转换音频完毕，开始播放')

        run(video)

        if os.path.isfile('Audio_tmp.wav'):
            os.remove('Audio_tmp.wav')
        if os.path.isfile('Video_tmp.mp4'):
            os.remove('Video_tmp.mp4')


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--video_dir',
        type=str,
        default='',
        help='视频路径'
    )
    parser.add_argument(
        '--ascii_mode',
        type=str2bool,
        default=False,
        help='采用灰度转ascii码模式'
    )
    parser.add_argument(
        '--audio_mode',
        type=str2bool,
        default=False,
        help='是否播放音频，需要ffmpeg、pyaudio、portaudio支持'
    )
    parser.add_argument(
        '--zifu',
        type=str,
        default='@',
        help='可以指定替换字符，默认为@'
    )
    parser.add_argument(
        '--video_scale',
        type=int,
        default=64,
        help='像素缩放比例，默认64，值越大需要更高的计算性能'
    )

    FLAGS, unparsed = parser.parse_known_args()
    main()
