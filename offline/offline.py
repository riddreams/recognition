import sys
from ctypes import *
from buildgrammar import *
from recognize import *

if __name__ == '__main__':
    build_grammar = BuildGrammar()
    grammar_id = build_grammar.build()

    # 登录
    msc = WinDLL(MSCDLL_PATH)
    ret = msc.MSPLogin(None, None, LOGIN_CONFIG)
    if MSP_SUCCESS != ret:
        print('登录失败：', ret)
        msc.MSPLogout()
        sys.exit(0)

    # 识别
    recognize = Recognize(grammar_id, msc)
    # recognize.run_asr('../wav/12345.pcm')
    # recognize.run_asr('../wav/wav_test.pcm')
    # recognize.run_asr('../wav/monitor1.pcm')
    # recognize.run_asr('../wav/monitor2.pcm')
    # recognize.run_asr('../wav/monitor3.pcm')

    recognize.run_asr('../wav/ouput5.pcm')
    recognize.run_asr('../wav/ouput53.pcm')
    recognize.run_asr('../wav/ouput56.pcm')
    recognize.run_asr('../wav/ouput59.pcm')
    recognize.run_asr('../wav/ouput62.pcm')

    # 退出
    msc.MSPLogout()
