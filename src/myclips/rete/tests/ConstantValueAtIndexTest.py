'''
Created on 24/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.tests.AlphaTest import AlphaTest
from myclips.rete.WME import WME
import myclips
from myclips.rete.tests import getWmeFragmentValue
from myclips.Fact import FactLengthNotComputableException

class ConstantValueAtIndexTest(AlphaTest):
    '''
    Check if a constant value of type Symbol, Integer, Float, String
    is place at a specified index. Index could be a exact index
    or an minimu index
    '''


    def __init__(self, index, value):
        '''
        Constructor
        '''
        self._index = index
        self._value = value
        
    @property
    def index(self):
        return self._index
    
    @property
    def valueType(self):
        return self._value.__class__
    
    @property
    def value(self):
        return self._value
    
    def isValid(self, wme):
        assert isinstance(wme, WME)
        try:
            wmeValue = getWmeFragmentValue(wme, self.index)
            
            if self.valueType == list:
                # need to valuate vs a multifield
                # check the wmeValue if is a comparable with a multifield
                if not isinstance(wmeValue, list):
                    return False
                
                if len(self.value) != len(wmeValue):
                    return False
                
                for (offset, value) in enumerate(self.value):
                    if value.__class__ != wmeValue[offset].__class__:
                        return False
                    
                    if value.evaluate() != wmeValue[offset].evaluate():
                        return False
                
                return True    
                
            else:
                
                return self.valueType == wmeValue.__class__ and self.value.evaluate() == wmeValue.evaluate()
            
        except FactLengthNotComputableException:
            return False
        except KeyError:
            return False
        except Exception, e:
            myclips.logger.warn("Unexpected exception caught in ConstantValueAtIndexTest: %s", repr(e))
            return False
    
    def __str__(self, *args, **kwargs):
        return "%s=%s"%(self.index,
                               self.value)
        
    def __eq__(self, other):
        return self.__class__ == other.__class__ \
                and self.index == other.index \
                and self.value == other.value
                
