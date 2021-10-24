# -*- coding: utf-8 -*-
"""
@file: edit_monitors
@desc:
@author: Jaden Wu
@time: 2021/10/5 21:49
"""
from PyQt4 import QtCore, QtGui
from dcs.infrastructures.qt.qt_main_window import MainWindow
from dcs.infrastructures.qt.qt_utils import (
    static,
    update_table,
    get_unicode_content,
    get_selected_rows,
)
from dcs.adapter.edit_monitor_controller import EditMonitorsController
from dcs.infrastructures.database import engine, make_session


class EditMonitors(object):
    def __init__(self, mw):
        if not mw:
            mw = MainWindow()
        self.ui = mw.ui
        self.mw = mw
        self.monitor_edit_table = self.ui.tableWidget2_1
        self.monitor_edit_fields = (
            "area",
            "code",
            "detector_num",
            "install_time",
            "phone_num_1",
            "phone_num_2",
            "phone_num_3",
            "phone_num_4"
        )
        # self.monitor_monitoring_table = self.ui.tableWidget1
        # self.detector_edit_table = self.ui.winfotableWidget

        self.mw.connect(self.ui.addButton, QtCore.SIGNAL('clicked()'), static(self.add_monitors))
        self.mw.connect(self.ui.lineEdit, QtCore.SIGNAL('returnPressed()'), self.add_monitors)
        self.mw.connect(self.monitor_edit_table, QtCore.SIGNAL('cellChanged(int,int)'), self.modify_monitor)
        self.mw.connect(self.ui.delButton, QtCore.SIGNAL('clicked()'), static(self.delete_monitors))
        self.mw.connect(self.ui.editButton, QtCore.SIGNAL('clicked()'), static(self.edit_monitor_enable))

        self.edit_monitor_controller = EditMonitorsController(self, make_session(engine))  # 放在最后

    def update_edit_table(self, edit_monitors_list):
        all_records = []
        for dev in edit_monitors_list:
            all_records.append([dev[k] for k in self.monitor_edit_fields])
        self.mw.disconnect(self.monitor_edit_table, QtCore.SIGNAL('cellChanged(int,int)'), self.modify_monitor)
        update_table(self.monitor_edit_table, all_records)
        self.mw.connect(self.monitor_edit_table, QtCore.SIGNAL('cellChanged(int,int)'), self.modify_monitor)

    def edit_monitor_enable(self):
        reply = QtGui.QMessageBox.question(
            self.mw,
            u"编辑控制器",
            u"要把控制器信息设置为可编辑吗？",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.ui.addButton.setEnabled(True)
            self.ui.delButton.setEnabled(True)
            self.ui.lineEdit.setEnabled(True)
            self.monitor_edit_table.setSelectionBehavior(QtGui.QTableWidget.SelectItems)
            self.monitor_edit_table.setEditTriggers(QtGui.QTableWidget.DoubleClicked)
        elif reply == QtGui.QMessageBox.No:
            self.ui.addButton.setEnabled(False)
            self.ui.delButton.setEnabled(False)
            self.ui.lineEdit.setEnabled(False)
            self.monitor_edit_table.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
            self.monitor_edit_table.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)

    def add_monitors(self):
        monitor_num = int(self.ui.lineEdit.text())
        self.edit_monitor_controller.add_monitor_rows(monitor_num)

    def modify_monitor(self, row, column):
        content = get_unicode_content(self.monitor_edit_table.item(row, column))
        self.edit_monitor_controller.modify_monitor_row(row, column, content)

    def delete_monitors(self):
        reply = QtGui.QMessageBox.question(
            self.mw,
            u"删除控制器",
            u"要删除选定的控制器吗？",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            remove_rows = get_selected_rows(self.monitor_edit_table)
            self.edit_monitor_controller.delete_monitor_rows(remove_rows)
