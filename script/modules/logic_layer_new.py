from abc import ABC, abstractclassmethod
from sqlalchemy.sql import exists
from sqlalchemy.orm import Session, joinedload, subqueryload
from sqlalchemy import func, create_engine, MetaData, inspect, and_
from .create_schema import *
from ..conf.setting import engine
import pandas as pd
import os

'''
Inputs from UI layer are in dict format. 
Outputs for logic layer: for queries, return pandas df(empty df for None).
                        for registration, return string 'Successful' or 'Fail'.
'''

class BaseEntity(ABC):
    def __init__(self):
        self.session = Session(bind=engine)

    def _check(self, single_tuple, colname):
        table_obj = eval(single_tuple[0])
        entry = single_tuple[1]
        result = self.session.query(table_obj).filter(getattr(table_obj, colname) == entry).first()
        return result

    def _check_relationships(self, input_tuple, colname='name'):
        result = dict((pair[0], self._check(pair, colname)) for pair in input_tuple) #check related instances first, if any existed, exit without checking instance to add
        if not input_tuple:
            print('no relationships')
            return True
        elif all(result.values()):
            print('all related instances are registered. new instance is OK to be registered')
            return True
        print('related instances not registered.')
        return False
        

class Courses(BaseEntity):
    def register(self, input_dict, colname):
        inst_to_add, *related_inst = input_dict.items()
        # input_tuple = list(input_dict.items())[0]
        new_existed= self._check(inst_to_add, colname)
        relation_existed = self._check_relationships(related_inst, colname)
        if (not new_existed) and relation_existed:
            table, course_name = inst_to_add
            new_inst = Course(name=course_name)
            self.session.add(new_inst)
            self.session.commit()
    def query(self):
        pass

class Students(BaseEntity):
    def register(self, email, name, course_name):
        course_checked = self._check(course_name)
        student_checked = self._check(email)
        if not course_checked:
            return 'Course not existed.'
        if not student_checked:
            new_instance = Student(email=email, name=name)
            course_checked.students.append(new_instance)
            self.session.add(new_instance)
            self.session.commit()
#     def query(self):
#         pass

class Lessons:
    pass
class Attendances:
    pass
class Score:
    pass
class Homework:
    pass

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

if __name__ == '__main__':
    a = Courses()
    a.register({'Course': 'chinese'}, 'name')

