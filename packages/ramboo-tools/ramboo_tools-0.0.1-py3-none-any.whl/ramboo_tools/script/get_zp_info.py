#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
手百正排数据查询接口
"""

# 系统库
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import sys
import random
import json
import subprocess
import urllib2

# 内部库
from feed_antispam_lib.util import print
from feed_antispam_lib import util
from feed_antispam_lib import global_data
from feed_antispam_lib import stream_processor


class ZpInfoDao(stream_processor.StreamProcessor):
    """
    正排库dao
    """

    def __init__(self, trace_bns=None):
        if trace_bns is None:
            trace_bns = 'trace-api-sh.SUPERPAGE.sh01'
        cmd = "get_instance_by_service -a %s | awk '{if($5==0){print $2,$4}}'" % trace_bns
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        self.trace_ip_port = []
        for line in popen.stdout.readlines():
            host, port = line.strip().split()
            self.trace_ip_port.append((host, port))

    def query(self, nid):
        """
        使用nid查询正排数据
        """
        ip, port = random.choice(self.trace_ip_port)
        url = 'http://%s:%s/api/zpFullInfo/' % (ip, port) + nid + '?s=1'
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        req.add_header('source', 'RTPD_lidonghui02')
        res = urllib2.urlopen(req, timeout=1).read()
        return json.loads(res)

    def stream_process_rows(self, rows=None, *objects, **kwargs):
        """
        处理输入流的一行数据，将会被stream_process()方法调用，返回结果将输出至输出流
        rows: 接收输入流的一行数据
        *objects, **kwargs: 接受其余参数
        """
        nid_row_num = kwargs.get('nid_row_num', 1)
        nid = rows[nid_row_num - 1]
        res = self.query(nid)
        res = json.dumps(res, ensure_ascii=False)
        print(res)
        return res

    def get_unittest_text_list(self):
        """
        提供单元测试数据
        """
        return [
            r'4351144403954315420',
            r'4351144403954315420',
        ]


def main():
    """
    主程序
    """
    import argparse
    parser = argparse.ArgumentParser(description='手百正排数据查询')
    parser.add_argument('-i', '--input', default=sys.stdin, help='input file name')
    parser.add_argument('-o', '--output', default=sys.stdout, help='output file name')
    parser.add_argument('-s', '--separator', default='\t', help='i/o stream separator, \\t default')
    parser.add_argument('-ut', '--unittest', action='store_true', help='unit test')
    parser.add_argument('-nrn', '--nid_row_num', default=1, help='nid row num, start at 1')
    args = parser.parse_args()

    zpInfoDaoObj = ZpInfoDao()

    if args.unittest:
        zpInfoDaoObj.unittest()
        return
    zpInfoDaoObj.stream_process(
        args.input, args.output,
        separator=args.separator,
        nid_row_num=int(args.nid_row_num),
    )


if __name__ == '__main__':
    main()
