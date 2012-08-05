'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_MinArgsLength, Constraint_ArgType
import myclips.parser.Types as types
from myclips.rete.WME import WME
from myclips.functions.Function import Function, InvalidArgValueError

class IfThenElse(Function):
    '''
    If-Then-Else conditional function
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.6.html#Heading280
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theCondition, theThen, *args, **kargs):
        """
        handler of the IfThenElse function:
            if-then-else conditional structure
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.6.html#Heading280
        """
        
        returnValue = types.NullValue()
        
        if not theThen.pyEqual("then"):
            raise InvalidArgValueError("Check appropriate syntax for if function: if expects second argument to be the `then` keyword")
        
        # try to split the then-actions from the else-actions
        
        thenActions = []
        elseActions = []
        
        workingOn = thenActions
        for action in args:
            if isinstance(action, types.Symbol) and action.pyEqual("else"): 
                workingOn = elseActions
            else:
                workingOn.append(action)
            
        # if no else is found, not problem: elseActions is empty and all actions are in thenActions
        
        
        # time to evaluate the condition
        
        if isinstance(theCondition, types.FunctionCall):
            theCondition = self.resolve(theEnv, theCondition)
        
        # CLIPS documentation:
        # then-actions are executed if the result of theCondition is not <Symbol:FALSE>
        # (even <NullValue> is a true-like value)
        # else-actions are executed only if return of theCondition is exactly <Symbol:FALSE>
        
        if isinstance(theCondition, types.Symbol) and theCondition.pyEqual("FALSE"):
            # execute ELSE
            theActions = elseActions
        else:
            # execute THEN
            theActions = thenActions

        for action in theActions:
            # function are executed
            if isinstance(action, types.FunctionCall):
                returnValue = self.resolve(theEnv, action)
            else:
                # types work as return values
                returnValue = action
            
        # CLIPS documentation:
        # the if-then-else return value is always the value of the last execute action
        return returnValue
            
    
IfThenElse.DEFINITION = FunctionDefinition("?SYSTEM?", "if", IfThenElse(), (types.Lexeme, types.Symbol, types.String, 
                                                                                    types.Number, types.Integer, types.Float,
                                                                                    list, types.NullValue, WME ), 
                                                                IfThenElse.do,
            [
                Constraint_MinArgsLength(3),
                Constraint_ArgType(types.Symbol, 1)
            ],forward=False)
        
        