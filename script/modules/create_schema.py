#coding=utf-8

from ..conf.setting import engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import Integer, String, Enum, Boolean

Base = declarative_base()
engine = engine

class Stu_Courses(Base):
    __tablename__ = 'student_m2m_course'
    
    id = Column(Integer, primary_key=True)
    students_id = Column(Integer, ForeignKey('student.id'))
    courses_id = Column(Integer, ForeignKey('course.id'))

# class Tea_Courses(Base):
#     __tablename__ = 'teacher_m2m_course'

#     id = Column(Integer, primary_key=True)
#     students_id = Column(Integer, ForeignKey('student.id'))
#     courses_id = Column(Integer, ForeignKey('course.id'))

Tea_Courses = Table(
    'teacher_m2m_course', Base.metadata,
    Column('teacher_id', Integer, ForeignKey('teacher.id')),
    Column('course_id', Integer, ForeignKey('course.id'))
)

class Teacher(Base):
    __tablename__ = "teacher"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)

class Lesson(Base):
    '''
    sessions.
    Usually different courses have different number of session.
    But here we assume all courses have same number duration.
    '''
    __tablename__ = 'lesson'

    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False, unique=True)

    courses = relationship('Course', secondary='session', backref='lesson')

class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False, unique=True)

    students = relationship('Student', secondary='student_m2m_course', backref='course')
    teachers = relationship('Teacher', secondary=Tea_Courses, backref='course')#lazy='joined' makes the relationship query a joined table with original tables. to be verified.

class Attendance(Base): 
    '''
    records attendance of each student for each session
    sessions_lessons m_to_m relationship set. 
    Additional attributes: homework, present_bool, score
    '''
    __tablename__ = 'attendance'

    homework = Column(String(100))
    score =  Column(Integer)
    attend = Column(Boolean)

    stu_id = Column(Integer, ForeignKey('student.id'), primary_key=True)
    session_id = Column(Integer, ForeignKey('session.id'), primary_key=True)

    session = relationship('Sessions', back_populates='student')
    student = relationship('Student', back_populates='session')

class Student(Base):
    #left
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False, unique=True)

    session = relationship('Attendance', back_populates='student')


class Sessions(Base):
    #right
    '''
    records sessions for each course.
    Courses_Lessons m_to_m relationship set. 
    '''
    __tablename__ = 'session'

    id = Column(Integer, primary_key=True)
    courses_id =  Column(Integer, ForeignKey('course.id'))
    lessons_id = Column(Integer, ForeignKey('lesson.id'))

    student = relationship('Attendance', back_populates='session')


Base.metadata.create_all(engine)





