# -*- coding: utf-8 -*-
"""
@file: add_devices
@desc: 添加设备
@author: Jaden Wu
@time: 2021/10/2 15:31
"""
from usecases.repo_if import repo_if

device_fields = (
    "area",
    "code",
    "detector_num",
    "install_time",
    "phone_num_1",
    "phone_num_2",
    "phone_num_3",
    "phone_num_4",
)


def add_devices(repo, device_values_list):
    """
    添加设备
    :param repo:
    :param device_values_list: 设备字段值元组构成的列表
    :return:
    """
    repo = repo if repo else repo_if
    device_list = []
    for device_values in device_values_list:
        device_list.append(dict(zip(device_fields, device_values)))
    add_res = repo.add_devices(device_list)
    return add_res
