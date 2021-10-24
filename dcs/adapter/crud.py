# -*- coding: utf-8 -*-
"""
@file: crud
@desc:
@author: Jaden Wu
@time: 2021/10/4 22:41
"""
from functools import partial
from sqlalchemy import and_, or_


class CRUD:
    def __init__(self, model, session):
        self.model = model
        self.session = session

    def __del__(self):
        self.session.close()

    @staticmethod
    def row2dict(query_obj, col_names):
        d = {}
        if query_obj:
            for column in query_obj.__table__.columns:
                name = column.name
                if (not col_names) or (name in col_names):
                    d[name] = getattr(query_obj, name)
        return d

    @staticmethod
    def _gen_query_condition(search_keys_dict, key_column_list):
        condition = []
        for key, column in key_column_list:
            condition.append(or_(*(map(lambda k: column == k,
                                       search_keys_dict.get(key, [])))))
        return condition

    def _query(self, model, cond):
        for v in cond.values():
            if isinstance(v, list) is False:
                raise Exception('dict value in cond should be list')
        key_column_list = [(col, getattr(model, col)) for col in cond.keys()]
        condition = self._gen_query_condition(cond, key_column_list)
        if condition:
            query_obj = self.session.query(model).filter(and_(*condition))
        else:
            query_obj = self.session.query(model)
        return query_obj

    def query(self, cond, ret_columns=()):
        """
        返回table中符合条件的记录
        :param cond: 条件  如： {"year": ["2001", "2002"], "security_classification": [1]}
                               表示年度为2001或2002且密级为1的记录
        :param ret_columns: 指定返回列，为空时返回全部列  如：("verify_state", "recog_state")
        :return: 记录列表
        """
        if all(cond.values()):
            row2dict = partial(self.row2dict, col_names=ret_columns)
            query_obj = self._query(self.model, cond)
            results = list(map(row2dict, query_obj))
            return results
        return []

    def count(self, cond):
        if all(cond.values()):
            query_obj = self._query(self.model, cond)
            return query_obj.count()
        return 0

    def add(self, records):
        """
        往table添加多条记录
        :param records: 记录信息列表
        :return: 成功返回True，失败返回False
        """
        for r in records:
            new_record = self.model(**r)
            self.session.add(new_record)
        self.session.commit()
        return True

    def update(self, cond, new_info):
        """
        更新table中符合条件的记录
        :param cond: 条件  如： {"year": ["2001", "2002"], "security_classification": [1]}
                              表示年度为2001或2002且密级为1的记录
        :param new_info: 需更新的字段及对应值
        :return: 成功返回True，失败返回False
        """
        query_obj = self._query(self.model, cond)
        for r in query_obj:
            for k, v in new_info.items():
                setattr(r, k, v)
        self.session.commit()
        return True

    def delete(self, cond):
        """
        删除table中符合条件的记录
        :param cond: 条件  如： {"year": ["2001", "2002"], "security_classification": [1]}
                              表示年度为2001或2002且密级为1的记录
        :return: 成功返回True，失败返回False
        """
        query_obj = self._query(self.model, cond)
        for r in query_obj:
            self.session.delete(r)
        self.session.commit()
        return True
