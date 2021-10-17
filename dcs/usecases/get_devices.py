# -*- coding: utf-8 -*-
"""
@file: get_devices
@desc:
@author: Jaden Wu
@time: 2021/10/4 16:53
"""
from dcs.usecases.repo_if import repo_if


def get_devices(repo):
    repo = repo if repo else repo_if
    device_list = repo.get_devices()
    return device_list
