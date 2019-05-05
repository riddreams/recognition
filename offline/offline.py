import sys
from ctypes import *
from buildgrammar import *
from recognize import *

if __name__ == '__main__':
    build_grammar = BuildGrammar()
    grammar_id = build_grammar.build()

    # 登录
    MSC_X64DLL = WinDLL(MSCDLL_PATH)
    ret = MSC_X64DLL.MSPLogin(None, None, LOGIN_CONFIG)
    if MSP_SUCCESS != ret:
        print('登录失败：', ret)
        MSC_X64DLL.MSPLogout()
        sys.exit(0)

    # 识别
    recognize = Recognize(grammar_id)
    recognize.run_asr('../wav/monitor1.pcm')
    recognize.run_asr('../wav/monitor2.pcm')
    recognize.run_asr('../wav/5.pcm')

    # 退出
    MSC_X64DLL.MSPLogout()
