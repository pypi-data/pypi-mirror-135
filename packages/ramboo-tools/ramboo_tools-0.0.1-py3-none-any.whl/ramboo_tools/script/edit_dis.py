#!/usr/bin/env python
# -*- coding: utf8 -*-

from ramboo_tools.stream_processor import StreamProcessor
from ramboo_tools.edit_distance import edit_dis


class EditDistanceProcessor(StreamProcessor):
    """
    计算最短编辑编辑距离
    """

    def rows_process(self, rows=None, *objects, **kwargs):
        field_num = int(self.cmd_args.get('field_num', 1))
        field_num_2 = int(self.cmd_args.get('field_num_2', 2))
        str1 = str(rows[field_num - 1])
        str2 = str(rows[field_num_2 - 1])
        res = edit_dis(str1, str2)
        return res

    def _add_cmd_args(self, parser):
        """
        添加命令行参数，子类可覆盖该方法并调用parser.add_argument()添加参数
        """
        parser.add_argument('-f2', '--field_num_2', default=2, type=str, help='content field num 2')


def main():
    EditDistanceProcessor().stream_process()


if __name__ == '__main__':
    main()
