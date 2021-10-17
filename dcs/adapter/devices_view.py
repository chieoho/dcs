# -*- coding: utf-8 -*-
"""
@file: devices_view
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

    def get_edit_devices(self, devices):
        del self.edit_devices_list[:]
        for dev in devices:
            area, code, detector_num, install_time, phone_num_1, phone_num_2, phone_num_3, phone_num_4 \
                = map(lambda k: dev[k], device_fields)
            self.edit_devices_list.append([area, code, str(detector_num), str(install_time.date()),
                                           phone_num_1, phone_num_2, phone_num_3, phone_num_4])
        return self.edit_devices_list


class MonitoringDevicesModel(object):
    def __init__(self):
        self.monitoring_devices_list = []

    def get_monitoring_devices(self):
        return self.monitoring_devices_list


class DevicesController(object):
    def __init__(self, repo, view):
        self.repo = repo
        self.view = view

        self.devices = []  # 主要为了保存model的行数与设备在数据库的id的对应关系

        self.edit_devices_model = EditDevicesModel()
        self.monitoring_devices_model = MonitoringDevicesModel()

    def add_device_rows(self, row_content_list):
        device_values_list = []
        for row_content in row_content_list:
            area, code, detector_num, _, phone_num_1, phone_num_2, phone_num_3, phone_num_4 = row_content
            install_time = datetime.now()
            device_values_list.append([area, code, int(detector_num), install_time,
                                       phone_num_1, phone_num_2, phone_num_3, phone_num_4])
        add_res = AddDevicesCase(self.repo).add_devices(device_values_list)
        return add_res

    def get_device_rows(self):
        del self.devices[:]
        self.devices.extend(GetDevicesCase(self.repo).get_devices())
        all_records = self.edit_devices_model.get_edit_devices(self.devices)
        return all_records

    def modify_device_row(self, row, col, content):
        _id = self.devices[row][device_id]
        new_device_info = {device_fields[col]: content}
        res = ModifyDeviceCase(self.repo).modify_device(_id, new_device_info)
        return res

    def delete_device_rows(self, rows):
        _id_list = map(lambda r: self.devices[r][device_id], rows)
        res = DeleteDevicesCase(self.repo).delete_devices(_id_list)
        return res

    def update_edit_table(self):
        all_records = self.get_device_rows()
        self.view.update_edit_table(all_records)

    def update_monitoring_table(self):
        self.view.update_monitoring_table(self.monitoring_devices_model)
