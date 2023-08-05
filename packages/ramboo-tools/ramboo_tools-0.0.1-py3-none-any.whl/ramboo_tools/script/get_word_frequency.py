#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
计算单字频率
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import sys

word_stat_dict = {}

LABEL_UNKNOWN = 0
LABEL_OK = 1
LABEL_SPAM = 2


def word_stat(comment, word_stat_dict, label=LABEL_UNKNOWN):
    """
    频率统计
    """
    for word in comment:
        if word not in word_stat_dict:
            word_stat_dict[word] = {}
        if label not in word_stat_dict[word]:
            word_stat_dict[word][label] = 0
        word_stat_dict[word][label] += 1


def output(word_stat_dict):
    """
    输出结果
    """
    for word, frequency_item in word_stat_dict.iteritems():
        frequency_all = frequency_ok = frequency_spam = 0
        for label, frequency in frequency_item.iteritems():
            if int(label) == LABEL_OK:
                frequency_ok = frequency
            elif int(label) == LABEL_SPAM:
                frequency_spam = frequency
            frequency_all += frequency
        output_line = "%s\t%s\t%s\t%s" % (word, frequency_all, frequency_ok, frequency_spam)
        print(output_line.encode('utf-8'))


def main():
    """
    主程序
    """
    line_count = 0
    for line in sys.stdin:
        try:
            line = line.strip().decode('utf-8', 'ignore')
            if line == '':
                continue
            line_count += 1
            if line_count == 1:
                # 跳过表头
                continue
            rows = line.split('\t')
            comment = rows[0]
            label = rows[1] if len(rows) > 1 else '0'
            word_stat(comment, word_stat_dict, label)
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
    output(word_stat_dict)


def unittest():
    """
    单元测试
    """
    word_stat_dict = {}
    word_stat('你好', word_stat_dict, LABEL_OK)
    word_stat('你不好', word_stat_dict, LABEL_SPAM)
    output(word_stat_dict)

if __name__ == '__main__':
    main()
    # unittest()
