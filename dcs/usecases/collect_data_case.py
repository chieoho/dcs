# -*- coding: utf-8 -*-
"""
@file: collection
@desc: 采集设备数据
@author: Jaden Wu
@time: 2021/10/2 15:33
"""


class CollectDataCase(object):
    def __init__(self, gatherer):
        super(CollectDataCase, self).__init__()
        self.gatherer = gatherer
        self.output_data = {}

    def get_data(self, monitor_code_list):
        self.output_data.clear()
        for monitor_code in monitor_code_list:
            data = self.gatherer.get_data(monitor_code)
            self.output_data[monitor_code] = data
        return self.output_data
