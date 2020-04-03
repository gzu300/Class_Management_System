from abc import ABC, abstractclassmethod
from sqlalchemy.orm import Session, joinedload, subqueryload
from sqlalchemy import func, create_engine, MetaData, inspect, and_
from sqlalchemy.inspection import inspect
from sqlalchemy.sql import exists
from .create_schema import *
from ..conf.setting import engine
import sqlalchemy
import pandas as pd
import os
'''
Inputs from UI layer are in dict format. 
Outputs for logic layer: for queries, return pandas df(empty df for None).
                        for registration, return string 'Successful' or 'Fail'.

THIS IS A TOTAL FAILURE. THIS PATTERN MADE ME STRUGGLE IN THE MUD. RATHER THAN THIS
SHITTY LOGIC RETRIEVEING COLUMNS AND RELATED COLUMNS, EXIPLICITILY EACH OPERATION ON
DIFFERENT TABLES IS MORE FEASIBLE AND CLEAR.

THIS IS THE LESSON TO BE LEARNED!!!!!
'''

class BaseEntity(ABC):
    def __init__(self):
        #format of input_list: [{'new_table':{'colname':'new_value'}}, {'related_table':'value'}]
        self.session = Session(bind=engine)
    @abstractclassmethod
    def add(self):
        pass
    @abstractclassmethod
    def query(self):
        pass
    @abstractclassmethod
    def update(self):
        pass


class TeacherMngr(BaseEntity):
    def query(self, user_response):
        teacher_name = user_response['Teacher']['name']
        teacher = self.session.query(Teacher).filter(Teacher.name==teacher_name).one_or_none()

        return teacher

    def update(self):
        pass

class CourseMngr(BaseEntity):
    def add(self, user_response):
        course = user_response['Course']
        course = Course(**course)
        self.session.add(course)
        self.session.commit()

    def query(self, user_response):
        result = self.session.query(Course)
        if not result.first():
            return 'No results found.'
        df = pd.read_sql(result.statement, con=engine)
        return df

    def update(self):
        pass

class StudentMngr(BaseEntity):
    def add(self, user_response):
        '''
        logic:
        create a new student instance;
        add relationship with the 'course';
        query section where 'course' name is the same as student.course; Note: There are multiple instances;
        append section to student in order to update attendance.
        '''
        student = user_response['Student']
        course_name = user_response['Course']['name']

        student = Student(**student)
        course = self.session.query(Course).filter(Course.name==course_name).one_or_none()
        student.course = [course]

        section_subquery_stmt = self.session.query(Course.id.label('course_id')).\
            filter(Course.name==course.name).subquery()
        section_stmt_list = self.session.query(Section, section_subquery_stmt).\
            filter(Section.courses_id==section_subquery_stmt.c.course_id).all() 
        section_list = [section for section, stmt in section_stmt_list]

        student.section = section_list
        self.session.add(student)
        self.session.commit()

    def update(self):
        pass
    def query(self):
        pass

class LessonMngr(BaseEntity):
    def add(self, user_response):
        '''
        logic:
        create a new lesson instance;
        add relationship with the 'course';
        query section with combined 'lesson' and 'course' instances. Note: there should be only one queried instance.
        query student which has the same 'course' name. Note: there are multiple student instances.
        append students to section so that attendance is added.
        '''
        lesson = user_response['Lesson']
        course_name = user_response['Course']['name']

        lesson = Lesson(**lesson)
        course = self.session.query(Course).filter(Course.name==course_name).one_or_none()
        lesson.course = [course]

        student_list = self.session.query(Student).join(Student.course).\
            filter(Course.name==course_name).all()

        section_subquery_stmt = self.session.query(
            Course.id.label('course_id'), Lesson.id.label('lesson_id')
        ).filter(Course.name==course.name, Lesson.name==lesson.name).subquery()

        section, *_ = self.session.query(Section, section_subquery_stmt).\
            filter(
                Section.courses_id==section_subquery_stmt.c.course_id,
                Section.lessons_id==section_subquery_stmt.c.lesson_id
            ).one_or_none()

        section.student = student_list
        self.session.add(lesson)
        self.session.commit()

    def update(self):
        pass
    def query(self):
        pass



class AttendanceMngr(BaseEntity):
    def add(self):
        '''
        attendance is added automatically whenever there is a new 'lesson' or 'student' instance.
        '''
        pass

    def update(self):
        pass
    def query(self):
        pass

class ScoreMngr(BaseEntity):
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

def get_columns(table):
    return eval(table).__table__.c.keys()[1:]

def query_student(obj, **kwargs):
    results = obj.session.query(Student).options(joinedload(Student.course)).filter_by(**kwargs)
    print(pd.read_sql(results.statement, con=engine))


if __name__ == '__main__':
    course = CourseMngr()
    student = StudentMngr()
    lesson = LessonMngr()
    # course.add({'Course':{'name': 'python'}})

    # student.add({'Student': {'email': 'zhu.com', 'name': 'zhu'}, 'Course': {'name': 'python'}})
    
    # # added a new lesson
    # lesson.add({'Lesson': {'name': 'day1'}, 'Course':{'name': 'python'}})

    # # add another new student
    # student.add({'Student': {'email': 'xia.com', 'name': 'xia'}, 'Course': {'name': 'python'}})

    # if students, lessons in different courses affect with each other  
    # course.add({'Course':{'name': 'linux'}})
    # student.add({'Student': {'email': '1.com', 'name': '1'}, 'Course': {'name': 'linux'}})
    # lesson.add({'Lesson': {'name': '3rd'}, 'Course':{'name': 'linux'}})


