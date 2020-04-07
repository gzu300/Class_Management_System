#coding=utf-8

from ..conf.setting import engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Session, relationship, backref, subqueryload, aliased
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import Integer, String, Enum, Boolean, and_
from sqlalchemy.inspection import inspect

Base = declarative_base()
engine = engine

class Stu_Courses(Base):
    __tablename__ = 'student_m2m_course'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    course_id = Column(Integer, ForeignKey('course.id'))

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
    name = Column(String(50), nullable=False, unique=True)

class Lesson(Base):
    '''
    sections.
    Usually different courses have different number of section.
    But here we assume all courses have same number duration.
    '''
    __tablename__ = 'lesson'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    course = relationship('Course', secondary='section', backref='lesson', collection_class=set)

class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    student = relationship('Student', secondary='student_m2m_course', backref='course', collection_class=set)
    teacher = relationship('Teacher', secondary=Tea_Courses, backref='course', collection_class=set)#lazy='joined' makes the relationship query a joined table with original tables. to be verified.

class Student(Base):
    #left
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)

    # section = relationship('Attendance', back_populates='student')
    section = association_proxy('attendance', 'section', creator=lambda sec: Attendance(section=sec))

class Attendance(Base): 
    '''
    records attendance of each student for each section
    sections_lessons m_to_m relationship set. 
    Additional attributes: homework, present_bool, score
    '''
    __tablename__ = 'attendance'

    homework = Column(String(100), nullable=True)
    score =  Column(Integer, nullable=True)
    attend = Column(Boolean, nullable=True)

    stu_id = Column(Integer, ForeignKey('student.id'), primary_key=True)
    section_id = Column(Integer, ForeignKey('section.id'), primary_key=True)

    student = relationship(Student, backref=backref('attendance',
                                                    cascade='all, delete-orphan'), collection_class=set)
    section = relationship('Section', backref=backref('attendance',
                                                    cascade='all, delete-orphan'), collection_class=set)

    def __init__(self, student=None, section=None):
        self.student=student
        self.section=section
        # self.homework=homework
        # self.score=score
        # self.attend=attend



class Section(Base):
    #right
    '''
    records sections for each course.
    Courses_Lessons m_to_m relationship set. 
    '''
    __tablename__ = 'section'
    id = Column(Integer, primary_key=True)
    courses_id =  Column(Integer, ForeignKey('course.id'))
    lessons_id = Column(Integer, ForeignKey('lesson.id'))

    student = association_proxy('attendance', 'student', creator=lambda stu: Attendance(student=stu))

Base.metadata.create_all(engine)

if __name__ == '__main__':
    session = Session(bind=engine)
    # python = Course(name='python')
    # linux = Course(name='linux')

    # python.student = [Student(email='zhu.com', name='zhu'), Student(email='xia.com', name='xia')]
    python = session.query(Course).filter(Course.name=='python').first()
    python.lesson.append(Lesson(name='day1'))

    stmt = session.query(Course.id.label('course_id'), Lesson.id.label('lesson_id')).filter(and_(Course.name=='python', Lesson.name=='day1')).subquery()
    section, *_ = session.query(Section, stmt).filter(and_(Section.courses_id==stmt.c.course_id, Section.lessons_id==stmt.c.lesson_id)).first()

    student = session.query(Student).options(subqueryload(Student.course)).filter(Course.name=='python').all()
    for each in student:
        section.student.append(each)
    session.add_all([section])
    session.commit()