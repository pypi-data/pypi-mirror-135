#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
@Time    : 2018-06-06
@Author  : RAMBOO
@Desc    : txt转xls 基于pandas库
"""

# 系统库
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# 第三方库
import sys
import six
import pandas
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

# 内部库
from ramboo_tools.stream_processor import StreamProcessor


class TextToXlsStreamProcessor(StreamProcessor):
    def __init__(self):
        super().__init__()
        self.output_excel = self.cmd_args.get('output_excel')
        assert self.output_excel, 'require -o/--output_excel option'
        if self.output_excel == sys.stdout:
            raise TypeError('-o/--output_excel param must be a file name')
        if '.xls' not in self.output_excel.name:
            raise ValueError('output excel file name must end with .xls(x)')
        self.column_name_list = self.cmd_args.get('column_name', [])
        self.data_list = []

    def _add_cmd_args(self, parser):
        import argparse

        parser.add_argument('-o', '--output_excel', required=True, type=argparse.FileType('w'), help='output file')
        parser.add_argument('-th', '--table_head', action='store_true', default=False, help='whether to use the 1st line as table head')
        parser.add_argument('-c', '--column_name', action='append', help='add table header column names (append), overwrite -th/--table_head option')

    def line_process(self, line, *args, **kwargs):
        line = ILLEGAL_CHARACTERS_RE.sub('', line)
        return super().line_process(line, *args, **kwargs)

    def rows_process(self, rows=None, *objects, **kwargs):
        contain_table_head = self.cmd_args.get('table_head', False)
        if self.line_count == 1 and contain_table_head and self.column_name_list is None:
            self.column_name_list = rows
            return None
        if six.PY2:
            rows = list(map(six.ensure_str, rows))
        self.data_list.append(rows)
        return None

    def _after_process(self, *objects, **kwargs):
        df = pandas.DataFrame(self.data_list, columns=self.column_name_list)
        df.to_excel(self.output_excel.name, sheet_name='Data', index=False)


def main():
    TextToXlsStreamProcessor().stream_process()


if __name__ == '__main__':
    main()
