# -*- coding: utf-8 -*-
"""
@file: delete_monitors
@desc:
@author: Jaden Wu
@time: 2021/10/10 21:19
"""
from dcs.usecases.repo_if import monitor_repo_if


class DeleteMonitorsCase(object):
    def __init__(self, repo):
        self.repo = repo if repo else monitor_repo_if

    def delete_monitors(self, _id_list):
        """
        """
        res = self.repo.delete_monitors(_id_list)
        return res
