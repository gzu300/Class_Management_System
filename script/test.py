import unittest
from .modules.logic_layer import LessonMngr, StudentMngr, CourseMngr, AttendanceMngr, HomeworkMngr, ScoreMngr, initialize
from .modules.create_schema import Session, Student, Course, Lesson, Section, Attendance
from .conf.setting import engine
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.sql import exists
from sqlalchemy import and_
import pandas as pd

class TestLesson(unittest.TestCase):
    def setUp(self):
        initialize()
        self.session = Session(bind=engine)

    def test_add_nostudent(self):
        course = CourseMngr({'Course': {'name': 'python_test1'}})
        course_ = course.add()
        user_response1 = {'Lesson': {'name': 'test_day1'}, 'Course': {'name': 'python_test1'}}
        lesson1 = LessonMngr(user_response1)
        lesson1_ = lesson1.add()
        result = self.session.query(exists().where(and_(
            Section.courses_id==course_.id,
            Section.lessons_id==lesson1_.id
        ))).one()[0]
        self.assertTrue(result)
    def test_add_hasstudent(self):
        course = CourseMngr({'Course': {'name': 'python_test1'}})
        course_ = course.add()
        student = StudentMngr({'Student': {'name': 'zhu', 'email': 'zhu.com'},  'Course': {'name': 'python_test1'}})
        student.add()
        user_response1 = {'Lesson': {'name': 'test_day1'}, 'Course': {'name': 'python_test1'}}
        lesson1 = LessonMngr(user_response1)
        lesson1_ = lesson1.add()
        result = self.session.query(exists().where(and_(
            Section.courses_id==course_.id,
            Section.lessons_id==lesson1_.id
        ))).one()[0]
        self.assertTrue(result)

    def test_add_no_course(self):
        user_response1 = {'Lesson': {'name': 'test_day1'}, 'Course': {'name': 'python_test1'}}
        lesson1 = LessonMngr(user_response1)
        result1 = lesson1.add()
        self.assertEqual(result1, 'Course python_test1 does not exist.')

    def test_add_lesson_course_duplicate(self):
        course = CourseMngr({'Course': {'name': 'python_test1'}})
        course.add()
        user_response1 = {'Lesson': {'name': 'test_day1'}, 'Course': {'name': 'python_test1'}}
        lesson1 = LessonMngr(user_response1)
        lesson1.add()
        result = lesson1.add()
        self.assertEqual(result, 'Lesson test_day1 for Course python_test1 already existed.')

    def test_add_only_link_course(self):
        course1 = CourseMngr({'Course': {'name': 'python_test1'}})
        course1.add()
        course2 = CourseMngr({'Course': {'name': 'python_test2'}})
        course2.add()
        user_response1 = {'Lesson': {'name': 'test_day1'}, 'Course': {'name': 'python_test1'}}
        lesson1 = LessonMngr(user_response1)
        lesson1.add()
        user_response2 = {'Lesson': {'name': 'test_day1'}, 'Course': {'name': 'python_test2'}}
        lesson2 = LessonMngr(user_response2)
        result2 = lesson2.add()
        python_test1, python_test2 = result2.course
        self.assertEqual(set([python_test1.name, python_test2.name]), set(['python_test1', 'python_test2']))
        

    def tearDown(self):
        try:
            result1 = self.session.query(Course).filter(Course.name=='python_test1').first()
            self.session.delete(result1)
        except UnmappedInstanceError:
            pass
        try:
            result2 = self.session.query(Course).filter(Course.name=='python_test2').first()
            self.session.delete(result2)
        except UnmappedInstanceError:
            pass
        try:
            student1 = self.session.query(Lesson).filter(Lesson.name=='test_day1').first()
            self.session.delete(student1)
        except UnmappedInstanceError:
            pass
        try:
            student1 = self.session.query(Student).filter(Student.email=='zhu.com').first()
            self.session.delete(student1)
        except UnmappedInstanceError:
            pass
        self.session.commit()

class TestStudent(unittest.TestCase):
    def setUp(self):
        initialize()
        self.session = Session(bind=engine)
        
    def test_add_no_course(self):
        user_response1 = {'Student': {'name': 'zhu', 'email': 'zhu.com'},  'Course': {'name': 'python_test1'}}
        student1 = StudentMngr(user_response1)
        result1 = student1.add()
        self.assertEqual(result1, 'Course python_test1 does not exist.')

    def test_add_student_course_duplicate(self):
        course = CourseMngr({'Course': {'name': 'python_test1'}})
        course.add()
        user_response1 = {'Student': {'name': 'zhu', 'email': 'zhu.com'},  'Course': {'name': 'python_test1'}}
        student1 = StudentMngr(user_response1)
        student1.add()
        result2 = student1.add()
        self.assertEqual(result2, 'Student name: zhu, email: zhu.com already existed.')

    def test_add_only_link_course(self):
        course1 = CourseMngr({'Course': {'name': 'python_test1'}})
        course1.add()
        course2 = CourseMngr({'Course': {'name': 'python_test2'}})
        course2.add()
        user_response1 = {'Student': {'name': 'zhu', 'email': 'zhu.com'},  'Course': {'name': 'python_test1'}}
        student1 = StudentMngr(user_response1)
        student1.add()
        user_response2 = {'Student': {'name': 'zhu', 'email': 'zhu.com'},  'Course': {'name': 'python_test2'}}
        student2 = StudentMngr(user_response2)
        result2 = student2.add()
        python_test1, python_test2 = result2.course
        self.assertEqual(python_test1.name, 'python_test1')
        self.assertEqual(python_test2.name, 'python_test2')

    def tearDown(self):
        try:
            result1 = self.session.query(Course).filter(Course.name=='python_test1').first()
            self.session.delete(result1)
        except UnmappedInstanceError:
            pass
        try:
            result2 = self.session.query(Course).filter(Course.name=='python_test2').first()
            self.session.delete(result2)
        except UnmappedInstanceError:
            pass
        try:
            student1 = self.session.query(Student).filter(Student.email=='zhu.com').first()
            self.session.delete(student1)
        except UnmappedInstanceError:
            pass
        self.session.commit()

class TestCourse(unittest.TestCase):
    def setUp(self):
        initialize()
        self.session = Session(bind=engine)
        self._user_response = {'Course': {'name': 'python_test1'}}
    def test_add(self):
        course = CourseMngr(self._user_response)
        course.add()
        answer = self.session.query(exists().where(Course.name==self._user_response['Course']['name'])).one()[0]
        self.assertTrue(answer)
    
    def test_add_duplicate(self):
        course = CourseMngr(self._user_response)
        course.add()
        second = course.add()
        self.assertEqual(second, 'Course python_test1 already exist.')

    def tearDown(self):
        result = self.session.query(Course).filter(Course.name=='python_test1').first()
        self.session.delete(result)
        self.session.commit()

class TestAttendance(unittest.TestCase):
    def setUp(self):
        initialize()
        self.session = Session(bind=engine)

    def test_add_and_query_attendance(self):
        course = CourseMngr({'Course': {'name': 'python_test1'}})
        course.add()
        user_response1 = {'Student': {'name': 'zhu', 'email': 'zhu.com'},  'Course': {'name': 'python_test1'}}
        student1 = StudentMngr(user_response1)
        student1.add()
        user_response1 = {'Lesson': {'name': 'test_day1'}, 'Course': {'name': 'python_test1'}}
        lesson1 = LessonMngr(user_response1)
        lesson1.add()
        user_response = {'Course': {'name': 'python_test1'},
                        'Student': {'name': 'zhu', 'email': 'zhu.com'},
                        'Lesson': {'name': 'test_day1'},
                        'Attendance': {'attend': '1'}}
        attendance = AttendanceMngr(user_response)
        result = attendance.update()
        self.assertEqual(result.attend, 1)
        query_result = attendance.query().iloc[0, :].values.tolist()
        query_answer = [True, 'zhu', 'zhu.com', 'python_test1', 'test_day1']
        self.assertEqual(query_result, query_answer)


    def tearDown(self):
        try:
            result1 = self.session.query(Course).filter(Course.name=='python_test1').first()
            self.session.delete(result1)
        except UnmappedInstanceError:
            pass
        try:
            result2 = self.session.query(Lesson).filter(Lesson.name=='test_day1').first()
            self.session.delete(result2)
        except UnmappedInstanceError:
            pass
        try:
            student1 = self.session.query(Student).filter(Student.email=='zhu.com').first()
            self.session.delete(student1)
        except UnmappedInstanceError:
            pass
        self.session.commit()

class TestHomework(unittest.TestCase):
    def setUp(self):
        initialize()
        self.session = Session(bind=engine)

    def test_add_and_query_homework(self):
        course = CourseMngr({'Course': {'name': 'python_test1'}})
        course.add()
        user_response1 = {'Student': {'name': 'zhu', 'email': 'zhu.com'},  'Course': {'name': 'python_test1'}}
        student1 = StudentMngr(user_response1)
        student1.add()
        user_response1 = {'Lesson': {'name': 'test_day1'}, 'Course': {'name': 'python_test1'}}
        lesson1 = LessonMngr(user_response1)
        lesson1.add()
        user_response = {'Course': {'name': 'python_test1'},
                        'Student': {'name': 'zhu', 'email': 'zhu.com'},
                        'Lesson': {'name': 'test_day1'},
                        'Homework': {'homework': '1'}}
        attendance = HomeworkMngr(user_response)
        result = attendance.update()
        self.assertEqual(result.homework, '1')
        query_result = attendance.query().iloc[0, :].values.tolist()
        query_answer = ['1', 'zhu', 'zhu.com', 'python_test1', 'test_day1']
        self.assertEqual(query_result, query_answer)


    def tearDown(self):
        try:
            result1 = self.session.query(Course).filter(Course.name=='python_test1').first()
            self.session.delete(result1)
        except UnmappedInstanceError:
            pass
        try:
            result2 = self.session.query(Lesson).filter(Lesson.name=='test_day1').first()
            self.session.delete(result2)
        except UnmappedInstanceError:
            pass
        try:
            student1 = self.session.query(Student).filter(Student.email=='zhu.com').first()
            self.session.delete(student1)
        except UnmappedInstanceError:
            pass
        self.session.commit()

if __name__ == '__main__':
    unittest.main()