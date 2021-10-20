# -*- coding: utf-8 -*-
"""
@file: test_edit_devices_view
@desc:
@author: Jaden Wu
@time: 2021/10/17 11:03
"""
from dcs.usecases.add_devices import device_id, device_fields
from dcs.usecases.repo_if import DevRepoIf
from dcs.adapter.edit_devices_view import EditDevicesController


add_row_content = {
    "area": u"A区",
    "code": "16",
    "detector_num": "1",
    "install_time": "2021-10-17",
    "phone_num_1": "",
    "phone_num_2": "",
    "phone_num_3": "",
    "phone_num_4": ""
}


class EditDevicesView(object):
    def __init__(self):
        self.view_data = []

    def update_edit_table(self, edit_devices_list):
        self.view_data = edit_devices_list


class Repo(DevRepoIf):
    def __init__(self):
        self.devices = []

    def add_devices(self, device_list):
        for device in device_list:
            device.update({device_id: len(self.devices)+1})
            self.devices.append(device)
        return True

    def modify_device(self, _id, new_device_info):
        self.devices[_id-1].update(new_device_info)
        return True

    def delete_devices(self, _id_list):
        for _id in _id_list:
            for i, dev in enumerate(self.devices):
                if dev[device_id] == _id:
                    del self.devices[i]
        return True

    def get_devices(self):
        return self.devices


def test_controller_add_dev():
    repo = Repo()
    view = EditDevicesView()
    controller = EditDevicesController(repo, view)
    row_content_list = [add_row_content]
    res = controller.add_device_rows(row_content_list)
    assert res is True
    assert row_content_list == view.view_data


def test_controller_modify_dev():
    modify_col = 1
    new_value = "01"

    repo = Repo()
    view = EditDevicesView()
    controller = EditDevicesController(repo, view)
    row_content_list = [add_row_content]
    controller.add_device_rows(row_content_list)
    res = controller.modify_device_row(0, modify_col, new_value)
    assert res is True
    assert view.view_data[0][device_fields[modify_col]] == new_value


def test_controller_delete_dev():
    repo = Repo()
    view = EditDevicesView()
    controller = EditDevicesController(repo, view)
    row_content_list = [add_row_content]
    controller.add_device_rows(row_content_list)
    res = controller.delete_device_rows([0])
    assert res is True
    assert view.view_data == []
