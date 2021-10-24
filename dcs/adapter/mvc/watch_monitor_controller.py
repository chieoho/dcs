# -*- coding: utf-8 -*-
"""
@file: watch_monitor_controller
@desc:
@author: Jaden Wu
@time: 2021/10/24 10:58
"""
from threading import Thread
import time

from dcs.usecases.collect_data_case import CollectDataCase
from dcs.usecases.get_monitors_case import GetMonitorsCase
from dcs.adapter.sqls.repo import MonitorRepo
from dcs.adapter.serial_port.gatherer import Gatherer

to_view = {
    "detector_num": str,
    "install_time": lambda it: str(it.date())
}


def identity(item):
    return item


watch_monitor_model = (
    "area",
    "code",
    "detector_num",
    "install_time",
    "phone_num_1",
    "phone_num_2",
    "phone_num_3",
    "phone_num_4"
)


class WatchMonitorController(Thread):
    def __init__(self, view, session, port):
        super(WatchMonitorController).__init__()
        self.view = view

        self.is_running = False
        self.monitor_repo = MonitorRepo(session)
        self.collect_case = CollectDataCase(Gatherer(port))
        self._update_edit_table()

    def _update_edit_table(self):
        monitors_from_repo = GetMonitorsCase(self.monitor_repo).get_monitors()
        watch_monitors_list = []
        for dev in monitors_from_repo:
            watch_monitors_list.append({k: to_view.get(k, identity)(dev[k]) for k in watch_monitor_model})
        self.view.update_edit_table(watch_monitors_list)

    def start(self):
        self.is_running = True

    def stop(self):
        self.is_running = False

    def run(self):
        while 1:
            if self.is_running:
                self.collect_case.get_data()
            time.sleep(0.5)
