# -*- coding: utf-8 -*-
"""
@file: edit_detectors_view
@desc:
@author: Jaden Wu
@time: 2021/10/20 9:25
"""
from datetime import datetime

from dcs.usecases.add_detectors import AddDetectorsCase, detector_fields, detector_id
from dcs.usecases.get_detectors import GetDetectorsCase
from dcs.usecases.modify_detector import ModifyDetectorCase
from dcs.usecases.delete_detectors import DeleteDetectorsCase


to_view = {
    "decimal_point": str,
    "install_time": lambda it: str(it.date())
}


to_case = {
    "decimal_point": int,
    "install_time": lambda it: datetime.strptime(it, "%Y-%m-%d")
}


def identity(item):
    return item


edit_det_model = (
    "area",
    "address_code",
    "position",
    "decimal_point",
    "material",
    "unit",
    "install_time"
)


class EditDetectorsController(object):
    def __init__(self, repo, view):
        self.repo = repo
        self.view = view

        self.detectors_from_repo = []  # 主要为了保存行数与设备在数据库的id的对应关系

    def _update_edit_table(self):
        del self.detectors_from_repo[:]
        detectors_from_repo = GetDetectorsCase(self.repo).get_detectors()
        self.detectors_from_repo.extend(detectors_from_repo)
        edit_detectors_list = []
        for dev in self.detectors_from_repo:
            model = {k: to_view.get(k, identity)(dev[k]) for k in edit_det_model}
            edit_detectors_list.append(model)
        self.view.update_edit_table(edit_detectors_list)

    def add_detector_rows(self, row_content_list):
        detector_values_list = []
        for row_content in row_content_list:
            detector_info = {k: to_case.get(k, identity)(row_content[k]) for k in detector_fields}
            detector_values_list.append(detector_info)
        add_res = AddDetectorsCase(self.repo).add_detectors(detector_values_list)
        self._update_edit_table()
        return add_res

    def modify_detector_row(self, row, col, content):
        _id = self.detectors_from_repo[row][detector_id]
        new_detector_info = {detector_fields[col]: content}
        modify_res = ModifyDetectorCase(self.repo).modify_detector(_id, new_detector_info)
        self._update_edit_table()
        return modify_res

    def delete_detector_rows(self, rows):
        _id_list = map(lambda r: self.detectors_from_repo[r][detector_id], rows)
        delete_res = DeleteDetectorsCase(self.repo).delete_detectors(_id_list)
        self._update_edit_table()
        return delete_res
