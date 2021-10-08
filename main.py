# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import Qt
from qt.main_window import MainWindow
from qt.edit_devices import AddController


def main():
    app = QtGui.QApplication(sys.argv)
    app.setFont(QApplication.font())

    main_win = MainWindow()
    AddController(main_win)

    main_win.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint)  # 去掉标题栏
    app.setFont(QApplication.font())
    main_win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
