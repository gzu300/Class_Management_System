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

    def _get_course(self, columns):
        return self.session.query(Course).filter_by(**columns)

    def _get_lesson(self, columns):
        return self.session.query(Lesson).filter_by(**columns)

    def _get_section(self, course_name, lesson_name):
        section_subquery_stmt = self.session.query(
            Course.id.label('course_id'), Lesson.id.label('lesson_id'),
            Course.name.label('course_name'), Lesson.name.label('lesson_name')
        ).filter(Course.name==course_name, Lesson.name==lesson_name).subquery()

        section = self.session.query(Section, section_subquery_stmt.c.course_name.label('course_name'), section_subquery_stmt.c.lesson_name.label('lesson_name')).\
            filter(
                Section.courses_id==section_subquery_stmt.c.course_id,
                Section.lessons_id==section_subquery_stmt.c.lesson_id
            )
        return section

    def _get_attendance(self, student, section):
        student_subquery = student.subquery()
        section_subquery = section.subquery()
        attendance = self.session.query(Attendance, student_subquery, section_subquery.c.course_name, section_subquery.c.lesson_name).\
            filter(
                Attendance.section_id==section_subquery.c.id,
                Attendance.stu_id==student_subquery.c.id
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
        return self._get_attendance(student, section) #a query object

    def _get_sections_from_course(self, course_name):

        section_subquery_stmt = self.session.query(Course.id.label('course_id')).\
            filter(Course.name==course_name).subquery()
        section_stmt_list = self.session.query(Section, section_subquery_stmt).\
            filter(Section.courses_id==section_subquery_stmt.c.course_id).all() 
        section_list = [section for section, stmt in section_stmt_list]
        
        return section_list

    def _get_students_from_course(self, course_name):
        student_list = self.session.query(Student).join(Student.course).\
            filter(Course.name==course_name).all()
        return student_list

        

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
        student_c = self._user_response['Student']
        course_c = self._user_response['Course']
        course_name = course_c['name']

        student_q = self._get_student(student_c)
        course_q = self._get_course(course_c)

        #exit when the course does not exist
        if not course_q.one_or_none():
            return f'Course {course_name} does not exist.'
        #exit when the student, the course exist and they already related
        student_course_exist = student_q.join(Student.course).filter(Course.name==course_name).one_or_none()
        if student_course_exist:
            return 'Student name: {1}, email: {0} already existed.'.format(student_c['email'], student_c['name'])


        section_list = self._get_sections_from_course(course_name)
        student = student_q.one_or_none()
        course = course_q.one_or_none()

        if not student:
            student = Student(**student_c)
        student.course.append(course)
        for each in section_list:
            student.section.append(each)
        self.session.add(student)
        self.session.commit()
        return student

    def query(self):
        return self._check_entry_existance('Student', 'email')
    
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
        lesson_c = self._user_response['Lesson']
        course_c = self._user_response['Course']
        course_name = course_c['name']

        course_q = self._get_course(course_c)
        lesson_q = self._get_lesson(lesson_c)

        if not course_q.one_or_none():
            return f'Course {course_name} does not exist.'

        lesson_course_exist = lesson_q.join(Lesson.course).filter(Course.name==course_name).one_or_none()
        if lesson_course_exist:
            return 'Lesson {1} for Course {0} already existed.'.format(course_name, lesson_c['name'])



        student_list = self._get_students_from_course(course_name)
        course = course_q.one_or_none()
        lesson = lesson_q.one_or_none()

        if not lesson:
            lesson = Lesson(**lesson_c)
        lesson.course.add(course)
        section = self._get_section(course_c['name'], lesson_c['name']).one_or_none()[0]
        for each in student_list:
            section.student.append(each)
        self.session.add(lesson)
        self.session.commit()
        return lesson

    def query(self):
        pass

    def _get_students_section_from_course(self, course_name, lesson_name):
        '''
        This is a special method only used in LessonMngr. Since relationship is between student and Section, which
        itself is a relationship as well, whenever we added a new lesson entry we need to retrieve the newly generated
        section and existed student. Only then we could buid relationship between student and section.
        Therefore this method returns two result, list of student and section for the add method above.
        '''
        student_list = self.session.query(Student).join(Student.course).\
            filter(Course.name==course_name).all()

        section = self._get_section(course_name, lesson_name).one_or_none()
        
        return (section, student_list)

class TeacherMngr(BaseEntity):
    def query(self):
        return self._check_entry_existance('Teacher', 'name')

class CourseMngr(BaseEntity):
    def add(self):
        course = self._user_response['Course']
        if not self._check_entry_existance('Course', 'name'):
            course = Course(**course)
            self.session.add(course)
            self.session.commit()
            return course
        return 'Course {0} already exist.'.format(course['name'])

    def query(self):
        course_name = self._user_response['Course']
        result =  self.session.query(Course).filter_by(**course_name)

        return self._to_df(result)
        



class AttendanceBaseMngr(BaseEntity):
    '''
    attendance is added automatically whenever there is a new 'lesson' or 'student' instance.
    ''' 
    

    def _update(self, column, value, func):
        
        attendance = self._query_raw()
        if isinstance(attendance, str):
            return attendance
        attendance, *_ = attendance.one_or_none()
        setattr(attendance, value, func(self._user_response[column][value]))
        self.session.commit()
        return attendance

    def _query(self, column):
        attendance = self._query_raw()
        if isinstance(attendance, str):
            return attendance
        att_sub = attendance.subquery()
        attendance = self.session.query(getattr(att_sub.c, column), att_sub.c.name, att_sub.c.email, att_sub.c.course_name, att_sub.c.lesson_name)
        df = self._to_df(attendance)
        return df

class AttendanceMngr(AttendanceBaseMngr):
    def update(self):
        return self._update('Attendance', 'attend', int)

    def query(self):
        return self._query('attend')


class ScoreMngr(AttendanceBaseMngr):
    
    def update(self):
        return self._update('Score', 'score', int)


    def query(self):
        '''
        order student.name and student.score by score according to course.
        '''
        course_name = self._user_response['Course']['name']
        lesson_name = self._user_response['Lesson']['name']
        
        section = self._get_section(course_name, lesson_name)
        student = self.session.query(Student) # select all the students
        attendance = self._get_attendance(student, section).subquery()
        rank = self.session.query(
            attendance.c.score,
            attendance.c.name,
            attendance.c.email,
            attendance.c.course_name,
            attendance.c.lesson_name
        ).order_by(attendance.c.score.desc())

        return self._to_df(rank)    

class HomeworkMngr(AttendanceBaseMngr):
    def update(self):
        return self._update('Homework', 'homework', str)

    def query(self):
        return self._query('homework')

    

        


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
    pass

