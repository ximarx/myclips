'''
Created on 24/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.tests.AlphaTest import AlphaTest
import myclips
from myclips.rete.tests.BetaTest import BetaTest

class OrConnectiveTest(AlphaTest, BetaTest):
    '''
    Forward execution of tests to wrapped tests
    This test is both an AlphaTest and a BetaTest:
    isValid call is forwarded as is to subtests
    '''


    def __init__(self, tests):
        '''
        Constructor
        '''
        self._tests = tests
        
    @property
    def tests(self):
        return self._tests
    
    def isValid(self, *args):
        try:
            for sTest in self.tests:
                if sTest.isValid(*args):
                    return True
                
            return False
            
        except Exception, e:
            myclips.logger.warn("Unexpected exception caught in OrConnectiveTest: %s", repr(e))
            return False
    
    def __str__(self, *args, **kwargs):
        return "OR(" + ",\n".join([str(x) for x in self.tests]) + ")"
        
    def __eq__(self, other):
        return self.__class__ == other.__class__ \
                and self.tests == other.tests
                
