'''
Created on 24/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.tests.AlphaTest import AlphaTest
from myclips.rete.WME import WME

class ConstantValueAtIndexTest(AlphaTest):
    '''
    Check if a constant value of type Symbol, Integer, Float, String
    is place at a specified index
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
        return self._value.evaluate()
    
    def isValid(self, wme):
        assert isinstance(wme, WME)
        return (isinstance(wme.fact[self.index], self.valueType) # first check if type is ok 
                    and wme.fact[self.index] == self.value) # then check if value itself is ok
    
    
    