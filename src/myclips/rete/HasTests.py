'''
Created on 04/lug/2012

@author: ximarx
'''

class HasTests(object):
    '''
    Interface to identify node with with tests
    to perform on activation
    '''

    def __init__(self, tests=None):
        '''
        Constructor
        '''
        self._tests = tests
        
    def hasTests(self):
        '''
        Check if memory is linked
        
        @return: boolean
        '''
        return self._tests != None and len(self._tests) > 0
    
    @property
    def tests(self):
        '''
        Get the linked memory to this node
        
        @return: Memory 
        '''
        return self._tests
    
    @tests.setter
    def tests(self, tests):
        '''
        Link a memory to this object
        
        @param memory: Memory 
        '''
        self._tests = tests
        
    
    def isValid(self, toTestItem):
        if self.hasTests():
            for test in self.tests:
                if not test.isValid(toTestItem):
                    return False
        return True