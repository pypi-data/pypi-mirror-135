#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Copyright (c) Baidu.com, Inc. All Rights Reserved
@Time    : 2018-11-21
@Author  : yuanhui03
@Desc    : 单词信息
"""

# 系统库
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import sys

# 第三方库
import jieba

# 内部库
from . import load_dict
from . import config


class TfIdf(object):
    """
    获取TF-IDF
    TF: 词频(在当前句子中的频率)
    DF: 文档频率(在整体语料库中的频率)
    IDF: 逆文档频率
    """

    def __init__(self):
        """
        初始化
        """
        self.df_dict = load_dict.load_map_dict(config.doc_frequency_dict_path, key_type='single')

    def get_word_df(self, word):
        """
        获取一个单词的DF
        """
        return self.df_dict.get(word, 0)

    def build_df_dict(self, corpus_file=None, output_stream=None, separator='\t', log_stream=None, is_corpus_seg=False, is_add_corpus=False):
        """
        生成df词典
        """
        need_close = False
        if corpus_file is None:
            corpus_file = config.doc_frequency_corpus_path
        if isinstance(corpus_file, (str, unicode)):
            corpus_file = open(corpus_file, 'r')
            need_close = True
        df_dict = self.df_dict if is_add_corpus else {}
        for line in corpus_file:
            line = line.decode('utf-8', 'ignore').strip('\n')
            if line == '':
                continue
            word_list = line.split(' ') if is_corpus_seg else jieba.cut(line)
            for word in word_list:
                if word not in df_dict:
                    df_dict[word] = 0
                df_dict[word] += 1
        if need_close:
            corpus_file.close()
        for word, frequency in df_dict.iteritems():
            output_line = separator.join(map(unicode, [word, frequency]))
            print(output_line.encode('utf-8'), file=output_stream)


def main():
    """
    主程序
    """
    import argparse

    parser = argparse.ArgumentParser(description='单词信息')
    parser.add_argument('-i', '--input', default=sys.stdin, help='input file name')
    parser.add_argument('-o', '--output', default=sys.stdout, help='output file name')
    parser.add_argument('-s', '--separator', default='\t', help='i/o stream separator, \\t default')
    parser.add_argument('-ut', '--unittest', action='store_true', help='unit test')
    parser.add_argument('-bdf', '--build_df_dict', action='store_true', help='build df dict')
    parser.add_argument('-cs', '--is_corpus_seg', action='store_true', help='corpus already seg')
    parser.add_argument('-add', '--is_add_corpus', action='store_true', help='add data to corpus')
    args = parser.parse_args()

    TfIdfObj = TfIdf()
    if args.unittest:
        TfIdfObj.unittest()
    elif args.build_df_dict:
        TfIdfObj.build_df_dict(args.input, args.output, args.separator, is_corpus_seg=args.is_corpus_seg, is_add_corpus=args.is_add_corpus)


if __name__ == '__main__':
    main()
