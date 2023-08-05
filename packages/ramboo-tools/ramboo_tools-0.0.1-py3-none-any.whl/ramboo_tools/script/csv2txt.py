#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
@Time    : 2018-08-02
@Author  : RAMBOO
@Desc    : csv转txt 基于csv库
"""

# 系统库
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import io

# 第三方库
import six
import csv

# 内部库
from ramboo_tools.stream_processor import StreamProcessor


class CsvToTextStreamProcessor(StreamProcessor):
    # 关闭输入保留
    keep_input_rows = False
    # 关闭固定列宽
    fixed_column_width = -1

    def __init__(self):
        super().__init__()
        csv_delimiter = self.cmd_args.get('csv_delimiter', ',')
        csv_encoding = self.cmd_args.get('csv_encoding', 'utf-8')
        dialect = self.cmd_args.get('format', 'unix')
        if dialect == 'auto':
            dialect = csv.Sniffer().sniff(self.input_stream.read(1024))
            self.input_stream.seek(0)
        self.input_stream = csv.reader(io.TextIOWrapper(self.input_stream.buffer, encoding=csv_encoding), delimiter=csv_delimiter, dialect=dialect)

    def _add_cmd_args(self, parser):
        parser.add_argument('-d', '--csv_delimiter', default=',', type=str, help='input csv delimiter')
        parser.add_argument('-e', '--csv_encoding', default='utf-8', type=str, help='input csv encoding, utf-8 defalut')
        parser.add_argument(
            '--format',
            default='unix',
            type=str,
            help='csv format: ' + '/'.join(csv.list_dialects() + ['auto']) + ', unix default. "auto" only available using file input',
        )

    @staticmethod
    def _convert(text):
        for str1, str2 in [
            ('\\', '\\\\'),
            ('\t', r'\t'),
            ('\r\n', r'\n'),
            ('\n', r'\n'),
        ]:
            text = text.replace(str1, str2)
        return text

    def rows_process(self, rows=None, *objects, **kwargs):
        rows = list(map(self._convert, rows))
        rows = list(map(six.ensure_text, rows))
        return rows


def main():
    CsvToTextStreamProcessor().stream_process()


if __name__ == '__main__':
    main()
