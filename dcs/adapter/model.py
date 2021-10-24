# -*- coding: utf-8 -*-
"""
@file: model
@desc:
@author: Jaden Wu
@time: 2021/10/4 21:54
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Monitor(Base):
    __tablename__ = "monitor"
    _id = Column(Integer, primary_key=True)
    area = Column(String(32))
    code = Column(String(16))
    detector_num = Column(Integer)
    install_time = Column(DateTime)
    phone_num_1 = Column(String(11))
    phone_num_2 = Column(String(11))
    phone_num_3 = Column(String(11))
    phone_num_4 = Column(String(11))


class Detector(Base):
    __tablename__ = "detector"
    _id = Column(Integer, primary_key=True)
    area = Column(String(32))
    monitor_code = Column(String(16))
    address_code = Column(String(16))
    position = Column(String(128))
    decimal_point = Column(Integer)
    material = Column(String(16))
    unit = Column(String(16))
    install_time = Column(DateTime)
