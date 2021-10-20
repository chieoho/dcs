# -*- coding: utf-8 -*-
"""
@file: add_detectors
@desc:
@author: Jaden Wu
@time: 2021/10/20 9:12
"""
from dcs.usecases.repo_if import det_repo_if


detector_id = "_id"
detector_fields = (

)


class AddDetectorsCase:
    def __init__(self, repo):
        self.repo = repo if repo else det_repo_if

    def add_detectors(self, detector_list):
        """
        :param detector_list:
        :return:
        """
        add_res = self.repo.add_detectors(detector_list)
        return add_res
