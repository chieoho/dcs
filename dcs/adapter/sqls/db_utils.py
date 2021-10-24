# -*- coding: utf-8 -*-
"""
@file: db_utils
@desc:
@author: Jaden Wu
@time: 2021/10/23 22:54
"""


def create_database(engine, db_name, character="utf8mb4"):
    """
    服务启动时，没有db先创建db
    参考sqlalchemy-utils改写
    https://github.com/kvesteri/sqlalchemy-ms_utils/blob/master/sqlalchemy_utils/functions/database.py
    """
    if engine.name == "sqlite":
        return
    text = (
        "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA "
        "WHERE SCHEMA_NAME = '{}'".format(db_name)
    )
    result_proxy = engine.execute(text)
    result = result_proxy.scalar()
    result_proxy.close()
    database_exists = bool(result)
    if not database_exists:
        result_proxy = engine.execute(
            "CREATE DATABASE {0} CHARACTER SET = '{1}'".format(db_name, character)
        )
        result_proxy.close()
    engine.dispose()
