#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import argparse
import logging

import six

from . import util
from .util import print


class StreamProcessor(object):
    """
    流式处理器基类，支持以标准I/O流形式处理数据，默认I/O编码utf-8
    """

    def __init__(self):
        """
        初始化
        """
        self.cmd_args = self.get_cmd_args()
        self.is_unit_test = self.cmd_args.get('unittest', False)
        self.input_stream = self.cmd_args.get('input_stream', sys.stdin)
        self.output_stream = self.cmd_args.get('output_stream', sys.stdout)
        self.separator = self.cmd_args.get('separator', '\t')
        self.encoding = self.cmd_args.get('encoding', 'utf-8')
        if self.cmd_args.get('skip_err_line', False):
            self.raise_line_error = True
            self.raise_row_error = True
        field_num = self.cmd_args['field_num']
        if isinstance(field_num, six.string_types) and field_num.isdigit():
            self.cmd_args['field_num'] = int(field_num)

    # 行处理异常是否中断流处理(False时跳过该行，但不输出)，需要raise_row_error=Ture时生效
    raise_line_error = False
    # 列处理异常是否中断行处理(False时输出列处理结果默认值: rows_result_default * fixed_column_width)
    raise_row_error = False
    # 列处理结果默认值
    rows_result_default = '-'
    # 输出列宽，结果将padding&裁剪至固定列宽，0表示不调整
    fixed_column_width = 1
    # 是否保留原始输入列
    keep_input_rows = True
    # 输出转义\t、\n
    output_convert = True

    def _output_convertor(self, text: str) -> str:
        return text.replace('\n', r'\n').replace('\t', r'\t') if isinstance(text, six.string_types) else text

    def _before_process(self, *args, **kwargs):
        """
        前置钩子
        """
        pass

    def _after_process(self, *args, **kwargs):
        """
        后置钩子
        """
        pass

    def _get_rows_from_line(self, line, *args, **kwargs):
        """
        从line获取rows
        """
        if isinstance(line, (list, tuple)):
            return line
        line = six.ensure_text(line, encoding=self.encoding).strip('\n')
        rows = line.split(self.separator)
        return rows

    def rows_process(self, rows, *args, **kwargs):
        """
        处理输入流一行的各列数据，返回结果将输出至输出流
        rows: 接收输入流一行的各列数据
        *args, **kwargs: 接受其余参数
        """
        raise NotImplementedError('StreamProcessor基类方法，需子类继承StreamProcessor后实现')

    def line_process(self, line, *args, **kwargs):
        """
        输入流一行数据才分为列数据，调用rows_process()处理，输出至输出流
        line: 接收输入流一行数据
        *args, **kwargs: 接受其余参数
        """
        if not line:
            raise ValueError(f'empty line[{line}]')
        self.line_count += 1
        rows = self._get_rows_from_line(line, *args, **kwargs)
        try:
            res = self.rows_process(rows, *args, **kwargs)
        except Exception as error:
            logging.exception(f'rows:{rows} error[{error}]')
            if self.raise_row_error:
                raise
            else:
                res = []
        if res is None:
            return
        if not isinstance(res, (list, tuple)):
            res = [res]
        if self.fixed_column_width > 0:
            if len(res) != self.fixed_column_width:
                logging.debug(f'padding & fix result width from[{len(res)}] to[{self.fixed_column_width}]')
            temp = list(res) + [self.rows_result_default] * self.fixed_column_width
            res = temp[: self.fixed_column_width]
        output_rows = rows if self.keep_input_rows else []
        output_rows.extend(res)
        if self.output_convert:
            output_rows = map(self._output_convertor, output_rows)
        print(*output_rows, sep=self.separator, encoding=self.encoding, file=self.output_stream)

    def stream_process(self, *args, **kwargs):
        """
        流式处理
        从输入流读取数据，调用line_process()方法进行行处理
        *args, **kwargs: 接收其余参数，透传至内部处理方法
        """
        close_file_list = []
        if self.is_unit_test:
            self.input_stream = self.unittest_text_list
            self.output_stream = sys.stdout
        else:
            self.input_stream, close_input = util.get_file_obj(self.input_stream, 'r', sys.stdin)
            if close_input:
                close_file_list.append(self.input_stream)
            self.output_stream, close_output = util.get_file_obj(self.output_stream, 'w', sys.stdout)
            if close_output:
                close_file_list.append(self.output_stream)

        self._before_process(*args, **kwargs)
        self.line_count = 0
        for line in self.input_stream:
            try:
                self.line_process(line, *args, **kwargs)
            except Exception as error:
                logging.exception(f'line_no[{self.line_count}] line:{line} error[{error}]')
                if self.raise_line_error:
                    raise
                else:
                    continue
        self._after_process(*args, **kwargs)
        for file_to_close in close_file_list:
            file_to_close.close()

    def _add_cmd_args(self, parser):
        """
        添加命令行参数，子类可覆盖该方法并调用parser.add_argument()添加参数
        """
        pass

    def get_cmd_args(self, return_dict=True):
        """
        获取并转换命令行参数
        """
        parser = argparse.ArgumentParser(description='stream processor')
        parser.add_argument('-input', '--input_stream', default=sys.stdin, type=argparse.FileType('r'), help='input file/stream')
        parser.add_argument('-output' '--output_stream', default=sys.stdout, type=argparse.FileType('w'), help='output file/stream')
        parser.add_argument('-sep', '--separator', default='\t', help=r'i/o rows separator, \t default')
        parser.add_argument('-ut', '--unittest', action='store_true', help='unit test')
        parser.add_argument('-f', '--field_num', default=1, type=str, help='input content row number, 1 default')
        parser.add_argument('--skip_err_line', action='store_true', help='True: skip error line, False[default]: output "-"')
        self._add_cmd_args(parser)

        args = parser.parse_args()
        res = args.__dict__ if return_dict else args
        return res

    @property
    def unittest_text_list(self):
        """
        提供单元测试数据
        """
        return [r'hello world', r'单元测试', r'unittest_text_list用于提供单元测试数据，子类可覆盖该方法提供测试数据']

    def unittest(self, *args, **kwargs):
        """
        单元测试
        """
        text_list = [six.ensure_binary(text, encoding='utf-8') for text in self.unittest_text_list]
        self.stream_process(text_list, *args, **kwargs)


class KVOutputStreamProcessor(StreamProcessor):
    """
    k/v输出类流处理器基类。该类处理共性：
    * 结果输出key/value dict：-pk/--print_key 打印key，否则打印value
    * 可定制化输出全部或部分key，-k/--output_keys 指定输出key
    * 全部key输出不定长，部分key输出定长
    """

    fixed_column_width = 0

    def __init__(self):
        super().__init__()

    def kv_rows_process(rows, *objects, **kwargs):
        """
        处理输入流一行的各列数据，得到dict结果
        rows: 接收输入流一行的各列数据
        *args, **kwargs: 接受其余参数
        """
        raise NotImplementedError('KVOutputStreamProcessor基类方法，需子类继承KVOutputStreamProcessor后实现')

    def rows_process(self, rows, *objects, **kwargs):
        """
        处理输入流一行的各列数据，返回结果将输出至输出流
        rows: 接收输入流一行的各列数据
        *args, **kwargs: 接受其余参数
        """
        output_keys = self.cmd_args.get('output_keys', None)
        print_key = self.cmd_args.get('print_key', False)
        output = self.kv_rows_process(rows, *objects, **kwargs)
        if output_keys:
            output = {key: output.get(key, self.rows_result_default) for key in output_keys}
            self.fixed_column_width = len(output_keys)
        if print_key:
            res = [f'{key}({type(value).__name__}):{value}' for key, value in output.items()]
        else:
            res = list(output.values())
        return res

    def get_cmd_args(self, return_dict=True):
        """
        获取并转换命令行参数
        """
        parser = argparse.ArgumentParser(description='stream processor')
        parser.add_argument('-input', '--input_stream', default=sys.stdin, type=argparse.FileType('r'), help='input file/stream')
        parser.add_argument('-output' '--output_stream', default=sys.stdout, type=argparse.FileType('w'), help='output file/stream')
        parser.add_argument('-sep', '--separator', default='\t', help=r'i/o rows separator, \t default')
        parser.add_argument('-ut', '--unittest', action='store_true', help='unit test')
        parser.add_argument('-f', '--field_num', default=1, type=str, help='input content row number, 1 default')
        parser.add_argument('--skip_err_line', action='store_true', help='True: skip error line, False[default]: output "-"')
        parser.add_argument('-k', '--output_keys', action='append', help='output keys(append), all keys default')
        parser.add_argument('-pk', '--print_key', action='store_true', help='whether to print key(<key:value> instead <value> only)')
        self._add_cmd_args(parser)

        args = parser.parse_args()
        res = args.__dict__ if return_dict else args
        return res
