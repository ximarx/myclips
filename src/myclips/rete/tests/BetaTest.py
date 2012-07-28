'''
Created on 24/lug/2012

@author: Francesco Capozzo
'''

class BetaTest(object):
    '''
    Base class for tests in beta network
    '''

    def isValid(self, token, wme):
        """
        Check token values / token tests configurations
        versus a new wme and return a list of filtered
        new set of results configurations that fits the test
        """
        raise NotImplementedError()
    
    def __eq__(self, other):
        return (self.__class__ == other.__class__)
    
