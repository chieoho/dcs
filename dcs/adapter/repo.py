# -*- coding: utf-8 -*-
"""
@file: repo
@desc:
@author: Jaden Wu
@time: 2021/10/5 8:42
"""
from dcs.usecases.repo_if import MonitorRepoIf, DetectorRepoIf
from dcs.adapter.model import Monitor, Detector
from dcs.adapter.crud import CRUD


class MonitorRepo(MonitorRepoIf):
    def __init__(self, session):
        self.monitor_crud = CRUD(Monitor, session)

    def get_monitors(self):
        return self.monitor_crud.query({})

    def get_monitors_count(self):
        return self.monitor_crud.count({})

    def add_monitors(self, monitor_list):
        return self.monitor_crud.add(monitor_list)

    def modify_monitor(self, _id, new_monitor_info):
        return self.monitor_crud.update({"_id": [_id]}, new_monitor_info)

    def delete_monitors(self, _id_list):
        return self.monitor_crud.delete({"_id": _id_list})


class DetectorRepo(DetectorRepoIf):
    def __init__(self, session):
        self.detector_crud = CRUD(Detector, session)
        
    def get_detectors(self, monitor_code):
        return self.detector_crud.query({"monitor_code": [monitor_code]})
    
    def get_detectors_count(self, monitor_code):
        return self.detector_crud.count({"monitor_code": [monitor_code]})

    def add_detectors(self, detector_list):
        return self.detector_crud.add(detector_list)

    def modify_detector(self, _id, new_detector_info):
        return self.detector_crud.update({"_id": [_id]}, new_detector_info)

    def delete_detectors(self, _id_list):
        return self.detector_crud.delete({"_id": _id_list})
