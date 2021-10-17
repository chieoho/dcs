# -*- coding: utf-8 -*-
"""
@file: test_add_devices
@desc:
@author: Jaden Wu
@time: 2021/10/17 9:54
"""
from dcs.usecases.add_devices import AddDevicesCase, device_fields


class Repo(object):
    @staticmethod
    def add_devices(dev_info_list):
        save_res = False
        if set(dev_info_list[0].keys()) == set(device_fields):
            save_res = True
        return save_res


def test_add_devices():
    case = AddDevicesCase(Repo())
    device_values = [None] * len(device_fields)
    device_values_list = [device_values]
    add_res = case.add_devices(device_values_list)
    assert add_res is True
