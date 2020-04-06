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
    def __init__(self, user_response):
        #format of input_list: [{'new_table':{'colname':'new_value'}}, {'related_table':'value'}]
        self.session = Session(bind=engine)
        self._user_response = user_response

    def add(self):
        pass

    def query(self):
        pass

    def update(self):
        pass

    def _check_entry_existance(self, table_name, clause_col):
        obj = eval(table_name)
        columns = self._user_response[table_name]
        return self.session.query(exists().where(getattr(obj, clause_col)==columns[clause_col])).one()[0]

    def _get_student(self, columns):
        return self.session.query(Student).filter_by(**columns)

    def _get_course_instance(self, course_name):
        return self.session.query(Course).filter(Course.name==course_name).one_or_none()

    def _get_section(self, course_name, lesson_name):
        section_subquery_stmt = self.session.query(
            Course.id.label('course_id'), Lesson.id.label('lesson_id')
        ).filter(Course.name==course_name, Lesson.name==lesson_name).subquery()

        section, *_ = self.session.query(Section, section_subquery_stmt).\
            filter(
                Section.courses_id==section_subquery_stmt.c.course_id,
                Section.lessons_id==section_subquery_stmt.c.lesson_id
            )
        return section

    def _get_attendance(self, student, section):
        student_subquery = student.subquery()
        section_subquery = section.subquery()
        attendance, *_ = self.session.query(Attendance, student_subquery, section_subquery).\
            filter(
                Attendance.section_id==section_subquery.id,
                Attendance.stu_id==student_subquery.id
            )
        return attendance

    def _query_raw(self):
        student_columns = self._user_response['Student']
        course_name = self._user_response['Course']['name']
        lesson_name = self._user_response['Lesson']['name']

        student = self._get_student(student_columns)
        if not student.one_or_none():
            return 'Error. Student: {0}, email: {1} not found.'.format(student['name'], student['email'])
        section = self._get_section(course_name, lesson_name)
        if not section.one_or_none():
            return f'Error. {course_name} and/or {lesson_name} registered.'
        return self._get_attendance(student, section)
        

    def _to_df(self, query_obj):
        if not query_obj.first():
            return 'No results found.'
        df = pd.read_sql(query_obj.statement, con=engine)
        return df

class StudentMngr(BaseEntity):
    def add(self):
        '''
        logic:
        create a new student instance;
        add relationship with the 'course';
        query section where 'course' name is the same as student.course; Note: There are multiple instances;
        append section to student in order to update attendance.
        '''
        student = self._user_response['Student']
        course_name = self._user_response['Course']['name']

        new_entry_exist = self._check_entry_existance('Student', 'email')
        if new_entry_exist:
            return 'Student name: {1}, email: {0} already existed.'.format(student['email'], student['name'])

        course = self._get_course_instance(course_name)
        if not course:
            return f'Course {course_name} does not exist.'

        section_list = self._get_sections_from_course(course_name)
        if not section_list:
            return f'Course {course_name} has no registered lessons.'

        student = Student(**student)
        student.course = [course]
        student.section = section_list
        self.session.add(student)
        self.session.commit()
        return student
    
    def _get_sections_from_course(self, course_name):

        section_subquery_stmt = self.session.query(Course.id.label('course_id')).\
            filter(Course.name==course_name).subquery()
        section_stmt_list = self.session.query(Section, section_subquery_stmt).\
            filter(Section.courses_id==section_subquery_stmt.c.course_id).all() 
        section_list = [section for section, stmt in section_stmt_list]
        
        return section_list

    

class TeacherMngr(BaseEntity):
    def query(self):
        return self._check_entry_existance('Teacher', 'name')

class CourseMngr(BaseEntity):
    def add(self):
        course = self._user_response['Course']
        course = Course(**course)
        self.session.add(course)
        self.session.commit()

    def query(self):
        course_name = self._user_response['Course']
        result =  self.session.query(Course).filter_by(**course_name)

        return self._to_df(result)
        

class LessonMngr(BaseEntity):
    def add(self):
        '''
        logic:
        create a new lesson instance;
        add relationship with the 'course';
        query section with combined 'lesson' and 'course' instances. Note: there should be only one queried instance.
        query student which has the same 'course' name. Note: there are multiple student instances.
        append students to section so that attendance is added.
        '''
        lesson = self._user_response['Lesson']
        course_name = self._user_response['Course']['name']

        new_entry_exist = self._check_entry_existance('Lesson', 'name')
        if new_entry_exist:
            return 'lesson {0} already exist'.format(lesson['name'])

        course = self._get_course_instance(course_name)
        if not course:
            return f'course {course_name} does not exist.'

        section, student_list = self._get_students_section_from_course(course_name, lesson['name'])
        if not student_list:
            return f'Course {course_name} has no registered students.'

        lesson = Lesson(**lesson)
        lesson.course = [course]
        section.student = student_list
        self.session.add(lesson)
        self.session.commit()
        return lesson

    def _get_students_section_from_course(self, course_name, lesson_name):

        student_list = self.session.query(Student).join(Student.course).\
            filter(Course.name==course_name).all()

        section = self._get_section(course_name, lesson_name)
        
        return (section, student_list)


class AttendanceMngr(BaseEntity):
    '''
    attendance is added automatically whenever there is a new 'lesson' or 'student' instance.
    ''' 
    

    def update(self):
        
        attendance = self._query_raw().one_or_none()
        if isinstance(attendance, str):
            return attendance

        attendance.attend = self._user_response['Attendance']['attend']
        self.session.commit()
        return attendance
        


    def query(self):
        attendance = self._query_raw().statement
        df = self._to_df(attendance)
        if df.empty:
            return 'Combination of lesson, course and student not found.'
        return df


class ScoreMngr(BaseEntity):
    def update(self):
        
        attendance = self._query_raw().one_or_none()
        if isinstance(attendance, str):
            return attendance

        attendance.score = self._user_response['Attendance']['attend']
        self.session.commit()
        return attendance

    def query(self):
        '''
        order student.name and student.score by score according to course.
        '''
        # student_columns = self._user_response['Student']
        course_name = self._user_response['Course']['name']
        # lesson_name = self._user_response['Lesson']['name']

        # student = self._get_student(student_columns)
        # course = self._get_course_instance(course_name)
        # lesson = self._get_lesson(lesson_name).one_or_none()
        # section = self._get_section(course_name, lesson_name)
        # attendance = self._get_attendance(student, section)

        course = self.session.query(Course.id, Student.name.label('student_name')).filter(Course.name==course_name).subquery()


        section = self.session.query(Section.id.label('section_id'), Course.name.label('course_name'), course.c.student_name.label('student_name')).\
            filter(Section.courses_id==course.c.id).subquery()

        result = self.session.query(Attendance.score, section.c.course_name, section.c.student_name).\
            join(section, Attendance.section_id==section.c.section_id)

        print(self._to_df(result))

        


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
    a = ScoreMngr({'Course': {'name': 'python'}})
    print(a.query())

    # course = CourseMngr()
    # student = StudentMngr()
    # lesson = LessonMngr()
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


