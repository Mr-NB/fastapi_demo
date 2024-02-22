import sys, re, logging, hashlib, json, time
from datetime import datetime
from time import time
from random import random

from app.mapping import *


class Util:
    @classmethod
    def format_Resp(cls, code_type=CodeStatus.SuccessCode,
                    data='',
                    message='',
                    sys_obj=None,
                    exp_obj=None,
                    exception='',
                    **kwargs
                    ):
        '''
        定义返回Response模板
        :param code_type:   int|错误状态
        :param errorDetail: str|错误详情
        :param data:   str|request成功后填充
        :param message:  str|提示信息
        :param sys_obj:  Obj|获取当前文件名,函数名,所在行数
        :return:
        '''
        Resp = {}
        Resp['code'] = code_type.value

        if sys_obj:
            Resp['errorDetail'] = {"file": sys_obj.f_code.co_filename.split('/')[-1],
                                   "function": sys_obj.f_code.co_name,
                                   "lineNo": sys_obj.f_lineno,
                                   "exception": exception
                                   }
        elif exp_obj:
            exception = cls.exception_handler(exp_obj)
            Resp['errorDetail'] = exception
            if not message:
                message = exception.get('exception')
        else:
            Resp['data'] = data
        Resp['message'] = message if message else code_type.name
        if kwargs:
            for key, value in kwargs.items():
                Resp[str(key)] = value
        return Resp

    @classmethod
    def exception_handler(clsm, exp_obj):
        tb_next = exp_obj[2].tb_next
        while tb_next:
            if not tb_next.tb_next:
                break
            else:
                tb_next = tb_next.tb_next
        if tb_next:
            tb_frame = tb_next.tb_frame
            filename = tb_frame.f_code.co_filename
            func_name = tb_frame.f_code.co_name
            lineno = tb_frame.f_lineno
        else:
            filename = ""
            func_name = ""
            lineno = ""
        exception = exp_obj[0].__name__ + ":" + str(exp_obj[1]).replace("'", '')
        return {"file": filename, "function": func_name,
                "lineNo": lineno, "exception": exception
                }

    @classmethod
    def key_validate(cls, data, node_name):
        '''
        针对A.B.C　的字符串类型进行递归判断,如果不存在相应字段,返回相应错误
        :param data:
        :type data: dict
        :param node_name:
        :type node_name: str
        :return:
        :rtype:
        '''
        key_list = node_name.split('.')
        if not isinstance(data, dict):
            return cls.format_Resp(code_type=CodeStatus.InvalidDataError, message='parameter data must be dict')
        try:
            for index, key in enumerate(key_list):
                match_res = re.findall(r'(.*)\[(.+?)\]', key)
                if match_res:
                    k1, index1 = match_res[0][0], match_res[0][1]
                    if not k1:
                        return cls.format_Resp(code_type=CodeStatus.ParametersMissError,
                                               message="{} doesn't exists".format(k1))

                    data = data[k1][int(index1)]
                else:
                    data = data[key]
            return cls.format_Resp(data=data)
        except:
            exp = sys.exc_info()
            return Util.format_Resp(code_type=CodeStatus.UnknownError, exc_obj=exp)

    @classmethod
    def get_now(cls, formatStr='%Y-%m-%d %H:%M:%S'):
        return datetime.now().strftime(formatStr)

    @classmethod
    def get_utc_time(cls):
        return datetime.utcnow()

    @classmethod
    def datetime_to_str(cls, obj, formatStr="%Y-%m-%d"):
        return obj.strftime(formatStr)

    @classmethod
    def str_to_datetime(cls, string, formatStr="%Y-%m-%d"):
        return datetime.strptime(string, formatStr)

    @classmethod
    def gen_md5_hash(cls, text):
        '''
        Generates md5 hash.
        :param obj:
        :return: Encoded string.
        '''
        return hashlib.md5(text.encode(encoding='utf-8')).hexdigest()

    @classmethod
    def get_now_timestamp(cls, ms=True):
        if ms:
            return int(time.time() * 1000)
        return int(time.time())

    @classmethod
    def get_trace_code(cls, length=10):
        return cls.gen_md5_hash("{}-{}".format(random(), time.time())).upper()[:length]

    @classmethod
    def cal_work_hour(cls, startDatetime, endDatetime, formatStr="%Y-%m-%d %H:%M"):
        totalSeconds = (datetime.strptime(endDatetime, formatStr) - datetime.strptime(startDatetime,
                                                                                      formatStr)).total_seconds()
        return round(totalSeconds / 3600, 2)

    @staticmethod
    def to_ascii(h):
        list_s = []
        for i in range(0, len(h), 2):
            list_s.append(chr(int(h[i:i + 2], 16)))
        return ''.join(list_s)

    @staticmethod
    def to_hex(s):
        list_h = []
        for c in s:
            list_h.append(str(hex(ord(str(c)))[2:]).zfill(2))
        return ''.join(list_h)

    @staticmethod
    def byte_to_hex(b):
        list_s = []
        for i in b:
            list_s.append(hex(i)[2:].zfill(2))
        return ''.join(list_s)

    @staticmethod
    def hex_to_bin(hexStr):

        return '{:08b}'.format(int(str(hexStr), 16))

    @staticmethod
    def crc16Modbus(bytes_data, start_pos, stop_pos, invert=False):
        a = 0xFFFF
        b = 0xA001
        for i in range(start_pos, stop_pos):
            a ^= bytes_data[i]
            for j in range(8):
                last = a % 2
                a >>= 1
                if last == 1:
                    a ^= b
        return (a << 8 & 0xff00) | a >> 8 if invert == False else a

    @staticmethod
    def sum_hex(hexStr):
        return sum([int("{}{}".format(hexStr[i], hexStr[i + 1]), 16) for i in range(0, len(hexStr), 2)]) & 0xFFFF

    @staticmethod
    def bin_to_int(binStr):
        return int(binStr.zfill(8), 2)

    @staticmethod
    def hexStr_to_int(hexStr):
        return int(hexStr, 16)

    @staticmethod
    def replace_char(old_string, char, index):
        '''
        字符串按索引位置替换字符
        '''
        old_string = str(old_string)
        # 新的字符串 = 老字符串[:要替换的索引位置] + 替换成的目标字符 + 老字符串[要替换的索引位置+1:]
        new_string = old_string[:index] + char + old_string[index + 1:]
        return new_string

    @staticmethod
    def filter_null(data):
        newDict = {}
        for k, v in data.items():
            if v != None:
                newDict[k] = v
        return newDict

    @classmethod
    def timeStamp_to_datetime(cls, timeStamp, formatStr='%Y-%m-%d %H:%M:%S'):
        length = len(str(timeStamp))
        if length == 13:
            return time.strftime(formatStr, time.localtime(int(timeStamp) / 1000))
        return time.strftime(formatStr, time.localtime(int(timeStamp)))
