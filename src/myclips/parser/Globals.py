'''
Created on 17/lug/2012

@author: Francesco Capozzo
'''

class GlobalsManager(object):
    '''
    Stores the list of allowed functions
    '''
    instance = None

    def __init__(self, funcs = None):
        '''
        Constructor
        '''
        self._funcs = funcs if isinstance(funcs, dict) else {}
        
#    def registerGlobal(self, globalDefinition):
#        if not isinstance(globalDefinition, GlobalDefinition):
#            raise ValueError("FunctionDefinition required")
#        self._funcs[globalDefinition.getVarName()] = globalDefinition

    def getFuncNames(self):
        return self._funcs.keys()
    
    def getFuncDefinition(self, funcName):
        return self._funcs[funcName]
    
    def getFunctions(self):
        '''FunctionManager().getFunctions() -> list of registered functions (funcName, funcDefinition) pairs, as 2-tuples'''
        return self._funcs.items()
    
    def reset(self):
        self._funcs = {}

# Standard instance
GlobalsManager.instance = GlobalsManager()