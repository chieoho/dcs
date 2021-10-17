# -*- coding: utf-8 -*-
"""
@file: modify_device
@desc:
@author: Jaden Wu
@time: 2021/10/10 15:56
"""
from dcs.usecases.repo_if import repo_if


def modify_device(repo, _id, new_device_info):
    """
    """
    repo = repo if repo else repo_if
    res = repo.modify_device(_id, new_device_info)
    return res
