import time
import sys
from ctypes import *
from const import *


class Recognize(object):
    def __init__(self, grammar_id, msc):
        self.grammar_id = grammar_id
        self.msc = msc

    def run_asr(self, path):
        aud_stat = c_int(2)
        ep_status = c_int(0)
        rec_status = c_int(2)
        errcode = c_int(-1)
        rss_status = c_int(2)
        pice_lne = 12800
        last_audio = 0
        rec_rslt = c_char_p
        pcm_count = 0

        asr_params = 'engine_type=local,asr_res_path={},sample_rate={},grm_build_path={},local_grammar={},' \
                     'result_type=plain,result_encoding=utf8' \
            .format(ASR_RES_PATH, SAMPLE_RATE_16K, GRM_BUILD_PATH, self.grammar_id)
        asr_params = asr_params.encode()
        # print(asr_params)

        session_id = c_char_p
        self.msc.QISRSessionBegin.restype = c_char_p
        session_id = self.msc.QISRSessionBegin(None, asr_params, byref(errcode))

        print('开始识别', path)
        asr_audiof = open(path, 'rb')
        while True:
            tmp = asr_audiof.read(pice_lne)
            # print(tmp)
            temp_len = len(tmp)
            if temp_len < pice_lne:
                last_audio = 1

            aud_stat = MSP_AUDIO_SAMPLE_CONTINUE

            if pcm_count == 0:
                aud_stat = MSP_AUDIO_SAMPLE_FIRST

            if temp_len <= 0:
                break

            self.msc.QISRAudioWrite.restype = c_int
            errcode = self.msc.QISRAudioWrite(session_id, tmp, len(tmp),
                                              aud_stat, byref(ep_status), byref(rec_status))

            pcm_count += temp_len
            # print(ep_status, ',', MSP_EP_AFTER_SPEECH)
            if MSP_EP_AFTER_SPEECH == ep_status.value:
                break

        asr_audiof.close()

        self.msc.QISRAudioWrite(session_id, None, 0, MSP_AUDIO_SAMPLE_LAST,
                                byref(ep_status), byref(rec_status))

        errcode = c_int(errcode)
        # print('errcode:', errcode)
        self.msc.QISRGetResult.restype = c_char_p
        while MSP_REC_STATUS_COMPLETE != rss_status.value and MSP_SUCCESS == errcode.value:
            rec_rslt = self.msc.QISRGetResult(session_id, byref(rss_status), 0, byref(errcode))
            time.sleep(0.1)

        if rec_rslt is not None:
            print('识别结果为:', rec_rslt.decode('utf8'))
        elif errcode.value != 0:
            print('识别出现错误:', errcode.value)
        else:
            print('没有识别结果')

        self.msc.QISRSessionEnd(session_id, None)
        return errcode.value

