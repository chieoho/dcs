# -*- coding: utf-8 -*-
"""
@file: test_modify_device
@desc:
@author: Jaden Wu
@time: 2021/10/17 10:12
"""
from dcs.usecases.modify_device import ModifyDeviceCase


class Repo(object):
    @staticmethod
    def modify_device(_id, new_device_info):
        modify_res = False
        if isinstance(_id, int) and isinstance(new_device_info, dict):
            modify_res = True
        return modify_res


def test_modify_device():
    case = ModifyDeviceCase(Repo())
    res = case.modify_device(1, {})
    assert res is True
