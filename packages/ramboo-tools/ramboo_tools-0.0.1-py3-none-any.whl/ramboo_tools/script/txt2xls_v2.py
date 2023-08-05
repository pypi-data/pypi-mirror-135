#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Copyright (c) Baidu.com, Inc. All Rights Reserved
@Time    : 2018-06-06
@Author  : yuanhui03
@Desc    : txt转xls 使用pandas库实现
"""

# 系统库
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import sys

# 第三方库
import pandas
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

# 内部库
from feed_antispam_lib import util


def stream_process(input_stream=None, output_stream=None, separator='\t',
                   column_name_list=None, table_head=False, log_stream=None):
    """
    流式处理
    """
    input_stream, close_input = util.get_file_obj(input_stream, 'r', sys.stdin)
    output_stream, close_output = util.get_file_obj(output_stream, 'w', sys.stdout)
    log_stream, close_log = util.get_file_obj(log_stream, 'w', sys.stderr)

    data_list = []
    line_count = 0
    for line in input_stream:
        try:
            line = line.decode('utf-8', 'ignore').strip('\n')
            line = ILLEGAL_CHARACTERS_RE.sub('', line)
            if line == '':
                continue
            line_count += 1
            rows = line.split(separator)
            if line_count == 1 and table_head and column_name_list is None:
                column_name_list = rows
                continue
            data_list.append([row.encode('utf-8', 'ignore') for row in rows])
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
    df = pandas.DataFrame(data_list, columns=column_name_list)
    df.to_excel(output_stream, sheet_name='Data', index=False)

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
        '。。	0	1.0',
        '可能暗访领导提前找的临时工，故弄玄虚	0	0.990234',
        '做戏而已。康麻子祭拜明孝陵一个道理。	0	0.998047',
        '这么厚的轻质砖要打断也不容易。 ===>>>签名：	0	0.996094',
        '想当年常香玉老前辈，为了抗美援朝，捐飞机✈️，现在这是怎么了！	0	0.996094',
        '[笑哭]博士的魔法盾一出来我就笑了 ===>>>签名：想要被世界温柔以待，就要先学会温柔对待你所处的世界^_^	0	0.986328',
        '滚你妈火星上说去，来地球干嘛	0	0.998047',
        '飞行员可能要上厕所大便[坏笑][大笑]	0	0.998047',
        '4864如果能被天佑以外的另一个人用，佑家军直播吃屎，	0	0.990234',
        '样品。打一弹就失望了。	0	1.0',
    ]
    text_list = [text.encode('utf-8') for text in text_list]
    stream_process(text_list, column_name_list=['content', 'predict', 'probility'])


def main():
    """
    主程序
    """
    import argparse
    parser = argparse.ArgumentParser(description='txt转xls 使用panda库实现')
    parser.add_argument('-i', '--input', default=sys.stdin, help='input file name')
    parser.add_argument('-o', '--output', default=sys.stdout, help='output file name')
    parser.add_argument('-ut', '--unittest', action='store_true', help='unit test')
    parser.add_argument('-s', '--separator', default='\t', help='i/o stream separator, \\t default')
    parser.add_argument('-th', '--table_head', action='store_true', default=False, help='whether to use the 1st line as table head')
    parser.add_argument('-c', '--column_name', action='append', help='column names, overwrite `table_head`')
    args = parser.parse_args()

    if args.unittest:
        unittest()
    else:
        stream_process(args.input, args.output, args.separator, args.column_name, args.table_head)


if __name__ == '__main__':
    main()
