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
    """Event sign used when new definition is added, observer will
    be notified with this sign!"""

    def __init__(self, scope):
        '''
        Create a new GlobalsManager for the scope

        @param scope: the scope owner of this manager
        @type scope: L{Scope}
        '''
        Observable.__init__(self, [
                GlobalsManager.EVENT_NEW_DEFINITION
            ])
        RestrictedManager.__init__(self, scope)
        
    def addDefinition(self, definition):
        '''
        Add a new definition and notify observers about this
        @param definition: a new function definition
        @type definition: L{GlobalVarDefinition}
        '''
        RestrictedManager.addDefinition(self, definition)
        
        # after i added the definition, i need to fire the event
        self.fire(self.__class__.EVENT_NEW_DEFINITION, definition)
        
        
class GlobalVarDefinition(RestrictedDefinition):
    '''
    Describe a global var definition
    '''
    def __init__(self, moduleName, defName, linkedType):
        '''
        Create a new definition from params
        @param moduleName: owner module's name
        @type moduleName: string
        @param defName: global def name
        @type defName: string
        @param linkedType: a types.GlobalVariable object linked to this definition
        @type linkedType: L{GlobalVariable}
        '''
        RestrictedDefinition.__init__(self, moduleName, defName, "defglobal", linkedType)