#coding=utf-8
from sqlalchemy.sql import exists
from sqlalchemy.orm import Session, joinedload, subqueryload
from sqlalchemy import func, create_engine, MetaData, inspect, and_
from .create_schema import *
from ..conf.setting import engine
import pandas as pd
import os

class Operations(object):
    def __init__(self):
        self.session = Session(bind=engine)
        self.initialize()

    def check(self, obj, c_name, name):
        '''
        return the first object found. Otherwise, return empty list.
        '''
        if hasattr(obj, c_name):
            result = self.session.query(obj).filter(getattr(obj, c_name)==name).first()
            return result
        

    def q_t(self, obj, related_c):
        '''
        Query and print obj and obj's related table.
        '''
        df = pd.DataFrame()
        to_join = getattr(obj, related_c)
        result = self.session.query(obj).options(joinedload(to_join))#equal to join two tables in sql.
        if result.first():
            list2 = getattr(result.first(), related_c)[0].__table__.c#get columns of related tables
            list1 = result.first().__table__.c

            df = pd.read_sql(result.statement, con=engine)
            df.columns = ['_'.join(str(each).split('.')) for each in list1+list2]#'.' affects the indexing later
        return df
    
    def rgt(self, rgtObj, checkObj, rgt_c_name, check_c_name, rgt_name, check_name, related_c, **kwargs):
        '''
        This method return the name of the course
        if course existed. return None
        '''
        rgt = self.check(rgtObj, rgt_c_name, rgt_name)
        check = self.check(checkObj, check_c_name, check_name)

        if not check:
            return
        if not rgt:
            rgt = rgtObj(**kwargs)
        getattr(rgt, related_c).append(check)#column name in relations is designed to be the same as Obj
        self.session.add(rgt)
        self.session.commit()
        return True


    def initialize(self).:
        if self.session.query(Teachers).count() == 0:
            print('Database is empty. Registering teacher Alex into system')
            teacher = Teachers(name='Alex')
            self.session.add(teacher)
            self.session.commit()
            self.session.close()

class TeacherMngr(Operations):
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
        Operations.__init__(self)
        self.view = 'teacher_view'

    def authenticate(self, enter):
        self.t_name = enter
        return self.check_teacher(enter)

    def check_teacher(self, enter):
        auth = Operations.check(self, obj=Teachers, c_name='name', name=enter)
        return auth

    def check_course(self, enter):
        existed = Operations.check(self, obj=Courses, c_name='name', name=enter)
        return existed
    
    def check_student(self, email):
        self.student = Operations.check(self, obj=Students, c_name='email', name=email)
        return self.student

    def check_lesson(self, lesson):
        existed = Operations.check(self, obj=Lessons, c_name='name', name=lesson)
        return existed

    def q_t_lessons(self, enter):
        result = Operations.q_t(self, obj=Lessons, related_c='courses')
        if not result.empty: #In combination with courses,
                             #lessons give too many rows.
                             #To select rows of indicated lesson names.
                             #empty df has now col names.
                             #to to exclude them.
            result = result.loc[result.course_name==enter, :]
        return result

    def q_t_courses(self):
        return Operations.q_t(self, obj=Courses, related_c='teachers')

    def q_t_students(self):
        return Operations.q_t(self, obj=Students, related_c='courses')

    def q_t_attendance(self, lesson, course):
        '''
        This method is different from other q_t methods. More arguments are needed.
        '''
        lessons = self.check_lesson(lesson=lesson)
        courses = self.check_course(enter=course)

        df = pd.DataFrame()
        if all([lessons, courses]):
            stmt = self.session.query(Sessions).\
                filter(and_(
                    Sessions.courses_id==courses.id,
                    Sessions.lessons_id==lessons.id
                )).subquery()

            result = self.session.query(Attendance.homework, Attendance.score, Attendance.attend, Students.name, Students.email, Lessons.name, Courses.name).\
                    filter(and_(
                        Attendance.session_id==stmt.c.id,
                        Attendance.stu_id==Students.id,
                        Courses.id==stmt.c.courses_id,
                        Lessons.id==stmt.c.lessons_id
                    ))
            df = pd.read_sql(result.statement, con=engine)   
        return df

    def rgt_course(self, name):
        '''
        This method return the name of the course
        if course existed. return None
        '''
        course = self.check_course(enter=name)
        teacher = self.check_teacher(enter=self.t_name)
        if not course:
            return
        course = Courses(name=name) #when the course not exist. init a new Course instance
        course.teachers.append(teacher)
        self.session.add(course)
        self.session.commit()
        return True                     #this is to be consistant with condition in ui.add_student_view

    def rgt_student(self, email, name, c_name):
        student = self.check_student(email=email)
        course = self.check_course(enter=c_name)
        if (not course) or student:
            return
        student = Students(email=email, name=name)
        course.students.append(student)
        self.session.add(student)
        self.session.commit()
        return True 

    def rgt_lesson(self, lesson, course):
        courses = self.check_course(enter=course)
        lessons = self.check_lesson(lesson=lesson)
        if (not courses) or lessons:
            return
        lessons = Lessons(name=lesson)
        courses.lessons.append(lessons)
        self.session.add(lessons)
        self.session.commit()
        return True

        # return self.rgt(Lessons, Courses, 'name', 'name', lesson, course, 'courses', name='courses')

    def rgt_attendance(self, lesson, course, student_email, if_attended=None):
        '''
        This method is a little bit complicated then the others. Here are the steps:
        First. it has to check all the Table objects exist upon arguments.
        Second. Then therer is possibility that relationships are missing even though objects exist.
                So it adds the relationships for course-student and lesson-course. This is essentional
                for the next step.
        Third. Locate the entry(row) of object from Session table.
        Forth. Add relationships for session-student. 
               For example: We have the following relstionships. a-b. b-c. 
               Since ORM could not tell there is relationship between a-c. So have to add explicitly
        Fifth. Locate the value of attend in attendance table and make assignment. 
        Finally. commit
        '''

        #check existance of prerequisites
        lessons = self.check_lesson(lesson=lesson)
        courses = self.check_course(enter=course)
        students = self.check_student(email=student_email)
        if not all([lessons, courses, students]):
            return

        #append relationship if not added.
        courses.students.append(students)
        lessons.courses.append(courses)

        #check and locate the Session table object
        session = self.session.query(Sessions).\
            filter(and_(
                Sessions.courses_id==courses.id,
                Sessions.lessons_id==lessons.id
            )).first() #Sessions table is a relationship table.
               #So query this table needs ids. Maybe in the future
               #a unique name could be added as index. But now
               #let's leave it like this first.
        if not session: # this shouldn't happen as previous step already added this entry of Session table.
            return
        
        '''
        # for chained joinedloads, the first item must return the object that can be used for the second joinedload
        # result = self.session.query(Sessions).options(joinedload(Sessions.students))
        # print(pd.read_sql(session.statement, con=engine))
        '''
        
        check = self.session.query(Attendance).\
            filter(
                and_(
                    Attendance.stu_id==students.id,
                    Attendance.session_id==session.id
                )
            ).first()

        if check:
            return

        #assign attendance
        attendance = Attendance(attend=if_attended)
        attendance.session_r = session
        attendance.student_r = students #this is different from sqlalchemy ORM tutorial.
                                        #Without this, student_id in attendance is None and cause error.
        students.sessions.append(attendance)
        #commit
        self.session.commit()
        return True

    def score(self, score):
        #check the existance
        for attendance in self.session.query(Sessions).first().students:
            print(attendance.attend)
        
        # give score
        # attendance.score = score
        # self.session.commit()
        # return True


    def test(self, name):
        student = self.session.query(Students).join(Students.courses).\
            filter(Courses.name==name).all()
        print(self.session.query(Students).join(Students.courses).first().__dict__)
        print(name)
        print(student)

class StudentMngr(Operations):
    '''
    -Submit hw
    -See the ranking for a course.
    '''
    def __init__(self):
        Operations.__init__(self)
        self.view = 'student_view'
    def submit(self):
        return
    def query(self):
        return

if __name__ == '__main__':
    a = TeacherMngr()
    a.score(10)

