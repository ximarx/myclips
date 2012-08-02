'''
Created on 17/lug/2012

@author: Francesco Capozzo
'''
from myclips.MyClipsException import MyClipsException

class ModulesManager(object):
    '''
    Stores the list of allowed functions
    '''
    instance = None

    def __init__(self):
        '''
        Constructor
        '''
        self._modules = {}
        self._currentScope = None
        
    def isDefined(self, moduleName):
        return self._modules.has_key(moduleName)
    
    def addMainScope(self):
        from myclips.Scope import Scope, ScopeExport
        Scope("MAIN", self, exports=[
                ScopeExport(Scope.PROMISE_NAME_ALL, Scope.PROMISE_NAME_ALL)
            ]) 
        # add the (initial-fact) template to the MAIN scope
        from myclips.TemplatesManager import TemplateDefinition
        self.currentScope.templates.addDefinition(TemplateDefinition("MAIN", "initial-fact", None))
        

    def addScope(self, scope):
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
        return self._currentScope
    
    @property
    def currentScope(self):
        return self._currentScope
        
    def getScope(self, moduleName):
        """
        Get the scope object for a defined module
        @return: the scope object for the module with moduleName
        @rtype: Scope
        @raise UnknownModuleError: if the moduleName is not a valid defined module name
        """
        try:
            return self._modules[moduleName]
        except KeyError:
            raise UnknownModuleError("Unable to find defmodule {0}".format(moduleName))
        
    def getModulesNames(self):
        return self._modules.keys()
        
    def reset(self):
        self._modules = {}

class ModulesManagerRedefinitionError(MyClipsException):
    pass

class UnknownModuleError(MyClipsException):
    pass

# Standard instance
ModulesManager.instance = ModulesManager()