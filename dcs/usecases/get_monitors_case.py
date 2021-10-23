# -*- coding: utf-8 -*-
"""
@file: get_monitors
@desc:
@author: Jaden Wu
@time: 2021/10/4 16:53
"""
from dcs.usecases.repo_if import monitor_repo_if


class GetMonitorsCase(object):
    def __init__(self, repo):
        self.repo = repo if repo else monitor_repo_if

    def get_monitors(self):
        monitor_list = self.repo.get_monitors()
        return monitor_list
