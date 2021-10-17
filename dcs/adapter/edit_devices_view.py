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


class EditDevicesModel(object):
    def __init__(self):
        self.edit_devices_list = []

    def set_devices(self, devices):
        del self.edit_devices_list[:]
        for dev in devices:
            area, code, detector_num, install_time, phone_num_1, phone_num_2, phone_num_3, phone_num_4 \
                = map(lambda k: dev[k], device_fields)
            self.edit_devices_list.append([area, code, str(detector_num), str(install_time.date()),
                                           phone_num_1, phone_num_2, phone_num_3, phone_num_4])


class EditDevicesController(object):
    def __init__(self, repo, view):
        self.repo = repo
        self.view = view

        self.devices = []  # 主要为了保存model的行数与设备在数据库的id的对应关系
        self.edit_devices_model = EditDevicesModel()
        self._update_edit_table()

    def _fetch_devices_from_db(self):
        del self.devices[:]
        self.devices.extend(GetDevicesCase(self.repo).get_devices())
        self.edit_devices_model.set_devices(self.devices)

    def _update_edit_table(self):
        self._fetch_devices_from_db()
        self.view.update_edit_table(self.edit_devices_model.edit_devices_list)

    def add_device_rows(self, row_content_list):
        device_values_list = []
        for row_content in row_content_list:
            area, code, detector_num, _, phone_num_1, phone_num_2, phone_num_3, phone_num_4 = row_content
            install_time = datetime.now()
            device_values_list.append([area, code, int(detector_num), install_time,
                                       phone_num_1, phone_num_2, phone_num_3, phone_num_4])
        add_res = AddDevicesCase(self.repo).add_devices(device_values_list)
        self._update_edit_table()
        return add_res

    def modify_device_row(self, row, col, content):
        _id = self.devices[row][device_id]
        new_device_info = {device_fields[col]: content}
        modify_res = ModifyDeviceCase(self.repo).modify_device(_id, new_device_info)
        self._update_edit_table()
        return modify_res

    def delete_device_rows(self, rows):
        _id_list = map(lambda r: self.devices[r][device_id], rows)
        delete_res = DeleteDevicesCase(self.repo).delete_devices(_id_list)
        self._update_edit_table()
        return delete_res
