'''
Created on 24/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.tests.AlphaTest import AlphaTest
from myclips.rete.WME import WME
import myclips
from myclips.facts.Fact import FactLengthNotComputableException

class OrderedFactLengthTest(AlphaTest):
    '''
    Check if a ordered fact has the exact length
    '''


    def __init__(self, length):
        '''
        Constructor
        '''
        self._length = length
        
    @property
    def length(self):
        return self._length
    
    def isValid(self, wme):
        assert isinstance(wme, WME)
        try:
            return len(wme.fact) == self.length
        except FactLengthNotComputableException:
            raise False
        except KeyError:
            return False
        except Exception, e:
            myclips.logger.warn("Unexpected exception caught in OrderedFactLengthTest: %s", repr(e))
            return False
    
    def __str__(self, *args, **kwargs):
        return "#wme=%s"%self.length
        
    def __eq__(self, other):
        return self.__class__ == other.__class__ \
                and self.length == other.length
                
