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
import csv

# 内部库
from ramboo_tools.stream_processor import StreamProcessor


class TextToCsvStreamProcessor(StreamProcessor):
    def __init__(self):
        super().__init__()
        csv_delimiter = self.cmd_args.get('csv_delimiter', ',')
        csv_encoding = self.cmd_args.get('csv_encoding', 'utf-8')
        dialect = self.cmd_args.get('format', 'unix')
        self.csv_writer = csv.writer(io.TextIOWrapper(self.output_stream.buffer, encoding=csv_encoding), delimiter=csv_delimiter, dialect=dialect)

    keep_input_rows = False

    def _add_cmd_args(self, parser):
        parser.add_argument('-d', '--csv_delimiter', default=',', type=str, help='input csv delimiter')
        parser.add_argument('-e', '--csv_encoding', default='utf-8', type=str, help='input csv encoding, gbk defalut')
        parser.add_argument(
            '--format',
            default='unix',
            type=str,
            help='csv format: ' + '/'.join(csv.list_dialects() + ['auto']) + ', unix default. ' '"auto" only available using file input',
        )
        parser.add_argument('-c', '--column_name', action='append', help='add table header column names (append)')

    def _before_process(self, *objects, **kwargs):
        header = self.cmd_args.get('column_name')
        if header:
            self.csv_writer.writerow(header)

    def rows_process(self, rows, *objects, **kwargs):
        self.csv_writer.writerow(rows)
        return None


def main():
    TextToCsvStreamProcessor().stream_process()


if __name__ == '__main__':
    main()
