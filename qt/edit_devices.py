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
from qt.main_window import MainWindow
from qt.utils import static
from control_system.add_device import add_controller
from control_system.get_devices import get_controllers
from database.repo import DevRepo


class AddController(object):
    def __init__(self, mw):
        if not mw:
            mw = MainWindow()
        self.ui = mw.ui
        self.mw = mw
        self.dev_repo = DevRepo()

        self.ui.addButton.setEnabled(True)
        self.mw.connect(self.ui.addButton, QtCore.SIGNAL('clicked()'), static(self.addDetectors))
        print(get_controllers(self.dev_repo))

    def addDetectors(self):
        tableWidget1 = self.ui.tableWidget1
        tableWidget2 = self.ui.tableWidget2_1
        # self.mw.disconnect(tableWidget2,  QtCore.SIGNAL('cellChanged(int,int)'), self.modify)
        addrowsqty = int(self.ui.lineEdit.text())
        RowIndex = tableWidget2.rowCount()
        controller_values_list = []
        for i in range(RowIndex,RowIndex+addrowsqty):
            tableWidget1.insertRow(i)
            tableWidget2.insertRow(i)
            region = u'A区'
            ctrllercode = '0'*(2-len(str(i+1)))+str(i+1)
            detectorqty = '1'
            assembletime = time.strftime('%Y-%m-%d')
            phonenum1 = ' '
            phonenum2 = ' '
            phonenum3 = ' '
            phonenum4 = ' '
            rowcontent = [
                region,
                ctrllercode,
                detectorqty,
                assembletime,
                phonenum1,
                phonenum2,
                phonenum3,
                phonenum4
            ]
            controller_values_list.append([
                region,
                ctrllercode,
                detectorqty,
                datetime.now(),
                phonenum1,
                phonenum2,
                phonenum3,
                phonenum4
            ])
            combo_id = 'not combo'
            for j in range(len(rowcontent)):
                if j != combo_id:
                    itemcontent = QtGui.QTableWidgetItem(rowcontent[j])
                    itemcontent.setTextAlignment(QtCore.Qt.AlignCenter)
                    tableWidget2.setItem(i,j,itemcontent)
                else:
                    combo = QtGui.QComboBox()
                    combo.setEditable(True)
                    combo.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
                    for t in [u'否', u'是']:
                        combo.addItem(t)
                    combo.lineEdit().setReadOnly(True)
                    tableWidget2.setCellWidget(i, j, combo)
            for (col_edit, col_dis) in zip([0, 1, 2, 3], [0, 5, 1, 6]):
                itemcontent = QtGui.QTableWidgetItem(rowcontent[col_edit])
                itemcontent.setTextAlignment(QtCore.Qt.AlignCenter)
                tableWidget1.setItem(i, col_dis, itemcontent)
        # self.mw.connect(tableWidget2,  QtCore.SIGNAL('cellChanged(int,int)'), self.modify)
        add_controller(self.dev_repo, controller_values_list)
