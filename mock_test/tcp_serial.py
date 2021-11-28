# -*- coding: utf-8 -*-
"""
@file: local.py
@desc:
@author: Jaden Wu
@time: 2021/10/25 18:01
"""
import struct
import socket


HEAD_STRUCT = '>I'
head_size = struct.calcsize(HEAD_STRUCT)


class Serial:
    def __init__(self):
        # server = ("139.198.168.173", 20002)
        server = ("192.168.3.12", 8080)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(server)

    def write(self, data):
        # head = struct.pack(HEAD_STRUCT, len(data))
        self.sock.sendall(data)

    def read(self, size):
        # head_data = self.sock.recv(head_size)
        # while len(head_data) < head_size:
        #     head_data += self.sock.recv(head_size - len(head_data))
        # data_size, = struct.unpack(HEAD_STRUCT, head_data)
        data = self.sock.recv(size)
        while len(data) < size:
            data += self.sock.recv(size - len(data))
        return data

    def close(self):
        pass
        # self.sock.close()
