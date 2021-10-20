# -*- coding: utf-8 -*-
"""
@file: modify_device
@desc:
@author: Jaden Wu
@time: 2021/10/10 15:56
"""
from dcs.usecases.repo_if import dev_repo_if


class ModifyDeviceCase(object):
    def __init__(self, repo):
        self.repo = repo if repo else dev_repo_if

    def modify_device(self, _id, new_device_info):
        """
        """
        res = self.repo.modify_device(_id, new_device_info)
        return res
