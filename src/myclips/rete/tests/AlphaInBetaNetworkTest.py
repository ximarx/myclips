'''
Created on 24/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.tests.BetaTest import BetaTest
import myclips
from myclips.rete.tests.locations import VariableReference
from myclips.rete.tests import getTokenAnchestor, getWmeFragmentValue

class AlphaInBetaNetworkTest(BetaTest):
    '''
    Execute pattern-tests (a list of tests done usually in alpha-network)
    in a join node (so, in beta-network)
    This test wrap a list of alpha-tests in a BetaTest derivate object.
    When evaluation is performed, this test forward evaluation over
    the right-from wme to alpha tests wrapped 
    '''


    def __init__(self, alphaTests):
        '''
        Create a new wrapper test from a list of alpha tests
        
        @param alphaTests: a list of alphaTests
        @type alphaTests: list
        '''
        
        self._tests = alphaTests
        
        
    @property
    def tests(self):
        return self._tests
    
    def isValid(self, token, wme):

        try:

            for test in self.tests:
                if not test.isValid(wme):
                    return False
                
            return True
        
        except Exception, e:
            # Another type of exception catch
            # better log this
            myclips.logger.warning("Unexpected exception catch in %s: token=%s, wme=%s, exception=%s", self, token, wme, repr(e))
            # anyway test failed
            return False
    
    def __str__(self, *args, **kwargs):
        return "\n".join([str(x) for x in self._tests])
        
    def __eq__(self, other):
        return self.__class__ == other.__class__ \
                and self._tests == other._tests
                
    def __neq__(self, other):
        return not self.__eq__(other)