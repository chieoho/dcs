# -*- coding: utf-8 -*-
"""
@file: test_devices_view
@desc:
@author: Jaden Wu
@time: 2021/10/17 11:03
"""
from dcs.adapter.devices_view import EditController, EditModel


class View(object):
    pass


def test_devices_view():
    edit_model = EditModel()
    controller = EditController(edit_model, View())
