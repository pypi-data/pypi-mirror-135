# -*- coding: utf-8 -*-
# coding=utf-8

"""
全局变量
"""

# 系统库
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import os
import threading

# debug开关
is_debug = int(os.environ.get('DEBUG', 0))
# 线程local数据，在线程内共享，在各线程间隔离
thread_local_data = None


def _init_thread_data():
    """
    线程内全局变量初始化
    """
    global thread_local_data
    # 创建全局ThreadLocal对象
    if thread_local_data is None:
        thread_local_data = threading.local()


def init():
    """
    全局变量初始化
    """
    _init_thread_data()
