#coding=utf-8
from abc import ABC, abstractclassmethod
import sys
import pandas as pd
from .logic_layer import Test
from .logic_layer_new import initialize

'''
This script deploys the factory pattern.
There are 2 factories: 
1. InternalUIFactory.   Circles inside UIs
                        responsible for displaying and connecting interfaces. 
                        Accepts integer(str format) inputs from user.
2. ExternalUIFactory.   Quries logic layer
                        responsible for interacting with logic layer and users.
                        Accepts various number of string inputs from users.
                        it passes dict with {Entity:Name} pairs to logic layer.

Every interface, internal and external, has a concrete instance and called in
application.
'''
####
#Abstract UI
####
class AbstractUI(ABC):
    @abstractclassmethod
    def display(self):
        pass
    @abstractclassmethod
    def generate_next_ui(self):
        pass
    @abstractclassmethod
    def run(self):
        pass

#####
#Internal Factory
#####

class InternalUIFactory(AbstractUI):
    def __init__(self, dict_toshow):
        self._dict_to_show = dict_toshow

    def display(self):
        display_categories(self._dict_to_show)

    def get_user_response(self):
        return input('Select the category:').strip().lower()

    def generate_next_ui(self):
        user_response = self.get_user_response()
        self._next_ui = self._dict_to_show.get(user_response)

    def run(self):
        self._next_ui = None
        while not self._next_ui:
            self.display()
            self.generate_next_ui()
        return self._next_ui

#####
#External Factory
#####

class ExternalUIFactory(AbstractUI):
    def __init__(self, next_ui, *args):
        self.next_ui = next_ui
        self._args = args

    def display(self):
        pass

    def get_user_response(self):
        user_response_list = [input(f'Enter {each} information:').strip().lower() for each in self._args]
        return user_response_list

    def generate_next_ui(self):
        user_response_list = self.get_user_response()
        self.retrieve_info(user_response_list)

    def show_error(self):
        pass

    def retrieve_info(self, input_list):
        print(dict(zip(self._args, input_list)))
        logic_test = Test()
        self._logic_response = logic_test.show(input_list)

    def run(self):
        self._logic_response = None
        while not self._logic_response:
            self.display()
            self.generate_next_ui()
        return self.next_ui

#####
#Concrete Internal UIs
#####

Welcome = InternalUIFactory({'1': 'TeacherLogin', '2': 'StudentLogin', 'q': 'Quit'})
Teacher_view = InternalUIFactory({'1': 'Student', '2': 'Course', '3': 'Lesson', '4': 'Attendance', '5': 'Score', 'q': 'Quit'})
Student_view = InternalUIFactory({'1': 'Homework'})
Student = InternalUIFactory({'1': 'Add_student', '2': 'Search_student', 'b': 'Back', 'q': 'Quit'})
Course = InternalUIFactory({'1': 'Add_course', '2': 'Search_course', 'b': 'Back', 'q': 'Quit'})
Lesson = InternalUIFactory({'1': 'Add_lesson', '2': 'Search_lesson', 'b': 'Back', 'q': 'Quit'})
Attendance = InternalUIFactory({'1': 'Add_attendance', '2': 'Search_attendance', 'b': 'Back', 'q': 'Quit'})
Score = InternalUIFactory({'1': 'Add_score', '2': 'Search_score', 'b': 'Back', 'q': 'Quit'})
Homework = InternalUIFactory({'1': 'Add_homework'})


#####
#Conrete External UIs
#####

#Teachers
class TeacherUIFactory(ExternalUIFactory):
    def __init__(self, *args):
        ExternalUIFactory.__init__(self, 'TeacherView', *args)

TeacherLogin = ExternalUIFactory('TeacherView', 'Teacher')

Add_course = TeacherUIFactory('Course')
Add_student = TeacherUIFactory('Course', 'Student')
Add_lesson = TeacherUIFactory('Course', 'Lesson')
Add_attendance = TeacherUIFactory('Course', 'Lesson', 'Student', 'Attendance')
Add_score = TeacherUIFactory('Course', 'Lesson', 'Student', 'Score')

Search_course = TeacherUIFactory('Course')
Search_student = TeacherUIFactory('Course', 'Student')
Search_lesson = TeacherUIFactory('Course', 'Lesson')
Search_attendance = TeacherUIFactory('Course', 'Lesson', 'Student', 'Attendance')
Search_score = TeacherUIFactory('Course', 'Lesson', 'Student', 'Score')

#Students
StudentLogin = ExternalUIFactory('StudentView', 'Student')

Add_homework = ExternalUIFactory('StudentView', 'Homework')

#####
#Misc functios and classes
#####


def display_categories(category_dict):
    '''
    Takes dictionary as arguments. print key, value pairs.
    '''
    print('='*10)
    for key, value in category_dict.items():
        print(key, value)
    print('='*10)

class Quit:
    def run(self):
        sys.exit()

class Back:
    def run(self):
        return 'Welcome'

#####
#Application
#####

def application(ui):

    UIs = {
        'Welcome': Welcome,
        'TeacherView': Teacher_view,
        'StudentView': Student_view,

        'Student': Student,
        'Course': Course,
        'Lesson': Lesson,
        'Attendance': Attendance,
        'Score': Score,
        'Homework': Homework,

        'TeacherLogin': TeacherLogin,
        'StudentLogin': StudentLogin,

        'Add_course': Add_course,
        'Search_course': Search_course,

        'Add_student': Add_student,
        'Search_student': Search_student,

        'Add_lesson': Add_lesson,
        'Search_lesson': Search_lesson,

        'Add_attendance': Add_attendance,
        'Search_attendance': Search_attendance,

        'Add_score': Add_score,
        'Search_score': Search_score,

        'Add_homework': Add_homework,

        'Quit': Quit(),
        'Back': Back()
    }
    initialize()
    while True:
        app = UIs.get(ui)
        ui = app.run()


if __name__ == '__main__':
    application('Welcome')



