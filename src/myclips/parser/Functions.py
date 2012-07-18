'''
Created on 17/lug/2012

@author: Francesco Capozzo
'''

class FunctionsManager(object):
    '''
    Stores the list of allowed functions
    '''
    instance = None

    def __init__(self, funcs = None):
        '''
        Constructor
        '''
        self._funcs = funcs if isinstance(funcs, dict) else {}
        
    def registerFunction(self, funcDefinition):
        if not isinstance(funcDefinition, FunctionDefinition):
            raise ValueError("FunctionDefinition required")
        self._funcs[funcDefinition.getFuncName()] = funcDefinition

    def getFuncNames(self):
        return self._funcs.keys()
    
    def getFuncDefinition(self, funcName):
        return self._funcs[funcName]
    
    def getFunctions(self):
        '''FunctionManager().getFunctions() -> list of registered functions (funcName, funcDefinition) pairs, as 2-tuples'''
        return self._funcs.items()
    
    def reset(self):
        self._funcs = {}
        
class FunctionDefinition(object):
    '''
    Collect definition information about a registered function
    '''
    def __init__(self, funcName, returnType, handler):
        self.funcName = funcName
        self.handler = handler
        self.returnType = returnType if isinstance(returnType, tuple) else (returnType,)
        
    def getFuncName(self):
        return self.funcName
    
    def getReturnTypes(self):
        return self.returnType
        
    def isValidCall(self, args):
        return (True,None)
    
class CustomFunctionDefinition(FunctionDefinition):
    
    def __init__(self, funcName, returnType, handler, constraints=None):
        FunctionDefinition.__init__(self, funcName, returnType, handler)
        self._constraints = [] if constraints is None else constraints
        
    def isValidCall(self, args):
        for c in self._constraints:
            # stop validation on first invalid
            if not c.isValid(args):
                return (False, c.getReason())
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


# Standard instance
FunctionsManager.instance = FunctionsManager()


def _SampleFunctionsInit():
    
    if len(FunctionsManager.instance.getFuncNames()) != 0:
        return

    # setup basic functions like aritmetic / comparison
    # FOR PARSING ONLY
    
    from myclips.parser.types.Types import Number, BaseParsedType, Lexeme, Integer, Float
    
    import sys
    
    
    FunctionsManager.instance.registerFunction(
        CustomFunctionDefinition("+", (Integer, Float), lambda *args: sum([t.evaluate() if isinstance(t, BaseParsedType) else t for t in args]),
            [
                Constraint_MinArgsLength(2),
                Constraint_ArgType(Number)
            ]))
    
    def r_mul(sequence):
        return (sequence[0] if len(sequence) == 1 
                else sequence[0] * r_mul(sequence[1:]))
    
    FunctionsManager.instance.registerFunction(
        CustomFunctionDefinition("*", (Integer, Float), lambda *args: r_mul([t.evaluate() if isinstance(t, BaseParsedType) else t for t in args]),
            [
                Constraint_MinArgsLength(2),
                Constraint_ArgType(Number)
            ]))
    
    FunctionsManager.instance.registerFunction(
        CustomFunctionDefinition("eq", True.__class__, lambda *args: not any([
                                                                (t.evaluate() if isinstance(t, BaseParsedType) else t) 
                                                                    != 
                                                                (args[0].evaluate() if isinstance(args[0], BaseParsedType) else args[0]) 
                                                                for (i,t) in enumerate(args) if i > 0]),
            [
                Constraint_MinArgsLength(2),
                Constraint_ArgType(Lexeme)
            ]))
    
    FunctionsManager.instance.registerFunction(
        CustomFunctionDefinition("neq", True.__class__, lambda *args: not any([
                                                                (t.evaluate() if isinstance(t, BaseParsedType) else t) 
                                                                    == 
                                                                (args[0].evaluate() if isinstance(args[0], BaseParsedType) else args[0]) 
                                                                for (i,t) in enumerate(args) if i > 0]),
            [
                Constraint_MinArgsLength(2),
                Constraint_ArgType(Lexeme)
            ]))
    
    FunctionsManager.instance.registerFunction(
        CustomFunctionDefinition("=", True.__class__, lambda *args: not any([
                                                                (t.evaluate() if isinstance(t, BaseParsedType) else t) 
                                                                    != 
                                                                (args[0].evaluate() if isinstance(args[0], BaseParsedType) else args[0]) 
                                                                for (i,t) in enumerate(args) if i > 0]),
            [
                Constraint_MinArgsLength(2),
                Constraint_ArgType(Number)
            ]))
    
    FunctionsManager.instance.registerFunction(
        CustomFunctionDefinition("<>", True.__class__, lambda *args: not any([
                                                                (t.evaluate() if isinstance(t, BaseParsedType) else t) 
                                                                    == 
                                                                (args[0].evaluate() if isinstance(args[0], BaseParsedType) else args[0]) 
                                                                for (i,t) in enumerate(args) if i > 0]),
            [
                Constraint_MinArgsLength(2),
                Constraint_ArgType(Number)
            ]))
    
    FunctionsManager.instance.registerFunction(
        CustomFunctionDefinition("printout", None.__class__, lambda *args: sys.stdout.writelines(args[1:]),
            [
                Constraint_MinArgsLength(2),
            ]))

    FunctionsManager.instance.registerFunction(
        CustomFunctionDefinition("float", Float, lambda arg: Float(arg.evaluate()),
            [
                Constraint_ArgType(Number),
                Constraint_ExactArgsLength(1)
            ]))
    
    FunctionsManager.instance.registerFunction(
        CustomFunctionDefinition("assert", None.__class__, lambda *args: args,
            [
                Constraint_MinArgsLength(1),
            ]))
    
    FunctionsManager.instance.registerFunction(
        CustomFunctionDefinition("retract", None.__class__, lambda *args: args,
            [
                Constraint_MinArgsLength(1),
            ]))
    
