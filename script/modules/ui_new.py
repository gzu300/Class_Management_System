#coding=utf-8
from abc import ABC, abstractclassmethod
import sys
import pandas as pd
# from .logic_layer import TeacherMngr, StudentMngr, Operations, AdminMngr

#####
#Abstract Factory
#####

class AbstractFactory(ABC):

    @abstractclassmethod
    def main(self):
        pass

    @abstractclassmethod
    def display(self):
        pass

    def getResponse(self):
        self._user_response = input().strip().lower()

    def process(self):
        pass
    @abstractclassmethod
    def giveResponse(self):
        pass

######
#concrete factory classes
######

class InternalUIFactory(AbstractFactory):
    def __init__(self, category_dict):
        self._response = None
        self._current_cat = category_dict

    def main(self):
        self.display()
        self.getResponse()
        self.process()
        self.giveResponse()
        return self._response

    def display(self):
        display_categories(self._current_cat)
    def getResponse(self):
        self._user_response = input().strip().lower()
    def process(self):
        return
    def giveResponse(self):
        return giveInternalResponse(self)
        
class Login(AbstractFactory):
    def __init__(self, role):
        self._role = role
    def main(self):
        self.display()
        self.getResponse()
        self.process()
        self.giveResponse()
        return self._response
    def display(self):
        print('Enter '+self._role+'\'s name below:')
    def giveResponse(self):
        self._response = self._role

class OperationFactory(AbstractFactory):
    def __init__(self, condition1, func):
        self.condition1 = condition1
        self.func = func
    def main(self):
        while True:
            self.display()
            self.getResponse()
            self.process()
            self.sql_to_df()
            self.giveResponse()
        return self._response
    def display(self):
        print('Enter name(s) below:')
    def giveResponse(self):
        self._response = 'Welcome'
    def process(self):
        #interact with logic layer.
        operation = self.func()
        return operation
    def sql_to_df(self):
        #df = pd.read_sql()
        print(pd.DataFrame({1: ['Dummy']}))

class OperationTwoArg(OperationFactory):
    def __init__(self, condition1, condition2, func):
        self.condition2 = condition2
        OperationFactory.__init__(self, condition1, func)
    
    def getResponse(self):
        self._user_response1, self._user_response2 = getTwoResponse(self)

class OperationFourArg(OperationTwoArg):
    def __init__(self, condition1, condition2, condition3, condition4, func):
        self.condition3 = condition3
        self.condition4 = condition4
        OperationTwoArg.__init__(self, condition1, condition2, func)
    
    def getResponse(self):
        self._user_response1, self._user_response2, self._user_response3, self._user_response4= getFourResponse(self)

#####
#concrete classes
#####

##one arg
class AddCourse(OperationFactory):
    def __init__(self):
        OperationFactory('course', addonearg)

class SearchCourse(OperationFactory):
    def __init__(self):
        OperationFactory('course', addonearg)

#two args
class AddStudent(OperationFactory):
    def __init__(self):
        OperationTwoArg('student', 'course', addtwoargs)

class SearchStudent(OperationFactory):
    def __init__(self):
        OperationTwoArg('student', 'course', searchtwoargs)

class AddLesson(OperationTwoArg):
    def __init__(self):
        OperationTwoArg.__init__(self, 'course', 'lesson', addtwoargs)

class SearchLesson(OperationTwoArg):
    def __init__(self):
        OperationTwoArg.__init__(self, 'course', 'lesson', searchtwoargs)

#four args
#actually four arguments
class AddAttendance(OperationFourArg):
    def __init__(self):
        OperationFourArg.__init__(self, 'student', 'course', 'lesson', 'attendance', addfourargs)

class SearchAttendance(OperationFourArg):
    def __init__(self):
        OperationFourArg.__init__(self, 'student', 'course', 'lesson', 'attendance', searchfourargs)

class AddScore(OperationFourArg):
    def __init__(self):
        OperationFourArg.__init__(self, 'student', 'course', 'lesson', 'score', addfourargs)

class SearchScore(OperationFourArg):
    def __init__(self):
        OperationFourArg.__init__(self, 'student', 'course', 'lesson', 'score', searchfourargs)





####
#concrete products
####
def addonearg():
    return
def searchonearg():
    return

def searchtwoargs():
    return
def addtwoargs():
    return

def addfourargs():
    return
def searchfourargs():
    return

def getFourResponse(obj):
    respond_1 = input(obj.condition1)
    respond_2 = input(obj.condition2)
    respond_3 = input(obj.condition3)
    respond_4 = input(obj.condition4)
    return (respond_1, respond_2, respond_3, respond_4) 
def getTwoResponse(obj):
    respond_1 = input(obj.condition1)
    respond_2 = input(obj.condition2)
    return (respond_1, respond_2)

def giveInternalResponse(obj):
        obj._response = obj._current_cat.get(obj._user_response)
        if not obj._response:
            obj.main()

def display_categories(category_dict):
    '''
    Takes dictionary as arguments. print key, value pairs.
    '''
    print('='*10)
    for key, value in category_dict.items():
        print(key, value)
    print('='*10)

def display_oneline(obj):
    print('Enter your name here:')

class Quit:
    def main(self):
        sys.exit()

#####
#Application
#####

def application(category):
    factory_dict = {
        'Welcome': InternalUIFactory({'1': 'TeacherLogin', '2': 'StudentLogin', 'q': 'Quit'}),
        'Teacher_view': InternalUIFactory({'1': 'Student', '2': 'Course', '3': 'Lesson', '4': 'Attendance', '5': 'Score', 'q': 'Quit'}),
        'Student_view': InternalUIFactory({'1': 'Homework'}),

        'Student': InternalUIFactory({'1': 'Add_student', '2': 'Search_student', 'b': 'Back', 'q': 'Quit'}),
        'Course': InternalUIFactory({'1': 'Add_course', '2': 'Search_course', 'b': 'Back', 'q': 'Quit'}),
        'Lesson': InternalUIFactory({'1': 'Add_lesson', '2': 'Search_lesson', 'b': 'Back', 'q': 'Quit'}),
        'Attendance': InternalUIFactory({'1': 'Add_attendance', '2': 'Search_attendance', 'b': 'Back', 'q': 'Quit'}),
        'Score': InternalUIFactory({'1': 'Add_score', '2': 'Search_score', 'b': 'Back', 'q': 'Quit'}),

        'TeacherLogin': Login('Teacher_view'),
        'StudentLogin': Login('Student_view'),

        'Add_course': AddCourse(),
        'Search_course': SearchCourse(),

        'Add_student': AddStudent(),
        'Search_student': SearchStudent(),

        'Add_lesson': AddLesson(),
        'Search_lesson': SearchLesson(),

        'Add_attendance': AddAttendance(),
        'Search_attendance': SearchAttendance(),

        'Add_score': AddScore(),
        'Search_score': SearchScore(),

        # 'Delete': InteractionFactory,
        # 'Search': InteractionFactory,

        'Quit': Quit()
    }
    return factory_dict.get(category)

def main(ui):
    while True:
        app = application(ui)
        ui = app.main()


if __name__ == '__main__':
    main('Welcome')



