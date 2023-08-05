#!/usr/bin/env python
# encoding=utf-8

# 系统库
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import sys
import json

# 第三方库
from six.moves.html_parser import HTMLParser

# 内部库
from ramboo_tools.stream_processor import StreamProcessor


class HtmlUnescapeProcessor(StreamProcessor):
    """
    Html编码转换
    """

    keep_input_rows = False

    def __init__(self):
        """
        初始化
        """
        super().__init__()
        self.parser = HTMLParser()

    def rows_process(self, rows, *args, **kwargs):
        """
        处理输入流一行的各列数据，返回结果将输出至输出流
        rows: 接收输入流一行的各列数据
        *args, **kwargs: 接受其余参数
        """
        res = [self.parser.unescape(row) for row in rows]
        return res

    @property
    def unittest_text_list(self):
        """
        提供单元测试数据
        """
        return [
            r'🐎',
            r'&#x1F40E;',
            r'❤️',
            r'&#x2764;&#xFE0F;',
            r'最好的王凯&#x2764;&#xFE0F;&#x2764;&#xFE0F;',
            r'穿AJ的都这么喜欢秀鞋子&#x1F40E;？',
            r'做这个的都是穷批&#x1F40E;',
            r'ヽ(爱&#x00B4;&#x2200;‘爱)ノ',
            r'做低调人，做高调事，此所谓人上人。助你东山再起，再创辉煌。【叩&#xD4E5; 同步】跟着队伍一起发展~7o^1&#x1D7F1;^81&#x0B68;~一起闯出个未来~！队员每月平均收入14&#xD4E6;~',
            r'坐等农大征集或填二批比较&#x1F42E;的。',
            r'作为一个男的声音这样还*别人的母&#x1F602;你自己听到自己声音不会软么',
        ]


def main():
    HtmlUnescapeProcessor().stream_process()


if __name__ == '__main__':
    main()
