# -*- coding: utf-8 -*-
"""
@file: utils
@desc:
@author: Jaden Wu
@time: 2021/10/5 21:54
"""
import inspect2
from PyQt4.QtGui import QTableWidgetItem
from PyQt4.QtCore import Qt


def static(method):
    def wrapper(*args):
        sign = inspect2.signature(method)
        return method(*args[0: len(sign.parameters)])
    return wrapper


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
                    item = QTableWidgetItem(value)
                    item.setTextAlignment(Qt.AlignCenter)
                    table.setItem(row, col, item)
                except Exception as e:
                    print(e)
