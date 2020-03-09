#coding=utf-8
from sqlalchemy.sql import exists
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, create_engine, MetaData, inspect
from .create_schema import *
from ..conf.setting import engine
import pandas as pd
import os

class AdminMngr(object):
    pass
'''
    def __init__(self, user, password, host):
        self.user = user
        self.password = password
        self.host = host
    
    def initialize(self):
        tmp_engine = create_engine('mysql+mysqldb://{0}:{1}@{2}'.format(self.user, self.password, self.host), echo=True)
        tmp_engine.execute('CREATE DATABASE IF NOT EXISTS class_management')
        tmp_engine.dispose()

        self.session = Session(bind=engine)

    def reboot(self):
        Base.metadata.create_all(engine)

    def connect(self):
        self.__engine = create_engine('mysql+mysqldb://{0}:{1}@{2}'.format(self.user, self.password, self.host), echo=True)

    def command(self, command):
        # engine = create_engine('mysql+mysqldb://root:sp880922@localhost', echo=True)
        self.__engine.execute(command)

    def dispose(self):
        self.__engine.dispose()

    def check_teacher(self, name):
        Base.metadata.reflect(bind=engine)
        print(Base.metadata.tables)
        # metadata = MetaData()
        # metadata.reflect(self.__engine)
        # print(metadata)
        #return result

    def rgt_teacher(self, name):
        pass
    # def initialize(self):
    #     if self.session.query(func.count(Teachers.id)).scalar() == 0:
    #         print('Database is empty. Registering teacher Alex into system')
    #         teacher = Teachers(name='Alex')
    #         self.session.add(teacher)
    #         self.session.commit()
    #         self.session.close()
'''
class Operations(object):
    def __init__(self):
        self.session = Session(bind=engine)

    def check(self, obj, c_name, name):
        result = self.session.query(obj).filter(getattr(obj, c_name)==name).first()
        return result
    # def check(self, obj, name):
    #     #used for teacher's and student's name check
    #     result = self.session.query(obj).filter(obj == name).first()
    #     return result

    def q_t(self, obj, related_c):
        to_join = getattr(obj, related_c)
        result = self.session.query(obj).options(joinedload(to_join))
        if not result.first():
            return pd.DataFrame()
        list2 = getattr(result.first(), related_c)[0].__table__.c#get columns of related tables
        list1 = result.first().__table__.c

        df = pd.read_sql(result.statement, con=engine)
        df.columns = list1+list2
        return df
    
    def rgt(self):
        return

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
    def authenticate(self, enter):
        self.t_name = enter
        auth = Operations.check(self, obj=Teachers, c_name='name', name=enter)
        return auth

    def check_course(self, enter):
        existed = Operations.check(self, obj=Courses, c_name='name', name=enter)
        return existed
    
    def check_student(self, email):
        self.student = Operations.check(self, obj=Students, c_name='email', name=email)
        return self.student

    def q_t_courses(self):
        return Operations.q_t(self, obj=Courses, related_c='teachers')
        # result = self.session.query(Courses).statement
        # result = self.session.query(Teachers).first()
        # print(result.teachers[0].name)
        # breakpoint()
        # df = pd.read_sql(result.statement, con=engine)
        # return df

    def q_t_students(self):
        return Operations.q_t(self, obj=Students, related_c='courses')

    def rgt_course(self, name):
        '''
        This method return the name of the course
        if course existed. return None
        '''
        course = self.check_course(enter=name)
        if not course:
            course = Courses(name=name) #when the course not exist. init a new Course instance  
        teacher = self.session.query(Teachers).filter(Teachers.name==self.t_name).first()
        course.teachers.append(teacher)
        self.session.add(course)
        self.session.commit()

    def rgt_student(self, email, name, c_name):
        student = self.check_student(email=email)
        course = self.check_course(enter=c_name)
        if not course:
            return 
        if not student:
            student = Students(email=email, name=name)
        course = self.session.query(Courses).filter(Courses.name==c_name).first()
        course.students.append(student)
        self.session.add(student)
        self.session.commit()
        return True #this is to be consistant with condition in ui.add_student_view
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

if __name__ == '__main__':
    a = AdminMngr(user='root', password='sp880922', host='localhost')
    a.check_teacher('alex')
