# -*- coding: utf-8 -*-
"""
@file: repo_if
@desc:
@author: Jaden Wu
@time: 2021/10/8 21:48
"""


class RepoIf(object):
    def add_devices(self, device_list):
        pass

    def get_devices(self):
        pass

    def modify_device(self, _id, new_device_info):
        pass

    def delete_devices(self, _id_list):
        pass


repo_if = RepoIf()
