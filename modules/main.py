#coding=utf-8

from sqlalchemy.orm import Session
from sqlalchemy import func
from .create_schema import *
from conf.setting import engine

class Operations(object):
    def __init__(self):
        self.session = Session(bind=engine)
        self.main()

    def initialize(self):
        print('Database is empty. Registering teacher Alex into system')
        cla = Courses(name='python')
        teacher = Teachers(name='Alex')
        lesson1 = Lessons(name='Day1')
        lesson2 = Lessons(name='Day2')
        self.session.add_all([cla, teacher, lesson1, lesson2])
        self.session.commit()

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
    
    def register_class(self):
        return
        

    def main(self):
        is_empty = self.session.query(func.count(Teachers.id)).scalar() == 0
        if is_empty:
            self.initialize()

        self.register()

    

    