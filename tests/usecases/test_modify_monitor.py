# -*- coding: utf-8 -*-
"""
@file: test_modify_monitor
@desc:
@author: Jaden Wu
@time: 2021/10/17 10:12
"""
from dcs.usecases.modify_monitor_case import ModifyMonitorCase


class Repo(object):
    @staticmethod
    def modify_monitor(_id, new_monitor_info):
        modify_res = False
        if isinstance(_id, int) and isinstance(new_monitor_info, dict):
            modify_res = True
        return modify_res


def test_modify_monitor():
    case = ModifyMonitorCase(Repo())
    res = case.modify_monitor(1, {})
    assert res is True
