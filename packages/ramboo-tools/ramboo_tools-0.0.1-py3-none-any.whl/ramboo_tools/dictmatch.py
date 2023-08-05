#!/usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from . import c_dmsearch


class DictMatch(object):
    """
    DictMatch
    """

    def __init__(self):
        """
        初始化
        """
        self.__dict_handle = c_dmsearch.create()
        if self.__dict_handle == -1:
            raise Exception('Create dict fail! ret=%d' % self.__dict_handle)
        self.__ext_info_map = {}

    def get_ext_info_by_key(self, key, default_value=None):
        """
        通过关键词获取扩展信息
        注：必须统一key编码，目前统一为py2的unicode
        """
        if isinstance(key, str):
            key = key.decode('utf-8')
        return self.__ext_info_map.get(key, default_value)

    def set_ext_info_by_key(self, key, ext_info):
        """
        通过关键词写入扩展信息
        注：必须统一key编码，目前统一为py2的unicode
        """
        if isinstance(key, str):
            key = key.decode('utf-8')
        self.__ext_info_map[key] = ext_info

    def add(self, keyword, ext_num=None, ext_info=None):
        """
        添加关键词
        keyword: 关键词
        ext_num: 扩展信息（一个int），dmsearch原生支持
        ext_info: 扩展信息（任意格式），自行存储，调用find()时取出
        """
        if ext_info is not None:
            self.set_ext_info_by_key(keyword, ext_info)
        if isinstance(keyword, unicode):
            keyword = keyword.encode('utf-8')
        if ext_num is None:
            return c_dmsearch.add(self.__dict_handle, keyword)
        else:
            return c_dmsearch.add(self.__dict_handle, keyword, ext_num)

    def save(self, output_filename):
        """
        保存关键词
        """
        return c_dmsearch.save(self.__dict_handle, output_filename)

    def load(self, filename):
        """
        读取关键词
        """
        return c_dmsearch.load(self.__dict_handle, filename)

    def find(self, text, output_type='dict', fmm=True):
        """
        查询关键词
        c_dmsearch.find()返回结果中每个元素包含：
        res[0]: 匹配到的关键词
        res[1]: 匹配起始位置(字节长度)
        res[2]: 匹配长度(字节长度)
        res[3]: 扩展信息(一个int)，add()时带入
        """
        if isinstance(text, unicode):
            text = text.encode('utf-8')
        if not fmm:
            dm_res = c_dmsearch.find(self.__dict_handle, text)
        else:
            dm_res = []
            tmp_dm_res = c_dmsearch.find(self.__dict_handle, text)
            lst_spos = lst_len = None
            for dm_res_item in tmp_dm_res:
                if lst_spos is not None:
                    if dm_res_item[1] == lst_spos and dm_res_item[2] > lst_len:
                        dm_res.pop()
                    elif dm_res_item[1] < lst_spos + lst_len:
                        continue
                dm_res.append(dm_res_item)
                lst_spos = dm_res_item[1]
                lst_len = dm_res_item[2]
        if output_type == 'dict':
            res = {}
            for dm_res_item in dm_res:
                text = dm_res_item[0]
                text_unicode = text.decode('utf-8')
                res[text_unicode] = {
                    'start': dm_res_item[1],
                    'text_len': dm_res_item[2],
                    'ext_num': dm_res_item[3],
                    'ext_info': self.get_ext_info_by_key(text, None),
                }
        else:
            res = []
            for dm_res_item in dm_res:
                item = list(dm_res_item)
                item.append(self.get_ext_info_by_key(dm_res_item[0], None))
                res.append(item)
        return res
