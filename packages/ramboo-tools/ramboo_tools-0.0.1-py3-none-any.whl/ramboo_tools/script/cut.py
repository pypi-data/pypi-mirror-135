#!/usr/bin/env python
# -*- coding: utf8 -*-

from ramboo_tools.stream_processor import StreamProcessor


class CutStreamProcessor(StreamProcessor):
    """
    实现linux cut命令的-d与-f参数功能，加强了-d，分隔符支持多个字符

    -d, --delimiter=DELIM   use DELIM instead of TAB for field delimiter
    -f, --fields=LIST       select only these fields;  also print any line
                            that contains no delimiter character, unless
                            the -s option is specified
    Use one, and only one of -b, -c or -f.  Each LIST is made up of one
    range, or many ranges separated by commas.  Selected input is written
    in the same order that it is read, and is written exactly once.
    Each range is one of:

    N     N'th byte, character or field, counted from 1
    N-    from N'th byte, character or field, to end of line
    N-M   from N'th to M'th (included) byte, character or field
    -M    from first to M'th (included) byte, character or field
    """

    fixed_column_width = 0
    keep_input_rows = False

    def __init__(self):
        super().__init__()
        self.separator = self.cmd_args.get('delimiter')
        if self.separator is None:
            self.separator = self.cmd_args.get('separator', '\t')
        field_num_raw = self.cmd_args.get('field_num', '1')
        field_num_set = set()
        field_num_before = float('-inf')
        field_num_after = float('inf')
        for field_num_str in str(field_num_raw).split(','):
            if field_num_str.isdigit():
                field_num_set.add(int(field_num_str))
            elif '-' in field_num_str:
                temp = field_num_str.split('-')
                assert len(temp) == 2, f'invalid decreasing range: [{field_num_str}], shoud be something like "...,a-b,..."'
                start, end = temp
                if start == '':
                    assert end.isdigit(), f'invalid field value: [{end}]'
                    field_num_before = max(field_num_before, int(end))
                    continue
                elif end == '':
                    assert start.isdigit(), f'invalid field value: [{start}]'
                    field_num_after = min(field_num_after, int(start))
                    continue
                else:
                    assert start.isdigit() and end.isdigit(), f'invalid field value: [{field_num_str}]'
                    start = int(start)
                    end = int(end)
                    assert start < end, f'invalid decreasing range: [{field_num_str}]'
                    for idx in range(start, end):
                        field_num_set.add(idx)
            else:
                raise RuntimeError(f'invalid field value: [{field_num_str}]')
        self.field_num_set = field_num_set
        self.field_num_before = field_num_before
        self.field_num_after = field_num_after

    def rows_process(self, rows=None, *objects, **kwargs):
        res = []
        for idx, row in enumerate(rows):
            field_num = idx + 1
            if field_num <= self.field_num_before or field_num >= self.field_num_after or field_num in self.field_num_set:
                res.append(row)
        return res

    def _add_cmd_args(self, parser):
        """
        添加命令行参数，子类可覆盖该方法并调用parser.add_argument()添加参数
        """
        parser.add_argument('-d', '--delimiter', type=str, help='separator of rows, same as -sep --seperator')


def main():
    CutStreamProcessor().stream_process()


if __name__ == '__main__':
    main()
