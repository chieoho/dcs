# -*- coding: utf-8 -*-
"""
@file: delete_devices
@desc:
@author: Jaden Wu
@time: 2021/10/10 21:19
"""
from usecases.repo_if import repo_if


def delete_devices(repo, _id_list):
    """
    """
    repo = repo if repo else repo_if
    res = repo.delete_devices(_id_list)
    return res
