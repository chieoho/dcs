# -*- coding: utf-8 -*-
"""
@file: watch_monitor_controller
@desc:
@author: Jaden Wu
@time: 2021/10/24 10:58
"""
from dcs.adapter.sqls.repo import MonitorRepo


class WatchMonitorController(object):
    def __init__(self, view, session, port):
        self.view = view

        self.monitor_repo = MonitorRepo(session)


