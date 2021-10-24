# -*- coding: utf-8 -*-
"""
@file: edit_detectors
@desc:
@author: Jaden Wu
@time: 2021/10/20 21:46
"""
from PyQt4 import QtCore, QtGui
from dcs.infrastructures.qt.qt_main_window import MainWindow
from dcs.infrastructures.qt.qt_utils import (
    static,
    update_table,
    get_unicode_content,
    get_selected_rows,
)
from dcs.adapter.edit_detector_controller import EditDetectorsController, edit_detector_model
from dcs.infrastructures.database import engine, make_session


class EditDetectors(object):
    def __init__(self, mw):
        if not mw:
            mw = MainWindow()
        self.ui = mw.ui
        self.mw = mw
        self.detector_edit_table = self.ui.winfotableWidget
        self.monitor_edit_table = self.ui.tableWidget2_1

        self.mw.connect(self.monitor_edit_table, QtCore.SIGNAL('cellDoubleClicked(int, int)'),
                        self.get_select_controller_for_edit)
        self.mw.connect(self.ui.waddButton, QtCore.SIGNAL('clicked()'), static(self.add_detectors))
        self.mw.connect(self.ui.wlineEdit, QtCore.SIGNAL('returnPressed()'), self.add_detectors)
        self.mw.connect(self.detector_edit_table, QtCore.SIGNAL('cellChanged(int,int)'), self.modify_detector)
        self.mw.connect(self.ui.wdelButton, QtCore.SIGNAL('clicked()'), static(self.delete_detectors))
        self.mw.connect(self.ui.weditButton, QtCore.SIGNAL('clicked()'), static(self.edit_detector_enable))

        self.edit_detector_controller = EditDetectorsController(self, make_session(engine))  # 放在最后

    def get_select_controller_for_edit(self, row):
        if self.ui.addButton.isEnabled():  # 控制器编辑状态下不跳转
            return
        monitor_code = get_unicode_content(self.monitor_edit_table.item(row, 1))
        monitor_area = get_unicode_content(self.monitor_edit_table.item(row, 0))
        self.ui.tabWidget2.setTabText(1, monitor_area + '-' + monitor_code + u'控制器')
        self.ui.tabWidget2.setCurrentIndex(1)
        self.edit_detector_controller.set_monitor_code(monitor_code)

        self.ui.weditButton.setEnabled(True)
        self.ui.readButton.setEnabled(True)
        self.ui.importexctrlButton.setEnabled(True)
        self.ui.exportexctrlButton.setEnabled(True)

    def update_edit_table(self, edit_detectors_list):
        all_records = []
        for dev in edit_detectors_list:
            all_records.append([dev[k] for k in edit_detector_model])
        self.mw.disconnect(self.detector_edit_table, QtCore.SIGNAL('cellChanged(int,int)'), self.modify_detector)
        update_table(self.detector_edit_table, all_records)
        self.mw.connect(self.detector_edit_table, QtCore.SIGNAL('cellChanged(int,int)'), self.modify_detector)

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

    def add_detectors(self):
        content = self.ui.tabWidget2.tabText(1).toLocal8Bit()
        content = unicode(content, 'gbk', 'ignore')
        area = '-'.join(content.split('-')[0: -1])
        monitor_code = content.split('-')[-1][0: 2]
        detector_num = int(self.ui.wlineEdit.text())
        self.edit_detector_controller.add_detector_rows(area, monitor_code, detector_num)

    def modify_detector(self, row, column):
        content = get_unicode_content(self.detector_edit_table.item(row, column))
        self.edit_detector_controller.modify_detector_row(row, column, content)

    def delete_detectors(self):
        reply = QtGui.QMessageBox.question(
            self.mw,
            u"删除控制器",
            u"要删除选定的控制器吗？",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            remove_rows = get_selected_rows(self.detector_edit_table)
            self.edit_detector_controller.delete_detector_rows(remove_rows)
