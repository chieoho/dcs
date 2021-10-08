# -*- coding: utf-8 -*-
"""
@file: repo_if
@desc:
@author: Jaden Wu
@time: 2021/10/8 21:48
"""


class RepoIf(object):
    def add_controllers(self, controller_list):
        pass

    def get_controllers(self):
        pass

    def delete_controllers(self, id_list):
        pass

    def modify_controllers(self, _id, controller_info):
        pass


repo_if = RepoIf()