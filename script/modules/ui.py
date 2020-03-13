#coding=utf-8
import sys
import pandas as pd
from .logic_layer import TeacherMngr, StudentMngr, Operations, AdminMngr

def doubleline_decorator(func):
    def wrapper(*args, **kwargs):
        print('='*10)
        df = func(*args, **kwargs)
        if df.empty:
            print('No record found', '='*10, sep='\n')
            return
        print(df, '='*10, sep='\n')
    return wrapper

def whileTrue_decorator(func):
    '''
    wraps a function into while loop.
    '''
    def wrapper(*args, **kwargs):
        while True:
            if ('b' in args):
                break
            result = func(*args, **kwargs)
            if not result:
                obj, *names = args
                print('Error: Registeratrion(s) for {0} is missing. Or for attendance, duplicate keys may happened.'.format(','.join(names)))
                return
            print('Successfully entered.')
            return result          
    return wrapper

class ui(object):

    def __init__(self):
        # a = Operations()
        # a.initialize()
        pass

    def main(self):
        while True:
            print(
                '='*10,
                'Welcome to class management system', 
                'Please select your category:', 
                '1. Teacher', 
                '2. Student',
                #'3. Admin',
                '4. Exit', 
                '='*10,
                sep='\n'
                )
            cat = input('Enter your category:')
            if cat == '1':
                self.t_login()
            elif cat == '2':
                self.s_login()
            # elif cat == '3':
            #     self.a_login()
            elif cat == '4':
                sys.exit()
            else:
                print('Please select a valid category.')

    def _login(self, Mngrobj):
        while True:
            self.mngr = Mngrobj() #create a instance first such that if Teacher table is empty. create a user called 'alex'
            name = input('You can enter \'q\' to go back to previous section. \nOtherwise, enter your username:').strip()
            if name == 'q':
                break
            if not self.mngr.authenticate(name):
                print('{0} is not in the record.'.format(name), '='*10, sep='\n')
                continue
            getattr(self, self.mngr.view)(name) # Run TeacherMngr or StudentMngr

    def a_login(self):
        #self._login(Mngrobj=AdminMngr, user_view=self.admin_view)
        return

    def t_login(self):
        # while True:
        #     name = input('You can enter \'q\' to go back to previous section. \nOtherwise, enter your name:').strip()
        #     if name == 'q':
        #         break
        #     else:
        #         self.mngr = TeacherMngr()
        #         if self.mngr.authenticate(name):
        #             self.teacher_view(name)
        #         else:
        #             print('{0} is not in the record.'.format(name), '='*10, sep='\n')
        self._login(Mngrobj=TeacherMngr)

    def s_login(self):
        enter = input('You can enter \'q\' to go back to previous section. \nOtherwise, enter your email address:')
        return enter

    def teacher_view(self ,name):
        while True:
            print(
                '='*10,
                'Welcome {0}. You have the following possible actions'.format(name),
                '1. Register a student.',
                '2. Register a course.',
                '3. Register a lesson.',
                '4, Register a attendance.',
                '5, Check course',
                '6. Check homework.',
                '7. Give score.',
                '8. Check students',
                '9. check attendance',
                '10. check lesson',
                'b, Go back.',
                'q, Exit',               
                '='*10,
                sep='\n'
            )
            enter = input('Enter your selection:').strip().lower()
            if enter == '1':
                self.add_student_view()
                continue
            if enter == '2':
                self.add_course_view()
                continue
            if enter == '3':
                course = input('Enter the name of the course:').strip().lower()
                lesson = input('Enter the name of the lesson:').strip().lower()

                self.add_lesson_view(lesson, course)
                continue
            if enter == '4':
                s_email = input('Enter student\'s email:').strip().lower()
                # s_name = input('Enter student\'s name:').strip().lower()
                l_name = input('Enter student\'s lesson:').strip().lower()
                c_name = input('Enter student\'s course:').strip().lower()
                if_attended = input('Is the student present? type in \'yes\' or \'no\'.').strip().lower()
                if if_attended == 'yes':
                    self.add_attendance_view(l_name, c_name, s_email, if_attended=True)
                elif if_attended == 'no':
                    self.add_attendance_view(l_name, c_name, s_email, if_attended=False)
                else:
                    print('No a valid entry for attendance')
                continue
            if enter == '5':
                self.teacher_course_view()
                continue
            if enter == '6':
                pass
            if enter == '7':
                pass
            if enter == '8':
                self.student_course_view()
                continue
            if enter == '9':
                c_name = input('Enter the name of the course:').strip().lower()
                l_name = input('Enter the name of the lesson:').strip().lower()
                self.session_student_view(l_name, c_name)
                continue
            if enter == '10':
                c_name = input('Enter the name of the course:').strip().lower()
                self.lesson_course_view(c_name)
                continue
            if enter == 'b':
                break
            if enter == 'q':
                sys.exit()
    
    @doubleline_decorator
    def student_view(self, name):
        print(
            'Welcome {0}. You have the following possible actions:'.format(name),
            '1. Submit a homework.',
            '2. Check your ranking.',
            '='*10,
            sep='\n'
        )
        enter = input('Make a selection:')
        return enter
        
    def add_student_view(self):
        s_email = input('Enter student\'s email:').strip().lower()
        s_name = input('Enter student\'s name:').strip().lower()
        c_name = input('Enter student\'s course:').strip().lower()
        result = self.mngr.rgt_student(email=s_email, name=s_name, c_name=c_name)
        if not result:
            print('Error: Course {0} does not exist. Or {1} already existed'.format(c_name, s_email), '='*10, sep='\n')
            return
        print('{0} with email: {1} successfully registered.'.format(s_name, s_email), '='*10, sep='\n')

    def add_course_view(self):
        enter = input('Enter the name of the new course:').strip().lower()

        if not self.mngr.rgt_course(enter):
            print('Error: {0} already existed.'.format(enter), '='*10, sep='\n')
        print('{0} has been successully registered.'.format(enter), '='*10, sep='\n')

    def add_teacher_view(self):
        enter = input('Enter teacher\'s name:').strip().lower()
        t_exist = self.mngr.check_teacher(enter)
        if t_exist:
            print('{0} already existed.'.format(enter))
            return
        self.mngr.rgt_teacher(enter)
        print('{0} has beed successully registered.'.format(enter), '='*10, sep='\n')


    @whileTrue_decorator    
    def add_lesson_view(self, lesson, course): 
        return self.mngr.rgt_lesson(lesson, course)

    @whileTrue_decorator
    def add_attendance_view(self, lesson, course, student_email, if_attended=None):
        return self.mngr.rgt_attendance(lesson, course, student_email, if_attended=if_attended)
        
    @doubleline_decorator
    def lesson_course_view(self, c_name):
        return self.mngr.q_t_lessons(c_name)
    
    @doubleline_decorator
    def teacher_course_view(self):
        return self.mngr.q_t_courses()

    @doubleline_decorator
    def student_course_view(self):
        return self.mngr.q_t_students()
    
    @doubleline_decorator
    def session_student_view(self, lesson, course):
        return self.mngr.q_t_attendance(lesson, course)

    @doubleline_decorator
    def check_homework(self):
        return
    def score(self):
        return
    def submit_hw(self):
        return
    @doubleline_decorator
    def check_rank(self):
        return



if __name__ == '__main__':
    df = pd.DataFrame({'a':[1,2,3], 'b':[1,2,3]})
    print(df)