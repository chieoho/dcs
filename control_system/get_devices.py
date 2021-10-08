# -*- coding: utf-8 -*-
"""
@file: get_devices
@desc:
@author: Jaden Wu
@time: 2021/10/4 16:53
"""
from control_system.repo_if import repo_if


def get_controllers(repo):
    repo = repo if repo else repo_if
    controller_list = repo.get_controllers()
    return controller_list
