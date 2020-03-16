#coding=utf-8
# import sys
# import pandas as pd
# from .logic_layer import TeacherMngr, StudentMngr, Operations, AdminMngr

class Base:
    mngr = None
    def __init__(self):
        self._options = {'b': Welcome}
        self._user_responses = []
        self._next_scene = None
        
    def interact(self):
        self.show_options()
        self.ask_user()
        self.communicate_logiclayer()
        self.reply_user()
        
    def ask_user(self):
        response = input('Select a cat:').strip().lower()
        self._next_scene = response

    def communicate_logiclayer(self):
        '''
        logic layer should return the message. No None result accepted
        '''
        df = 'a result from logiclayer'
        print(df)
        
    def reply_user(self):
        scene=self._options.get(self._next_scene)
        if scene:
            next_scene = scene()
            next_scene.interact()
        
    def show_options(self):
        for cat, ui_objs in self._options.items():
            print(cat, ui_objs.__name__)
            
class Operations:
    def login(self):
        return
    def add(self):
        return
    def update(self):
        return
    def query(self):
        return
    def delete(self):
        return
            
class Welcome(Base):
    def __init__(self):
        Base.__init__(self)
        self._options.update({'1': Teacher})

class Lesson(Base):
    pass
    
class Course(Base):
    def __init__(self):
        Base.__init__(self)
        self._options.update({'1': 'add'})
    
class Teacher(Base):
    def __init__(self):
        Base.__init__(self)
        self._options.update({'1': Course})
        Base.mngr = 'Teacher'
    
class Student(Base):
    pass
    
class Attendance(Base):
    pass
    
if __name__ == '__main__':
    CATEGORIES = {'Welcome': {'1': Teacher}, 'Teacher': {'1': Course}}
    # ui = Welcome()
    # ui.main()


