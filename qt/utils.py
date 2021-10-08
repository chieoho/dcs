# -*- coding: utf-8 -*-
"""
@file: utils
@desc:
@author: Jaden Wu
@time: 2021/10/5 21:54
"""
import inspect2


def static(method):
    def wrapper(*args):
        sign = inspect2.signature(method)
        return method(*args[0: len(sign.parameters)])
    return wrapper
