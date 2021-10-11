# -*- coding: utf-8 -*-
"""
@file: edit_devices
@desc:
@author: Jaden Wu
@time: 2021/10/5 21:49
"""
import time
from PyQt4 import QtCore, QtGui
from infrastructures.qt.main_window import MainWindow
from infrastructures.qt.utils import static
from adapter.adapter import (
    add_device_rows,
    get_device_rows,
    modify_device_row,
    delete_device_rows
)
from infrastructures.database.repo import DevRepo


class EditDevices(object):
    def __init__(self, mw):
        if not mw:
            mw = MainWindow()
        self.ui = mw.ui
        self.mw = mw
        self.edit_table = self.ui.tableWidget2_1
        self.monitoring_table = self.ui.tableWidget1

        self.edit_table.setEditTriggers(QtGui.QTableWidget.DoubleClicked)

        self.mw.connect(self.ui.addButton, QtCore.SIGNAL('clicked()'), static(self.add_devices))
        self.mw.connect(self.edit_table, QtCore.SIGNAL('cellChanged(int,int)'), self.modify_device)
        self.mw.connect(self.ui.delButton, QtCore.SIGNAL('clicked()'), static(self.delete_devices))

        self.dev_repo = DevRepo()
        self.update_table()

    def _update_table(self):
        """
        在现有的行更新数据
        :return:
        """
        row_cnt = self.edit_table.rowCount()
        all_records = get_device_rows(self.dev_repo)
        records_cnt = len(all_records)
        # 删除多出的行
        if records_cnt < row_cnt:
            for row in range(row_cnt - 1, records_cnt - 1, -1):
                self.edit_table.removeRow(row)
                self.monitoring_table.removeRow(row)
        for row, _record in enumerate(all_records):
            # 记录多于现有行数时，插入新行
            if row > row_cnt - 1:
                self.monitoring_table.insertRow(row)
                self.edit_table.insertRow(row)
            extract_dict = {0: 0, 1: 5, 2: 1, 3: 6}
            for i, record in enumerate(_record):
                try:
                    if i in extract_dict:
                        record1 = QtGui.QTableWidgetItem(record)
                        record1.setTextAlignment(QtCore.Qt.AlignCenter)
                        self.monitoring_table.setItem(row, extract_dict.get(i), record1)
                    record2 = QtGui.QTableWidgetItem(record)
                    record2.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.edit_table.setItem(row, i, record2)
                except Exception as e:
                    print(e)

    def update_table(self):
        self.mw.disconnect(self.edit_table, QtCore.SIGNAL('cellChanged(int,int)'), self.modify_device)
        self._update_table()
        self.mw.connect(self.edit_table, QtCore.SIGNAL('cellChanged(int,int)'), self.modify_device)

    def add_devices(self):
        device_qty = int(self.ui.lineEdit.text())
        row_cnt = self.edit_table.rowCount()
        device_values_list = []
        for i in range(row_cnt, row_cnt + device_qty):
            region = u'A区'
            device_code = '0'*(2-len(str(i+1)))+str(i+1)
            install_time = time.strftime('%Y-%m-%d')
            phone_num_1 = ' '
            phone_num_2 = ' '
            phone_num_3 = ' '
            phone_num_4 = ' '
            row_content = [
                region,
                device_code,
                str(device_qty),
                install_time,
                phone_num_1,
                phone_num_2,
                phone_num_3,
                phone_num_4
            ]
            device_values_list.append(row_content)
        add_device_rows(self.dev_repo, device_values_list)
        self.update_table()

    def modify_device(self, row, column):
        content = self.mw.get_unicode_content(self.edit_table.item(row, column))
        modify_device_row(self.dev_repo, row, column, content)
        self.update_table()

    def delete_devices(self):
        reply = QtGui.QMessageBox.question(
            self.mw,
            u"删除控制器",
            u"要删除选定的控制器吗？",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            remove_rows = self.mw.get_selected_rows(self.edit_table)
            delete_device_rows(self.dev_repo, remove_rows)
            self.update_table()
