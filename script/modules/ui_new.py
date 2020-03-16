#coding=utf-8
from abc import ABC, abstractclassmethod
# import sys
# import pandas as pd
# from .logic_layer import TeacherMngr, StudentMngr, Operations, AdminMngr

class Base:
    def __init__(self, idisplay, igetResponse):
        self._idisplay = idisplay
        self._igetResponse = igetResponse
    def display(self):
        return self._idisplay.display()
    def getResponse(self):
        return self._igetResponse.getResponse()

#Behaviour classes
class IDisplay(ABC):
    @abstractclassmethod
    def display(self):
        pass

class IgetResponse(ABC):
    @abstractclassmethod
    def getResponse(self):
        pass

#Parent class for the same categories
class Actions(IDisplay):
    '''
    for add, update, delete and qery concrete classes.
    '''
    def display(self):
        print('concrete display method, in {0} class'.format(self.__class__.__name__))
    def getResponse(self):
        print('concrete getResponse method')

#specific concrete classes
class Add(Actions):
    


    
if __name__ == '__main__':
    add = Base(Add(), Add())
    add.display()


