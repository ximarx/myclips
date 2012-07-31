'''
Created on 17/lug/2012

@author: Francesco Capozzo
'''
from myclips.Observable import Observable
from myclips.RestrictedManager import RestrictedManager, RestrictedDefinition,\
    MultipleDefinitionError
import myclips


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
        
        # need to import system function definitions
        # bypass registerSystemFunction to avoid debug logger
        self._systemsFunctions = Functions_ImportSystemDefinitions()
        
        
    @property
    def systemFunctions(self):
        return self._systemsFunctions.keys()
    
    def getSystemFunctionDefinition(self, funcName):
        return self._systemsFunctions[funcName] 
        
    def hasSystemFunction(self, funcName):
        return self._systemsFunctions.has_key(funcName)

    def has(self, definitionName):
        return ((self.hasSystemFunction(definitionName) or RestrictedManager.has(self, definitionName))
                    and not self.getDefinition(definitionName).isForward)
    
    def addDefinition(self, definition):
        # need to check definition:
        # if definition scope different from this one
        # i need to mark the function as not forward
        # and lock redefinition
        if definition.moduleName != self.scope.moduleName and definition.isForward:
            definition.isForward = False
            myclips.logger.debug("DefFunction %s::%s imported. Can't be redefined", definition.moduleName, definition.name)
             
        RestrictedManager.addDefinition(self, definition)
        
        # after i added the definition, i need to fire the event
        self.fire(self.__class__.EVENT_NEW_DEFINITION, definition)
        
    
    def getDefinition(self, defName):
        try:
            return self.getSystemFunctionDefinition(defName)
        except:
            return RestrictedManager.getDefinition(self, defName)
    
    def registerSystemFunction(self, definition):
        if self.hasSystemFunction(definition.name):
            raise MultipleDefinitionError("Cannot redefine {0} {2}::{1} while it is in use".format(
                        definition.definitionType,
                        definition.name,
                        "?SYSTEM?"
                    ))
        self._systemsFunctions[definition.name] = definition
        myclips.logger.debug("System function %s registered", definition.name)
            
        
class FunctionDefinition(RestrictedDefinition):
    def __init__(self, moduleName, defName, linkedType, returnTypes, handler=None, constraints=None, forward=True):
        RestrictedDefinition.__init__(self, moduleName, defName, "deffunction", linkedType)
        self._handler = handler
        self._returnTypes = returnTypes if isinstance(returnTypes, tuple) else (returnTypes,)
        self._constraints = constraints if isinstance(constraints, list) else []
        self._forward = bool(forward)
        
    @property
    def handler(self):
        '''
        Get the callable handler that realize
        the real implementation of the function
        '''
        return self._handler
    
    @property
    def returnTypes(self):
        '''
        Return a tuple of all return types the function
        can use as output
        @rtype: tuple
        '''
        return self._returnTypes
    
    @property
    def isForward(self):
        return self._forward
    
    @isForward.setter
    def isForward(self, value):
        self._forward = value
    
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
        import myclips.parser.Types as types
        if self.argIndex == None:
            invalidArgs = [True if isinstance(x, self.argType)
                                else True if isinstance(x, types.Variable)
                                    else True if isinstance(x, types.FunctionCall)
                                                    and self.argType in x.funcDefinition.returnTypes
                                        else True if isinstance(x, types.FunctionCall)
                                                        and any([issubclass(retType, self.argType) for retType in x.funcDefinition.returnTypes])
                                            else False
                           for x in args]
            return (not any([not x for x in invalidArgs]))
        else:
            x = args[self.argIndex]
            return (True if isinstance(x, self.argType)
                                else True if isinstance(x, types.Variable)
                                    else True if isinstance(x, types.FunctionCall)
                                                    and self.argType in x.funcDefinition.returnTypes
                                        else True if isinstance(x, types.FunctionCall)
                                                        and any([issubclass(retType, self.argType) for retType in x.funcDefinition.returnTypes])
                                            else False)

    
    

FUNCTIONS_DEFINITIONS = {}
    
def Functions_ImportSystemDefinitions():
    
    from myclips.functions.__init__ import SystemFunctionBroker
    
    return SystemFunctionBroker.definitions()

    if len(FUNCTIONS_DEFINITIONS) > 0:
        return FUNCTIONS_DEFINITIONS

    # setup basic functions like aritmetic / comparison
    # FOR PARSING ONLY
    
    from myclips.parser.Types import Number, BaseParsedType, Lexeme, Integer, Float
    
    import sys
    
    
    
    FUNCTIONS_DEFINITIONS["+"] = FunctionDefinition("?SYSTEM?", "+", object(), (Integer, Float), lambda *args: sum([t.evaluate() if isinstance(t, BaseParsedType) else t for t in args]),
            [
                Constraint_MinArgsLength(2),
                Constraint_ArgType(Number)
            ],forward=False)
    
    def r_mul(sequence):
        return (sequence[0] if len(sequence) == 1 
                else sequence[0] * r_mul(sequence[1:]))
    
    FUNCTIONS_DEFINITIONS["*"] = FunctionDefinition("?SYSTEM?", "*", object(), (Integer, Float), lambda *args: r_mul([t.evaluate() if isinstance(t, BaseParsedType) else t for t in args]),
            [
                Constraint_MinArgsLength(2),
                Constraint_ArgType(Number)
            ],forward=False)
    
    FUNCTIONS_DEFINITIONS["eq"] = FunctionDefinition("?SYSTEM?", "eq", object(), True.__class__, lambda *args: not any([
                                                                (t.evaluate() if isinstance(t, BaseParsedType) else t) 
                                                                    != 
                                                                (args[0].evaluate() if isinstance(args[0], BaseParsedType) else args[0]) 
                                                                for (i,t) in enumerate(args) if i > 0]),
            [
                Constraint_MinArgsLength(2),
                Constraint_ArgType(Lexeme)
            ],forward=False)
    
    FUNCTIONS_DEFINITIONS["neq"] = FunctionDefinition("?SYSTEM?", "neq", object(), True.__class__, lambda *args: not any([
                                                                (t.evaluate() if isinstance(t, BaseParsedType) else t) 
                                                                    == 
                                                                (args[0].evaluate() if isinstance(args[0], BaseParsedType) else args[0]) 
                                                                for (i,t) in enumerate(args) if i > 0]),
            [
                Constraint_MinArgsLength(2),
                Constraint_ArgType(Lexeme)
            ],forward=False)
    
    FUNCTIONS_DEFINITIONS["="] = FunctionDefinition("?SYSTEM?", "=", object(), True.__class__, lambda *args: not any([
                                                                (t.evaluate() if isinstance(t, BaseParsedType) else t) 
                                                                    != 
                                                                (args[0].evaluate() if isinstance(args[0], BaseParsedType) else args[0]) 
                                                                for (i,t) in enumerate(args) if i > 0]),
            [
                Constraint_MinArgsLength(2),
                Constraint_ArgType(Number)
            ],forward=False)
    
    FUNCTIONS_DEFINITIONS["<>"] = FunctionDefinition("?SYSTEM?", "<>", object(), True.__class__, lambda *args: not any([
                                                                (t.evaluate() if isinstance(t, BaseParsedType) else t) 
                                                                    == 
                                                                (args[0].evaluate() if isinstance(args[0], BaseParsedType) else args[0]) 
                                                                for (i,t) in enumerate(args) if i > 0]),
            [
                Constraint_MinArgsLength(2),
                Constraint_ArgType(Number)
            ],forward=False)
    
    FUNCTIONS_DEFINITIONS["printout"] = FunctionDefinition("?SYSTEM?", "printout", object(), None.__class__, lambda *args: sys.stdout.writelines(args[1:]),
            [
                Constraint_MinArgsLength(2),
            ],forward=False)

    FUNCTIONS_DEFINITIONS["float"] = FunctionDefinition("?SYSTEM?", "float", object(), Float, lambda arg: Float(arg.evaluate()),
            [
                Constraint_ArgType(Number),
                Constraint_ExactArgsLength(1)
            ],forward=False)
    
    FUNCTIONS_DEFINITIONS["assert"] = FunctionDefinition("?SYSTEM?", "assert", object(), None.__class__, lambda *args: args,
            [
                Constraint_MinArgsLength(1),
            ],forward=False)
    
    FUNCTIONS_DEFINITIONS["retract"] = FunctionDefinition("?SYSTEM?", "retract", object(), None.__class__, lambda *args: args,
            [
                Constraint_MinArgsLength(1),
            ],forward=False)
    
    return FUNCTIONS_DEFINITIONS