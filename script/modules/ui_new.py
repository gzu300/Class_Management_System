#coding=utf-8
from abc import ABC, abstractclassmethod
import sys
import pandas as pd
from .logic_layer import Test
from .logic_layer_new import *

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
    def get_user_response(self):
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
        

    @abstractclassmethod
    def generate_next_ui(self):
        pass

    def get_user_response(self):
        #There might be multiple inputs to create a new table. 
        #For example Student table needs email and name.
        #this generates a dictionary for new table with {'table_name': {colname: value}}.
        #'related_entries' is a dictionary of related tableS with {'table_name': {colname: value}}

        self._user_response = gather_multiple_responses(self._args) #funcs in logic layer
        self._mngr = eval(self._args[0]+'Mngr')(self._user_response)
        return self._user_response

    def run(self):
        self.get_user_response()
        self.generate_next_ui()
        return self.next_ui


class AuthFactory(ExternalUIFactory):

    def generate_next_ui(self):
        existed = self._mngr.query(ExternalUIFactory.role)
        if existed:
            self.next_ui = 'TeacherView'
            return
        self.next_ui = 'Welcome'

    def get_user_response(self):
        ExternalUIFactory.role = ExternalUIFactory.get_user_response(self)

class QueryFactory(ExternalUIFactory):
    def generate_next_ui(self):
        result = self._mngr.query(self._user_response)
        print(result)

class AddFactory(ExternalUIFactory):
    def generate_next_ui(self):
        result = self._mngr.add(self._user_response)
        print(result)

    def run(self):
        self.get_user_response()
        self.generate_next_ui()
        return self.next_ui



#####
#Concrete Internal UIs
#####

Welcome = InternalUIFactory({'1': 'TeacherLogin', '2': 'StudentLogin', 'q': 'Quit'})
Teacher_view = InternalUIFactory({'1': 'Student', '2': 'Course', '3': 'Lesson', '4': 'Attendance', '5': 'Score', 'q': 'Quit'})
Student_view = InternalUIFactory({'1': 'Homework'})
Student_op = InternalUIFactory({'1': 'Add_student', '2': 'Search_student', 'b': 'Back', 'q': 'Quit'})
Course_op = InternalUIFactory({'1': 'Add_course', '2': 'Search_course', 'b': 'Back', 'q': 'Quit'})
Lesson_op = InternalUIFactory({'1': 'Add_lesson', '2': 'Search_lesson', 'b': 'Back', 'q': 'Quit'})
Attendance_op = InternalUIFactory({'1': 'Add_attendance', '2': 'Search_attendance', 'b': 'Back', 'q': 'Quit'})
Score_op = InternalUIFactory({'1': 'Add_score', '2': 'Search_score', 'b': 'Back', 'q': 'Quit'})
Homework_op = InternalUIFactory({'1': 'Add_homework'})


#####
#Conrete External UIs
#####

TeacherLogin = AuthFactory('TeacherView', 'Teacher')

Add_course = AddFactory('TeacherView', 'Course')
Add_student = AddFactory('TeacherView', 'Student', 'Course')
Add_lesson = AddFactory('TeacherView', 'Lesson', 'Course')

Search_course = QueryFactory('TeacherView', 'Course')
# Search_student = TeacherUIFactory('query', 'Students')
# Search_lesson = TeacherUIFactory('query', 'Lessons')
# Search_attendance = TeacherUIFactory('query', 'Attendances')
# Search_score = TeacherUIFactory('query', 'Scores')

#Students
# StudentLogin = ExternalUIFactory('StudentView', 'query', 'Students')

# Add_homework = ExternalUIFactory('StudentView', 'add', 'Homeworks')

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

def gather_one_response(table_schema):
    return {each: input(f'Enter {table_schema}\'s {each} information: ') for each in get_columns(table_schema)}

def gather_multiple_responses(table_list):
    return {table: gather_one_response(table) for table in table_list}

#####
#Application
#####

def application(ui):

    UIs = {
        'Welcome': Welcome,
        'TeacherView': Teacher_view,
        'StudentView': Student_view,

        'Student': Student_op,
        'Course': Course_op,
        'Lesson': Lesson_op,
        'Attendance': Attendance_op,
        'Score': Score_op,
        'Homework': Homework_op,

        'TeacherLogin': TeacherLogin,
        # 'StudentLogin': StudentLogin,

        'Add_course': Add_course,
        'Search_course': Search_course,

        'Add_student': Add_student,
        # 'Search_student': Search_student,

        # 'Add_lesson': Add_lesson,
        # # 'Search_lesson': Search_lesson,

        # 'Add_attendance': Add_attendance,
        # 'Search_attendance': Search_attendance,

        # 'Add_score': Add_score,
        # 'Search_score': Search_score,

        # 'Add_homework': Add_homework,

        'Quit': Quit(),
        'Back': Back()
    }
    initialize()
    while True:
        app = UIs.get(ui)
        ui = app.run()


if __name__ == '__main__':
    application('Welcome')


