# -*- coding: utf-8 -*-
"""
@file: utils
@desc:
@author: Jaden Wu
@time: 2021/10/5 21:54
"""
import time
import string

import inspect2

from PyQt4.QtGui import QTableWidgetItem, QColor
from PyQt4.QtCore import Qt


def static(method):
    def wrapper(*args):
        sign = inspect2.signature(method)
        return method(*args[0: len(sign.parameters)])
    return wrapper


def update_table(table, all_records):
    """
    在现有的行更新数据
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


def _half2full(ustring):
    """把字符串半角转全角"""
    r_string = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code < 0x0020 or inside_code > 0x7e:  # 不是半角字符则返回原来的字符
            r_string += uchar
        if inside_code == 0x0020:  # 除了空格其他的全角半角的公式为:半角=全角-0xfee0
            inside_code = 0x3000
        else:
            inside_code += 0xfee0
        r_string += unichr(inside_code)
    return r_string


def write_text(text_browser, txt_path, content, color=QColor(0, 255, 0)):
    for ch in string.digits + string.letters:
        content = content.replace(ch, _half2full(ch))
    equ_len_content = content + u'　' * (14 - len(content))  # 空格是全角
    now_time = time.strftime('%Y-%m-%d %H:%M:%S')
    text_browser.setTextColor(color)
    work_info = equ_len_content + '\n' + now_time + u'；' + '\n'
    text_browser.append(work_info)
    text_browser_vsb = text_browser.verticalScrollBar()
    text_browser_vsb.setValue(text_browser_vsb.maximum())
    with open(txt_path, 'a') as f:
        f.write(work_info.encode('utf-8') + '\n')
    return now_time


def get_unicode_content(table_index):
    try:
        content = table_index.text().toLocal8Bit()
        content = unicode(content, 'gbk', 'ignore')
        return content
    except Exception as e:
        print(e)


def get_selected_rows(table_widget):
    rows = []
    for index in table_widget.selectedIndexes():
        if index.column() == 0:
            rows.append(index.row())
    rows = list(set(rows))  # 去除重复元素
    rows.sort()  # 升序
    rows.reverse()  # 颠倒
    return rows
