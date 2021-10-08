# -*- coding: utf-8 -*-
"""
@file: add_device
@desc: 添加设备
@author: Jaden Wu
@time: 2021/10/2 15:31
"""
from control_system.repo_if import repo_if

controller_fields = (
    "area",
    "code",
    "detector_num",
    "install_time",
    "phone_num_1",
    "phone_num_2",
    "phone_num_3",
    "phone_num_4",
)


def add_controller(repo, controller_values_list):
    """
    添加控制器
    :param repo:
    :param controller_values_list: 控制器字段值元组构成的列表
    :return:
    """
    repo = repo if repo else repo_if
    controller_list = []
    for controller_values in controller_values_list:
        controller_list.append(dict(zip(controller_fields, controller_values)))
    repo.add_controllers(controller_list)
