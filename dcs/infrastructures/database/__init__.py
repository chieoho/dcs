# -*- coding: utf-8 -*-
"""
@file: __init__
@desc:
@author: Jaden Wu
@time: 2021/10/4 21:56
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from dcs.adapter.sqls.model import Base
from dcs.adapter.sqls.db_utils import create_database


class DB(object):
    name = "alarmrecords"
    uri = "sqlite:///%s.db" % name


def make_session(engine_):
    Base.metadata.create_all(engine_)
    session_factory = sessionmaker(bind=engine_)
    session_obj = scoped_session(session_factory)
    session_ = session_obj()
    return session_


create_database(create_engine(DB.uri.replace(DB.name, "")), DB.name)  # 开始还没有db
engine = create_engine(DB.uri)
