# -*- coding: utf-8 -*-
"""
@file: repo
@desc:
@author: Jaden Wu
@time: 2021/10/5 8:42
"""
from dcs.usecases.repo_if import RepoIf
from dcs.infrastructures.database.model import CtrlDev
from dcs.infrastructures.database.crud import CRUD


class DevRepo(RepoIf):
    def __init__(self):
        self.dev_repo = CRUD(CtrlDev)

    def add_devices(self, device_list):
        return self.dev_repo.add(device_list)

    def get_devices(self):
        return self.dev_repo.query({})

    def modify_device(self, _id, new_device_info):
        return self.dev_repo.update({"_id": [_id]}, new_device_info)

    def delete_devices(self, _id_list):
        return self.dev_repo.delete({"_id": _id_list})