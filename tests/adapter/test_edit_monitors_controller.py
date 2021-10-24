# -*- coding: utf-8 -*-
"""
@file: test_edit_monitors_view
@desc:
@author: Jaden Wu
@time: 2021/10/17 11:03
"""
from dcs.usecases.add_monitors_case import monitor_fields
from dcs.adapter.edit_monitor_controller import EditMonitorsController
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from dcs.adapter.model import Base


class DB(object):
    name = "alarmrecords"
    uri = "sqlite://"


def make_session(engine_):
    Base.metadata.create_all(engine_)
    session_factory = sessionmaker(bind=engine_)
    session_obj = scoped_session(session_factory)
    session_ = session_obj()
    return session_


engine = create_engine(DB.uri)


class EditMonitorsView(object):
    def __init__(self):
        self.view_data = []

    def update_edit_table(self, edit_monitors_list):
        self.view_data = edit_monitors_list


def test_controller_add_monitor():
    view = EditMonitorsView()
    controller = EditMonitorsController(view, make_session(engine))
    res = controller.add_monitor_rows(1)
    assert res is True
    assert set(monitor_fields) == set(view.view_data[0].keys())


def test_controller_modify_monitor():
    modify_col = 1
    new_value = "01"

    view = EditMonitorsView()
    controller = EditMonitorsController(view, make_session(engine))
    controller.add_monitor_rows(1)
    res = controller.modify_monitor_row(0, modify_col, new_value)
    assert res is True
    assert view.view_data[0][monitor_fields[modify_col]] == new_value


def test_controller_delete_monitor():
    view = EditMonitorsView()
    controller = EditMonitorsController(view, make_session(engine))
    controller.add_monitor_rows(1)
    before_del_cnt = len(view.view_data)
    res = controller.delete_monitor_rows([0])
    after_del_cnt = len(view.view_data)
    assert res is True
    assert before_del_cnt - 1 == after_del_cnt
