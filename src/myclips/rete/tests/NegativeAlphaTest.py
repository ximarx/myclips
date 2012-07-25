'''
Created on 24/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.tests.AlphaTest import AlphaTest

class NegativeAlphaTest(AlphaTest):
    '''
    Reverse the result of the test embedded inside this
    '''


    def __init__(self, test):
        '''
        Build a new Negative alpha test
        '''
        assert isinstance(test, AlphaTest)
        self._test = test
        
    def isValid(self, wme):
        return not self.test.isValid(wme)
    
    @property
    def test(self):
        return self._test
    
    def __str__(self, *args, **kwargs):
        return "NOT(%s)"%self.test     