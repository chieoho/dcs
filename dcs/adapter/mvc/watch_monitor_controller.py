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
from dcs.adapter.gatherer.gatherer import Gatherer

to_view = {
    "detector_num": str,
    "install_time": lambda it: str(it.date())
}


def identity(item):
    return item


watch_monitor_model = (
    "area",
    "detector_num",
    "alarm_num",
    "fault_num",
    "state",
    "code",
    "install_time"
)


class WatchMonitorController(Thread):
    def __init__(self, view, session, port):
        super(WatchMonitorController, self).__init__()
        self.view = view

        self.is_running = False
        self.monitor_repo = MonitorRepo(session)
        self.collect_case = CollectDataCase(Gatherer(port))
        self._update_edit_table()

    def _update_edit_table(self):
        monitors_from_repo = GetMonitorsCase(self.monitor_repo).get_monitors()
        watch_monitors_list = []
        for mon in monitors_from_repo:
            monitor_info = {k: to_view.get(k, identity)(mon.get(k, "")) for k in watch_monitor_model}
            watch_monitors_list.append(monitor_info)
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
