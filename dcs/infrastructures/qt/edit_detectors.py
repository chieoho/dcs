# -*- coding: utf-8 -*-
"""
@file: edit_detectors
@desc:
@author: Jaden Wu
@time: 2021/10/20 21:46
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
from dcs.adapter.edit_detector_view import EditDetectorsController
from dcs.infrastructures.database.repo import DetRepo


class EditDetectors(object):
    def __init__(self, mw):
        if not mw:
            mw = MainWindow()
        self.ui = mw.ui
        self.mw = mw
        self.detector_edit_table = self.ui.winfotableWidget
        self.det_edit_fields = (
            "area",
            "address_code",
            "position",
            "decimal_point",
            "material",
            "unit",
            "install_time"
        )

        self.mw.connect(self.ui.waddButton, QtCore.SIGNAL('clicked()'), static(self.add_detectors))
        self.mw.connect(self.ui.wlineEdit, QtCore.SIGNAL('returnPressed()'), self.add_detectors)
        self.mw.connect(self.detector_edit_table, QtCore.SIGNAL('cellChanged(int,int)'), self.modify_detector)
        self.mw.connect(self.ui.wdelButton, QtCore.SIGNAL('clicked()'), static(self.delete_detectors))
        self.mw.connect(self.ui.weditButton, QtCore.SIGNAL('clicked()'), static(self.edit_detector_enable))

        self.edit_det_controller = EditDetectorsController(DetRepo(), self)  # 放在最后

    def update_edit_table(self, edit_detectors_list):
        all_records = []
        for dev in edit_detectors_list:
            all_records.append([dev[k] for k in self.det_edit_fields])
        self.mw.disconnect(self.detector_edit_table, QtCore.SIGNAL('cellChanged(int,int)'), self.modify_detector)
        update_table(self.detector_edit_table, all_records)
        self.mw.connect(self.detector_edit_table, QtCore.SIGNAL('cellChanged(int,int)'), self.modify_detector)

    def add_detectors(self):
        detector_qty = int(self.ui.lineEdit.text())
        row_cnt = self.detector_edit_table.rowCount()
        detector_values_list = []
        for i in range(row_cnt, row_cnt + detector_qty):
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
            detector_values_list.append(dict(zip(self.det_edit_fields, row_content)))
        self.edit_det_controller.add_detector_rows(detector_values_list)

    def modify_detector(self, row, column):
        content = get_unicode_content(self.detector_edit_table.item(row, column))
        self.edit_det_controller.modify_detector_row(row, column, content)

    def delete_detectors(self):
        reply = QtGui.QMessageBox.question(
            self.mw,
            u"删除控制器",
            u"要删除选定的控制器吗？",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            remove_rows = get_selected_rows(self.detector_edit_table)
            self.edit_det_controller.delete_detector_rows(remove_rows)

    def edit_detector_enable(self):
        reply = QtGui.QMessageBox.question(
            self.mw,
            u"编辑监测器",
            u"要把监测器信息设置为可编辑吗？",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.ui.waddButton.setEnabled(True)
            self.ui.wdelButton.setEnabled(True)
            self.ui.wlineEdit.setEnabled(True)
            self.detector_edit_table.setSelectionBehavior(QtGui.QTableWidget.SelectItems)
            self.detector_edit_table.setEditTriggers(QtGui.QTableWidget.DoubleClicked)
        elif reply == QtGui.QMessageBox.No:
            self.ui.waddButton.setEnabled(False)
            self.ui.wdelButton.setEnabled(False)
            self.ui.wlineEdit.setEnabled(False)
            self.detector_edit_table.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
            self.detector_edit_table.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
