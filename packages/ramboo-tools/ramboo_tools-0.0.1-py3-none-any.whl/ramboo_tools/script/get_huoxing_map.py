#!/usr/bin/env python
# coding=utf-8
"""
文本转火星文
"""

# 系统库
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sys

# 重复请求次数，每次生成4条火星文
REPEAT_TIMES_LIMIT = 25


def main():
    """
    主程序
    """
    line_count = 0
    huoxing_map = {}
    for line in sys.stdin:
        try:
            line = line.decode('utf-8', 'ignore').strip('\n')
            if line == '':
                continue
            line_count += 1
            rows = line.split('\t')
            # FIX : 原文首尾空格，转为火星文时会去除
            comment = rows[0].strip(' ')
            huoxing_text = rows[1]
            # FIX : 原文空格未转义，插入空格后1个空格变3个
            while (huoxing_text.find('   ') != -1):
                huoxing_text = huoxing_text.replace('   ', ' _ ', 1)
            huoxing_text_ch_list = huoxing_text.split(' ')
            if len(comment) != len(huoxing_text_ch_list):
                output_line = "to fix\t%s" % line
                print(output_line.encode('utf-8'))
                continue
            for index, ch in enumerate(comment):
                huoxing_ch = huoxing_text_ch_list[index]
                if ch == huoxing_ch:
                    continue
                # FIX : 原文空格未转义，插入空格后1个空格变3个
                if ch == ' ' and huoxing_ch == '_':
                    continue
                if ch not in huoxing_map:
                    huoxing_map[ch] = {}
                huoxing_map[ch][huoxing_ch] = 1
            if line_count % 10000 == 0:
                print("line[%s] finish" % line_count, file=sys.stderr)

        except Exception as e:
            import traceback
            print("line[%s] comment[%s] ERROR:" % (line_count, comment), file=sys.stderr)
            print(traceback.format_exc(), file=sys.stderr)
            continue
        else:
            pass
        finally:
            pass
    for ch in huoxing_map:
        for huoxing_ch in huoxing_map[ch]:
            output_rows = [ch, huoxing_ch]
            output_line = '\t'.join(output_rows)
            print(output_line.encode('utf-8'))


if __name__ == '__main__':
    main()
