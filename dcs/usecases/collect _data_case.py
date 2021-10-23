# -*- coding: utf-8 -*-
"""
@file: collection
@desc: 采集设备数据
@author: Jaden Wu
@time: 2021/10/2 15:33
"""
import time
from threading import Thread


class Collection(Thread):
    def __init__(self, gatherer, interval, monitor_num_list):
        super(Collection, self).__init__()
        self.gatherer = gatherer
        self.interval = interval
        self.monitor_num_list = monitor_num_list
        self.output_data = {}

    def run(self):
        while 1:
            for monitor_num in self.monitor_num_list:
                data = self.gatherer.get_data(monitor_num)
                self.output_data[monitor_num] = data
            time.sleep(self.interval)
