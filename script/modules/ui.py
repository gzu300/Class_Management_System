#coding=utf-8
import sys
import pandas as pd
from .logic_layer import TeacherMngr, StudentMngr, Operations, AdminMngr

def doubleline_decorator(func):
    def wrapper(*args, **kwargs):
        print('='*10)
        a = func(*args, **kwargs)
        print('='*10)
        return a
    return wrapper

def whileTrue_decorator(func):
    '''
    wraps a function into while loop.
    '''
    def wrapper(*args):
        while True:
            if any([each == 'b' for each in args]):
                break
            return func(*args)
            
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

    def _login(self, Mngrobj, user_view):
        while True:
            user = input('You can enter \'q\' to go back to previous section. \nOtherwise, enter your username:').strip()
            if user == 'q':
                break
            else:
                pwd = input('Password:').strip()
                host = input('Your host:').strip()
                self.mngr = Mngrobj(user=user, password=pwd, host=host)
                user_view()

    def a_login(self):
        self._login(Mngrobj=AdminMngr, user_view=self.admin_view)

    def t_login(self):
        while True:
            name = input('You can enter \'q\' to go back to previous section. \nOtherwise, enter your name:').strip()
            if name == 'q':
                break
            else:
                self.mngr = TeacherMngr()
                if self.mngr.authenticate(name):
                    self.teacher_view(name)
                else:
                    print('{0} is not in the record.'.format(name), '='*10, sep='\n')

    def s_login(self):
        enter = input('You can enter \'q\' to go back to previous section. \nOtherwise, enter your email address:')
        return enter
    
    def admin_view(self):
        while True:
            print(
                '='*10,
                '1. Register a teacher.',
                '2. Free style.',
                '3. Init table schema.',
                '4. Go back.',
                '5. Exit.',
                '='*10,
                sep='\n'
            )
            enter = input('Make a selection:')
            if enter == '1':
                self.add_teacher_view()
                continue
            elif enter == '2':
                while True:
                    self.mngr.connect()
                    command = input('Key in the SQL command:').strip()
                    if command=='q':
                        self.mngr.dispose()
                        break
                    else:
                        self.mngr.command(command)
            elif enter == '3':
                self.mngr.reboot()
                print('db rebooted.', '='*10, sep='\n')
                # print('THIS OPTION IS NOT IN USE, YET.')
                # continue
            elif enter == '4':
                break
            elif enter == '5':
                sys.exit()


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
                self.add_attendance_view()
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
            print('Course does not exist. Register course: {0} first.'.format(c_name), '='*10, sep='\n')
            return
        print('{0} with email: {1} successfully registered.'.format(s_name, s_email), '='*10, sep='\n')

    def add_course_view(self):
        enter = input('Enter the name of the new course:').strip().lower()

        self.mngr.rgt_course(enter)
        print('{0} has beed successully registered.'.format(enter), '='*10, sep='\n')

    def add_teacher_view(self):
        enter = input('Enter teacher\'s name:').strip().lower()
        t_exist = self.mngr.check_teacher(enter)
        if t_exist:
            print('{0} already existed.'.format(enter))
            return
        self.mngr.rgt_teacher(enter)
        print('{0} has beed successully registered.'.format(enter), '='*10, sep='\n')
    
    @doubleline_decorator
    def teacher_course_view(self):
        df = self.mngr.q_t_courses()
        if df.empty:
            print('No course registerd. Registered a course first.', '='*10, sep='\n')
            return
        print(df, sep='\n')

    @doubleline_decorator
    def student_course_view(self):
        df = self.mngr.q_t_students()
        if df.empty:
            print('No course registerd. Registered a course first.', '='*10, sep='\n')
            return
        print(df, sep='\n')

    @whileTrue_decorator    
    def add_lesson_view(self, lesson, course): 
        if not self.mngr.rgt_lesson(lesson, course):
            print('Can\' find course ({0}). Register the course first.'.format(course))
            return
        print('Lesson({0}) successfully added to course({1}).'.format(lesson, course))
    def add_attendance_view(self):
        self.mngr.rgt_attendance('day1', 'linux', 'zhu@email.com')

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