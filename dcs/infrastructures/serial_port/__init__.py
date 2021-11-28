# -*- coding: utf-8 -*-
"""
@file: __init__.py
@desc:
@author: Jaden Wu
@time: 2021/10/24 18:22
"""
import serial


def init_port(port, brt, timeout, raise_or_not=False, parity='M', byte_size=8, stop_bits=1):
    try:
        # 超时会接收到空字符串，超时以一次读操作来算，跟读多少字节没关系
        port = serial.Serial(port=port, baudrate=brt, bytesize=byte_size,
                             parity=parity, stopbits=stop_bits, timeout=timeout,  # 单位为秒
                             writeTimeout=60)
        return port
    except serial.SerialException as e:
        print(e)
        if raise_or_not:
            raise e
