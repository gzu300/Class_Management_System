from abc import ABC, abstractclassmethod
from sqlalchemy.orm import Session, joinedload, subqueryload
from sqlalchemy import func, create_engine, MetaData, inspect, and_
from sqlalchemy.inspection import inspect
from .create_schema import *
from ..conf.setting import engine
import sqlalchemy
import pandas as pd
import os
'''
Inputs from UI layer are in dict format. 
Outputs for logic layer: for queries, return pandas df(empty df for None).
                        for registration, return string 'Successful' or 'Fail'.
'''

class BaseEntity(ABC):
    def __init__(self):
        #format of input_list: [{'new_table':{'colname':'new_value'}}, {'related_table':'value'}]
        self.session = Session(bind=engine)

    def _get_columns(self, mapper):
        return {mapper.class_.__name__: mapper.columns.keys()[1:]}

    def _release_items(self, user_response):
        new_entry, *related_entry = user_response
        self._new_tbl_name, *_ = new_entry
        self._new_tbl_cols = new_entry[self._new_tbl_name]
        return new_entry, related_entry

    def _query(self, entry_dict):
        result_list = []
        for table, cols_value in entry_dict.items():
            result_list.append(self.session.query(eval(table)).filter_by(**cols_value).first())
        return result_list

    def _add(self, entry_dict):
        self._new_entry = eval(self._new_tbl_name)(**entry_dict[self._new_tbl_name])
        try:
            self.session.add(self._new_entry)
            self.session.flush() #flush the db to test for exception
        except sqlalchemy.exc.IntegrityError:
            self.session.rollback()
            print('registration failed due to entry already existed.')
            return 
        return self._new_entry
        

    def _append_relation(self, related_entry):
        if not related_entry:
            return
        result = self._query(related_entry[0]) #there should be only one elemnt in the list...
        try:
            for related_obj in result:
                getattr(related_obj, self._new_tbl_name.lower()).append(self._new_entry)
        except AttributeError:
            self.session.rollback()
            print(f'registration failed since related column does not exist. register first.')

    def register(self, user_response):
        new_entry, related_entry = self._release_items(user_response)
        added = self._add(new_entry)
        if added:
            self._append_relation(related_entry)
            self.session.commit()
            print('registration done')



#####
#Functions
#####

def initialize():
    session = Session(bind=engine)
    if session.query(Teacher).count() == 0:
        print('Database is empty. Registering teacher Alex into system')
        teacher = Teacher(name='Alex')
        session.add(teacher)
        session.commit()
        session.close()

def get_columns(table):
    return eval(table).__table__.c.keys()[1:]

def get_mngr():
    eval()


if __name__ == '__main__':
    a = BaseEntity()
    a.register([{'Student': {'name': 'zhu', 'email': 'zhu.com'}}, {'Course': {'name': 'python'}}])
    


