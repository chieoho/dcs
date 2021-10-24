# -*- coding: utf-8 -*-
"""
@file: edit_monitors_controller
@desc:
@author: Jaden Wu
@time: 2021/10/17 11:21
"""
from datetime import datetime

from dcs.usecases.add_monitors_case import AddMonitorsCase, monitor_fields, monitor_id
from dcs.usecases.get_monitors_case import GetMonitorsCase
from dcs.usecases.modify_monitor_case import ModifyMonitorCase
from dcs.usecases.delete_monitors_case import DeleteMonitorsCase
from dcs.adapter.repo import MonitorRepo, DetectorRepo


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


edit_monitor_model = (
    "area",
    "code",
    "detector_num",
    "install_time",
    "phone_num_1",
    "phone_num_2",
    "phone_num_3",
    "phone_num_4"
)


class EditMonitorsController(object):
    def __init__(self, view, session):
        self.view = view

        self.monitor_repo = MonitorRepo(session)
        self.detector_repo = DetectorRepo(session)
        self.monitors_from_repo = []  # 主要为了保存行数与设备在数据库的id的对应关系
        self._update_edit_table()

    def _update_edit_table(self):
        del self.monitors_from_repo[:]
        monitors_from_repo = GetMonitorsCase(self.monitor_repo).get_monitors()
        self.monitors_from_repo.extend(monitors_from_repo)
        edit_monitors_list = []
        for dev in self.monitors_from_repo:
            edit_monitors_list.append({k: to_view.get(k, identity)(dev[k]) for k in edit_monitor_model})
        self.view.update_edit_table(edit_monitors_list)

    def add_monitor_rows(self, monitor_num):
        add_res = AddMonitorsCase(self.monitor_repo).add_monitors(monitor_num)
        self._update_edit_table()
        return add_res

    def modify_monitor_row(self, row, col, content):
        _id = self.monitors_from_repo[row][monitor_id]
        new_monitor_info = {monitor_fields[col]: content}
        modify_res = ModifyMonitorCase(self.monitor_repo).modify_monitor(_id, new_monitor_info)
        self._update_edit_table()
        return modify_res

    def delete_monitor_rows(self, rows):
        _id_list = map(lambda r: self.monitors_from_repo[r][monitor_id], rows)
        delete_res = DeleteMonitorsCase(self.monitor_repo).delete_monitors(_id_list)
        self._update_edit_table()
        return delete_res
