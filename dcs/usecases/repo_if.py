# -*- coding: utf-8 -*-
"""
@file: repo_if
@desc:
@author: Jaden Wu
@time: 2021/10/8 21:48
"""


class MonitorRepoIf(object):
    def get_monitors(self):
        pass

    def get_monitors_count(self):
        pass

    def add_monitors(self, monitor_list):
        pass

    def modify_monitor(self, _id, new_monitor_info):
        pass

    def delete_monitors(self, _id_list):
        pass


class DetectorRepoIf(object):
    def get_detectors(self, monitor_code):
        pass

    def get_detectors_count(self, monitor_code):
        pass

    def add_detectors(self, detector_list):
        pass

    def modify_detector(self, _id, new_detector_info):
        pass

    def delete_detectors(self, _id_list):
        pass


monitor_repo_if = MonitorRepoIf()
detector_repo_if = DetectorRepoIf()
