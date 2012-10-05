'''
Created on 19/lug/2012

@author: Francesco Capozzo
'''
import myclips

class RestrictedManager(object):
    '''
    Define an interface for all constructs
    manager that are under a scope visibility
    constraint
    '''

    def __init__(self, scope):
        '''
        Initialize the manager
        '''
        self._scope = scope
        '''the scope owner of this instance'''
        self._definitions = {}
        '''the definitions container'''
        
    @property
    def scope(self):
        '''
        Get the scope
        @rtype: L{Scope}
        '''
        return self._scope
        
    @property
    def definitions(self):
        '''
        Get registerd definition names
        @rtype: list of string
        '''
        return self._definitions.keys()
    
    def getDefinition(self, defName):
        '''
        Get a single definition by defName
        @param defName: the definition name
        @type defName: string
        @rtype: RestrictedDefinition
        '''
        return self._definitions[defName]

    def has(self, definitionName):
        '''
        Check if a definition name is already used
        @param definitionName: a def name to check
        @type definitionName: string
        @rtype: boolean
        '''
        return self._definitions.has_key(definitionName)

    def addDefinition(self, definition):
        '''
        Add a new definition, using RestrictedManager.has
        to check if definition can be added
        @param definition: the definition
        @type definition: RestrictedDefinition
        @raise MultipleDefinitionError: is def name is used
        '''
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
    '''
    Represents a definition stored in a RestrictedManager
    '''
    
    def __init__(self, moduleName, defName, defType, linkedType ):
        '''
        Init the definition
        @param moduleName: the owner module's name
        @type moduleName: string
        @param defName: the def name
        @type defName: string
        @param defType: the def type symbolic rappresentation
        @type defType: string
        @param linkedType: a custom instance linked to the definition
        @type linkedType: object
        '''
        self._defName = defName
        self._moduleName = moduleName
        self._defType = defType
        self._linkedType = linkedType
        # dict of Scope().moduleName : Scope()
        self._scopes = {}
        
    def __eq__(self, other):
        toTestItems = ['__class__', 'name', 'moduleName', 'definitionType',
                       'linkedType']
        try:
            for test in toTestItems:
                # try to split for the inner reference comparison
                splitted = test.split(".", 2)
                if len(splitted) == 2:
                    objRefThis = getattr(self, splitted[0])
                    objRefOther = getattr(other, splitted[0])
                    attribute = splitted[1]
                else:
                    objRefThis = self
                    objRefOther = other
                    attribute = splitted[0]
                    
                if getattr(objRefThis, attribute) != getattr(objRefOther, attribute):
                    myclips.logger.debug("Different item %s: %s vs %s", 
                                            test, 
                                            str(getattr(objRefThis, attribute)), 
                                            getattr(objRefOther, attribute))
                    return False
                
            # everything is the same
            return True
        except Exception, e:
            # error? -> not equal
            myclips.logger.debug("Exception on comparison %s: %s", 
                                    test, 
                                    str(e))
            return False
        
    def __neq__(self, other):
        return not self.__eq__(other)
    
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
    '''
    Raised on redefinition error
    '''
    