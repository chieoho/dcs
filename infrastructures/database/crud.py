# -*- coding: utf-8 -*-
"""
@file: crud
@desc:
@author: Jaden Wu
@time: 2021/10/4 22:41
"""
from functools import partial
from infrastructures.database import engine, make_session
from sqlalchemy import and_, or_


class CRUD:
    def __init__(self, model):
        self.model = model
        self.session = make_session(engine)

    def __del__(self):
        self.session.close()

    def add(self, records):
        for r in records:
            new_record = self.model(**r)
            self.session.add(new_record)
        self.session.commit()
        return True

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
            condition.append(or_(*list(map(lambda k: column.like('%{}%'.format(k)),
                                           search_keys_dict.get(key, [])))))
        return condition

    def _query(self, model, cond):
        for v in cond.values():
            if isinstance(v, list) is False:
                raise Exception('dict value in cond should be list')
        key_column_list = [(col, getattr(model, col)) for col in cond.keys()]
        condition = self._gen_query_condition(cond, key_column_list)
        query_obj = self.session.query(model).filter(and_(*condition))
        return query_obj

    def query(self, cond, ret_columns=()):
        if all(cond.values()):
            row2dict = partial(self.row2dict, col_names=ret_columns)
            query_obj = self._query(self.model, cond)
            results = list(map(row2dict, query_obj))
            return results
        return []

    def update(self, cond, new_info):
        query_obj = self._query(self.model, cond)
        for r in query_obj:
            for k, v in new_info.items():
                setattr(r, k, v)
        self.session.commit()
        return True

    def delete(self, cond):
        query_obj = self._query(self.model, cond)
        for r in query_obj:
            self.session.delete(r)
        self.session.commit()
        return True
