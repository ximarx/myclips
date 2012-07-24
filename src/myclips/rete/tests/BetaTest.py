'''
Created on 24/lug/2012

@author: Francesco Capozzo
'''

class BetaTest(object):
    '''
    Base class for tests in beta network
    '''

    def isValid(self, token, wme):
        raise NotImplementedError()
    
    def __eq__(self, other):
        return (self.__class__ == other.__class__)
    