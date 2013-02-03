'''
Created on 03/feb/2013

@author: Ximarx
'''
from myclips.MyClipsException import MyClipsException

class Fact(object):
    '''
    Base class for all facts:
        store info about modules
    '''


    def __init__(self, moduleName="MAIN"):
        '''
        Constructor
        '''
        self._moduleName = moduleName
        
    @property
    def moduleName(self):
        '''
        Get the module name for the owner of this fact
        @rtype: string
        '''
        return self._moduleName
    
    @moduleName.setter
    def moduleName(self, value):
        '''
        Set a module name as owner of this fact
        @param value: the module name
        @type value: string
        '''
        self._moduleName = value


class FactInvalidIndex(MyClipsException):
    '''
    Trying to get an invalid index for a Ordered-Fact? You'll get this!
    '''


class FactInvalidSlotName(MyClipsException):
    '''
    Trying to get an invalid slot for a Template-Fact? You'll get this!
    '''

class FactLengthNotComputableException(MyClipsException):
    '''
    Trying to compute len of a Template-Fact? You'll get this!
    '''
