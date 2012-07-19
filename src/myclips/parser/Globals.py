'''
Created on 17/lug/2012

@author: Francesco Capozzo
'''

class GlobalsManager(object):
    '''
    Stores the list of allowed functions
    '''
    instance = None

    def __init__(self, globalsV = None):
        '''
        Constructor
        '''
        self._globals = globalsV if isinstance(globalsV, dict) else {None: {}}
        
#    def registerGlobal(self, globalDefinition):
#        if not isinstance(globalDefinition, GlobalDefinition):
#            raise ValueError("FunctionDefinition required")
#        self._funcs[globalDefinition.getVarName()] = globalDefinition

    def getGlobalsNames(self):
        return self._globals.keys()
    
    def getGlobal(self, globalName, moduleName=None):
        return self._globals[moduleName][globalName]
    
    def getGlobals(self, moduleName=None):
        '''GlobalsManager().getGlobals() -> list of registered globals (globalName, globalDefinition) pairs, as 2-tuples'''
        return self._globals[moduleName].items()
    
    def addGlobal(self, globalName, expression, moduleName=None):
        try:
            mod = self._globals[moduleName]
        except KeyError:
            mod = {}
            self._globals[moduleName] = mod
        finally:
            mod[globalName] = expression        
        
    def getAllGlobals(self):
        '''GlobalsManager().getAllGlobals() -> list of registered globals (moduleName, globalName, globalDefinition) pairs, as 2-tuples'''
        t = []
        for x in [[(modName, globName, glob) for (globName, glob) in modGlobs.items()] for (modName, modGlobs) in self._globals.items()]:
            t += x
        #t.sort() # could be problematic
        return t
        
    def isDefined(self, globalName, moduleName=None):
        try:
            self._globals[moduleName][globalName]
            return True
        except:
            return False
        
    def reset(self):
        self._globals = {None: {}}

# Standard instance
GlobalsManager.instance = GlobalsManager()