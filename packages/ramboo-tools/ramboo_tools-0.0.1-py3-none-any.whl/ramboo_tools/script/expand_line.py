#!/usr/bin/env python
# -*- coding: utf8 -*-

from ramboo_tools.stream_processor import StreamProcessor


class ExpandLineStreamProcessor(StreamProcessor):
    """
    多行展开：
    before:
        1\ta,b,c
    after:
        1\ta
        1\tb
        1\tc
    """

    def __init__(self):
        super().__init__()
        self.expand_separator = self.cmd_args.get('expand_separator', ',')
        self.keep_empty_line = self.cmd_args.get('keep_empty_line', False)

    def rows_process(self, rows=None, *objects, **kwargs):
        field_num = int(self.cmd_args.get('field_num', 1))
        content = str(rows[field_num - 1])
        expand_data_list = content.split(self.expand_separator)
        for expand_data in expand_data_list:
            if not self.keep_empty_line and not expand_data:
                continue
            rows[field_num - 1] = expand_data
            print(*rows, sep=self.separator, file=self.output_stream)
        return None

    def _add_cmd_args(self, parser):
        """
        添加命令行参数，子类可覆盖该方法并调用parser.add_argument()添加参数
        """
        parser.add_argument('-s', '--expand_separator', default=',', type=str, help='separator of the content to expand')
        parser.add_argument('-k', '--keep_empty_line', action='store_true', help='True: skip empty field, False[default]')


def main():
    ExpandLineStreamProcessor().stream_process()


if __name__ == '__main__':
    main()
