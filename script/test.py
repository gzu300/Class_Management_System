import unittest
from .modules.logic_layer_new import LessonMngr, StudentMngr, CourseMngr, AttendanceMngr, initialize
from .modules.create_schema import Session, Student, Course, Lesson, Section, Attendance
from .conf.setting import engine
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.sql import exists

# class TestLesson(unittest.TestCase):
#     def test_add(self):
#         user_response = {'Lesson': {'name': 'testday1'}, 'Course': {'name': 'python_test1'}}
#         lesson = LessonMngr(user_response)
#         lesson_test = lesson.add()
#         column_values = user_response['Lesson']
        
#         lesson_answer = lesson.session.query(Lesson).filter_by(**column_values).one_or_none()
#         self.assertEqual(lesson_test, lesson_answer)

class TestStudent(unittest.TestCase):
    def setUp(self):
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

    def test_add_both_exist(self):
        course = CourseMngr({'Course': {'name': 'python_test1'}})
        course.add()
        user_response1 = {'Student': {'name': 'zhu', 'email': 'zhu.com'},  'Course': {'name': 'python_test1'}}
        student1 = StudentMngr(user_response1)
        student1.add()
        result = student1.add()
        self.assertEqual(result, 'Student name: zhu, email: zhu.com already existed.')

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
        result = self.session.query(Course).filter(Course.name==self._user_response['Course']['name']).first()
        self.session.delete(result)
        self.session.commit()

if __name__ == '__main__':
    initialize()
    unittest.main()