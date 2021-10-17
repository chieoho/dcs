# -*- coding: utf-8 -*-
"""
@file: test_delete_devices
@desc:
@author: Jaden Wu
@time: 2021/10/17 10:47
"""
from dcs.usecases.delete_devices import DeleteDevicesCase


class Repo(object):
    @staticmethod
    def delete_devices(_id_list):
        delete_res = False
        if isinstance(_id_list, list):
            delete_res = True
        return delete_res


def test_delete_devices():
    case = DeleteDevicesCase(Repo())
    _id_list = [1, 2]
    res = case.delete_devices(_id_list)
    assert res is True
