# -*- coding: utf-8 -*-
"""
@file: edit_devices
@desc:
@author: Jaden Wu
@time: 2021/10/5 21:49
"""
import time
import re

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
        self.device_edit_table = self.ui.tableWidget2_1
        self.device_monitoring_table = self.ui.tableWidget1
        self.detector_edit_table = self.ui.winfotableWidget

        self.mw.connect(self.ui.addButton, QtCore.SIGNAL('clicked()'), static(self.add_devices))
        self.mw.connect(self.ui.lineEdit, QtCore.SIGNAL('returnPressed()'), self.add_devices)
        self.mw.connect(self.device_edit_table, QtCore.SIGNAL('cellChanged(int,int)'), self.modify_device)
        self.mw.connect(self.ui.delButton, QtCore.SIGNAL('clicked()'), static(self.delete_devices))
        self.mw.connect(self.ui.editButton, QtCore.SIGNAL('clicked()'), static(self.edit_device_enable))

        self.mw.connect(self.device_edit_table, QtCore.SIGNAL('cellDoubleClicked(int, int)'),
                        self.get_select_ctrller_for_edit)

        self.dev_repo = DevRepo()
        self.update_device_table()

    def update_device_table(self):
        all_records = get_device_rows(self.dev_repo)
        self.mw.disconnect(self.device_edit_table, QtCore.SIGNAL('cellChanged(int,int)'), self.modify_device)
        self.update_table(self.device_edit_table, all_records)
        self.mw.connect(self.device_edit_table, QtCore.SIGNAL('cellChanged(int,int)'), self.modify_device)
        self.update_table(self.device_monitoring_table, all_records)

    @staticmethod
    def update_table(table, all_records):
        """
        在现有的行更新数据
        :return:
        """
        row_cnt = table.rowCount()
        records_cnt = len(all_records)
        # 删除多出的行
        if records_cnt < row_cnt:
            for row in range(row_cnt - 1, records_cnt - 1, -1):
                table.removeRow(row)
        for row, record in enumerate(all_records):
            # 记录多于现有行数时，插入新行
            if row > row_cnt - 1:
                table.insertRow(row)
            for col, value in enumerate(record):
                try:
                    item = QtGui.QTableWidgetItem(value)
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    table.setItem(row, col, item)
                except Exception as e:
                    print(e)

    def add_devices(self):
        device_qty = int(self.ui.lineEdit.text())
        row_cnt = self.device_edit_table.rowCount()
        device_values_list = []
        for i in range(row_cnt, row_cnt + device_qty):
            region = u'A区'
            device_code = '0' * (2 - len(str(i + 1))) + str(i + 1)
            detector_qty = "1"
            install_time = time.strftime('%Y-%m-%d')
            phone_num_1 = ' '
            phone_num_2 = ' '
            phone_num_3 = ' '
            phone_num_4 = ' '
            row_content = [
                region,
                device_code,
                detector_qty,
                install_time,
                phone_num_1,
                phone_num_2,
                phone_num_3,
                phone_num_4
            ]
            device_values_list.append(row_content)
        add_device_rows(self.dev_repo, device_values_list)
        self.update_device_table()

    def modify_device(self, row, column):
        content = self.mw.get_unicode_content(self.device_edit_table.item(row, column))
        modify_device_row(self.dev_repo, row, column, content)
        self.update_device_table()

    def delete_devices(self):
        reply = QtGui.QMessageBox.question(
            self.mw,
            u"删除控制器",
            u"要删除选定的控制器吗？",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            remove_rows = self.mw.get_selected_rows(self.device_edit_table)
            delete_device_rows(self.dev_repo, remove_rows)
            self.update_device_table()

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

    def get_select_ctrller_for_edit(self, row, column):
        _ = column
        if self.ui.addButton.isEnabled():  # 控制器编辑状态下不跳转
            return
        ctrller_num = self.mw.get_unicode_content(self.device_edit_table.item(row, 1))
        self.disp_select_ctrller_edit()
        monitor_region = self.mw.get_unicode_content(self.ui.tableWidget2_1.item(row, 0))
        self.ui.tabWidget2.setTabText(1, monitor_region + '-' + ctrller_num + u'控制器')
        self.ui.tabWidget2.setCurrentIndex(1)

        self.ui.weditButton.setEnabled(True)
        self.ui.readButton.setEnabled(True)
        self.ui.importexctrlButton.setEnabled(True)
        self.ui.exportexctrlButton.setEnabled(True)

    def disp_select_ctrller_edit(self):
        self.mw.disconnect(self.detector_edit_table, QtCore.SIGNAL('cellChanged(int,int)'), self.modify_detector)
        for i in range(self.detector_edit_table.rowCount(), -1, -1):
            self.detector_edit_table.removeRow(i)
        all_records = []
        for row, _record in enumerate(all_records):
            self.detector_edit_table.insertRow(row)
            for col, item_ in enumerate(_record):
                item = QtGui.QTableWidgetItem(item_)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.detector_edit_table.setItem(row, col, item)
        self.mw.connect(self.detector_edit_table, QtCore.SIGNAL('cellChanged(int,int)'), self.modify_detector)

    def modify_detector(self, row, column):
        content = self.mw.get_unicode_content(self.detector_edit_table.item(row, column))
        if column == 0:
            pass
        elif column == 1:
            if re.match(r'^[0-9]{1,4}$', content):
                self.mw.write_text(u'第%s行检测器地址码输入有效！' % (row + 1))
                content = '%04d' % int(content)
                self.mw.disconnect(self.detector_edit_table, QtCore.SIGNAL('cellChanged(int,int)'),
                                   self.modify_detector)
                self.detector_edit_table.item(row, column).setTextColor(QtCore.SIGNAL('White'))
                self.mw.tableWidgetsetItem(self.detector_edit_table, row, 1, content)
                self.mw.connect(self.detector_edit_table, QtCore.SIGNAL('cellChanged(int,int)'),
                                self.modify_detector)
            else:
                self.mw.write_text(u'第%s行检测器地址码输入无效，请重新输入！' % (row + 1), QtCore.SIGNAL('Red'))
                self.mw.disconnect(self.detector_edit_table, QtCore.SIGNAL('cellChanged(int,int)'),
                                   self.modify_detector)
                self.detector_edit_table.item(row, column).setTextColor(QtCore.SIGNAL('Red'))  # 红色
                self.mw.connect(self.detector_edit_table, QtCore.SIGNAL('cellChanged(int,int)'),
                                self.modify_detector)
        elif column == 2:
            pass
        else:
            pass

    def add_detector(self):
        tableWidget2 = self.ui.winfotableWidget
        self.disconnect(tableWidget2, SIGNAL('cellChanged(int,int)'), self.wmodify)
        addrowsqty = int(self.ui.wlineEdit.text())
        RowIndex = tableWidget2.rowCount()

        content = self.ui.tabWidget2.tabText(1).toLocal8Bit()
        content = unicode(content, 'gbk', 'ignore')
        region = '-'.join(content.split('-')[0: -1])
        ctrller_num = content.split('-')[-1][0: 2]

        self.mydb.transaction()
        for i in range(RowIndex, RowIndex + addrowsqty):
            tableWidget2.insertRow(i)
            addrcode = '8001'
            assembleaddr = '0' * (3 - len(str(i + 1))) + str(i + 1)
            decimal = '1'
            material = u'甲烷'
            unit = '%LEL'
            assembletime = str(time.strftime('%Y-%m-%d', time.localtime()))
            rowcontent = [region, addrcode, assembleaddr, decimal, material, unit, assembletime]
            thread.start_new_thread(self.sql_addrecords, (self.current_sql, [rowcontent]))  # Wow，用线程快
            for j in range(7):
                itemcontent = QTableWidgetItem(rowcontent[j])
                itemcontent.setTextAlignment(Qt.AlignCenter)
                tableWidget2.setItem(i, j, itemcontent)
        self.mydb.commit()
        self.connect(tableWidget2, SIGNAL('cellChanged(int,int)'), self.wmodify)
