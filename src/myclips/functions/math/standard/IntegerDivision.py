'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_MinArgsLength, Constraint_ArgType
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgTypeError

class IntegerDivision(Function):
    '''
    The div function returns the value of the first argument divided by each of the subsequent arguments.
    Each of its arguments should be a numeric expression. 
    Each argument is automatically converted to an integer and integer division is performed. 
    This function returns an integer.
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.5.html#Heading258
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theFirst, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.5.html#Heading258
        """
        
        theFirst = self.resolve(theEnv, theFirst) if isinstance(theFirst, (types.FunctionCall, types.Variable)) else theFirst 
        
        if not isinstance(theFirst, (types.Integer, types.Float)):
            raise InvalidArgTypeError("Function div expected argument #1 to be of type integer or float")
        
        theDiv = int(theFirst.evaluate())
        
        for (index, theSecond) in enumerate(args):
            if isinstance(theSecond, (types.FunctionCall, types.Variable)):
                theSecond = self.resolve(theEnv, theSecond)
                
            if not isinstance(theSecond, (types.Integer, types.Float)):
                raise InvalidArgTypeError("Function div expected argument #%d to be of type integer or float"%index + 2)
            
            # Division is always performed between integer values
            # and result is always casted to an integer
            theDiv = int(theDiv / int(theSecond.evaluate()))
            
        # WARNING:
        # this function always return an Integer!
        return types.Integer(theDiv)
        
            
    
IntegerDivision.DEFINITION = FunctionDefinition("?SYSTEM?", "div", IntegerDivision(), types.Integer, 
                                                                IntegerDivision.do,
            [
                Constraint_MinArgsLength(2),
                Constraint_ArgType(types.Number)
            ],forward=False)
        
        