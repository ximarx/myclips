'''
Created on 24/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.tests.BetaTest import BetaTest

class NegativeBetaTest(BetaTest):
    '''
    Reverse the result of the test embedded inside this
    '''


    def __init__(self, test):
        '''
        Build a new Negative alpha test
        '''
        assert isinstance(test, BetaTest)
        self._test = test
        
    def isValid(self, token, wme):
        return not self.test.isValid(token, wme)
    
    @property
    def test(self):
        return self._test
    
    def __str__(self, *args, **kwargs):
        return "NOT(%s)"%self.test
    
    def __eq__(self, other):
        return self.__class__ == other.__class__ \
                and self.test == other.test              