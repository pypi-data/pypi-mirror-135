#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Copyright (c) Baidu.com, Inc. All Rights Reserved
@Time    : 2019-09-06
@Author  : yuanhui03
@Desc    : 文本匹配，支持多词匹配
"""

# 系统库
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import sys
import json

# 内部库
from ramboo_tools.util import print
from ramboo_tools import global_data
from ramboo_tools.stream_processor import StreamProcessor
from ramboo_tools import dictmatch
from ramboo_tools import load_dict


class TextMatch(StreamProcessor):
    """文本匹配，支持多词匹配，基于dictmatch"""

    def __init__(self, dict_path, subword_seperator='&', quick_match=False):
        self.subword_seperator = subword_seperator
        self.quick_match = quick_match
        self.dm = dictmatch.DictMatch()
        keywords = load_dict.load_list_dict(dict_path)
        for keyword in keywords:
            subwords = keyword.split(self.subword_seperator)
            for subword in subwords:
                # 存储subword->keyword映射关系的list
                keyword_list = self.dm.get_ext_info_by_key(subword, [])
                keyword_list.append(keyword)
                self.dm.add(subword, ext_info=keyword_list)

    def rows_process(self, rows=None, *objects, **kwargs):
        """
        处理输入流的一行数据，将会被stream_process()方法调用，返回结果将输出至输出流
        rows: 接收输入流的一行数据
        *objects, **kwargs: 接受其余参数
        """
        res = None
        content_row_num = kwargs.get('content_row_num', 1)
        output_line = kwargs.get('output_line', 'match')
        if output_line not in ['all', 'match']:
            raise ValueError('output_line error:', output_line)
        content = rows[content_row_num - 1]
        match_res = self.dm.find(content)
        if not match_res and output_line == 'match':
            return res
        if global_data.is_debug:
            print('match_res:', json.dumps(match_res, ensure_ascii=False))
        # 收集所有有可能匹配的keyword
        check_keyword_list = []
        for subword, info in match_res.items():
            check_keyword_list.extend(info['ext_info'])
        # 去重（快速模式不需要，match任意一个就完成）
        if not self.quick_match:
            check_keyword_list = list(set(check_keyword_list))
        if global_data.is_debug:
            print('check_keyword_list:', ' / '.join(check_keyword_list))
        # 收集成功匹配的keyword
        match_keyword_list = []
        for check_keyword in check_keyword_list:
            is_match = True
            if self.subword_seperator not in check_keyword:
                # 单词匹配，直接匹配成功
                pass
            else:
                # 多词匹配，需检查其他subword均存在匹配结果才算匹配成功，否则匹配失败
                check_subword_list = check_keyword.split(self.subword_seperator)
                for check_subword in check_subword_list:
                    if check_subword not in match_res:
                        is_match = False
                        break
            if is_match:
                match_keyword_list.append(check_keyword)
                if self.quick_match:
                    # 快速匹配模式，只要有一个keyword match成功就够了
                    break
        if not match_keyword_list and output_line == 'match':
            return res
        res = ','.join(match_keyword_list)
        if global_data.is_debug:
            print('match_keyword_list:', ' / '.join(match_keyword_list))
        return res

    def get_unittest_text_list(self):
        """
        提供单元测试数据
        """
        return [
            # 'hello world',
            # 'hello hello world',
            # 'world',
            # '11111',
            # '22222',
            # '123123',
            '111222',
            '111333',
        ]


def main():
    """
    主程序
    """
    import argparse

    parser = argparse.ArgumentParser(description='文本匹配，支持多词匹配')
    parser.add_argument('-i', '--input', default=sys.stdin, help='input file name')
    parser.add_argument('-o', '--output', default=sys.stdout, help='output file name')
    parser.add_argument('-ut', '--unittest', action='store_true', help='unit test')
    parser.add_argument('-s', '--separator', default='\t', help=r'i/o stream separator, \t default')
    parser.add_argument('-ss', '--subword_seperator', default='&', help='subword seperator, & default')
    parser.add_argument('-crn', '--content_row_num', default=1, help='content row num, start at 1')
    parser.add_argument('-quick', '--quick_match', action='store_true', help='quick match mode, display 1st match keyword only')
    parser.add_argument('-d', '--dict', help='keyword dict, 1 keyword per line')
    parser.add_argument('-ol', '--output_line', default='match', help=('match[default] : output only match lines; all : output all lines'))
    args = parser.parse_args()

    textMatchObj = TextMatch(dict_path=args.dict, subword_seperator=args.subword_seperator, quick_match=args.quick_match)

    if args.unittest:
        textMatchObj.unittest()
    else:
        textMatchObj.stream_process(
            args.input,
            args.output,
            separator=args.separator,
            keep_input=True,
            content_row_num=int(args.content_row_num),
            output_line=args.output_line,
        )


if __name__ == '__main__':
    main()
