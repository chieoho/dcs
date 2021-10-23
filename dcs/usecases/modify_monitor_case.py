# -*- coding: utf-8 -*-
"""
@file: modify_monitor
@desc:
@author: Jaden Wu
@time: 2021/10/10 15:56
"""
from dcs.usecases.repo_if import monitor_repo_if


class ModifyMonitorCase(object):
    def __init__(self, repo):
        self.repo = repo if repo else monitor_repo_if

    def modify_monitor(self, _id, new_monitor_info):
        """
        """
        res = self.repo.modify_monitor(_id, new_monitor_info)
        return res
