'''
Created on 17/lug/2012

@author: Francesco Capozzo
'''
from myclips.MyClipsException import MyClipsException

class ModulesManager(object):
    '''
    Stores availabled scopes
    '''
    instance = None

    def __init__(self):
        '''
        Create a new ModulesManager instance
        '''
        self._modules = {}
        '''store a dict of moduleName => L{Scope} pairs'''
        self._currentScope = None
        '''the currentScope, context of execution of the engine'''
        
    def isDefined(self, moduleName):
        '''
        Check if a module has been defined
        @param moduleName: a module name
        @type moduleName: string
        @rtype: boolean
        '''
        return self._modules.has_key(moduleName)
    
    def addMainScope(self):
        '''
        Register a MAIN scope, exporting everything
        Same effect of
            (defmodule MAIN (export ?ALL))
        '''
        from myclips.Scope import Scope, ScopeExport
        Scope("MAIN", self, exports=[
                ScopeExport(Scope.PROMISE_NAME_ALL, Scope.PROMISE_NAME_ALL)
            ]) 
        # add the (initial-fact) template to the MAIN scope
        from myclips.TemplatesManager import TemplateDefinition
        self.currentScope.templates.addDefinition(TemplateDefinition("MAIN", "initial-fact", None))
        

    def addScope(self, scope):
        '''
        Add a new Scope, changing the currentScope to this new one
        @param scope: the Scope
        @type scope: L{Scope}
        '''
        if self.isDefined(scope.moduleName):
            raise ModulesManagerRedefinitionError("Cannot redefine defmodule {0} while it is in use".format(scope.moduleName))
        self._modules[scope.moduleName] = scope
        self._currentScope = scope
        
    def changeCurrentScope(self, moduleName):
        """
        Try to switch the current scope to another one
        @raise UnknownModuleError: if the moduleName is not a valid defined module name
        """
        self._currentScope = self.getScope(moduleName)
        
    def getCurrentScope(self):
        '''
        Get the current scope
        @rtype: L{Scope}
        '''
        return self._currentScope
    
    @property
    def currentScope(self):
        '''
        Get the current scope
        @rtype: L{Scope}
        '''
        return self._currentScope
        
    def getScope(self, moduleName):
        """
        Get the scope object for a defined module
        @return: the scope object for the module with moduleName
        @rtype: L{Scope}
        @raise UnknownModuleError: if the moduleName is not a valid defined module name
        """
        try:
            return self._modules[moduleName]
        except KeyError:
            raise UnknownModuleError("Unable to find defmodule {0}".format(moduleName))
        
    def getModulesNames(self):
        '''
        Get the list of definited modules
        '''
        return self._modules.keys()
        
    def reset(self):
        '''
        Reset defined scopes
        '''
        self._modules = {}

class ModulesManagerRedefinitionError(MyClipsException):
    '''
    Used on module redefinition
    '''

class UnknownModuleError(MyClipsException):
    '''
    If you try to switch the current module to a not defined one
    '''

# Standard instance
ModulesManager.instance = ModulesManager()