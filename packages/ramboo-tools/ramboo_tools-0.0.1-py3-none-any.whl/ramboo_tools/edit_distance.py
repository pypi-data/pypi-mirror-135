#!/usr/bin/env python
# -*- coding: utf8 -*-


def edit_dis(str1, str2):
    """
    计算str1与str2最短编辑距离
    """
    len1 = len(str1)
    len2 = len(str2)
    if len1 == 0 or len2 == 0:
        return len1 + len2
    # dp[i][j]: str1[:i]与str2[:j]的最短编辑距离
    dp = [[float('INF') for _ in range(len2 + 1)] for _ in range(len1 + 1)]
    for i in range(len1 + 1):
        for j in range(len2 + 1):
            # print(i, j, dp)
            if i == 0 or j == 0:
                dp[i][j] = i + j
                continue
            deletion = dp[i - 1][j] + 1
            insertion = dp[i][j - 1] + 1
            substitution = dp[i - 1][j - 1]
            if str1[i - 1] != str2[j - 1]:
                substitution += 1
            dp[i][j] = min(insertion, deletion, substitution)
    # print(dp)
    return dp[len1][len2]
