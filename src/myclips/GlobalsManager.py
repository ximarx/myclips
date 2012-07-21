'''
Created on 17/lug/2012

@author: Francesco Capozzo
'''
from myclips.Observable import Observable
from myclips.RestrictedManager import RestrictedManager, RestrictedDefinition


class GlobalsManager(RestrictedManager, Observable):
    '''
    Stores the list of allowed globals definitions for the scope
    '''
    instance = None
    EVENT_NEW_DEFINITION = "EVENT_GlobalsManager_NewDefinition"

    def __init__(self, scope):
        '''
        Constructor
        '''
        Observable.__init__(self, [
                GlobalsManager.EVENT_NEW_DEFINITION
            ])
        RestrictedManager.__init__(self, scope)
        
    def addDefinition(self, definition):
        RestrictedManager.addDefinition(self, definition)
        
        # after i added the definition, i need to fire the event
        self.fire(self.__class__.EVENT_NEW_DEFINITION, definition)
        
        
class GlobalVarDefinition(RestrictedDefinition):
    def __init__(self, moduleName, defName, linkedType):
        RestrictedDefinition.__init__(self, moduleName, defName, "defglobal", linkedType)