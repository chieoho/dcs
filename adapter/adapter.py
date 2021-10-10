# -*- coding: utf-8 -*-
"""
@file: adapter
@desc:
@author: Jaden Wu
@time: 2021/10/10 8:45
"""
from datetime import datetime
from usecases.add_devices import add_devices, device_fields
from usecases.get_devices import get_devices
from usecases.modify_device import modify_device


def add_device_rows(repo, row_content_list):
    device_values_list = []
    for row_content in row_content_list:
        area, code, detector_num, _, phone_num_1, phone_num_2, phone_num_3, phone_num_4 = row_content
        install_time = datetime.now()
        device_values_list.append([area, code, int(detector_num), install_time,
                                   phone_num_1, phone_num_2, phone_num_3, phone_num_4])
    add_res = add_devices(repo, device_values_list)
    return add_res


def get_device_rows(repo):
    devices = get_devices(repo)
    all_records = []
    for dev in devices:
        area, code, detector_num, install_time, phone_num_1, phone_num_2, phone_num_3, phone_num_4 \
            = map(lambda k: dev[k], device_fields)
        all_records.append([area, code, str(detector_num), str(install_time.date()),
                            phone_num_1, phone_num_2, phone_num_3, phone_num_4])
    return all_records


def modify_device_row(repo, row, col, content):
    _id = row + 1
    new_device_info = {device_fields[col]: content}
    res = modify_device(repo, _id, new_device_info)
    return res
