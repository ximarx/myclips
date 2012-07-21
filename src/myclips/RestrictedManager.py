'''
Created on 19/lug/2012

@author: Francesco Capozzo
'''

class RestrictedManager(object):
    '''
    Define an interface for all constructs
    manager that are under a scope visibility
    constraints
    '''

    def __init__(self, scope):
        '''
        Constructor
        '''
        self._scope = scope
        self._definitions = {}
        
    @property
    def scope(self):
        return self._scope
        
    @property
    def definitions(self):
        return self._definitions.keys()
    
    def getDefinition(self, defName):
        return self._definitions[defName]

    def has(self, definitionName):
        return self._definitions.has_key(definitionName)

    def addDefinition(self, definition):
        if self.has(definition.name):
            raise MultipleDefinitionError("Cannot redefine {0} {2}::{1} while it is in use".format(
                        definition.definitionType,
                        definition.name,
                        definition.moduleName
                    ))
        
        self._definitions[definition.name] = definition
    
    def __repr__(self, *args, **kwargs):
        return "::".join((self.scope.moduleName, self.__class__.__name__))
    
class RestrictedDefinition(object):
    
    def __init__(self, moduleName, defName, defType, linkedType ):
        self._defName = defName
        self._moduleName = moduleName
        self._defType = defType
        self._linkedType = linkedType
        # dict of Scope().moduleName : Scope()
        self._scopes = {}
    
    @property    
    def name(self):
        return self._defName
    
    @property
    def definitionType(self):
        return self._defType
    
    @property
    def linkedType(self):
        return self._linkedType
    
    @property
    def moduleName(self):
        return self._moduleName
    
    @property
    def scopes(self):
        return self._scopes.keys()
    
    def addScope(self, scope):
        self._scopes[scope.moduleName] = scope
        
    def isAllowed(self, scope):
        return self._moduleName == scope.moduleName or self._scopes.has_key(scope.moduleName)
    
    
class MultipleDefinitionError(Exception):
    pass
    