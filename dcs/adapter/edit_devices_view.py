# -*- coding: utf-8 -*-
"""
@file: edit_devices_view
@desc:
@author: Jaden Wu
@time: 2021/10/17 11:21
"""
from datetime import datetime

from dcs.usecases.add_devices import AddDevicesCase, device_fields, device_id
from dcs.usecases.get_devices import GetDevicesCase
from dcs.usecases.modify_device import ModifyDeviceCase
from dcs.usecases.delete_devices import DeleteDevicesCase


to_view = {
    "detector_num": str,
    "install_time": lambda it: str(it.date())
}


to_case = {
    "detector_num": int,
    "install_time": lambda it: datetime.strptime(it, "%Y-%m-%d")
}


def identity(item):
    return item


class EditDevicesController(object):
    def __init__(self, repo, view):
        self.repo = repo
        self.view = view

        self.devices_from_repo = []  # 主要为了保存行数与设备在数据库的id的对应关系
        self._update_edit_table()

    def _update_edit_table(self):
        del self.devices_from_repo[:]
        devices_from_repo = GetDevicesCase(self.repo).get_devices()
        self.devices_from_repo.extend(devices_from_repo)
        edit_devices_list = []
        for dev in self.devices_from_repo:
            edit_devices_list.append({k: to_view.get(k, identity)(dev[k]) for k in device_fields})
        self.view.update_edit_table(edit_devices_list)

    def add_device_rows(self, row_content_list):
        device_values_list = []
        for row_content in row_content_list:
            device_values_list.append({k: to_case.get(k, identity)(row_content[k]) for k in device_fields})
        add_res = AddDevicesCase(self.repo).add_devices(device_values_list)
        self._update_edit_table()
        return add_res

    def modify_device_row(self, row, col, content):
        _id = self.devices_from_repo[row][device_id]
        new_device_info = {device_fields[col]: content}
        modify_res = ModifyDeviceCase(self.repo).modify_device(_id, new_device_info)
        self._update_edit_table()
        return modify_res

    def delete_device_rows(self, rows):
        _id_list = map(lambda r: self.devices_from_repo[r][device_id], rows)
        delete_res = DeleteDevicesCase(self.repo).delete_devices(_id_list)
        self._update_edit_table()
        return delete_res
