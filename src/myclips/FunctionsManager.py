'''
Created on 17/lug/2012

@author: Francesco Capozzo
'''
from myclips.Observable import Observable
from myclips.RestrictedManager import RestrictedManager, RestrictedDefinition


class FunctionsManager(RestrictedManager, Observable):
    '''
    Stores the list of allowed globals definitions for the scope
    '''
    instance = None
    EVENT_NEW_DEFINITION = "EVENT_FunctionsManager_NewDefinition"

    def __init__(self, scope):
        '''
        Constructor
        '''
        Observable.__init__(self, [
                FunctionsManager.EVENT_NEW_DEFINITION
            ])
        RestrictedManager.__init__(self, scope)
        
        
class FunctionDefinition(RestrictedDefinition):
    def __init__(self, moduleName, defName, linkedType, returnType, handler, constraints=None):
        RestrictedDefinition.__init__(self, moduleName, defName, "deffunction", linkedType)
        self._handler = handler
        self._returnType = returnType if isinstance(returnType, tuple) else (returnType,)
        self._constraints = constraints if isinstance(constraints, list) else [] 
        
    @property
    def handler(self):
        '''
        Get the callable handler that realize
        the real implementation of the function
        '''
        return self._handler
    
    @property
    def returnType(self):
        '''
        Return a tuple of all return types the function
        can use as output
        @rtype: tuple
        '''
        return self._returnType
    
    def isValidCall(self, args):
        for c in self._constraints:
            # stop validation on first invalid
            if not c.isValid(args):
                return (False, c.getReason())
            
        return self.customValidation(args)
    
    def customValidation(self, args):
        '''
        Override this method to execute custom validations
        on inputs that can't be done with constraints
        This validation is performed as last (after all constraints check)
        if all constraints are ok
        
        @param args: a list/tuple of args
        @type args: list
        @return: a tuple (True|False, None|str:Reason of failure)
        @rtype: tuple
        '''
        return (True, None)
    
class FunctionConstraint(object):
    def getReason(self):
        return ""
    def isValid(self, args):
        return True
    
class Constraint_MinArgsLength(FunctionConstraint):
    def __init__(self, value):
        self.value = value
        
    def getReason(self):
        return "expected at least {0} argument(s)".format(self.value)
    
    def isValid(self, args):
        return (len(args) >= self.value)

class Constraint_MaxArgsLength(FunctionConstraint):
    def __init__(self, value):
        self.value = value
    
    def getReason(self):
        return "expected no more than {0} argument(s)".format(self.value)
    
    def isValid(self, args):
        return (len(args) <= self.value)

class Constraint_ExactArgsLength(FunctionConstraint):
    def __init__(self, value):
        self.value = value

    def getReason(self):
        return "expected exactly {0} argument(s)".format(self.value)
    
    def isValid(self, args):
        return (len(args) == self.value)
    
class Constraint_ArgType(FunctionConstraint):
    def __init__(self, argType, argIndex=None):
        self.argType = argType
        self.argIndex = argIndex

    def getReason(self):
        return "expected argument {0} to be of type {1}".format("#"+str(self.argIndex) if self.argIndex is not None else "#ALL",
                                                                " or ".join([t.__name__ for t in self.argType])
                                                                    if isinstance(self.argType, tuple) 
                                                                    else self.argType.__name__
                                                                )
        
    def isValid(self, args):
        import myclips.parser.types.Types as types
        if self.argIndex == None:
            invalidArgs = [True if isinstance(x, self.argType)
                                else True if isinstance(x, types.Variable)
                                    else True if isinstance(x, types.FunctionCall)
                                                    and self.argType in x.funcDefinition.getReturnTypes()
                                        else True if isinstance(x, types.FunctionCall)
                                                        and any([issubclass(retType, self.argType) for retType in x.funcDefinition.getReturnTypes()])
                                            else False
                           for x in args]
            return (not any([not x for x in invalidArgs]))
        else:
            x = args[self.argIndex]
            return (True if isinstance(x, self.argType)
                                else True if isinstance(x, types.Variable)
                                    else True if isinstance(x, types.FunctionCall)
                                                    and self.argType in x.funcDefinition.getReturnTypes()
                                        else True if isinstance(x, types.FunctionCall)
                                                        and any([issubclass(retType, self.argType) for retType in x.funcDefinition.getReturnTypes()])
                                            else False)

    
    
    