# -*- coding: utf-8 -*-
"""
@file: test_delete_monitors
@desc:
@author: Jaden Wu
@time: 2021/10/17 10:47
"""
from dcs.usecases.delete_monitors_case import DeleteMonitorsCase


class Repo(object):
    @staticmethod
    def delete_monitors(_id_list):
        delete_res = False
        if isinstance(_id_list, list):
            delete_res = True
        return delete_res


def test_delete_monitors():
    case = DeleteMonitorsCase(Repo())
    _id_list = [1, 2]
    res = case.delete_monitors(_id_list)
    assert res is True
