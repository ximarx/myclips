'''
Created on 24/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.tests.AlphaTest import AlphaTest
from myclips.rete.WME import WME
import myclips

class MultislotLengthTest(AlphaTest):
    '''
    Check if a ordered fact has the exact length
    '''


    def __init__(self, slotName, length):
        '''
        Constructor
        '''
        self._length = length
        self._slotName = slotName
        
    @property
    def length(self):
        return self._length
    
    @property
    def slotName(self):
        return self._slotName
    
    def isValid(self, wme):
        assert isinstance(wme, WME)
        try:
            return len(wme.fact[self.slotName]) == self.length
        except KeyError:
            return False
        except Exception, e:
            myclips.logger.warn("Unexpected exception caught in OrderedFactLengthTest: %s", repr(e))
            return False
    
    def __str__(self, *args, **kwargs):
        return "#wme[%s]=%s"%(self.slotName, self.length)
        
    def __eq__(self, other):
        return self.__class__ == other.__class__ \
                and self.length == other.length \
                and self.slotName == other.slotName
                
    
