# -*- coding: utf-8 -*-
"""
@file: define
@desc:
@author: Jaden Wu
@time: 2021/10/24 10:43
"""

DATA_HEAD = 'FFFF'
READ_CODE = '03'

CONTROLLER_STATUS_ADDR = '1000'
CONTROLLER_STATUS_LEN = 1
DETECTOR_VALUE_ADDR = '2000'
DETECTOR_VALUE_LEN = 3
DETECTOR_STATUS_ADDR = '3000'
DETECTOR_STATUS_LEN = 1
DETECTOR_UNIT_ADDR = '4000'
DETECTOR_UNIT_LEN = 1
DETECTOR_DECIMAL_ADDR = '5000'
DETECTOR_DECIMAL_LEN = 1
DETECTOR_MATERIAL_ADDR = '6000'
DETECTOR_MATERIAL_LEN = 1

INVALID_VALUE = '---'


class Undefine(object):
    TEXT = u'未定义'
    COLOR = 'Orange'


class CtrllerWiringFault(object):
    STATUS = u'连线故障'
    COLOR = 'Orange'


CTRLLER_COLOR_DICT = {
 '00': '#00FF00',  # 绿色
 '01': 'Orange',
 '02': 'Orange',
 '03': 'Orange'
}

CTRLLER_STATUS_DICT = {
  '00': u'正常',
  '01': u'主电欠压',
  '02': u'备电欠压',
  '03': u'备电连线故障',
}

NORMAL_STATUS = '00'
NOT_NORMAL_COLOR_LST = ['Red', 'Orange']

DETECTOR_COLOR_DICT = {
   '00': '#00FF00',  # 绿色
   '01': 'Red',
   '02': 'Red',
   '03': 'White',
   '04': 'Orange',
   '05': 'White',
   '06': 'Orange',
   '07': 'Red',
   '08': 'Red',
   '09': 'Red',
   '0A': '#00FF00',
   '0B': 'Red',
   '0C': 'Red',
   '0D': 'White',
   '0E': '#00FF00',
   '0F': '#00FF00'
}  

DETECTOR_STATUS_DICT = {
  '00': u'正常',
  '01': u'低限报警',
  '02': u'高限报警',
  '03': u'屏蔽',
  '04': u'连线故障',
  '05': u' ',  # 未定义（状态栏不显示任何内容）,
  '06': u'传感器故障',
  '07': u'低限报警转传感器故障',  
  '08': u'高限报警转传感器故障',  
  '09': u'高限报警转低限报警',  
  '0A': u' ',  # 未定义（状态栏不显示任何内容）
  '0B': u'低限报警转连线故障',  
  '0C': u'高限报警转连线故障',
  '0D': u' ',  # 未定义（状态栏不显示任何内容）
  '0E': u'低限报警恢复',
  '0F': u'高限报警恢复'
}        


CTRL_MODEL_STATUS_DICT = {
  '0F0E0B': u'高限断开/低限断开',
  '0F0E1B': u'高限断开/低限闭合',
  '0F1E1B': u'高限闭合/低限闭合'
}
                              

MATERIAL_DICT = {
    '00': u'有毒气体',
    '01': u'可燃气体 ',
    '02': u'一氧化碳 ',
    '03': u'氧气',
    '04': u'氢气',  
    '05': u'甲烷 ',
    '06': u'丙烷',
    '07': u'二氧化碳',
    '08': u'臭氧 ',
    '09': u'硫化氢 ',
    '0A': u'二氧化硫',
    '0B': u'氨气',
    '0C': u'氯气',
    '0D': u'环氧乙烷',
    '0E': u'氯化氢',
    '0F': u'磷化氢',
    '10': u'溴化氢',
    '11': u'氰化氢',
    '12': u'三氢化砷',
    '13': u'氟化氢',
    '14': u'溴气',
    '15': u'一氧化氮',
    '16': u'二氧化氮',
    '17': u'氮氧化物',
    '18': u'二氧化氯',
    '19': u'硅烷',
    '1A': u'二硫化碳',
    '1B': u'氟气',
    '1C': u'乙硼烷',
    '1D': u'锗烷',
    '1E': u'氮气',
    '1F': u'四氢噻吩',
    '20': u'乙炔',
    '21': u'乙烯',
    '22': u'甲醛',
    '23': u'液化石油气',
    '24': u'碳氢',
    '25': u'苯',
    '26': u'过氧化氢',
    '27': u'VOC',
    '28': u'六氟化硫', 
    '29': u'甲苯',
    '2A': u'联乙烯',
    '2B': u'氧硫化碳',
    '2C': u'联氨',
    '2D': u'硒化氢',
    '2E': u'苯乙烯',
    '2F': u'异丁烯',
    '30': u'亚甲基',
    '31': u'笑气',
    '32': u'天然气',
    '33': u'光气',
    '34': u'氯乙烯',
    '35': u'甲醇',
    '36': u'乙醇',
    '37': u'异丙醇',
    '38': u'丙酮',
    '39': u'乙醛',
    '3A': u'丙烯腈',
    '3B': u'二甲基硫醚',
    '3C': u'环氧氯丙烷',
    '3D': u'乙酸乙酯',
    '3E': u'甲基乙基酮',
    '3F': u'甲硫醇',
    '40': u'四氯乙烯',
    '41': u'亚硫酰氯',
    '42': u'乙酸乙烯酯',
    '43': u'硫醇TBM',
    '44': u'TVOC',
    '45': u'环已烷',
    '46': u'三氯乙烯',
    '47': u'二甲苯',
    '48': u'氟利昂',
    '49': u'一氯甲烷',
    '4A': u'二氯甲烷',
    '4B': u'三氯甲烷',
    '4C': u'一甲胺',
    '4D': u'正戊烷',
    '4E': u'正己烷',
    '4F': u'正庚烷',
    '50': u'异辛烷',
    '51': u'乙烷',
    '52': u'石油醚',
    '53': u'丁烷',
    '54': u'直流电流',
    '55': u'交流电流',
    '56': u'直流电压',
    '57': u'交流电压',
    '58': u'PM2.5',
    '59': u'PM10',
    '5A': u'温度',
    '5B': u'湿度',
    '5C': u'压力',
    '5D': u'流量'
}

UNIT_DICT = {
    '00': u'%LEL',
    '01': u'%VOL',
    '02': u'PPM',
    '03': u'PPb',
    '04': u'特殊单位',
    '05': u'mg/m3',
    '06': u'ug/m3',
    '07': u'V',
    '08': u'mV',
    '09': u'mA',
    '10': u'A',
    '11': u'℃',
    '12': u'%RH',
    '13': u'hPa',
    '14': u'mBar',
    '15': u'Bar',
    '16': u'kPa',
    '17': u'MPa',
    '18': u'mL/min',
    '19': u'L/min',
    '20': u'm3/h',
    'undefined': ' '
}
