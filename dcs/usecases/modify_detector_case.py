# -*- coding: utf-8 -*-
"""
@file: modify_detector
@desc:
@author: Jaden Wu
@time: 2021/10/20 9:12
"""
from dcs.usecases.repo_if import detector_repo_if


class ModifyDetectorCase(object):
    def __init__(self, repo):
        self.repo = repo if repo else detector_repo_if

    def modify_detector(self, _id, new_detector_info):
        """
        """
        res = self.repo.modify_detector(_id, new_detector_info)
        return res
