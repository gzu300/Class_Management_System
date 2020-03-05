#coding=utf-8
from sqlalchemy.orm import Session
from conf.setting import engine
from .create_schema import *

class TeacherMngr(object):
    '''
    - Register new course
    - Rigister student into a course
    - Register a new session
    - Query who enrolled the course
    - Query a student's enrollment
    - Record attendance of studnts
    - Give scores for students's hw for every session
    '''
    def __init__(self):
        self.session = Session(bind=engine)

    def rgt_course(self, user, course_name):
        course_name = course_name.lower()
        course_exist = self.session.query(Courses.name).filter(Courses.name == course_name).first()
        if not course_exist:
            course = Courses(name=course_name)
            print('='*10, '{0}, {1} has beed registered.'.format(user, course_name), '='*10, sep='\n')
            self.session.add(course)
            self.session.commit()
        else:
            print('Course \'{0}\' already existed.'.format(course_name))

    def rgt_student(self):
        '''
        letter q is not a valid selection'
        '''
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

class StudentMngr(object):
    '''
    -Submit hw
    -See the ranking for a course.
    '''
    def submit(self):
        return
    def query(self):
        return
