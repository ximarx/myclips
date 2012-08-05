'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_MinArgsLength, Constraint_ArgType
import myclips.parser.Types as types
from myclips.rete.WME import WME
from myclips.functions.Function import Function, BreakException,\
    InvalidArgValueError, InvalidArgTypeError
from myclips.MyClipsException import MyClipsException

class Switch(Function):
    '''
    Switch conditional function:
        The switch function allows a particular group of actions 
        (among several groups of actions) to be performed based on a specified value
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.6.html#Heading287
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theExpression, *args, **kargs):
        """
        handler of the Switch function:
            regroup a list of case functions and execute the right one
            for the theCondition value. Execute a default case
            if not case cases match if a default case exists,
            otherwise return None
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.6.html#Heading287
        """
        
        # theExpression have to be evaluated and compared to each case
        # if expression value match the case, it's executed
        # and its return value returned
        # if no expression match and a default is provided, default is executed
        
        # phase 1:
        # filter/check case function in args
        # and isolate the last default function (if any)
        
        theCases = []
        theDefault = None
        if len(args) > 0:
            for index in range(0, len(args)):
                caseFunc = args[index]
                if isinstance(caseFunc, types.FunctionCall) and caseFunc.funcName == "case":
                    theCases.append(caseFunc)
                elif isinstance(caseFunc, types.FunctionCall) and caseFunc.funcName == "default":
                    if index == len(args) - 1:
                        theDefault = caseFunc
                    else:
                        raise InvalidArgValueError("Default clause for a switch function have to be the last one")
                else:
                    raise InvalidArgTypeError("Invalid argument for a switch function: %s"%str(caseFunc))
                
        
        # phase 2:
        # calculate the value for the theExpression
        if isinstance(theExpression, (types.FunctionCall, types.Variable) ):
            theResult = self.resolve(theEnv, theExpression)
        else:
            theResult = theExpression

        returnValue = None
        
        # phase 3:
        # evaluate the "case function" arguments
        for caseFunc in theCases:
            # execute the case Function
            # if it return something not None, it's ok
            # if return is None = it's not the right case
            # (maybe it's better and exception)
            try:
                returnValue = caseFunc.funcDefinition.linkedType.__class__.execute(theEnv, theResult, *(caseFunc.funcArgs))
                break # break the for at the first positive case clause executed
            except InvalidCaseException:
                pass

        # phase 4:
        # if returnValue == None, then no case match
        # try to execute the default if any
        # otherwise return None
            
        if returnValue is None and theDefault is not None:
            return theDefault.funcDefinition.linkedType.__class__.execute(theEnv, theResult, *(theDefault.funcArgs))
        else:
            return returnValue if returnValue is not None else types.Symbol("FALSE")
            
            
            
class Case(Function):
    '''
    Case clause function for switch function
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.6.html#Heading287
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theValue, theComparison, theThen, *args, **kargs):
        """
        handler of the Case function:
            check theValue against theComparison: if they match
            the actions in the case arguments are executed
            otherwise an InvalidCaseException is raised to return control
            to the outer switch function 
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.6.html#Heading287
        """
        
        returnValue = types.Symbol("FALSE")
        
        # check for case format first:
        if not isinstance(theThen, types.Symbol) or theThen.pyEqual("then"):
            raise InvalidArgValueError("The `then` keyword is expected as second argument of a case clause")
        
        # resolve theComparison to its real value
        if isinstance(theComparison, (types.FunctionCall, types.Variable)):
            theComparison = self.resolve(theEnv, theComparison)
        
        # this is not the case    
        if theValue != theComparison:
            raise InvalidCaseException()
        
        # CLIPS documentation:
        # the return value of a case function is the one returned from the last
        # action in the case arguments
        for action in args:
            # function are executed
            if isinstance(action, (types.FunctionCall, types.Variable)):
                returnValue = self.resolve(theEnv, action)
            else:
                returnValue = action
            
        return returnValue
    
    
class Default(Function):
    '''
    Default clause function for switch function
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.6.html#Heading287
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, *args, **kargs):
        """
        handler of the Default function:
            execute all action is the args
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.6.html#Heading287
        """
        
        returnValue = types.Symbol("FALSE")
        
        # CLIPS documentation:
        # the return value of a default function is the one returned from the last
        # action in the case arguments
        for action in args:
            # function are executed
            if isinstance(action, (types.FunctionCall, types.Variable)):
                returnValue = self.resolve(theEnv, action)
            else:
                returnValue = action
            
        return returnValue    
    
class InvalidCaseException(MyClipsException):
    pass    
    
Switch.DEFINITION = FunctionDefinition("?SYSTEM?", "switch", Switch(), (types.Lexeme, types.Symbol, types.String, 
                                                                                    types.Number, types.Integer, types.Float,
                                                                                    list, types.NullValue, WME ), 
                                                                Switch.do,
            [
                Constraint_MinArgsLength(3),
                Constraint_ArgType(types.FunctionCall, (1,None) )
            ],forward=False)
        
Case.DEFINITION = FunctionDefinition("?SYSTEM?", "case", Case(), (types.Lexeme, types.Symbol, types.String, 
                                                                                    types.Number, types.Integer, types.Float,
                                                                                    list, types.NullValue, WME ), 
                                                                Case.do,
            [
                Constraint_MinArgsLength(3),
                Constraint_ArgType(types.Symbol, 1)
            ],forward=False)
        
Default.DEFINITION = FunctionDefinition("?SYSTEM?", "default", Default(), (types.Lexeme, types.Symbol, types.String, 
                                                                                    types.Number, types.Integer, types.Float,
                                                                                    list, types.NullValue, WME ), 
                                                                Default.do,
            [
                Constraint_MinArgsLength(1)
            ],forward=False)
        
                