# -*- coding: utf-8 -*-
"""
@file: modbus_crc
@desc:
@author: Jaden Wu
@time: 2021/10/24 10:43
"""


def modbus_crc16(hex_str):
    """
    计算Modbus CRC16的值
    :param hex_str:
    :return:crc value: str
    """
    # data = bytearray.fromhex(unicode(hex_str))
    data = bytearray.fromhex(hex_str)
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for i in range(8):
            if (crc & 1) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    crc = ((crc & 0x00FF) << 8) + (crc >> 8)  # 高八位与低八位互换
    crc_value = '%04X' % crc
    return crc_value


if __name__ == '__main__':
    print modbus_crc16("010301000001")
    print modbus_crc16('abcdef')
    print modbus_crc16('010303000000')
