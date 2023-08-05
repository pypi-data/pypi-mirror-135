#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Copyright (c) Baidu.com, Inc. All Rights Reserved
@Time    : 2019-04-01
@Author  : yuanhui03
@Desc    : 模型效果测试
"""

# 系统库
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import sys
import re

# 第三方库
import six
from sklearn import metrics

# 内部库
from feed_antispam_lib.util import print
from feed_antispam_lib import util
from feed_antispam_lib import config
from feed_antispam_lib import char_info
from feed_antispam_lib import stream_processor


class ModelTest(stream_processor.StreamProcessor):
    """
    模型效果测试
    """

    def __init__(self, spam_label_list='1,2,3,4', step_len=1):
        """
        初始化
        """
        self.spam_label_list = spam_label_list.split(',')
        self.step_len = step_len

    def build_test_report(self):
        """
        生成测试报告
        """
        # fpr, tpr, thresholds = metrics.roc_curve(y_actual_list, y_spam_proba_list)
        auc = metrics.roc_auc_score(self.y_actual_list, self.y_spam_proba_list)
        print("AUC[%.2f]" % (auc * 100), file=self.output_stream)
        for temp in range(self.step_len, 100, self.step_len):
            threshold = float(temp) / 100
            y_predict_list = [int(y_spam_proba >= threshold) for y_spam_proba in self.y_spam_proba_list]
            print("threshold[%s]" % threshold, file=self.output_stream)
            report = metrics.classification_report(
                self.y_actual_list, y_predict_list, target_names=[' ok ', 'spam'], digits=4
            )
            print(report, file=self.output_stream)

    def rows_process(self, rows, *objects, **kwargs):
        """
        处理输入流的一行数据，将会被stream_process()方法调用，返回结果将输出至输出流
        rows: 接收输入流的一行数据
        *objects, **kwargs: 接受其余参数
        """
        label_row_num = kwargs.get('label_row_num', 1)
        score_row_num = kwargs.get('score_row_num', 2)
        label_row = rows[label_row_num - 1]
        label_list = re.split(r'[\s%s]' % char_info.punc_list, label_row)
        label_list = [config.LABEL_MAP.get(label, label) for label in label_list]
        if config.LABEL_VALUE_UNKNOWN in label_list:
            if not len(label_list) == 1:
                raise ValueError('-1 label mix with other label')
            # 跳过未知标签(-1)
            return
        # if any(label not in config.LABEL_MAP.values() for label in label_list):
        #     raise ValueError('label error: %s', '/'.join(label_list))
        y_actual = 0
        for spam_label in self.spam_label_list:
            if spam_label in label_list:
                y_actual = 1
                break
        self.y_actual_list.append(y_actual)
        spam_proba = float(rows[score_row_num - 1])
        self.y_spam_proba_list.append(spam_proba)

    def before_stream_process(self, *objects, **kwargs):
        """
        前置钩子
        """
        self.y_actual_list = []
        self.y_spam_proba_list = []

    def after_stream_process(self, *objects, **kwargs):
        """
        后置钩子
        """
        self.build_test_report()

    def unittest(self):
        """
        单元测试
        """
        self.stream_process(
            input_stream='data/model/sample/result/unittest/result.txt',
            output_stream='data/model/sample/result/unittest/report.txt',
        )


def main():
    """
    主程序
    """
    import argparse
    parser = argparse.ArgumentParser(description='模型效果测试')
    parser.add_argument('-i', '--input', default=sys.stdin, help='input file name')
    parser.add_argument('-o', '--output', default=sys.stdout, help='output file name')
    parser.add_argument('-ut', '--unittest', action='store_true', help='unit test')
    parser.add_argument('-s', '--separator', default='\t', help='test data separator, \\t default')
    parser.add_argument('-spam', '--spam_label_list', default='1,2,3,4',
                        help='spam label list, 1 policy / 2 porn / 3 ad / 4 curse / 0 ok, sep by ",", all spam label default')
    parser.add_argument('-step', '--step_len', default=1, help=r'threshold step len%, 1% default')
    parser.add_argument('-lrn', '--label_row_num', default=1, help='label row num, start at 1')
    parser.add_argument('-srn', '--score_row_num', default=2, help='score row num, start at 1')
    args = parser.parse_args()

    spam_label_list = six.ensure_text(args.spam_label_list, encoding='utf-8').strip('\n')
    modelTestObj = ModelTest(spam_label_list=spam_label_list, step_len=int(args.step_len))
    if args.unittest:
        modelTestObj.unittest()
        return
    modelTestObj.stream_process(
        args.input, args.output,
        separator=args.separator,
        label_row_num=int(args.label_row_num),
        score_row_num=int(args.score_row_num)
    )


if __name__ == '__main__':
    main()
