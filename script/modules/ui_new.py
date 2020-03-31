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

28/03/2020
todo:
1. related columns can be retrieved from inspect function. 
So arguments in ExternalUIFactory for relationship is not needed.
2. implement _retrieve_relationships methods
3. in logic layer. finish _release_items method.
4. then finish the higher level methods '_check_relationships' for related entities.
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
    def __init__(self, next_ui, func, *args):
        self.next_ui = next_ui
        self._new, *self._related = args
        self._func = '_'+func
        self._mngr = eval(self._new)()

    def display(self):
        pass

    def get_user_add_response(self):
        #There might be multiple inputs to create a new table. 
        #For example Student table needs email and name.
        #this generates a dictionary for new table with {'table_name': {colname: value}}.
        #'related_entries' is a dictionary of related tableS with {'table_name': {colname: value}}
        new_entries = [gather_one_response(self._new)]
        related_entries = gather_multiple_responses(self._related) #funcs in logic layer
        #concat into a single list.
        self._user_response = new_entries + related_entries

    def generate_next_ui(self):
        #generate next ui according to logic layer's response.
        result = self.interact_add_request()
        print(result)

        
    def interact_add_request(self):
        #send user_response to logic layer and get reply
        return self._mngr.register(self._user_response)
        

    def _add(self):
        self.display()
        self.get_user_add_response()
        self.generate_next_ui()

    def _query(self):
        pass

    def run(self):
        getattr(self, self._func)()
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

#Teachers
class TeacherUIFactory(ExternalUIFactory):
    def __init__(self, *args):
        ExternalUIFactory.__init__(self, 'TeacherView', *args)

TeacherLogin = ExternalUIFactory('TeacherView', 'query', 'Teachers')

Add_course = TeacherUIFactory('add', 'Courses')
Add_student = TeacherUIFactory('add', 'Students', 'Courses')
Add_lesson = TeacherUIFactory('add', 'Lessons', 'Courses')
# Add_attendance = TeacherUIFactory('add', 'Attendances')
# Add_score = TeacherUIFactory('add', 'Scores')

# Search_course = TeacherUIFactory('query', 'Courses')
# Search_student = TeacherUIFactory('query', 'Students')
# Search_lesson = TeacherUIFactory('query', 'Lessons')
# Search_attendance = TeacherUIFactory('query', 'Attendances')
# Search_score = TeacherUIFactory('query', 'Scores')

#Students
StudentLogin = ExternalUIFactory('StudentView', 'query', 'Students')

Add_homework = ExternalUIFactory('StudentView', 'add', 'Homeworks')

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

def gather_one_response(table):
    table_schema = table[:-1] #table schema is in singular
    return {table_schema: {each: input(f'Enter {table_schema}\'s {each} information: ') for each in get_columns(table_schema)}}

def gather_multiple_responses(table_list):
    return [gather_one_response(obj) for obj in table_list]

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

        'Student': Student_op,
        'Course': Course_op,
        'Lesson': Lesson_op,
        'Attendance': Attendance_op,
        'Score': Score_op,
        'Homework': Homework_op,

        'TeacherLogin': TeacherLogin,
        'StudentLogin': StudentLogin,

        'Add_course': Add_course,
        # 'Search_course': Search_course,

        'Add_student': Add_student,
        # 'Search_student': Search_student,

        'Add_lesson': Add_lesson,
        # 'Search_lesson': Search_lesson,

        # 'Add_attendance': Add_attendance,
        # 'Search_attendance': Search_attendance,

        # 'Add_score': Add_score,
        # 'Search_score': Search_score,

        'Add_homework': Add_homework,

        'Quit': Quit(),
        'Back': Back()
    }
    initialize()
    while True:
        app = UIs.get(ui)
        ui = app.run()


if __name__ == '__main__':
    # application('Welcome')
    a = TeacherUIFactory('add', 'Courses', 'Students')
    print(a.run())



