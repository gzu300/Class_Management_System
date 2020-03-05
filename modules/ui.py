#coding=utf-8

import pandas as pd

class ui(object):

    def categorize(self):
        print(
            '='*10,
            'Welcome to class management system', 
            'Please select your category:', 
            '1. Teacher', 
            '2. Student',
            '3. Exit', 
            '='*10,
            sep='\n'
              )
        cat = input('Enter your category:')
        # if cat == '1':
        #     return 'Teacher'
        # elif cat == '2':
        #     return 'Student'
        # elif cat == '3':
        #     return 'Exit'
        # else:
        #     print('Please select a valid category.')
        return cat
    def t_login(self):
        enter = input('You can enter \'q\' to go back to previous section. \nOtherwise, enter your name:')
        return enter

    def s_login(self):
        enter = input('You can enter \'q\' to go back to previous section. \nOtherwise, enter your email address:')
        return enter

    def teacher_view(self ,name):
        print(
            '='*10,
            'Welcome {0}. You have the following possible actions'.format(name),
            '1. Register a student.',
            '2. Register a course.',
            '3. Register a session.',
            '4, Register a attendance.',
            '5. Check homework.',
            '6. Give score.',
            '7, Go back.',
            '8, Exit',
            '='*10,
            sep='\n'
        )
        enter = input('Enter your selection:')
        return enter
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
        enter = input('Enter the name of the new course:').strip()
        return enter
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