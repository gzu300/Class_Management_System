#coding=utf-8

from sqlalchemy.orm import Session
from sqlalchemy import func
from .create_schema import *
from .ui import ui
from .logic_layer import *
from conf.setting import engine
import sys
import pdb

class Operations(object):
    def __init__(self):
        self.session = Session(bind=engine)
        self.ui = ui()

    def initialize(self):
        print('Database is empty. Registering teacher Alex into system...')
        cla = Courses(name='python')
        teacher = Teachers(name='Alex')
        lesson1 = Lessons(name='Day1')
        lesson2 = Lessons(name='Day2')
        self.session.add_all([cla, teacher, lesson1, lesson2])
        self.session.commit()

    def categorize(self):
        self.category = None
        while not self.category:
            cat_input = self.ui.categorize().strip()
            if cat_input == '1': #teacher
                self.category = 'Teachers'
            elif  cat_input == '2': #student
                self.category = 'Students' 
            elif cat_input == '3': #exit
                sys.exit()
            else:
                print('\n'*5, 'You have entered an invalid selection.')
    
    def authenticate(self):
        self.user_exist = None
        while not self.user_exist:
            if self.category == 'Teachers':
                user = self.ui.t_login()
                self.user_exist = self.session.query(Teachers).filter(Teachers.name == user).first()
                if self.user_exist:
                    self.user=user
            elif self.category == 'Students':
                user = self.ui.s_login()
                self.user_exist = self.session.query(Students).filter(Students.email == user).first()    
            else:
                self.user_exist=None
                print('Auth type is wrong. should be String type')

    def register(self):
        name = input('Enter student name:')
        email = input('Enter student email:')
        course = input('Enter student course:')


        stu = Students(name=name, email=email)
        course = self.session.query(Courses).filter(Courses.name == course).first()#associate course with student
        course.students.append(stu)#insert course.id and student.id into 'Stu_Course' table
        self.session.add(stu)
        self.session.commit()
        print('Student {0} with email {1} has been registered.'.format(name, email))
    
    def teacher_action(self):
        while True:
            operation = self.ui.teacher_view(self.user)
            if operation == '2':
                self.course_name = self.ui.add_course_view()
                self.mngr.rgt_course(self.user, self.course_name)
            elif operation == '8':
                sys.exit()
            else:
                print('\n'*5, 'Please enter a valid selection.')
    def student_action(self):
        pass
        

    def main(self):
        is_empty = self.session.query(func.count(Teachers.id)).scalar() == 0
        if is_empty:
            self.initialize()
        self.categorize()
        while True:
            self.authenticate()
            if self.category == 'Teachers':
                self.mngr = TeacherMngr()
                self.teacher_action()
            elif self.category == 'Students':
                self.mngr = StudentMngr()
                self.student_action()


    def test(self):
        result = self.session.query(Courses.name).filter(Courses.name == 'python').scalar()
        print(type(result))