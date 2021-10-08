# -*- coding: utf-8 -*-
"""
@file: repo
@desc:
@author: Jaden Wu
@time: 2021/10/5 8:42
"""
from control_system.repo_if import RepoIf
from database.model import CtrlDev
from database.crud import CRUD


class DevRepo(RepoIf):
    def __init__(self):
        self.dev_repo = CRUD(CtrlDev)

    def add_controllers(self, controller_list):
        self.dev_repo.add(controller_list)

    def get_controllers(self):
        self.dev_repo.query({})
