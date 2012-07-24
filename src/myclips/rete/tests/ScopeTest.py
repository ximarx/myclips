'''
Created on 24/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.tests.AlphaTest import AlphaTest
from myclips.rete.WME import WME

class ScopeTest(AlphaTest):
    '''
    classdocs
    '''


    def __init__(self, moduleName):
        '''
        Constructor
        '''
        self._moduleName = moduleName
        
    @property
    def moduleName(self):
        return self._moduleName
    
    def isValid(self, wme):
        assert isinstance(wme, WME)
        return wme.fact.moduleName == self.moduleName 