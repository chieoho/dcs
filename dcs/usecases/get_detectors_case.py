# -*- coding: utf-8 -*-
"""
@file: get_detectors
@desc:
@author: Jaden Wu
@time: 2021/10/4 16:53
"""
from dcs.usecases.repo_if import detector_repo_if


class GetDetectorsCase(object):
    def __init__(self, repo):
        self.repo = repo if repo else detector_repo_if

    def get_detectors(self, monitor_code):
        detector_list = self.repo.get_detectors(monitor_code)
        return detector_list
