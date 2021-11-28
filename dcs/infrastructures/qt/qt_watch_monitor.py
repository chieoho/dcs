# -*- coding: utf-8 -*-
"""
@file: qt_watch_monitor
@desc:
@author: Jaden Wu
@time: 2021/10/24 18:22
"""
from PyQt4 import QtCore, QtGui
from dcs.infrastructures.qt.qt_main_window import MainWindow
from dcs.infrastructures.qt.qt_utils import (
    static,
    update_table,
    get_unicode_content,
    get_selected_rows,
)
from dcs.adapter.mvc.watch_monitor_controller import WatchMonitorController
from dcs.infrastructures.database import engine, make_session
from dcs.infrastructures.serial_port import init_port


class WatchMonitors(object):
    def __init__(self, mw):
        if not mw:
            mw = MainWindow()
        self.ui = mw.ui
        self.mw = mw
        self.watch_monitor_table = self.ui.tableWidget1
        self.watch_monitor_fields = (
            "area",
            "detector_num",
            "alarm_num",
            "fault_num",
            "state",
            "code",
            "install_time"
        )
        self.watch_monitor_controller = WatchMonitorController(
            self,
            make_session(engine),
            init_port('COM1', 9600, 0.1, False)
        )
        self.watch_monitor_controller.start()

    def update_table(self, edit_monitors_list):
        all_records = []
        for dev in edit_monitors_list:
            all_records.append([dev[k] for k in self.watch_monitor_fields])
        update_table(self.watch_monitor_table, all_records)
