#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Copyright (c) Baidu.com, Inc. All Rights Reserved
@Time    : 2018-05-30
@Author  : yuanhui03
@Desc    : 文本转火星文
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import sys

# 内部库
from feed_antispam_lib import util
from .fzlftHuoxingDao import get_huoxing_text_list

# 重复请求次数，每次生成4条火星文
REPEAT_TIMES_LIMIT = 25


def stream_process(input_stream=None, output_stream=None, separator='\t', log_stream=None):
    """
    流式处理
    """
    input_stream, close_input = util.get_file_obj(input_stream, 'r', sys.stdin)
    output_stream, close_output = util.get_file_obj(output_stream, 'w', sys.stdout)
    log_stream, close_log = util.get_file_obj(log_stream, 'w', sys.stderr)

    line_count = 0
    for line in input_stream:
        try:
            line = line.decode('utf-8', 'ignore').strip('\n')
            if line == '':
                continue
            line_count += 1
            # if line_count == 1:
            #     # 跳过表头
            #     continue
            rows = line.split(separator)
            comment = rows[0]
            for repeat_time in range(REPEAT_TIMES_LIMIT):
                huoxing_text_list = get_huoxing_text_list(comment)
                for huoxing_text in huoxing_text_list:
                    output_rows = [comment, huoxing_text]
                    output_rows.extend(rows[1:])
                    output_line = separator.join(output_rows)
                    print(output_line.encode('utf-8'), file=output_stream)
            if line_count % 10000 == 0:
                print("line[%s] finish" % line_count, file=log_stream)
        except Exception as e:
            import traceback
            output_line = "line_no[%s] line[%s] ERROR:" % (line_count, line)
            print(output_line.encode('utf-8'), file=log_stream)
            print(traceback.format_exc(), file=log_stream)
            continue
        else:
            pass
        finally:
            pass
    if close_input:
        input_stream.close()
    if close_output:
        output_stream.close()
    if close_log:
        log_stream.close()


def unittest():
    """
    单元测试
    """
    text_list = [
        '加QQ加微信1234567890',
        '关注公众号bilibili',
        '联系电话1351234568',
    ]
    text_list = [text.encode('utf-8') for text in text_list]
    stream_process(text_list)


def main():
    """
    主程序
    """
    import argparse
    parser = argparse.ArgumentParser(description='生成火星文')
    parser.add_argument('-i', '--input', default=sys.stdin, help='input file name')
    parser.add_argument('-o', '--output', default=sys.stdout, help='output file name')
    parser.add_argument('-s', '--separator', default='\t', help='i/o stream separator, \\t default')
    parser.add_argument('-ut', '--unittest', action='store_true', help='unit test')
    args = parser.parse_args()

    if args.unittest:
        unittest()
    else:
        stream_process(args.input, args.output, args.separator)

if __name__ == '__main__':
    main()
