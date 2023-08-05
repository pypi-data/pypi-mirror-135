#!/usr/bin/env python
# -*- coding: utf8 -*-
# 系统库
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import sys
import argparse

# 第三方库
import six
import pandas


class XlsToTextStreamProcessor(object):
    @staticmethod
    def convert(text):
        for str1, str2 in [
            ('\\', '\\\\'),
            ('\t', r'\t'),
            ('\r\n', r'\n'),
            ('\n', r'\n'),
        ]:
            text = str(text).replace(str1, str2)
        return text

    def process(self, *objects, **kwargs):
        parser = argparse.ArgumentParser(description='stream processor')
        parser.add_argument('-i', '--input_excel', required=True, type=argparse.FileType('r'), help='input excel file')
        parser.add_argument('-output' '--output_stream', default=sys.stdout, type=argparse.FileType('w'), help='output file/stream')
        parser.add_argument('-sep', '--seperator', default='\t', help=r'i/o rows seperator, \t default')
        args = parser.parse_args()
        self.cmd_args = args.__dict__
        self.input_excel = self.cmd_args.get('input_excel', None)
        if not self.input_excel:
            raise ValueError('need -o input_excel')
        if self.input_excel == sys.stdin:
            raise TypeError('--input_excel must be file')
        if '.xls' not in self.input_excel.name:
            raise ValueError('input excel file name must be xxx.xls(x)')
        data_frame = pandas.read_excel(self.input_excel.name, header=None)
        data_frame.fillna('', inplace=True)
        data_list = data_frame.to_records(index=False)
        for rows in data_list:
            rows = list(map(six.ensure_text, map(self.convert, rows)))
            print(*rows, sep=self.cmd_args.get('seperator', '\t'), file=self.cmd_args.get('output', sys.stdout))


def main():
    XlsToTextStreamProcessor().process()


if __name__ == '__main__':
    main()
