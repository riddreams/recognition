import wave
import os
import subprocess
import numpy as np
import pylab as pl
from pydub import AudioSegment


def splitaudio(path):
    f = wave.open(path, "rb")
    params = f.getparams()
    print(params)
    nchannels, sampwidth, framerate, nframes = params[:4]
    str_data = f.readframes(nframes)
    wave_data = np.fromstring(str_data, dtype=np.short)
    f.close()

    wav_time = nframes / framerate
    print('音频时长', wav_time, 's')

    # 音频能量归一化
    l2norm = np.linalg.norm(wave_data)
    wav = np.array([i/l2norm for i in wave_data], dtype=np.float)

    length = nframes // (wav_time * 1)
    short_enery = []
    sum_temp = 0
    for i in range(len(wav)):
        sum_temp += wav[i] ** 2
        if (i + 1) % length == 0:
            short_enery.append(sum_temp)
            sum_temp = 0
        elif i == len(wav) - 1:
            short_enery.append(sum_temp)

    # print('短时能量数', len(short_enery))
    # print('短时能量', short_enery)
    index = np.where(np.array(short_enery, dtype=np.float) > 0.01)[0]
    print('短时能量大于0.01的索引', index)

    frame = []
    i = 0
    while i < len(index)-1:
        tmp_list = [index[i]]
        tmp = index[i]
        j = i + 1
        while j < len(index):
            if tmp + 1 == index[j]:
                tmp = index[j]
                j = j + 1
            else:
                break
        tmp_list.append(tmp)
        frame.append(tmp_list)
        if j > i+1:
            i = j
        else:
            i += 1

    audio = AudioSegment.from_wav(path)
    for fr in frame:
        start = 1000 * (fr[0]-2)
        end = 1000 * (fr[1]+2)
        sound = audio[start:end]
        from_path = 'ouput'+str(fr[0])+'.wav'
        to_path = '../wav/ouput'+str(fr[0])+'.pcm'
        sound.export(from_path, format='wav')
        from_path = os.path.abspath(from_path)
        to_path = os.path.abspath(to_path)
        # wav格式，采样率16kHz，单声道，路径中包含空格可用引号
        str_cmd = 'ffmpeg -y -i \"' + from_path + '\" -acodec pcm_s16le -f s16le -ac 1 -ar 16000 \"' + to_path + '\"'
        # print(str_cmd)
        subprocess.call(str_cmd)

    print(frame)
    # t = np.arange(0, len(short_enery))
    # pl.plot(t, short_enery)
    # pl.show()


if __name__ == '__main__':
    splitaudio('../wav/5.wav')

