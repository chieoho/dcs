# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from infrastructures.qt.ui.dcs_ui import Ui_MainWindow


buttonStyleSheet = '''
QPushButton {
border: 1px solid rgb(200, 200, 200);
border-right-color: rgb(189, 181, 119);
border-left-color: rgb(230, 230, 230);
padding: 0px;
}
QPushButton:hover{background-color:rgb(220, 220, 220);}
QPushButton:pressed {
background: qradialgradient(cx: 0.4, cy: -0.1,
fx: 0.4, fy: -0.1,
radius: 1.35, stop: 0 #fff, stop: 1 #ddd);
}
'''
small_segm = 0.007
last_small_segm = 0.01
grad_len = 0.0001
segm_1, segm_2, segm_3, segm_4, segm_5, segm_6 = 0.16, 0.30, 0.44, 0.60, 0.74, 1 - last_small_segm - grad_len
status_bar_segm = (0, small_segm,
                   small_segm + grad_len, segm_1,

                   segm_1 + grad_len, segm_1 + grad_len + small_segm,
                   segm_1 + small_segm + 2 * grad_len, segm_2,

                   segm_2 + grad_len, segm_2 + grad_len + small_segm,
                   segm_2 + small_segm + 2 * grad_len, segm_3,

                   segm_3 + grad_len, segm_3 + grad_len + small_segm,
                   segm_3 + small_segm + 2 * grad_len, segm_4,

                   segm_4 + grad_len, segm_4 + grad_len + small_segm,
                   segm_4 + small_segm + 2 * grad_len, segm_5,

                   segm_5 + grad_len, segm_5 + grad_len + small_segm,
                   segm_5 + small_segm + 2 * grad_len, segm_6,

                   segm_6 + grad_len, 1
                   )
statusBarStyleSheet = '''
color: white;
background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
stop:%s rgb(100, 100, 100), 
stop:%s rgb(100, 100, 100), 

stop:%s rgb(160, 160, 160),
stop:%s rgb(160, 160, 160),

stop:%s rgb(100, 100, 100),
stop:%s rgb(100, 100, 100),

stop:%s rgb(160, 160, 160), 
stop:%s rgb(160, 160, 160), 

stop:%s rgb(100, 100, 100),
stop:%s rgb(100, 100, 100),

stop:%s rgb(160, 160, 160), 
stop:%s rgb(160, 160, 160), 

stop:%s rgb(100, 100, 100),
stop:%s rgb(100, 100, 100),

stop:%s rgb(160, 160, 160), 
stop:%s rgb(160, 160, 160), 

stop:%s rgb(100, 100, 100),
stop:%s rgb(100, 100, 100),

stop:%s rgb(160, 160, 160), 
stop:%s rgb(160, 160, 160), 

stop:%s rgb(100, 100, 100),
stop:%s rgb(100, 100, 100),

stop:%s rgb(160, 160, 160), 
stop:%s rgb(160, 160, 160),

stop:%s rgb(100, 100, 100)
stop:%s rgb(100, 100, 100));
''' % status_bar_segm


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.stateid = 1
        self.width0 = 0.0
        self.height0 = 0.0
        self.componentarray = []
        self.origeoarray = []
        self.activeStateColor = "background:rgb(83, 166, 249);padding: 0px;border: 1px solid rgb(200, 200, 200);"
        self.firsttime = True

        self.run_icon = QtGui.QIcon()
        self.run_pixmap = QtGui.QPixmap("ico/run.png")
        self.run_icon.addPixmap(self.run_pixmap)

        self.stop_icon = QtGui.QIcon()
        self.stop_pixmap = QtGui.QPixmap("ico/stop.png")
        self.stop_icon.addPixmap(self.stop_pixmap)

        self.gray_icon = QtGui.QIcon()
        self.gray_pixmap = QtGui.QPixmap("ico/gray_led.png")
        self.gray_icon.addPixmap(self.gray_pixmap)

        self.green_icon = QtGui.QIcon()
        self.green_pixmap = QtGui.QPixmap("ico/green_led.png")
        self.green_icon.addPixmap(self.green_pixmap)

        self.red_icon = QtGui.QIcon()
        self.red_pixmap = QtGui.QPixmap("ico/red_led.png")
        self.red_icon.addPixmap(self.red_pixmap)

        self.yellow_icon = QtGui.QIcon()
        self.yellow_pixmap = QtGui.QPixmap("ico/yellow_led.png")
        self.yellow_icon.addPixmap(self.yellow_pixmap)

        self.ui.port_led_Button.setIcon(self.green_icon)
        self.port_led_on = True

        self.update_timer = QtCore.QTimer()
        self.update_timer.start(400)
        self.connect(self.update_timer, QtCore.SIGNAL('timeout()'), self.fullScreen)

        self.connect(self.ui.mainuiButton, QtCore.SIGNAL('clicked()'), self.mainuiBthandle)
        self.connect(self.ui.deinfoButton, QtCore.SIGNAL('clicked()'), self.deviceinfoBthandle)
        self.connect(self.ui.alarmquButton, QtCore.SIGNAL('clicked()'), self.alarmquBthandle)
        self.connect(self.ui.controlButton, QtCore.SIGNAL('clicked()'), self.controlBthandle)
        self.connect(self.ui.exitButton, QtCore.SIGNAL('clicked()'), self.exitSystem)

        self.objects = [(self.ui.tabWidget1, self.ui.mainuiButton),
                        (self.ui.tabWidget2, self.ui.deinfoButton),
                        (self.ui.tabWidget3, self.ui.alarmquButton),
                        (self.ui.widget, self.ui.controlButton),
                        ]
        # self.setmainBtnEnabl(False)
        self.inittablewidget()
        self.originalgeo()

    def setmainBtnEnabl(self, Enabl):
        self.ui.mainuiButton.setEnabled(Enabl)
        self.ui.deinfoButton.setEnabled(Enabl)
        self.ui.controlButton.setEnabled(Enabl)
        self.ui.alarmquButton.setEnabled(Enabl)
        self.ui.startButton.setEnabled(Enabl)

    def inittablewidget(self):
        componentlist = dir(self.ui)
        for component in componentlist:
            if component.find('tableWidget') != -1:
                s1 = 'self.ui.' + component + '.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)'  # 列头自适应宽度
                eval(s1)
                s2 = 'self.ui.' + component + '.setSelectionBehavior(QtGui.QTableWidget.SelectRows)'  # 设置选择行为，以行为单位
                eval(s2)

    def originalgeo(self):
        componentlist = dir(self.ui)
        KeyWorld = (
        'tabWidget', 'Button', 'tableWidget', 'label', 'textEdit', 'dateEdit', 'comboBox', 'lineEdit', 'groupBox',
        'textBrowser', 'widget')
        for keyworld in KeyWorld:
            for component in componentlist:
                if component.find(keyworld) != -1:
                    self.componentarray.append(component)
                    s = 'self.ui.' + component + '.geometry()'
                    self.origeoarray.append(eval(s))

    def resizeEvent(self, event):
        size = event.size()
        if self.firsttime:
            self.firsttime = False
            self.width0 = size.width() * 1.0
            self.height0 = size.height() * 1.0
        widthtimes = size.width() / self.width0
        heighttimes = size.height() / self.height0

        i = 0
        for component in self.componentarray:
            s = 'self.ui.' + component + \
                '.setGeometry(QtCore.QRect(self.origeoarray[i].x()*widthtimes, self.origeoarray[i].y()*heighttimes,' \
                'self.origeoarray[i].width()*widthtimes, self.origeoarray[i].height()*heighttimes))'
            eval(s)
            i += 1
        self.statemachine(QtCore.QRect(self.origeoarray[-1].width() * widthtimes,  # 状态机切换x坐标
                                       self.origeoarray[0].y() * heighttimes,
                                       self.origeoarray[0].width() * widthtimes,
                                       self.origeoarray[0].height() * heighttimes))
        self.objects[self.stateid - 1][1].setEnabled(False)
        self.objects[self.stateid - 1][1].setStyleSheet(self.activeStateColor)

        self.ui.statusBar.setMinimumHeight(25 * heighttimes)

    def createStates(self, objects, selectedRect, parent):
        i = 0
        for obj in objects:
            i += 1
            self.state = QtCore.QState(parent)
            self.state.assignProperty(obj[0], 'geometry', selectedRect)
            if i == self.stateid:
                parent.setInitialState(self.state)
            parent.addTransition(obj[1].clicked, self.state)

    def createAnimations(self, objects, machine):
        for obj in objects:
            self.animation = QtCore.QPropertyAnimation(obj[0], 'geometry', obj[0])
            self.animation.setDuration(0)  # 1200ms
            self.animation.setEasingCurve(QtCore.QEasingCurve.OutExpo)  # OutBounce,OutExpo,OutElastic
            machine.addDefaultAnimation(self.animation)

    def statemachine(self, selectedRect):
        self.machine = QtCore.QStateMachine()
        self.machine.setGlobalRestorePolicy(QtCore.QStateMachine.RestoreProperties)

        self.group = QtCore.QState(self.machine)
        self.selectedRect = selectedRect

        self.createStates(self.objects, self.selectedRect, self.group)
        self.createAnimations(self.objects, self.machine)

        self.machine.setInitialState(self.group)
        self.machine.start()

    def mainuiBthandle(self):
        self.stateid = 1
        self.ui.deinfoButton.setEnabled(True)
        self.ui.alarmquButton.setEnabled(True)
        self.ui.controlButton.setEnabled(True)
        self.ui.mainuiButton.setEnabled(False)

        self.ui.deinfoButton.setStyleSheet(buttonStyleSheet)  # cool
        self.ui.alarmquButton.setStyleSheet(buttonStyleSheet)
        self.ui.controlButton.setStyleSheet(buttonStyleSheet)
        self.ui.mainuiButton.setStyleSheet(self.activeStateColor)

    def deviceinfoBthandle(self):
        self.stateid = 2
        self.ui.mainuiButton.setEnabled(True)
        self.ui.alarmquButton.setEnabled(True)
        self.ui.controlButton.setEnabled(True)
        self.ui.deinfoButton.setEnabled(False)

        self.ui.mainuiButton.setStyleSheet(buttonStyleSheet)  # 恢复原来的背景色
        self.ui.alarmquButton.setStyleSheet(buttonStyleSheet)
        self.ui.controlButton.setStyleSheet(buttonStyleSheet)
        self.ui.deinfoButton.setStyleSheet(self.activeStateColor)

        # self.ui.addButton.setEnabled(False)
        self.ui.delButton.setEnabled(False)
        self.ui.lineEdit.setEnabled(False)
        self.ui.tableWidget2_1.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
        # self.ui.tableWidget2_1.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)

        self.ui.waddButton.setEnabled(False)
        self.ui.wdelButton.setEnabled(False)
        self.ui.wlineEdit.setEnabled(False)
        self.ui.winfotableWidget.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
        self.ui.winfotableWidget.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)

    def alarmquBthandle(self):
        self.stateid = 3
        self.ui.mainuiButton.setEnabled(True)
        self.ui.deinfoButton.setEnabled(True)
        self.ui.controlButton.setEnabled(True)
        self.ui.alarmquButton.setEnabled(False)

        self.ui.mainuiButton.setStyleSheet(buttonStyleSheet)
        self.ui.deinfoButton.setStyleSheet(buttonStyleSheet)
        self.ui.controlButton.setStyleSheet(buttonStyleSheet)
        self.ui.alarmquButton.setStyleSheet(self.activeStateColor)

        self.ui.dateEdit1.setDate(QtCore.QDate.currentDate())
        self.ui.dateEdit2.setDate(QtCore.QDate.currentDate())
        self.ui.wdateEdit1.setDate(QtCore.QDate.currentDate())
        self.ui.wdateEdit2.setDate(QtCore.QDate.currentDate())
        self.ui.dateEdit_conctt_1.setDate(QtCore.QDate.currentDate())
        self.ui.dateEdit_conctt_2.setDate(QtCore.QDate.currentDate())

        self.ui.wcomboBox_dev.clear()
        self.ui.wcomboBox_dev.addItem(u'所有')

        self.combox_region = []
        self.combox_ctrller = []
        self.combox_region.append(u'所有')
        self.combox_ctrller.append(u'所有')
        for i in range(0, self.ui.tableWidget1.rowCount()):
            self.combox_region.append(self.getucontent(self.ui.tableWidget1.item(i, 0)))
            self.combox_ctrller.append(self.getucontent(self.ui.tableWidget1.item(i, 5)))
        self.ui.comboBox_region.clear()
        self.ui.comboBox_ctrller.clear()
        self.ui.wcomboBox_region.clear()
        self.ui.wcomboBox_ctrller.clear()
        self.ui.comboBox_conctt_ctrller.clear()
        for comboxitem in self.combox_region:
            self.ui.comboBox_region.addItem(comboxitem)
            self.ui.wcomboBox_region.addItem(comboxitem)
        for comboxitem in self.combox_ctrller:
            self.ui.comboBox_ctrller.addItem(comboxitem)
            self.ui.wcomboBox_ctrller.addItem(comboxitem)
            if comboxitem != u'所有':
                self.ui.comboBox_conctt_ctrller.addItem(comboxitem)

    def controlBthandle(self):
        self.stateid = 4
        self.ui.deinfoButton.setEnabled(True)
        self.ui.alarmquButton.setEnabled(True)
        self.ui.mainuiButton.setEnabled(True)
        self.ui.controlButton.setEnabled(False)

        self.ui.deinfoButton.setStyleSheet(buttonStyleSheet)  # cool
        self.ui.alarmquButton.setStyleSheet(buttonStyleSheet)
        self.ui.mainuiButton.setStyleSheet(buttonStyleSheet)
        self.ui.controlButton.setStyleSheet(self.activeStateColor)

    def fullScreen(self):
        self.showFullScreen()
        self.disconnect(self.update_timer, QtCore.SIGNAL('timeout()'), self.fullScreen)

    def simulatebutton(self, button):
        press = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonPress, QtCore.QPoint(0, 0), QtCore.Qt.LeftButton, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
        QtGui.QApplication.postEvent(button, press)
        release = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonRelease, QtCore.QPoint(0, 0), QtCore.Qt.LeftButton, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
        QtGui.QApplication.postEvent(button, release)

    def exitSystem(self):
        reply = QtGui.QMessageBox.question(
            self,
            u"关闭系统",
            u"确定要关闭系统吗？",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            QtGui.QMainWindow.close(self)
        elif reply == QtGui.QMessageBox.No:
            pass

    @staticmethod
    def get_unicode_content(table_index):
        try:
            content = table_index.text().toLocal8Bit()
            content = unicode(content, 'gbk', 'ignore')
            return content
        except Exception as e:
            print(e)

    @staticmethod
    def get_selected_rows(table_widget):
        rows = []
        for index in table_widget.selectedIndexes():
            if index.column() == 0:
                rows.append(index.row())
        rows = list(set(rows))  # 去除重复元素
        rows.sort()  # 升序
        rows.reverse()  # 颠倒
        return rows
