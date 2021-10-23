# -*- coding: utf-8 -*-
"""
@file: test_add_monitors
@desc:
@author: Jaden Wu
@time: 2021/10/17 9:54
"""
from dcs.usecases.repo_if import MonitorRepoIf
from dcs.usecases.add_monitors_case import AddMonitorsCase, monitor_fields


class Repo(MonitorRepoIf):
    def get_monitors_count(self):
        return 0

    def add_monitors(self, monitor_list):
        add_res = False
        if set(monitor_fields) == set(monitor_list[0].keys()):
            add_res = True
        return add_res


def test_add_monitors():
    case = AddMonitorsCase(Repo())
    add_res = case.add_monitors(1)
    assert add_res is True
