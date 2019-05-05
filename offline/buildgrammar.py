import time
import sys
from ctypes import *
from const import *


class UserData(Structure):
    _fields_ = [("build_fini", c_int),
                ("update_fini", c_int),
                ("errcode", c_int),
                ("grammar_id", c_char * MAX_GRAMMARID_LEN)]


def build_grm_cb(ecode, info, udata):
    # print(3, udata.contents)
    if udata.contents is not None:
        udata.contents.build_fini = 1
        udata.contents.errcode = ecode

    if MSP_SUCCESS == ecode and info is not None:
        print('构建语法成功,语法ID:', info.decode())
        if udata.contents is not None:
            udata.contents.grammar_id = info
    else:
        print('构建语法失败:', ecode)

    return 0


class BuildGrammar(object):
    def __init__(self):
        # 调用动态链接库
        self.msc = WinDLL(MSCDLL_PATH)
        # 绑定回调函数
        self.GRMCBFUN = CFUNCTYPE(c_int, c_int, c_char_p, POINTER(UserData))
        self.build_grm_cb = self.GRMCBFUN(build_grm_cb)

    def build_grammar(self, udata):
        # print(2, udata.contents)
        with open(GRM_FILE, 'rb') as grm_file:
            grm_content = grm_file.read()
        length = len(grm_content)

        grm_build_params = 'engine_type = local, asr_res_path = {}, sample_rate = {}, grm_build_path = {}'.format(
            ASR_RES_PATH, SAMPLE_RATE_16K, GRM_BUILD_PATH)
        # print('grm_build_params:', grm_build_params)

        build_ret = self.msc.QISRBuildGrammar(b'bnf', grm_content, length, grm_build_params.encode(), self.build_grm_cb, udata)
        return build_ret

    def build(self):
        # 登录
        ret = self.msc.MSPLogin(None, None, LOGIN_CONFIG)
        if MSP_SUCCESS != ret:
            print('登录失败：', ret)
            self.msc.MSPLogout()
            sys.exit(0)

        asr_data = UserData()
        cp = pointer(asr_data)
        # print(1, cp.contents)
        print('正在构建离线识别语法网络...')
        ret = self.build_grammar(cp)
        if MSP_SUCCESS != ret:
            print('构建离线识别语法网络失败:', ret)
            self.msc.MSPLogout()
            sys.exit(0)

        while asr_data.build_fini != 1:
            # print('asr_data.build_fini:', asr_data.build_fini)
            time.sleep(0.3)

        # print('asr_data.grammar_id:', asr_data.grammar_id)
        if MSP_SUCCESS != asr_data.errcode:
            self.msc.MSPLogout()
            sys.exit(0)
        print('离线识别语法网络构建完成')

        self.msc.MSPLogout()
        return asr_data.grammar_id.decode()
