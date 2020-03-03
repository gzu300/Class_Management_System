#coding=utf-8

from conf.setting import engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Enum

Base = declarative_base()

class Teachers(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)

class Students(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False, unique=True)

class Lessons(Base):
    '''
    sessions.
    Usually different courses have different number of session.
    But here we assume all courses have same number duration.
    '''
    __tablename__ = 'lesson'

    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False, unique=True)

class Courses(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False, unique=True)

class Sessions(Base):
    '''
    records sessions for each course.
    Courses_Lessons m_to_m relationship set. 
    '''
    __tablename__ = 'session'

    id = Column(Integer, primary_key=True)
    courses_id =  Column(Integer, ForeignKey('course.id'))
    lessons_id = Column(Integer, ForeignKey('lesson.id'))

    courses = relationship('Courses', back_populates='sessions_m2m_courses')
    lessons = relationship('Lessons', back_populates='sessions_m2m_lessons')

class Attendance(Base):
    '''
    records attendance of each student for each session
    Sessions_Students m_to_m relationship set. 
    Additional attributes: homework, present_bool, score
    '''
    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True)
    homework = Column(String(100))
    score =  Column(Integer)
    sessions_id = Column(Integer, ForeignKey('session.id'))
    courses_id = Column(Integer, ForeignKey('course.id'))

    sessions = relationship('Sessions', back_populates='attendance_m2m_sesssions')
    lessons = relationship('Lessons', back_populates='attendance_m2m_lessons')

Base.metadata.create_all(engine)

