from ctypes import *
import time

# 调用动态链接库
MSC_X64DLL = WinDLL('../bin/msc.dll')
LOGIN_CONFIG = b'appid = 5cc8309a'
SAMPLE_RATE_16K = 16000
MSP_SUCCESS = 0
# 返回结果状态
MSP_AUDIO_SAMPLE_FIRST = 1
MSP_AUDIO_SAMPLE_CONTINUE = 2
MSP_AUDIO_SAMPLE_LAST = 4
MSP_REC_STATUS_COMPLETE = 5


class Msp:
    def __init__(self):
        pass

    @staticmethod
    def login():
        ret = MSC_X64DLL.MSPLogin(None, None, LOGIN_CONFIG)
        if ret == MSP_SUCCESS:
            print('登录讯飞成功')
        else:
            print('登录讯飞失败：', ret)

    @staticmethod
    def logout():
        ret = MSC_X64DLL.MSPLogout()
        if ret == MSP_SUCCESS:
            print('退出讯飞成功')
        else:
            print('退出讯飞失败：', ret)

    @staticmethod
    def isr(audiofile, session_begin_params):
        ret = c_int()
        session_id = c_voidp()
        MSC_X64DLL.QISRSessionBegin.restype = c_char_p
        session_id = MSC_X64DLL.QISRSessionBegin(None, session_begin_params, byref(ret))

        pice_lne = 1638 * 2
        ep_status = c_int(0)
        recog_status = c_int(0)

        wav_file = open(audiofile, 'rb')
        wav_data = wav_file.read(pice_lne)

        ret = MSC_X64DLL.QISRAudioWrite(session_id, wav_data, len(wav_data), MSP_AUDIO_SAMPLE_FIRST,
                                        byref(ep_status), byref(recog_status))

        time.sleep(0.1)
        while wav_data:
            wav_data = wav_file.read(pice_lne)
            if len(wav_data) == 0:
                break
            ret = MSC_X64DLL.QISRAudioWrite(session_id, wav_data, len(wav_data), MSP_AUDIO_SAMPLE_CONTINUE,
                                            byref(ep_status), byref(recog_status))
            time.sleep(0.1)
        wav_file.close()
        ret = MSC_X64DLL.QISRAudioWrite(session_id, None, 0, MSP_AUDIO_SAMPLE_LAST,
                                        byref(ep_status), byref(recog_status))

        result = '识别结果为:'
        counter = 0
        while recog_status.value != MSP_REC_STATUS_COMPLETE:
            ret = c_int()
            MSC_X64DLL.QISRGetResult.restype = c_char_p
            ret_str = MSC_X64DLL.QISRGetResult(session_id, byref(recog_status), 0, byref(ret))
            if ret_str is not None:
                result += ret_str.decode()
            counter += 1
            time.sleep(0.2)
            counter += 1
        return result


def xf_text(path, sample_rate):
    session_begin_params = "sub = iat, domain = iat, language = zh_cn, accent = mandarin, " \
                           "sample_rate = {}, result_type = plain, result_encoding = utf8".format(sample_rate)
    session_begin_params = session_begin_params.encode('utf8')
    text = Msp.isr(path, session_begin_params)
    print(text)


if __name__ == '__main__':

    Msp.login()
    while True:
        print('选择要在线识别的语音文件：')
        print('0.退出')
        print('1.12345')
        print('2.wav_test')
        print('3.monitor1')
        print('4.monitor2')
        print('5.monitor3')
        file = input()
        if file == '0':
            print('bye bye!')
            break
        elif file == '1':
            file_path = '../wav/12345.wav'
        elif file == '2':
            file_path = '../wav/wav_test.pcm'
        elif file == '3':
            file_path = '../wav/monitor1.pcm'
        elif file == '4':
            file_path = '../wav/monitor2.wav'
        elif file == '5':
            file_path = '../wav/monitor3.wav'
        else:
            continue
        xf_text(file_path, SAMPLE_RATE_16K)
    Msp.logout()
