#coding=utf-8
import sys
import pandas as pd
from .logic_layer import TeacherMngr, StudentMngr, Operations, AdminMngr

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
                '3. Admin',
                '4. Exit', 
                '='*10,
                sep='\n'
                )
            cat = input('Enter your category:')
            if cat == '1':
                self.t_login()
            elif cat == '2':
                self.s_login()
            elif cat == '3':
                self.a_login()
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
                # if self.mngr.authenticate(user=user, password=pwd, host=host):
                #     user_view(name)
                # else:
                #     print('{0} is not in the record.'.format(name), '='*10, sep='\n')

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
                '3. Register a session.',
                '4, Register a attendance.',
                '5, Check course',
                '6. Check homework.',
                '7. Give score.',
                '8, Go back.',
                '9, Exit',               
                '='*10,
                sep='\n'
            )
            enter = input('Enter your selection:').strip().lower()
            if enter == '1':
                pass
            elif enter == '2':
                self.add_course_view()
                continue
            elif enter == '3':
                pass
            elif enter == '4':
                pass
            elif enter == '5':
                self.teacher_course_view()
                continue
            elif enter == '6':
                pass
            elif enter == '7':
                pass
            elif enter == '8':
                break
            elif enter == '9':
                sys.exit()
    def student_view(self, name):
        print(
            '='*10,
            'Welcome {0}. You have the following possible actions:'.format(name),
            '1. Submit a homework.',
            '2. Check your ranking.',
            '='*10,
            sep='\n'
        )
        enter = input('Make a selection:')
        return enter
    def add_student_view(self):
        return
    def add_course_view(self):
        enter = input('Enter the name of the new course:').strip().lower()
        c_exist = self.mngr.check_course(enter)
        if c_exist:
            print('Course already existed.')
        else:
            self.mngr.rgt_course(enter)
            print('{0} has beed successully registered.'.format(enter), '='*10, sep='\n')

    def add_teacher_view(self):
        enter = input('Enter teacher\'s name:').strip().lower()
        t_exist = self.mngr.check_teacher(enter)
        if t_exist:
            print('{0} already existed.'.format(enter))
        else:
            self.mngr.rgt_teacher(enter)
            print('{0} has beed successully registered.'.format(enter), '='*10, sep='\n')
    
    def teacher_course_view(self):
        print('='*10)
        c_name = input('Enter the course you would like to search:').strip().lower()
        df = self.mngr.q_t_courses(c_name)
        print(df, '='*10, sep='\n')
        
    def add_session_view(self):
        return
    def add_attend(self):
        return
    def check_homework(self):
        return
    def score(self):
        return
    def submit_hw(self):
        return
    def check_rank(self):
        return



if __name__ == '__main__':
    df = pd.DataFrame({'a':[1,2,3], 'b':[1,2,3]})
    print(df)