#!/usr/bin/env python
# -*- coding: utf8 -*-

# 系统库
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import sys
import os
import re

# 内部库
from . import util
from . import dictmatch


def load_dict(dict_file, dict_type='list'):
    """
    读取词典
    """
    if dict_type == 'list' or dict_type == 'pattern':
        dict_obj = []
    elif dict_type == 'multi_key_map' or dict_type == 'single_key_map':
        dict_obj = {}
    elif dict_type == 'dm':
        dict_obj = dictmatch.DictMatch()
    file_obj, need_close = util.get_file_obj(dict_file)
    for line in file_obj:
        line = line.decode('utf8', 'ignore').strip('\n')
        if len(line) == 0:
            continue
        if line.find('#') == 0:
            # 该行为注释
            continue
        if dict_type == 'list':
            # list词典，加载至list对象
            dict_obj.append(line)
        elif dict_type == 'pattern':
            # 正则词典，加载至正则对象list
            dict_obj.append(re.compile(line))
        elif dict_type == 'multi_key_map':
            # 映射词典（key \t value），加载至dict对象，key重复时value为set集合
            rows = line.split('\t')
            key = rows[0]
            value = rows[1] if len(rows) > 1 else ''
            if key not in dict_obj:
                dict_obj[key] = set()
            dict_obj[key].add(value)
        elif dict_type == 'single_key_map':
            # 单key映射词典（key \t value），加载至dict对象
            key, value = line.split('\t')
            dict_obj[key] = value
        elif dict_type == 'dm':
            # 多模匹配词典，加载至dict_match
            # 兼容\t分割格式，只取第一列
            rows = line.split('\t')
            content = rows[0]
            ext_info = rows[1] if len(rows) > 1 else ''
            dict_obj.add(content.encode('utf-8'), ext_info=ext_info)
    if need_close:
        file_obj.close()
    return dict_obj


def load_match_dict(dict_file):
    """
    读取多模匹配词典，加载至dict_match
    """
    return load_dict(dict_file, 'dm')


def load_pattern_dict(dict_file):
    """
    读取正则词典，加载至正则对象
    """
    return load_dict(dict_file, 'pattern')


def load_list_dict(dict_file):
    """
    读取词典，加载至list
    """
    return load_dict(dict_file, 'list')


def load_map_dict(dict_file, key_type='multi'):
    """
    读取词典（两列 key \t value），加载至dict。
    key_type='multi' 同个key的value重复时加载至一个该key下的set。
    key_type='single' key只会出现一次
    """
    res = None
    if key_type == 'multi':
        res = load_dict(dict_file, 'multi_key_map')
    elif key_type == 'single':
        res = load_dict(dict_file, 'single_key_map')
    return res
