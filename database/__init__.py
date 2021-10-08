# -*- coding: utf-8 -*-
"""
@file: __init__
@desc:
@author: Jaden Wu
@time: 2021/10/4 21:56
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()


def create_database(url, database, character="utf8mb4"):
    """
    服务启动时，没有db先创建db
    参考sqlalchemy-utils改写
    https://github.com/kvesteri/sqlalchemy-ms_utils/blob/master/sqlalchemy_utils/functions/database.py
    """
    engine_ = create_engine(url)
    if "sqlite:" in url:
        return
    text = (
        "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA "
        "WHERE SCHEMA_NAME = '{}'".format(database)
    )
    result_proxy = engine_.execute(text)
    result = result_proxy.scalar()
    result_proxy.close()
    database_exists = bool(result)
    if not database_exists:
        result_proxy = engine_.execute(
            "CREATE DATABASE {0} CHARACTER SET = '{1}'".format(database, character)
        )
        result_proxy.close()
    engine_.dispose()


class DB(object):
    name = "alarmrecords"
    uri = "sqlite:///%s.db" % name


def make_session(engine_):
    Base.metadata.create_all(engine_)
    session_factory = sessionmaker(bind=engine_)
    session_obj = scoped_session(session_factory)
    session_ = session_obj()
    return session_


create_database(DB.uri.replace(DB.name, ""), DB.name)  # 开始还没有db
engine = create_engine(DB.uri)
