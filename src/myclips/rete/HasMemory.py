'''
Created on 04/lug/2012

@author: ximarx
'''

class HasMemory(object):
    '''
    Interface to identify node with direct local memory linked
    '''

    def __init__(self, memory=None):
        '''
        Constructor
        '''
        self._memory = memory
        
    def hasMemory(self):
        '''
        Check if memory is linked
        
        @return: boolean
        '''
        return self._memory != None
    
    @property
    def memory(self):
        '''
        Get the linked memory to this node
        
        @return: Memory 
        '''
        return self._memory
    
    @memory.setter
    def memory(self, memory):
        '''
        Link a memory to this object
        
        @param memory: Memory 
        '''
        self._memory = memory
        
    
    