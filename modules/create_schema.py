#coding=utf-8

from conf.setting import engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import Integer, String, Enum

Base = declarative_base()

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

class Attendance(Base):
    '''
    records attendance of each student for each session
    sessions_lessons m_to_m relationship set. 
    Additional attributes: homework, present_bool, score
    '''
    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True)
    homework = Column(String(100))
    score =  Column(Integer)
    stu_cou_id = Column(Integer, ForeignKey('student_m2m_course.id'))
    lessons_id = Column(Integer, ForeignKey('lesson.id'))

    # sessions = relationship('Sessions', back_populates='attendance_m2m_sesssions')
    # lessons = relationship('Lessons', back_populates='attendance_m2m_lessons')

    

class Teachers(Base):
    __tablename__ = "teacher"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)

class Students(Base):
    __tablename__ = 'student'

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

    attendance = relationship('Stu_Courses', secondary='attendance', backref='lessons')

class Courses(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False, unique=True)

    students = relationship('Students', secondary='student_m2m_course', backref='courses')
    teachers = relationship('Teachers', secondary=Tea_Courses, backref='courses', lazy='joined')#lazy='joined' makes the relationship query a joined table with original tables. to be verified.

# class Sessions(Base):
#     '''
#     records sessions for each course.
#     Courses_Lessons m_to_m relationship set. 
#     '''
#     __tablename__ = 'session'

#     id = Column(Integer, primary_key=True)
#     courses_id =  Column(Integer, ForeignKey('course.id'))
#     lessons_id = Column(Integer, ForeignKey('lesson.id'))

#     courses = relationship('Courses', back_populates='courses_m2m_lessons')
#     lessons = relationship('Lessons', back_populates='courses_m2m_lessons')

Base.metadata.create_all(engine)

