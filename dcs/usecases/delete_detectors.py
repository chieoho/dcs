# -*- coding: utf-8 -*-
"""
@file: delete_detectors
@desc:
@author: Jaden Wu
@time: 2021/10/20 9:12
"""
from dcs.usecases.repo_if import det_repo_if


class DeleteDetectorsCase(object):
    def __init__(self, repo):
        self.repo = repo if repo else det_repo_if

    def delete_detectors(self, _id_list):
        """
        """
        res = self.repo.delete_detectors(_id_list)
        return res
