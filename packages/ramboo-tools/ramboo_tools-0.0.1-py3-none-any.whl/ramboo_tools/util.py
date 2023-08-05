#!/usr/bin/env python
# -*- coding: utf8 -*-
# 系统库
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import os
import sys
import json
from json.decoder import JSONDecodeError
import time
import random
import hashlib
import math
import functools
import logging


# 第三方库
import six

# 内部库
from . import global_data

print_org = print


def print(*objects, **kwargs):
    """
    封装print方法，添加encoding
    """
    encoding = kwargs.get('encoding', 'utf-8')
    sep = six.ensure_str(kwargs.get('sep', ' '), encoding)
    end = six.ensure_str(kwargs.get('end', '\n'), encoding)
    file = kwargs.get('file', sys.stdout)
    new_objects = []
    for obj in objects:
        obj = six.ensure_str(obj, encoding) if isinstance(obj, (six.binary_type, six.text_type)) else obj
        new_objects.append(obj)
    return print_org(*new_objects, sep=sep, end=end, file=file)


def full_path(relative_path, start_dir=None):
    """
    以start_dir目录为起点，获取relative_path对应的完整路径
    start_dir默认为系统path路径列表第一位
    """
    if start_dir is None:
        start_dir = sys.path[0]
    start_dir = six.ensure_text(start_dir)
    relative_path = six.ensure_text(relative_path)
    res = os.path.join(start_dir, relative_path)
    res = os.path.normpath(res)
    res = six.ensure_binary(res)
    return res


def find_file(file_path, search_dir_list=None):
    """
    在搜索路径中搜索file_path，搜索路径默认为系统path
    """
    if search_dir_list is None:
        search_dir_list = sys.path
    for search_dir in search_dir_list:
        search_path = full_path(file_path, search_dir)
        if os.path.exists(search_path):
            return search_path
    raise ValueError('file not exists[%s]' % file_path)


def get_file_obj(file_obj, mode='r', default=None):
    """
    获取文件对象
    file_obj: 兼容文件对象、绝对路径、相对路径
    mode: 文件打开方式(file_obj为路径时适用)
    default: 失败时返回的默认值
    return: 文件对象, 文件是否需要关闭(file_obj为路径时适用)
    """
    raw_file_obj = file_obj
    need_close = False
    if isinstance(file_obj, (six.binary_type, six.text_type)):
        file_obj = open(find_file(file_obj), mode)
        need_close = True
    if not (hasattr(file_obj, 'read') or hasattr(file_obj, '__iter__')):
        file_obj = default
    if not (hasattr(file_obj, 'read') or hasattr(file_obj, '__iter__')):
        raise ValueError('cannot open file[%s]' % raw_file_obj)
    return file_obj, need_close


def build_log_str(log_action=None, **kwargs):
    """
    构建log字符串
    """

    ret = ''
    if not isinstance(kwargs, dict):
        return ret

    row = []
    if log_action is not None:
        row.append('%s[%s]' % ('log_action', log_action))
    log_id = -1
    if hasattr(global_data.thread_local_data, 'log_id'):
        log_id = global_data.thread_local_data.log_id
    row.append('%s[%s]' % ('log_id', log_id))
    for key, value in kwargs.items():
        if not isinstance(value, (six.text_type, six.binary_type)):
            value = json.dumps(value, ensure_ascii=False)
        value = six.ensure_text(value)
        row.append('%s[%s]' % (key, value))
    ret = ' '.join(row)
    ret = six.ensure_str(ret)

    return ret


def build_log_id():
    """
    生成log_id
    """
    return '%s%s' % (int(time.time()), random.randint(10000, 99999))


def get_md5(input_str, encoding='utf-8'):
    """
    计算字符串md5
    """
    md5_obj = hashlib.md5()
    md5_obj.update(six.ensure_binary(input_str, encoding=encoding))
    md5 = md5_obj.hexdigest()
    return md5


def get_file_md5(file_path):
    """
    计算文件md5
    """
    md5_obj = hashlib.md5()
    file_path = find_file(file_path)
    with open(file_path, 'rb') as file_obj:
        while True:
            data = file_obj.read(8192)
            if not data:
                break
            md5_obj.update(data)
    md5 = md5_obj.hexdigest()
    return md5


def sigmoid(x):
    """
    sigmoid函数
    使用math库实现，效率较低
    高性能版本可以使用：
        from scipy.special import expit
        return expit(x)
    """
    if isinstance(x, (six.binary_type, six.text_type)):
        x = float(x)
    return 1 / (1 + math.exp(-x))


def liner_normalize(x, min_num=0, max_num=sys.float_info.max):
    """
    线性归一化
    """
    if not max_num > min_num:
        raise Exception('max_num <= min_num when liner_normalize')
    x = max(min(x, max_num), min_num)
    return float((x - min_num) / (max_num - min_num))


def get_error_message(error):
    """
    获取错误消息和堆栈纪录
    逐步弃用，建议使用：logging.exception(error)
    """
    import traceback

    exc = six.ensure_text(traceback.format_exc())
    error_msg = getattr(error, 'message', '')
    if error_msg == '':
        error_msg = str(error)
    if error_msg == '':
        error_msg = repr(error)
    error_msg = six.ensure_text(error_msg)
    return error_msg, exc


def retry_func(retry_num=3, delay_seconds=1):
    """
    重试函数
    @param retry_num: 重试次数
    @param delay_seconds: 间隔秒数
    @return:
    """

    def decorator(func):
        """
        装饰器
        @param func:
        @return:
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """
            wrapper
            @param args:
            @param kwargs:
            @return:
            """
            for i in range(retry_num):
                try:
                    ret = func(*args, **kwargs)
                except Exception as error:
                    logging.exception(error)
                    time.sleep(delay_seconds)
                else:
                    return ret
            raise RuntimeError('max retry limit')

        return wrapper

    return decorator


def delay_qps_func(qps):
    """
    按照qps延迟函数
    @param qps:控制qps上限
    @return:
    """
    interval = 1.0 / qps

    def decorator(func):
        """
        装饰器
        @param func:
        @return:
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """
            wrapper
            @param args:
            @param kwargs:
            @return:
            """
            time_begin = time.time()
            try:
                ret = func(*args, **kwargs)
            except Exception as error:
                raise
            else:
                return ret
            finally:
                time_end = time.time()
                if time_end - time_begin > interval:
                    pass
                else:
                    time.sleep(interval - (time_end - time_begin))

        return wrapper

    return decorator


def time_log_func(level=logging.DEBUG):
    """
    耗时日志函数
    @param level:日志级别
    @return:
    """

    def decorator(func):
        """
        装饰器
        @param func:
        @return:
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """
            wrapper
            @param args:
            @param kwargs:
            @return:
            """
            time_begin = time.time()
            try:
                ret = func(*args, **kwargs)
            except Exception as error:
                raise
            else:
                return ret
            finally:
                time_end = time.time()
                logging.log(level, f'{func.__name__} costtime[{1000*(time_end-time_begin)}]ms')

        return wrapper

    return decorator


def try_json_decode_str(json_str):
    """
    尝试解析json字符串
    """
    if not isinstance(json_str, str):
        return json_str
    try:
        json_data = json.loads(json_str)
        return json_data
    except JSONDecodeError as error:
        pass
    return json_str


def try_json_decode(json_str):
    """
    尝试解析json字符串
    若解析结果为dict，递归尝试解析dict内所有json字符串
    """
    data = try_json_decode_str(json_str)
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = try_json_decode(value)
    return data
