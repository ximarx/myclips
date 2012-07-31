import sys
import os
import myclips
from myclips.MyClipsException import MyClipsException
from myclips.functions.Function import Function

FUNCTIONS_DIR = os.path.dirname(__file__)
FUNCTIONS_MANIFEST = "_dev_functions.json"


class FunctionEnv(object):
    
    def __init__(self, variables, network, modulesManager, RESOURCES):
        self._variables = variables
        self._network = network
        self._modulesManager = modulesManager,
        self._RESOURCES = RESOURCES
        
    @property
    def variables(self):
        return self._variables
    
    @property
    def network(self):
        return self._network
    
    @property
    def modulesManager(self):
        return self._modulesManager
    
    @property
    def RESOURCES(self):
        return self._RESOURCES
    
    
      
class SystemFunctionBroker(object):
    
    _functions = {}
    _ready = False
        
    @classmethod
    def register(cls, funcInstance):
        if not isinstance(funcInstance, Function):
            myclips.logger.error("Invalid function definition: %s", repr(funcInstance))
            return
        
        funcDefinition = funcInstance.definition()
        
        from myclips.FunctionsManager import FunctionDefinition
        
        assert isinstance(funcDefinition, FunctionDefinition)
        
        if cls._functions.has_key(funcDefinition.name):
            raise SystemFunctionRedefinitionError("Redefinition attempt: %s"%funcDefinition.name)
        
        cls._functions[funcDefinition.name] = funcDefinition
        
    
    @classmethod
    def definitions(cls):
        cls.bootstrap()
        return cls._functions
    
    
    @classmethod
    def bootstrap(cls):
        if cls._ready:
            return
        
        import json
        
        manifestPath = "/".join([FUNCTIONS_DIR.rstrip("/"), FUNCTIONS_MANIFEST])
        
        try:
            funcList = json.load(open(manifestPath, "rU"))
            cls._ready = True
        except Exception, e:
            myclips.logger.error("Functions manifest file %s cannot be loaded: %s", manifestPath, repr(e))
        else:
            for funcDict in funcList:
                try:
                    funcModule = funcDict['module']
                    funcClass = funcDict['class']
                except KeyError, e:
                    myclips.logger.error("Malformed function definition in manifest file %s:\n\tError: %s\n\tDefinition: %s", manifestPath, repr(e), str(funcDict))
                else:
                    try:
                        funcInstance = myclips.newInstance(funcClass, None, funcModule)
                    except ImportError, e:
                        myclips.logger.error("Error loading function definition class: %s", e)
                    else:
                        cls.register(funcInstance)

                    
class SystemFunctionRedefinitionError(MyClipsException):
    '''
    Raised on attempt to redefine a already defined
    system function 
    '''
    pass



if __name__ == '__main__':
    
    from myclips.ModulesManager import ModulesManager
    
    MM = ModulesManager()
    MM.addMainScope()
    
    print MM.currentScope.functions.systemFunctions
    print MM.currentScope.functions.has('assert')
    
