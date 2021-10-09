# -*- coding: utf-8 -*-
"""
@file: add_controller
@desc:
@author: Jaden Wu
@time: 2021/10/5 21:49
"""
from datetime import datetime
import time
from PyQt4 import QtCore, QtGui
from infrastructures.qt.main_window import MainWindow
from infrastructures.qt.utils import static
from usecases.add_device import add_controller, controller_fields
from usecases.get_devices import get_controllers
from infrastructures.database.repo import DevRepo


class AddController(object):
    def __init__(self, mw):
        if not mw:
            mw = MainWindow()
        self.ui = mw.ui
        self.mw = mw
        self.dev_repo = DevRepo()

        self.ui.addButton.setEnabled(True)
        self.mw.connect(self.ui.addButton, QtCore.SIGNAL('clicked()'), static(self.add_controllers))
        self.populate_table()

    def add_controllers(self):
        edit_table = self.ui.tableWidget2_1
        monitoring_table = self.ui.tableWidget1
        # self.mw.disconnect(edit_table,  QtCore.SIGNAL('cellChanged(int,int)'), self.modify)
        controller_qty = int(self.ui.lineEdit.text())
        row = edit_table.rowCount()
        controller_values_list = []
        for i in range(row, row+controller_qty):
            monitoring_table.insertRow(i)
            edit_table.insertRow(i)
            region = u'A区'
            controller_code = '0'*(2-len(str(i+1)))+str(i+1)
            install_time = time.strftime('%Y-%m-%d')
            phone_num_1 = ' '
            phone_num_2 = ' '
            phone_num_3 = ' '
            phone_num_4 = ' '
            row_content = [
                region,
                controller_code,
                str(controller_qty),
                install_time,
                phone_num_1,
                phone_num_2,
                phone_num_3,
                phone_num_4
            ]
            controller_values_list.append([
                region,
                controller_code,
                str(controller_qty),
                datetime.now(),
                phone_num_1,
                phone_num_2,
                phone_num_3,
                phone_num_4
            ])
            combo_id = 'not combo'
            for j in range(len(row_content)):
                if j != combo_id:
                    item_content = QtGui.QTableWidgetItem(row_content[j])
                    item_content.setTextAlignment(QtCore.Qt.AlignCenter)
                    edit_table.setItem(i, j, item_content)
                else:
                    combo = QtGui.QComboBox()
                    combo.setEditable(True)
                    combo.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
                    for t in [u'否', u'是']:
                        combo.addItem(t)
                    combo.lineEdit().setReadOnly(True)
                    edit_table.setCellWidget(i, j, combo)
            for (col_edit, col_dis) in zip([0, 1, 2, 3], [0, 5, 1, 6]):
                item_content = QtGui.QTableWidgetItem(row_content[col_edit])
                item_content.setTextAlignment(QtCore.Qt.AlignCenter)
                monitoring_table.setItem(i, col_dis, item_content)
        # self.mw.connect(edit_table,  QtCore.SIGNAL('cellChanged(int,int)'), self.modify)
        add_controller(self.dev_repo, controller_values_list)

    def populate_table(self):
        all_records = get_controllers(self.dev_repo)
        all_records = [map(lambda k: d[k], controller_fields) for d in all_records]
        for RowIndex, _record in enumerate(all_records):
            self.ui.tableWidget1.insertRow(RowIndex)
            self.ui.tableWidget2_1.insertRow(RowIndex)
            extract_dict = {0: 0, 1: 5, 2: 1, 3: 6}
            for i, record in enumerate(_record):
                try:
                    if i in extract_dict:
                        record1 = QtGui.QTableWidgetItem(record)
                        record1.setTextAlignment(QtCore.Qt.AlignCenter)
                        self.ui.tableWidget1.setItem(RowIndex, extract_dict.get(i), record1)
                    record2 = QtGui.QTableWidgetItem(record)
                    record2.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.ui.tableWidget2_1.setItem(RowIndex, i, record2)
                except Exception, e:
                    print e
