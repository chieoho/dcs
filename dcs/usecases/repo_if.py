# -*- coding: utf-8 -*-
"""
@file: repo_if
@desc:
@author: Jaden Wu
@time: 2021/10/8 21:48
"""


class DevRepoIf(object):
    def add_devices(self, device_list):
        pass

    def get_devices(self):
        pass

    def modify_device(self, _id, new_device_info):
        pass

    def delete_devices(self, _id_list):
        pass


class DetRepoIf(object):
    def add_detectors(self, detector_list):
        pass

    def get_detectors(self):
        pass

    def modify_detector(self, _id, new_detector_info):
        pass

    def delete_detectors(self, _id_list):
        pass


dev_repo_if = DevRepoIf()
det_repo_if = DetRepoIf()
