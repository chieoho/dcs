# -*- coding: utf-8 -*-
"""
@file: repo
@desc:
@author: Jaden Wu
@time: 2021/10/5 8:42
"""
from usecases.repo_if import RepoIf
from infrastructures.database.model import CtrlDev
from infrastructures.database.crud import CRUD


class DevRepo(RepoIf):
    def __init__(self):
        self.dev_repo = CRUD(CtrlDev)

    def add_controllers(self, controller_list):
        return self.dev_repo.add(controller_list)

    def get_controllers(self):
        return self.dev_repo.query({})
