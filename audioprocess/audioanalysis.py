import wave
import numpy as np
import pylab as pl


# 计算每一帧的能量, 256个采样点为一帧
def calenergy(wavedata):
    ene = []
    sumene = 0
    for i in range(len(wavedata)):
        sumene = sumene + (int(wavedata[i]) * int(wavedata[i]))
        if (i + 1) % 256 == 0:
            ene.append(sumene)
            sumene = 0
        elif i == len(wavedata) - 1:
            ene.append(sumene)
    return ene


if __name__ == '__main__':

    f = wave.open("../wav/5.wav", "rb")
    # getparams() 一次性返回所有的WAV文件的格式信息
    params = f.getparams()
    # nframes 采样点数目
    nchannels, sampwidth, framerate, nframes = params[:4]
    # readframes() 按照采样点读取数据，返回二进制字符串
    str_data = f.readframes(nframes)

    # 转成二字节数组形式（每个采样点占两个字节）
    wave_data = np.fromstring(str_data, dtype=np.short)
    print("采样点数目：" + str(len(wave_data)))
    f.close()

    energy = calenergy(wave_data)

    time = np.arange(0, len(wave_data)) * (1.0 / framerate)
    time2 = np.arange(0, len(energy)) * (len(wave_data) / len(energy) / framerate)
    pl.subplot(211)
    pl.plot(time, wave_data)
    pl.ylabel("Amplitude")
    pl.subplot(212)
    pl.plot(time2, energy)
    pl.ylabel("short energy")
    pl.xlabel("time (seconds)")
    pl.show()
