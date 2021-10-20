# -*- coding: utf-8 -*-
"""
@file: add_devices
@desc: 添加设备
@author: Jaden Wu
@time: 2021/10/2 15:31
"""
from dcs.usecases.repo_if import dev_repo_if


device_id = "_id"
device_fields = (
    "area",
    "code",
    "detector_num",
    "install_time",
    "phone_num_1",
    "phone_num_2",
    "phone_num_3",
    "phone_num_4"
)


class AddDevicesCase:
    def __init__(self, repo):
        self.repo = repo if repo else dev_repo_if

    def add_devices(self, device_list):
        """
        添加设备
        :param device_list: 字典列表
        :return:
        """
        add_res = self.repo.add_devices(device_list)
        return add_res
