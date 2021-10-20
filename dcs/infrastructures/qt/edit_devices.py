# -*- coding: utf-8 -*-
"""
@file: edit_devices
@desc:
@author: Jaden Wu
@time: 2021/10/5 21:49
"""
import time

from PyQt4 import QtCore, QtGui
from dcs.infrastructures.qt.main_window import MainWindow
from dcs.infrastructures.qt.utils import (
    static,
    update_table,
    get_unicode_content,
    get_selected_rows,
)
from dcs.adapter.edit_devices_view import EditDevicesController
from dcs.infrastructures.database.repo import DevRepo


class EditDevices(object):
    def __init__(self, mw):
        if not mw:
            mw = MainWindow()
        self.ui = mw.ui
        self.mw = mw
        self.device_edit_table = self.ui.tableWidget2_1
        self.dev_edit_fields = (
            "area",
            "code",
            "detector_num",
            "install_time",
            "phone_num_1",
            "phone_num_2",
            "phone_num_3",
            "phone_num_4"
        )
        # self.device_monitoring_table = self.ui.tableWidget1
        # self.detector_edit_table = self.ui.winfotableWidget

        self.mw.connect(self.ui.addButton, QtCore.SIGNAL('clicked()'), static(self.add_devices))
        self.mw.connect(self.ui.lineEdit, QtCore.SIGNAL('returnPressed()'), self.add_devices)
        self.mw.connect(self.device_edit_table, QtCore.SIGNAL('cellChanged(int,int)'), self.modify_device)
        self.mw.connect(self.ui.delButton, QtCore.SIGNAL('clicked()'), static(self.delete_devices))
        self.mw.connect(self.ui.editButton, QtCore.SIGNAL('clicked()'), static(self.edit_device_enable))
        self.mw.connect(self.device_edit_table, QtCore.SIGNAL('cellDoubleClicked(int, int)'),
                        self.get_select_controller_for_edit)

        self.edit_dev_controller = EditDevicesController(DevRepo(), self)  # 放在最后

    def update_edit_table(self, edit_devices_list):
        all_records = []
        for dev in edit_devices_list:
            all_records.append([dev[k] for k in self.dev_edit_fields])
        self.mw.disconnect(self.device_edit_table, QtCore.SIGNAL('cellChanged(int,int)'), self.modify_device)
        update_table(self.device_edit_table, all_records)
        self.mw.connect(self.device_edit_table, QtCore.SIGNAL('cellChanged(int,int)'), self.modify_device)

    def add_devices(self):
        device_qty = int(self.ui.lineEdit.text())
        row_cnt = self.device_edit_table.rowCount()
        device_values_list = []
        for i in range(row_cnt, row_cnt + device_qty):
            row_content = [
                u"A区",
                "0" * (2 - len(str(i + 1))) + str(i + 1),
                "1",
                time.strftime("%Y-%m-%d"),
                " ",
                " ",
                " ",
                " "
            ]
            device_values_list.append(dict(zip(self.dev_edit_fields, row_content)))
        self.edit_dev_controller.add_device_rows(device_values_list)

    def modify_device(self, row, column):
        content = get_unicode_content(self.device_edit_table.item(row, column))
        self.edit_dev_controller.modify_device_row(row, column, content)

    def delete_devices(self):
        reply = QtGui.QMessageBox.question(
            self.mw,
            u"删除控制器",
            u"要删除选定的控制器吗？",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            remove_rows = get_selected_rows(self.device_edit_table)
            self.edit_dev_controller.delete_device_rows(remove_rows)

    def edit_device_enable(self):
        reply = QtGui.QMessageBox.question(
            self.mw,
            u"编辑控制器",
            u"要把控制器信息设置为可编辑吗？",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.ui.addButton.setEnabled(True)
            self.ui.delButton.setEnabled(True)
            self.ui.lineEdit.setEnabled(True)
            self.device_edit_table.setSelectionBehavior(QtGui.QTableWidget.SelectItems)
            self.device_edit_table.setEditTriggers(QtGui.QTableWidget.DoubleClicked)
        elif reply == QtGui.QMessageBox.No:
            self.ui.addButton.setEnabled(False)
            self.ui.delButton.setEnabled(False)
            self.ui.lineEdit.setEnabled(False)
            self.device_edit_table.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
            self.device_edit_table.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)

    def get_select_controller_for_edit(self, row):
        if self.ui.addButton.isEnabled():  # 控制器编辑状态下不跳转
            return
        controller_num = get_unicode_content(self.device_edit_table.item(row, 1))
        monitor_region = get_unicode_content(self.device_edit_table.item(row, 0))
        self.ui.tabWidget2.setTabText(1, monitor_region + '-' + controller_num + u'控制器')
        self.ui.tabWidget2.setCurrentIndex(1)

        self.ui.weditButton.setEnabled(True)
        self.ui.readButton.setEnabled(True)
        self.ui.importexctrlButton.setEnabled(True)
        self.ui.exportexctrlButton.setEnabled(True)
