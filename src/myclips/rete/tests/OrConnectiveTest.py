'''
Created on 24/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.tests.AlphaTest import AlphaTest
from myclips.rete.WME import WME
import myclips
from myclips.rete.tests import getWmeFragmentValue
from myclips.Fact import FactLengthNotComputableException, FactInvalidSlotName,\
    FactInvalidIndex

class OrConnectiveTest(AlphaTest):
    '''
    Check if a constant value of type Symbol, Integer, Float, String
    is place at a specified index. Index could be a exact index
    or an minimu index
    '''


    def __init__(self, tests):
        '''
        Constructor
        '''
        self._tests = tests
        
    @property
    def tests(self):
        return self._tests
    
    def isValid(self, wme):
        try:
            for sTest in self.tests:
                if sTest.isValid(wme):
                    return True
                
            return False
            
        except (FactLengthNotComputableException, FactInvalidSlotName, FactInvalidIndex):
            return False
        except KeyError:
            return False
        except Exception, e:
            myclips.logger.warn("Unexpected exception caught in ConstantValueAtIndexTest: %s", repr(e))
            return False
    
    def __str__(self, *args, **kwargs):
        return " or ".join(self.tests)
        
    def __eq__(self, other):
        return self.__class__ == other.__class__ \
                and self.tests == other.tests
                
