# -*- coding: utf-8 -*-
"""
@file: local_gatherer
@desc:
@author: Jaden Wu
@time: 2021/10/25 10:32
"""
import time
from kafka import KafkaConsumer
import serial

consumer = KafkaConsumer('port-write', bootstrap_servers=['139.198.168.173:9092'])

elapsed = []
for msg in consumer:
    elapsed.append(time.time() - float(msg.value))
    print(sum(elapsed) / len(elapsed))
