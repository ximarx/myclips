'''
Created on 24/lug/2012

@author: Francesco Capozzo
'''

class AlphaTest(object):
    '''
    Base class for tests injected in PropertyTestNode
    '''
        
    def isValid(self, wme):
        raise NotImplementedError()
    

    def __eq__(self, other):
        return (self.__class__ == other.__class__)
    
