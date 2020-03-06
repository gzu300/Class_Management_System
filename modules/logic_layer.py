#coding=utf-8
from sqlalchemy.sql import exists
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from .create_schema import *
from conf.setting import engine
import pandas as pd

class Operations(object):
    def __init__(self):
        self.session = Session(bind=engine)

    def check(self, obj, name):
        ext = exists().where(obj == name)

        result = self.session.query(obj).filter(ext).all()
        return result
    # def check(self, obj, name):
    #     #used for teacher's and student's name check
    #     result = self.session.query(obj).filter(obj == name).first()
    #     return result
    def initialize(self):
        if self.session.query(func.count(Teachers.id)).scalar() == 0:
            print('Database is empty. Registering teacher Alex into system')
            teacher = Teachers(name='Alex')
            self.session.add(teacher)
            self.session.commit()
            self.session.close()

class TeacherMngr(Operations):
    '''
    - Register new course
    - Rigister student into a course
    - Register a new session
    - Query who enrolled the course
    - Query a student's enrollment
    - Record attendance of studnts
    - Give scores for students's hw for every session
    '''
    def authenticate(self, name):
        self.t_name = name
        auth = Operations.check(self, obj=Teachers.name, name=name)
        return auth

    def check_course(self, name):
        existed = Operations.check(self, obj=Courses.name, name=name)
        return existed
    
    def check_student(self, email):
        existed = Operations.check(self, obj=Students.email, name=email)
        return existed

    def q_t_courses(self, c_name):
        result = self.session.query(Courses).\
            filter_by(name = c_name).statement
        # result = self.session.query(Teachers).first()
        # print(result.teachers[0].name)
        # breakpoint()
        df = pd.read_sql(result, con=engine)
        return df

    def rgt_course(self, name):
        '''
        This method return the name of the course
        if course existed. return None
        '''
        course = Courses(name=name)
        teacher = self.session.query(Teachers).filter(Teachers.name==self.t_name).first()
        course.teachers.append(teacher)
        self.session.add(course)
        self.session.commit()
    def rgt_student(self):
        return
    def rgt_session(self):
        return
    def rec_attendance(self):
        return
    def score(self):
        return
    def query_student(self):
        return
    def query_course(self):
        return

class StudentMngr(Operations):
    '''
    -Submit hw
    -See the ranking for a course.
    '''
    def submit(self):
        return
    def query(self):
        return
