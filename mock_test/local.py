# -*- coding: utf-8 -*-
"""
@file: remote_gatherer
@desc:
@author: Jaden Wu
@time: 2021/10/25 10:29
"""
import time
from kafka import KafkaProducer, KafkaConsumer

producer = KafkaProducer(bootstrap_servers='139.198.168.173:9092')
consumer = KafkaConsumer('port-write', bootstrap_servers=['139.198.168.173:9092'])

while 1:
    producer.send('port-write', str(time.time()))
