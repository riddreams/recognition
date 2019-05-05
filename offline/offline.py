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
    recognize.run_asr('../wav/monitor1.wav')
    recognize.run_asr('../wav/monitor1.pcm')

    # 退出
    msc.MSPLogout()
