from pydub import AudioSegment
import subprocess
import os


def video2wav(from_path, to_path):
    from_path = os.path.abspath(from_path)
    to_path = os.path.abspath(to_path)
    # wav格式，采样率16kHz，单声道，路径中包含空格可用引号
    str_cmd = 'ffmpeg -i \"' + from_path + '\" -ac 1 -ar 16000 \"' + to_path + '\"'
    # print(str_cmd)
    subprocess.call(str_cmd)


def audio2pcm(from_path, to_path):
    from_path = os.path.abspath(from_path)
    to_path = os.path.abspath(to_path)
    # pcm格式，采样宽度2byte(16bit)，采样率16kHz，单声道，路径中包含空格可用引号
    str_cmd = 'ffmpeg -y -i \"' + from_path + '\" -acodec pcm_s16le -f s16le -ac 1 -ar 16000 \"' + to_path + '\"'
    # print(str_cmd)
    subprocess.call(str_cmd)


def playvideo(path):
    path = os.path.abspath(path)
    # 用ffmpeg的ffplay播放pcm文件，播完自动退出，采样宽度2byte(16bit)，采样率16kHz，单声道
    subprocess.call('ffplay -autoexit -ar 16000 -ac 1 -f s16le -i \"' + path + '\"')


if __name__ == '__main__':
    # audio2pcm('../wav/wav_test.wav', '../wav/wav_test.pcm')
    # pcm格式，采样宽度2byte(16bit)，采样率16kHz，单声道
    monitor = AudioSegment.from_file('../wav/monitor1.pcm', format='pcm', sample_width=2, frame_rate=16000, channels=1)
    time_len = monitor.duration_seconds
    print('monitor1时长:', time_len, 's')
    # playvideo('../wav/monitor1.pcm')
    # video2wav('../wav/5.mp4', '../wav/5.wav')

