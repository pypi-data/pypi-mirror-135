#!/usr/bin/env python
# -*- coding: utf8 -*-
import six

left_brackets_ch = '([{'
right_brackets_ch = ')]}'
quotes_ch = '"\''


def str_format(obj, indent=4, fold=True, comma_count_th=30, keep_str=True):
    """
    indent: 缩进长度
    flod: 是否折叠(连续多行时隐藏comma_count_th行之后的数据)
    keep_str: 是否保持字符串原格式
    """
    res = ''
    str_raw = obj if isinstance(obj, six.string_types) else str(obj)
    deep = 0
    last_ch = ''
    comma_count = 0
    not_folding = True
    is_in_str = False
    for ch in str_raw:
        # 保持字符串原格式
        if keep_str:
            if ch in quotes_ch:
                is_in_str = not is_in_str
            if is_in_str:
                if not_folding:
                    res += ch
                continue
        if ch in right_brackets_ch:
            deep -= 1
            res += '\n'
            res += ' ' * deep * indent
            comma_count = 0
        if last_ch == ',' and ch == ' ':
            last_ch = ch
            continue
        if fold:
            if comma_count >= comma_count_th:
                if not_folding:
                    res += '(fold)...'
                not_folding = False
            else:
                not_folding = True
        if not_folding:
            res += ch
        if ch in left_brackets_ch:
            deep += 1
            res += '\n'
            res += ' ' * deep * indent
            comma_count = 0
        if ch == ',':
            comma_count += 1
            if not_folding:
                res += '\n'
                res += ' ' * deep * indent
        last_ch = ch
    return res


def pprint(obj, *args, **kvarg):
    print(str_format(obj, *args, **kvarg))


pp = str_format
