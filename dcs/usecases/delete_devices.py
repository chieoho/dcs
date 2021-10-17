# -*- coding: utf-8 -*-
"""
@file: delete_devices
@desc:
@author: Jaden Wu
@time: 2021/10/10 21:19
"""
from dcs.usecases.repo_if import repo_if


class DeleteDevicesCase(object):
    def __init__(self, repo):
        self.repo = repo if repo else repo_if

    def delete_devices(self, _id_list):
        """
        """
        res = self.repo.delete_devices(_id_list)
        return res
