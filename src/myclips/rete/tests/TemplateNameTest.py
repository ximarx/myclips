'''
Created on 24/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.tests.AlphaTest import AlphaTest
from myclips.rete.WME import WME

class TemplateNameTest(AlphaTest):
    '''
    classdocs
    '''


    def __init__(self, templateName):
        '''
        Constructor
        '''
        self._templateName = templateName
        
    @property
    def templateName(self):
        return self._templateName
    
    def isValid(self, wme):
        assert isinstance(wme, WME)
        return wme.fact.templateName == self.templateName
    
    def __str__(self, *args, **kwargs):
        return "Template=%s"%self.templateName
    
    def __eq__(self, other):
        return self.__class__ == other.__class__ \
                and self.templateName == other.templateName
                