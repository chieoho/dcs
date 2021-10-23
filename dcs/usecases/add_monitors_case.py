# -*- coding: utf-8 -*-
"""
@file: add_monitors
@desc: 添加设备
@author: Jaden Wu
@time: 2021/10/2 15:31
"""
from datetime import datetime
from dcs.usecases.repo_if import monitor_repo_if


monitor_id = "_id"
monitor_fields = (
    "area",
    "code",
    "detector_num",
    "install_time",
    "phone_num_1",
    "phone_num_2",
    "phone_num_3",
    "phone_num_4"
)


class AddMonitorsCase:
    def __init__(self, monitor_repo):
        self.monitor_repo = monitor_repo if monitor_repo else monitor_repo_if

    def add_monitors(self, monitor_num):
        """
        添加设备
        :param monitor_num: 字典列表
        :return:
        """
        monitor_list = []
        monitor_cnt = self.monitor_repo.get_monitors_count()
        for i in range(monitor_cnt, monitor_cnt + monitor_num):
            monitor_default_values = [
                u"A区",
                "0" * (2 - len(str(i + 1))) + str(i + 1),
                0,
                datetime.now(),
                " ",
                " ",
                " ",
                " "
            ]
            monitor_info = dict(zip(monitor_fields, monitor_default_values))
            monitor_list.append(monitor_info)
        add_monitor_res = self.monitor_repo.add_monitors(monitor_list)
        return add_monitor_res
