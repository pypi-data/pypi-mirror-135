#!/usr/bin/env python
# -*- coding: utf8 -*-

from ramboo_tools.stream_processor import StreamProcessor
from ramboo_tools.pretty_printer import pp


class PrettyPrintStreamProcessor(StreamProcessor):
    """
    优雅的打印对象，对括号进行多行展开
    """

    def __init__(self):
        super().__init__()
        self.field_num_separator = self.cmd_args.get('field_num_separator', ',')

    def rows_process(self, rows=None, *objects, **kwargs):
        field_num_list = list(map(int, str(self.cmd_args.get('field_num', '1')).split(self.field_num_separator)))
        not_fold = self.cmd_args.get('not_fold', True)
        fold = not not_fold
        format_str = self.cmd_args.get('format_str', True)
        keep_str = not format_str
        for field_num in field_num_list:
            content = str(rows[field_num - 1])
            rows[field_num - 1] = pp(content, fold=fold, keep_str=keep_str)
        print(*rows, sep=self.separator, file=self.output_stream)
        return None

    def _add_cmd_args(self, parser):
        """
        添加命令行参数，子类可覆盖该方法并调用parser.add_argument()添加参数
        """
        parser.add_argument(
            '-s', '--field_num_separator', default=',', type=str, help='separator for -f/--field_num, "," default (i.e: "," for "1,2,3")'
        )
        parser.add_argument('--not_fold', action='store_true', help='wether to fold content over 30 lines')
        parser.add_argument('--format_str', action='store_true', help='wether to format str in content')


def main():
    PrettyPrintStreamProcessor().stream_process()


if __name__ == '__main__':
    main()
