# -*- coding: utf-8 -*-
"""
@file: get_devices
@desc:
@author: Jaden Wu
@time: 2021/10/4 16:53
"""
from dcs.usecases.repo_if import repo_if


class GetDevicesCase(object):
    def __init__(self, repo):
        self.repo = repo if repo else repo_if

    def get_devices(self):
        device_list = self.repo.get_devices()
        return device_list
