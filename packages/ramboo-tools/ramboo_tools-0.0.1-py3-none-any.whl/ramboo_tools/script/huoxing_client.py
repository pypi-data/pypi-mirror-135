#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
调用fzlft.com API生成火星文
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import sys
from HTMLParser import HTMLParser

# 第三方库
import requests

REQUEST_URL = "http://www.fzlft.com/huo/"
# 请求重试次数上限
REQUEST_RETRY_LIMIT = 5
# 火星文区域标识
HUOXING_START_KEYWORD = '<textarea id="result" onkeyup="s(this)" onclick="s(this)">'
HUOXING_END_KEYWORD = '</textarea>'

HTMLParser_obj = HTMLParser()


def get_huoxing_text_list(text):
    """
    调用fzlft.com API生成火星文
    每次4种随机结果+1条正繁体字，首位会添加特殊符号
    生成对的火星文首位会添加特殊符号，因此首尾添加两行再去掉，避免特殊符号影响
    """
    ret = ''

    # 首尾添加两行(非空白符)再去掉，避免特殊符号影响
    query_text = '1\n%s\n1' % text
    payload = {
        'q': ' '.join(query_text),
    }
    for retry_times in range(REQUEST_RETRY_LIMIT):
        try:
            response = requests.request("POST", REQUEST_URL, data=payload)
            response_text = response.text
            huoxign_start = response_text.find(HUOXING_START_KEYWORD) + len(HUOXING_START_KEYWORD)
            huoxing_end = response_text.find(HUOXING_END_KEYWORD, huoxign_start)
            if huoxign_start == -1 or huoxing_end == -1:
                continue
            huoxing_textarea = response_text[huoxign_start:huoxing_end]
            huoxing_textarea = HTMLParser_obj.unescape(huoxing_textarea)
            huoxing_textarea = huoxing_textarea.replace('\r\n', '')
            huoxing_text_list = huoxing_textarea.split('------------------------------------')
            # 只取第二行，首尾两行是特殊符号
            huoxing_text_list = [
                huoxing_text.split('\n')[1].strip(' ')
                for huoxing_text in huoxing_text_list
            ]
            # 只取前四个结果，第五个只是繁体
            ret = huoxing_text_list[:4]

            break
        except requests.exceptions.ConnectionError as e:
            continue
        else:
            pass
        finally:
            pass
    return ret


def unittest():
    """
    单元测试
    """
    text = '加微信1234567890'
    res = get_huoxing_text_list(text)
    for huoxing_text in res:
        print(huoxing_text.encode('utf-8'))


if __name__ == '__main__':
    unittest()
