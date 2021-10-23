# -*- coding: utf-8 -*-
"""
@file: add_detectors
@desc:
@author: Jaden Wu
@time: 2021/10/20 9:12
"""
from datetime import datetime

from dcs.usecases.repo_if import detector_repo_if


detector_id = "_id"
detector_fields = (
    "area",
    "monitor_code",
    "address_code",
    "position",
    "decimal_point",
    "material",
    "unit",
    "install_time"
)


class AddDetectorsCase:
    def __init__(self, detector_repo):
        self.detector_repo = detector_repo if detector_repo else detector_repo_if

    def add_detectors(self, area, monitor_code, detector_num):
        """
        :param area:
        :param monitor_code:
        :param detector_num:
        :return:
        """
        detector_list = []
        detector_cnt = self.detector_repo.get_detectors_count(monitor_code)
        for i in range(detector_cnt, detector_cnt + detector_num):
            detector_default_values = [
                area,
                monitor_code,
                "8001",
                "0" * (3 - len(str(i + 1))) + str(i + 1),
                1,
                u'甲烷',
                "%LEL",
                datetime.now()
            ]
            detector_info = dict(zip(detector_fields, detector_default_values))
            detector_list.append(detector_info)
        add_res = self.detector_repo.add_detectors(detector_list)
        return add_res
