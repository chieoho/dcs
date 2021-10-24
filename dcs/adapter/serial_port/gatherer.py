# -*- coding: utf-8 -*-
"""
@file: gatherer
@desc:
@author: Jaden Wu
@time: 2021/10/24 10:43
"""
from define import *
from modbus_crc import modbus_crc16
import time


class Gatherer(object):
    def __init__(self, port):
        self.port = port
        self.num_data_dict = dict()

    def close_port(self):
        try:
            self.port.close()
        except Exception, e:
            print "'port.close' " + str(e)

    def process_recv_data(self, byte_len):
        recv_data = self.port.read(byte_len)
        if recv_data:
            return recv_data.encode('hex').upper()
        else:
            return recv_data  # ''

    def read_register(self, slave_num, start, length):
        start = int(start, 16)
        end = start + length
        step = 0xff
        seg_length = step
        ret_slave_num = 0
        ret_data = ''
        for seg_start in range(start, end, step):
            seg_end = seg_start + step  # 十进制和十六进制是可以直接运算的
            if seg_end > end:
                seg_length = end - seg_start
            seg_start = '%04x' % seg_start
            read_res = self.read_within_ff_register(slave_num, seg_start, seg_length)
            if read_res:
                ret_slave_num, data = read_res
            else:
                ret_slave_num, data = slave_num, ''
            ret_data += data
        if len(ret_data) != 2 * length:
            return False
        return ret_slave_num, ret_data

    def read_within_ff_register(self, slave_num, start_addr, length):
        length = '%04x' % int(length)
        if all([READ_CODE, start_addr, length]) is False:
            return False
        frame_content = slave_num + READ_CODE + start_addr + length
        crc_code = modbus_crc16(frame_content)
        str_cmd = frame_content + crc_code
        self.port.write(str_cmd.decode('hex'))

        ret_slave_num = self.process_recv_data(1)
        while ret_slave_num == DATA_HEAD[0: 2]:
            ret_slave_num = self.process_recv_data(1)
        if not ret_slave_num:
            return False
        ret_read_code = self.process_recv_data(1)
        if ret_read_code != READ_CODE:
            return False
        ret_data_len = self.process_recv_data(1)
        ret_data = self.process_recv_data(int(ret_data_len, 16))
        ret_frame_content = ret_slave_num + ret_read_code + ret_data_len + ret_data
        ret_crc_code = self.process_recv_data(2)
        if ret_crc_code is '':
            return False
        if ret_crc_code != modbus_crc16(ret_frame_content):
            while self.port.read(1) is not '':
                pass
            return False
        time.sleep(0.2)
        return ret_slave_num, ret_data

    def collect_detector_status_value(self, ctrller_num_lst, detector_qty_lst):
        for ctrller_num, detector_qty in zip(ctrller_num_lst, detector_qty_lst):
            detector_qty = int(detector_qty)
            status_res = self.read_register(ctrller_num, DETECTOR_STATUS_ADDR, DETECTOR_STATUS_LEN * detector_qty)
            value_res = self.read_register(ctrller_num, DETECTOR_VALUE_ADDR, DETECTOR_VALUE_LEN * detector_qty)
            if (not value_res) or (not status_res):
                yield False
            else:  # yield之后下次会接着运行，所以这里要用else
                ctrller_num_status, status_data = status_res
                ctrller_num_value, value_data = value_res
                if ctrller_num_status == ctrller_num_value == ctrller_num:
                    status_lst = (lambda s, n: [s[i: i + n] for i in xrange(0, len(s), n)])(status_data,
                                                                                            2 * DETECTOR_STATUS_LEN)
                    value_lst = (lambda s, n: [s[i: i + n] for i in xrange(0, len(s), n)])(value_data,
                                                                                           2 * DETECTOR_VALUE_LEN)
                    yield ctrller_num, status_lst, value_lst
                else:
                    yield False

    def collect_detector_unit_decimal_material(self, ctrller_num_lst, detector_qty_lst):
        for ctrller_num, detector_qty in zip(ctrller_num_lst, detector_qty_lst):
            unit_res = self.read_register(ctrller_num, DETECTOR_UNIT_ADDR, DETECTOR_UNIT_LEN * detector_qty)
            decimal_res = self.read_register(ctrller_num, DETECTOR_DECIMAL_ADDR, DETECTOR_DECIMAL_LEN * detector_qty)
            material_res = self.read_register(ctrller_num, DETECTOR_MATERIAL_ADDR, DETECTOR_MATERIAL_LEN * detector_qty)
            if not material_res or not decimal_res or not unit_res:
                yield False
            else:  # yield之后下次会接着运行，所以这里要用else
                ctrller_num_unit, unit_data = unit_res
                ctrller_num_decimal, decimal_data = decimal_res
                ctrller_num_material, material_data = material_res
                if ctrller_num_unit == ctrller_num_decimal == ctrller_num_material == ctrller_num:
                    unit_lst = (lambda s, n: [s[i: i + n] for i in xrange(0, len(s), n)])(unit_data,
                                                                                          2 * DETECTOR_UNIT_LEN)
                    decimal_lst = (lambda s, n: [s[i: i + n] for i in xrange(0, len(s), n)])(decimal_data,
                                                                                             2 * DETECTOR_DECIMAL_LEN)
                    material_lst = (lambda s, n: [s[i: i + n] for i in xrange(0, len(s), n)])(material_data,
                                                                                              2 * DETECTOR_MATERIAL_LEN)
                    yield ctrller_num, unit_lst, decimal_lst, material_lst
                else:
                    yield False

    def collect_ctrller_status(self, ctrller_num_lst):
        for ctrller_num in ctrller_num_lst:
            read_res = self.read_register(ctrller_num, CONTROLLER_STATUS_ADDR, 1)
            if not read_res:
                yield False
            else:  # yield之后下次会接着运行，所以这里要用else
                ret_ctrller_num, ret_data = read_res
                if ret_ctrller_num == ctrller_num:
                    status_lst = ret_data
                    yield ctrller_num, status_lst
                else:
                    yield False

    @staticmethod
    def calc_seg_addr(base_addr, obj_len, obj_num):
        return '%04x' % (int(base_addr, 16) + obj_len * obj_num)

    #  跨控制器指定探测器
    def collect_select_detector_info(self, ctrller_num_lst, detector_num_lst):
        for ctrller_num, detector_num in zip(ctrller_num_lst, detector_num_lst):
            value_seg_addr = self.calc_seg_addr(DETECTOR_VALUE_ADDR, DETECTOR_VALUE_LEN, detector_num)
            detector_value = self.read_register(ctrller_num, value_seg_addr, DETECTOR_VALUE_LEN)

            status_seg_addr = self.calc_seg_addr(DETECTOR_STATUS_ADDR, DETECTOR_STATUS_LEN, detector_num)
            detector_status = self.read_register(ctrller_num, status_seg_addr, DETECTOR_STATUS_LEN)

            unit_seg_addr = self.calc_seg_addr(DETECTOR_UNIT_ADDR, DETECTOR_UNIT_LEN, detector_num)
            detector_unit = self.read_register(ctrller_num, unit_seg_addr, DETECTOR_UNIT_LEN)

            decimal_seg_addr = self.calc_seg_addr(DETECTOR_DECIMAL_ADDR, DETECTOR_DECIMAL_LEN, detector_num)
            detector_decimal = self.read_register(ctrller_num, decimal_seg_addr, DETECTOR_DECIMAL_LEN)

            material_seg_addr = self.calc_seg_addr(DETECTOR_MATERIAL_ADDR, DETECTOR_MATERIAL_LEN, detector_num)
            detector_material = self.read_register(ctrller_num, material_seg_addr, DETECTOR_MATERIAL_LEN)

            if not all([detector_value, detector_status, detector_unit, detector_decimal, detector_material]):
                yield False
            else:  # yield之后下次会接着运行，所以这里要用else
                yield ctrller_num, detector_num, detector_value, detector_status, detector_unit, detector_decimal, \
                      detector_material
